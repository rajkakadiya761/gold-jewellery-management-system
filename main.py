# ################################   Libraries   ################################
# import ctypes
# import os.path
# import uuid

# import cv2
# import loader

# #############################   Global variables   ############################

# # Uncomment the source you want to select;
# # for file & rtsp don't forget to change the path in assets\configs\settings.json
# VID_SOURCE = "USB_CAM"
# # VID_SOURCE = "FILE"
# # VID_SOURCE = "RTSP"

# # Change to True if you need to flip image
# NEED_FLIP = False

# # Default width & height of the images
# WIDTH = 730
# HEIGHT = 640

# # Store the current jewellery information
# jewellery = None
# impose = None
# mx = my = None
# dw = dh = None


# #############################   Helper functions   ############################

# def update_impose():
#     """
#     Update the new jewellery info when previous or next button is pressed.

#     Returns:
#         None
#     """
#     global impose, mx, my, dw, dh
#     impose = jewellery["path"]
#     mx, my = jewellery["x"], jewellery["y"]
#     dw, dh = jewellery["dw"], jewellery["dh"]


# def save_picture(curr_frame):
#     """
#     Save the current frame as JPEG image.

#     Args:
#         curr_frame (np.array): Current frame when user wanted to save it
#     Returns:
#         None
#     """
#     # Create the output folder if not exists
#     if not os.path.exists(loader.get_absolute_path("captures", True)):
#         os.makedirs(loader.get_absolute_path("captures", True))

#     filename = r"captures\Capture_"+str(uuid.uuid4())[:6]+".jpg"
#     filename = loader.get_absolute_path(filename, True)
#     # Get a unique filename
#     while os.path.exists(filename):
#         filename = r"captures\Capture_" + str(uuid.uuid4())[:6]+".jpg"
#         filename = loader.get_absolute_path(filename, True)
#     cv2.imwrite(filename, curr_frame)


# ###############################   Main Program   ##############################

# if __name__ == "__main__":
#     # Set window icon during .exe execution
#     # MY_APP_ID = "asutosh.arjbx.v0.0.1"  # arbitrary string
#     # ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(MY_APP_ID)

#     # Get the source from settings configuration file
#     # print(loader.get_source(VID_SOURCE))
#     cam = cv2.VideoCapture(loader.get_source(VID_SOURCE))
#     cv2.imshow("preview", loader.generate_loading_screen(HEIGHT, WIDTH))

#     # Load the required files into memory
#     cascade, jewelleries = loader.load_files()
#     jewel_key_list = list(jewelleries)

#     # Set the first jewellery as current jewellery in use
#     curr_jewel_index = 0
#     jewellery = jewelleries[jewel_key_list[curr_jewel_index]]
#     impose = jewellery["path"]
#     mx, my = jewellery["x"], jewellery["y"]
#     dw, dh = jewellery["dw"], jewellery["dh"]

#     # Start reading the frames from source
#     # alpha = 0.9 # 0.0 to 1.0
#     check, frame = cam.read()
#     cv2.waitKey(2000)

#     if check:
#         # If able to read the source; start capturing frames
#         while check:
#             check, frame = cam.read()
#             if not check:
#                 continue

#             # If you need to flip the image horizontally;
#             # just change the NEED_FLIP to True above in global variable section
#             if NEED_FLIP:
#                 frame = cv2.flip(frame, 1)

#             # Resize the frame
#             frame = cv2.resize(frame, (WIDTH, HEIGHT))
#             # cv2.imshow('preview', frame)

#             # Detect available faces in frame
#             gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#             # you can change the scaleFactor & minNeighbors if required
#             faces = cascade.detectMultiScale(gray, scaleFactor=1.8, minNeighbors=3)
#             # for x, y, w, h in faces:
#             #     frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 0), 2)

#             # Show the filter, if only 1 face is found otherwise it may create inconsistency
#             # You can try with multiple faces... here
#             if len(faces) == 1:
#                 # Extract face location
#                 x, y, w, h = faces[0]

#                 # Adjust the jewelery to the face's placement
#                 frame = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
#                 fw, fh = int(w * dw), int(w * dh)
#                 new_impose = cv2.resize(impose, (fw, fh))

#                 # Super impose the jewellery over captured frame
#                 iw, ih, c = new_impose.shape
#                 # for i in range(0, iw):
#                 #     for j in range(0, ih):
#                 #         if new_impose[i, j][3] != 0:
#                 #             if y + i + h + my < HEIGHT and x + j + mx < WIDTH:
#                 #                 # print(y + i + h + my, x + j + mx)
#                 #                 frame[y + i + h + my, x + j + mx] = new_impose[i, j]
#                 for i in range(0, iw):
#                  for j in range(0, ih):
#                    if new_impose.shape[2] == 4:  # Only check alpha if image has 4 channels
#                     if new_impose[i, j][3] != 0:
#                      if y + i + h + my < HEIGHT and x + j + mx < WIDTH:
#                       frame[y + i + h + my, x + j + mx] = new_impose[i, j]
#                      else:  # No alpha channel, copy pixel directly
#                       if y + i + h + my < HEIGHT and x + j + mx < WIDTH:
#                        frame[y + i + h + my, x + j + mx] = new_impose[i, j]


#             # Display the final image
#             cv2.imshow("preview", frame)

#             # Set ESC key to quit the program
#             k = cv2.waitKey(15)
#             if k == 27:
#                 break

#             # Goto next jewellery when N is pressed
#             elif k == ord("n") or k == ord("N"):
#                 if curr_jewel_index + 1 != len(jewel_key_list):
#                     curr_jewel_index += 1
#                 else:
#                     curr_jewel_index = 0
#                 jewellery = jewelleries[jewel_key_list[curr_jewel_index]]
#                 update_impose()

#             # Goto previous jewellery when P is pressed
#             elif k == ord("p") or k == ord("P"):
#                 if curr_jewel_index - 1 < 0:
#                     curr_jewel_index = len(jewel_key_list) - 1
#                 else:
#                     curr_jewel_index -= 1
#                 jewellery = jewelleries[jewel_key_list[curr_jewel_index]]
#                 update_impose()

#             # Save the picture when S is pressed
#             elif k == ord("s") or k == ord("S"):
#                 save_picture(frame)

#     else:
#         print("Error: Can't read camera")

#     cv2.destroyAllWindows()
#     cam.release()

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

# Store jewellery image info
impose = None
mx = my = 0
dw = dh = 1

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
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
                fw, fh = int(w * dw), int(w * dh)
                new_impose = cv2.resize(impose, (fw, fh))

                iw, ih, c = new_impose.shape
                for i in range(0, iw):
                    for j in range(0, ih):
                        if new_impose.shape[2] == 4 and new_impose[i, j][3] != 0:
                            if y + i + h + my < HEIGHT and x + j + mx < WIDTH:
                                frame[y + i + h + my, x + j + mx] = new_impose[i, j]

            cv2.imshow("preview", frame)

            k = cv2.waitKey(15)
            if k == 27:
                break
            elif k == ord("n"):
             new_product_id = fetch_product_id()  # Fetch a new product ID dynamically
             print(f"🔍 New product_id fetched: {new_product_id}")  # Debugging output

             if new_product_id and new_product_id != product_id:
              product_id = new_product_id  # Update product_id
              print(f"🔄 Switching to new product_id: {product_id}")  # Debugging
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
