################################   Libraries   ################################
import os.path
import uuid, loader, cv2, requests, sys, time
from sqlalchemy import ForeignKey, create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
import win32gui, win32con, win32process, win32api
import ctypes

################################   Database Setup   ###########################

# MySQL Connection URI (update with your credentials)
DATABASE_URL = "mysql+pymysql://root@127.0.0.1:3306/arihant"
engine = create_engine(DATABASE_URL, echo=False)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Define ORM model
Base = declarative_base()

class ProcessedImage(Base):
    __tablename__ = 'processed_images'

    png_id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey('Products.product_id', ondelete='CASCADE'), nullable=False)
    png_image = Column(String(255), nullable=False)

    def __init__(self, product_id, png_image):
        self.product_id = product_id
        self.png_image = png_image

#############################   Global variables   ############################
VID_SOURCE = "USB_CAM"
NEED_FLIP = False
WIDTH = 730
HEIGHT = 640

# Refined ear positioning parameters
EAR_X_OFFSET = 0.45        # Horizontal position relative to face width (closer to ear)
EAR_Y_OFFSET = 0.28        # Vertical position relative to face height (higher than neck)
EAR_SCALE = 0.9              # Increased size relative to face width (larger earrings)
RIGHT_EAR_SHIFT = -0.17  
LEFT_EAR_SHIFT = 0.0      # Additional shift for the left earring towards the right
DISTANCE_FACTOR = 0.0      # Reduce distance between earrings
CENTER_ADJUSTMENT = -0.25    # Adjust the overall center position

impose = None
mx = my = 0
dw = dh = 1

def fetch_product_id():
    """Fetch the product_id dynamically from Flask backend"""
    url = "http://127.0.0.1:5000/get-product-id"  # Flask API endpoint
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get("product_id")
    return None

def get_image_path(product_id):
    """Fetch the image path using the product_id"""
    url = "http://127.0.0.1:5000/get-image-path"
    response = requests.post(url, json={"product_id": product_id})
    
    if response.status_code == 200:
        return response.json().get("image_path")
    return None

# Fetch the product ID dynamically
image_path = None

if len(sys.argv) > 1:
    image_path = sys.argv[1]
    print(f"Received Image Path: {image_path}")
else:
    # If no CLI argument, fetch product ID and get image path dynamically
    product_id = fetch_product_id()
    if product_id:
        print(f"Fetched product_id: {product_id}")
        image_path = get_image_path(product_id)

# Load the image
if image_path:
    impose = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    if impose is None:
        print("Error: Failed to load the image.")
        sys.exit(1)
    else:
        print("Image successfully loaded for AR processing.")
else:
    print("Error: No image path found.")
    sys.exit(1)
    
def list_open_windows():
    """List all open windows (for debugging window names)"""
    def enum_handler(hwnd, results):
        if win32gui.IsWindowVisible(hwnd):
            results.append((hwnd, win32gui.GetWindowText(hwnd)))

    results = []
    win32gui.EnumWindows(enum_handler, results)
    for hwnd, title in results:
        print(hwnd, title)

def bring_window_to_front(window_name):
    """Ensure OpenCV window appears in front of other windows."""
    hwnd = win32gui.FindWindow(None, window_name)
    if not hwnd:
        print(f" Error: Window '{window_name}' not found!")
        return
    
    print(f"Found window '{window_name}', bringing it to the front...")

    # If minimized, restore the window
    if win32gui.IsIconic(hwnd):
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)

    # Force window to front using SetForegroundWindow with thread input attachment
    try:
        win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
        win32gui.SetForegroundWindow(hwnd)
        win32gui.SetWindowPos(hwnd, win32con.HWND_NOTOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
    except Exception as e:
        print(f" Error bringing window to front: {e}")

    print("Window should now be in front.")

def update_impose(product_id):
    """Update the imposed jewellery image based on the product_id."""
    global impose
    print(f"🛠 Updating image for product_id: {product_id}")  # Debugging

    image_path = get_image_path(product_id)
    print(f"🖼 Retrieved image path: {image_path}")  # Debugging

    if image_path:
        impose = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)

        if impose is not None:
            print(f"Image successfully loaded for product_id {product_id}")
        else:
            print(f"Failed to load image for product_id {product_id}")
    else:
        print(f"⚠ No image path found for product_id {product_id}")


