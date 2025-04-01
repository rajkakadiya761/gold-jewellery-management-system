################################   Libraries   ################################
import os.path
import uuid, loader, cv2, requests, sys, time
from sqlalchemy import ForeignKey, create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
import win32gui, win32con, win32process, win32api
import ctypes
import numpy as np  # Import numpy
import mediapipe as mp

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

# Store jewellery image info
impose = None
mx = my = 0
dw = dh = 1

# Adjust these values for hand positioning
HAND_X_OFFSET = -70  # Horizontal offset from wrist (negative to shift left)
HAND_Y_OFFSET = -30  # Vertical offset from wrist (negative to move up)
JEWELLERY_SCALE = 1.0 # Scale factor for bracelet size.

#############################   Hand Detection Setup  ##########################
# MediaPipe setup
mp_hands = mp.solutions.hands
hands_detector = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.7) #Increased confidence

#############################   Helper functions   ############################

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

#############################   Main Program Modifications  ####################
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

    while True:
        check, frame = cam.read()
        if not check:
            continue

        if NEED_FLIP:
            frame = cv2.flip(frame, 1)

        frame = cv2.resize(frame, (WIDTH, HEIGHT))
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands_detector.process(frame_rgb)

        # Load the image inside the loop so it can update
        if image_path:
            impose = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
            if impose is None:
                print(f"Error: Failed to load bracelet image from path '{image_path}'.")
                continue  # Go to next frame if image fails to load.
            else:
                print(f"Bracelet image loaded successfully. Shape: {impose.shape}")
        else:
            print("Error: No image path found.")
            continue  # Go to next frame

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]
                x_wrist = int(wrist.x * WIDTH)
                y_wrist = int(wrist.y * HEIGHT)

                # Create transparent overlay
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)

                # Calculate jewellery size based on scale factor
                jewellery_width  = int(JEWELLERY_SCALE * WIDTH / 5)   #Scale relative to frame width
                jewellery_height = int(JEWELLERY_SCALE * HEIGHT / 5)  #Scale relative to frame height
                new_impose = cv2.resize(impose, (jewellery_width, jewellery_height))

                y_offset = y_wrist + HAND_Y_OFFSET
                x_offset = x_wrist + HAND_X_OFFSET

                print(f"Wrist Coordinates: x={x_wrist}, y={y_wrist}")
                print(f"Bracelet Position: x_offset={x_offset}, y_offset={y_offset}")

                #Ensure the offsets aren't causing the image out of bounds and is causing a crash
                if x_offset < 0 or y_offset < 0 or x_offset + jewellery_width > WIDTH or y_offset + jewellery_height > HEIGHT:
                    print("Warning: Bracelet is out of bounds. Adjusting offsets.")
                    continue

                for i in range(new_impose.shape[0]):
                    for j in range(new_impose.shape[1]):
                        if new_impose[i, j][3] > 0:  # Ensure alpha is greater than 0
                            frame[y_offset + i, x_offset + j] = new_impose[i, j]
        
        cv2.putText(frame, "Press ESC to exit", (10, 20), cv2.FONT_HERSHEY_SIMPLEX,  0.7, (0, 0, 0), 2, cv2.LINE_AA)
        cv2.imshow("preview", frame)

        # Add waitKey to process GUI events
        key = cv2.waitKey(15)
        if key == 27:  # Exit on 'Esc' key
            break

    # Release resources properly
    cam.release()
    cv2.destroyAllWindows()
    session.close()