def save_picture(curr_frame):
    """Save the current frame as JPEG image."""
    save_dir = loader.get_absolute_path("captures", True)
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    filename = loader.get_absolute_path(f"captures/Capture_{uuid.uuid4().hex[:6]}.jpg", True)
    cv2.imwrite(filename, curr_frame)

###############################   Main Program   ##############################

if __name__ == "__main__":
    cam = cv2.VideoCapture(loader.get_source(VID_SOURCE))
    cv2.imshow("preview", loader.generate_loading_screen(HEIGHT, WIDTH))
    cv2.waitKey(100)  # Small delay to let the window initialize
    bring_window_to_front("preview")

    product_id = fetch_product_id()
    if product_id:
        update_impose(product_id)
    else:
        print("Error: Product ID not found.")

    check, frame = cam.read()
    cv2.waitKey(2000)

    if check:
        while check:
            check, frame = cam.read()
            if not check:
                continue

            if NEED_FLIP:
                frame = cv2.flip(frame, 1)

            frame = cv2.resize(frame, (WIDTH, HEIGHT))
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            cascade, _ = loader.load_files()
            faces = cascade.detectMultiScale(gray, scaleFactor=1.8, minNeighbors=3)

            if len(faces) == 1 and impose is not None:
                x, y, w, h = faces[0]

                # Calculate positions for both ears
                offsets = [
                    (EAR_X_OFFSET + CENTER_ADJUSTMENT + RIGHT_EAR_SHIFT),  # Right ear
                    (-EAR_X_OFFSET + CENTER_ADJUSTMENT + LEFT_EAR_SHIFT)  # Left ear
                ]

                for offset in offsets:
                    mx = int(w * offset)  # Horizontal offset from face left or right
                    my = int(h * EAR_Y_OFFSET)  # Vertical offset from face top

                    # Adjusted scaling for ear jewellery
                    dw = dh = int(w * EAR_SCALE)  # Scale based on face width

                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
                    new_impose = cv2.resize(impose, (dw, dh))

                    iw, ih, _ = new_impose.shape
                    for i in range(iw):
                        for j in range(ih):
                            if new_impose.shape[2] == 4 and new_impose[i, j][3] != 0:
                                # Position calculation adjusted for ear
                                pos_x = x + mx + j
                                pos_y = y + my + i

                                if 0 <= pos_x < WIDTH and 0 <= pos_y < HEIGHT:
                                    frame[pos_y, pos_x] = new_impose[i, j]

            cv2.putText(frame, "Press ESC to exit", (10, 20), cv2.FONT_HERSHEY_SIMPLEX,  0.7, (0, 0, 0), 2, cv2.LINE_AA) 
            cv2.imshow("preview", frame)

            k = cv2.waitKey(15)
            if k == 27:
                break
            elif k == ord("n"):
                new_product_id = fetch_product_id()  # Fetch a new product ID dynamically
                print(f"🔍 New product_id fetched: {new_product_id}")  # Debugging output

                if new_product_id and new_product_id != product_id:
                    product_id = new_product_id  # Update product_id
                    print(f"Switching to new product_id: {product_id}")  # Debugging
                    update_impose(product_id)  # Update imposed image

                    # Check if new image is loaded
                    if impose is not None:
                        print(f" Successfully updated impose image for product_id {product_id}")
                    else:
                        print(f"Failed to update impose image for product_id {product_id}")
                else:
                    print(f" No new product_id found, keeping {product_id}")

            elif k == ord("s"):
                save_picture(frame)

    else:
        print("Error: Can't read camera")

    cam.release()
    cv2.destroyAllWindows()
    session.close()
