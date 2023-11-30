# import Tkinter to create our GUI.
from tkinter import Tk, Label, Button, Frame
# import openCV for receiving the video frames
import cv2
# make imports from the Pillow library for displaying the video stream with Tkinter.
from PIL import Image, ImageTk
# Import the tello module
from djitellopy import tello
# Import threading for our takeoff/land method
import threading
# import our flight commands
from flight_commands import start_flying, stop_flying


# Class for controlling the drone via keyboard commands
class DroneController:
    def __init__(self):

        # Initialize the Tkinter window, give it a title, and define its minimum size on the screen.
        self.root = Tk()
        self.root.title("Search and Rescue Drone Controller")

        # Create a hidden frame to handle input from key presses and releases
        self.input_frame = Frame(self.root)

        # Initialize, connect, and turn on the drones video stream
        self.drone = tello.Tello()
        self.drone.connect()
        self.drone.streamon()
        # Initialize a variable to get the video frames from the drone
        self.frame = self.drone.get_frame_read()

        # Define a speed for the drone to fly at
        self.drone.speed = 50

        # Label for displaying video stream
        self.cap_lbl = Label(self.root)

        # Create a button to send takeoff and land commands to the drone
        self.takeoff_land_button = Button(self.root, text="Takeoff/Land", command=lambda: self.takeoff_land())

        # Create a new parameter to determine if camera direction is set to the bottom camera (yes = True, no = False)
        self.camera_down = False

        # Create a new button for switching the camera direction and set it to a new class method that we will create last.
        self.camera_dir_button = Button(self.root, text="Switch Camera Direction",
                                        command=lambda: self.set_camera_direction())

        ################ STEP 1 ########################
        # Create a new parameter to determine if face detection is active.
        self.face_detection = False
        # Create a new button for activating face detection and set it to a new class method that we will create last.
        self.face_detection_button = Button(self.root, text="Detect Faces",
                                            command=lambda: self.set_detect_face())
        ################################################

    ################# STEP 3 #######################
    # Define a method for activating and deactivating face detection.
    def set_detect_face(self):
        if self.face_detection:
            self.face_detection = False
        else:
            self.face_detection = True
    #################################################

    ################# STEP 4 #######################
    # Get our detect_faces method from a previous video and define it as a static method in our class.
    @staticmethod
    def detect_faces(frame):
        """Print the number of faces detected in the drones camera stream to the output window and
        draws a box around any faces in the cv2 window if they are detected"""

        # Create a cascade
        faceCascade = cv2.CascadeClassifier("data-files\haarcascade_frontalface_default.xml")

        # Covert the frame to grayscale
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Get numpy array with values for faces detected by passing in grayscale image, scale factor, and minimum neighbors
        faces = faceCascade.detectMultiScale(frame_gray, 1.2, 3)

        # For the x, y coordinates and width, height detected
        for (x, y, w, h) in faces:
            # Draw a rectangle around the face using these values
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
        # Update the face count with the number of faces detected
        face_count = "Faces: " + str(len(faces))
        cv2.putText(frame, face_count, (10, 25), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 1,
                    2)  # Print the face count as standard output
        print(face_count)

    # Define a method for setting the camera direction
    def set_camera_direction(self):
        if self.camera_down:
            self.camera_down = False
            self.drone.set_video_direction(self.drone.CAMERA_FORWARD)
        else:
            self.camera_down = True
            self.drone.set_video_direction(self.drone.CAMERA_DOWNWARD)

    # Define a method for taking off and landing
    def takeoff_land(self):
        # Set the command for taking off or landing by checking the drones is_flying attribute
        if self.drone.is_flying:
            threading.Thread(target=lambda: self.drone.land()).start()
        else:
            threading.Thread(target=lambda: self.drone.takeoff()).start()

    # Method to run the application
    def run_app(self):
        try:
            # Add the button and video stream label to the window
            self.takeoff_land_button.grid(column=1, row=2)

            # Bind the key presses with to the flight commands by associating them with a direction to travel.
            self.input_frame.bind('<KeyPress-w>',
                                  lambda event: start_flying(event, 'upward', self.drone, self.drone.speed))
            self.input_frame.bind('<KeyRelease-w>', lambda event: stop_flying(event, self.drone))

            self.input_frame.bind('<KeyPress-a>',
                                  lambda event: start_flying(event, 'yaw_left', self.drone, self.drone.speed))
            self.input_frame.bind('<KeyRelease-a>', lambda event: stop_flying(event, self.drone))

            self.input_frame.bind('<KeyPress-s>',
                                  lambda event: start_flying(event, 'downward', self.drone, self.drone.speed))
            self.input_frame.bind('<KeyRelease-s>', lambda event: stop_flying(event, self.drone))

            self.input_frame.bind('<KeyPress-d>',
                                  lambda event: start_flying(event, 'yaw_right', self.drone, self.drone.speed))
            self.input_frame.bind('<KeyRelease-d>', lambda event: stop_flying(event, self.drone))

            self.input_frame.bind('<KeyPress-Up>',
                                  lambda event: start_flying(event, 'forward', self.drone, self.drone.speed))
            self.input_frame.bind('<KeyRelease-Up>', lambda event: stop_flying(event, self.drone))

            self.input_frame.bind('<KeyPress-Down>',
                                  lambda event: start_flying(event, 'backward', self.drone, self.drone.speed))
            self.input_frame.bind('<KeyRelease-Down>', lambda event: stop_flying(event, self.drone))

            self.input_frame.bind('<KeyPress-Left>',
                                  lambda event: start_flying(event, 'left', self.drone, self.drone.speed))
            self.input_frame.bind('<KeyRelease-Left>', lambda event: stop_flying(event, self.drone))

            self.input_frame.bind('<KeyPress-Right>',
                                  lambda event: start_flying(event, 'right', self.drone, self.drone.speed))
            self.input_frame.bind('<KeyRelease-Right>', lambda event: stop_flying(event, self.drone))

            # Pack the hidden frame and give direct input focus to it.
            self.input_frame.grid(column=2, row=1)
            self.input_frame.focus_set()

            self.camera_dir_button.grid(column=0, row=1)

            ############### STEP 2 ########################################
            # Add our new button to the gui.
            self.face_detection_button.grid(column=0, row=2)
            ################################################################

            self.cap_lbl.grid(column=1, row=1)

            # Call the video stream method
            self.video_stream()

            # Start the tkinter main loop
            self.root.mainloop()

        except Exception as e:
            print(f"Error running the application: {e}")
        finally:
            # When the root window is exited out of ensure to clean up any resources.
            self.cleanup()

    # Method to display video stream
    def video_stream(self):
        # Define the height and width to resize the current frame to
        h = 480
        w = 720

        # Read a frame from our drone
        frame = self.frame.frame

        frame = cv2.resize(frame, (w, h))

        # After resizing check camera direction and if self.camera_down is True then crop appropriately.
        if self.camera_down:
            frame = frame[0:240, 0:320]

        ######################### STEP 5 #############################
        # After resizing check if face_detection is True and if so then run our detect_faces method on the frame
        if self.face_detection:
            print("running detect_faces")
            self.detect_faces(frame)
        ###############################################################

        # Convert the current frame to the rgb colorspace
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)

        # Convert this to a Pillow Image object
        img = Image.fromarray(cv2image)

        # Convert this then to a Tkinter compatible PhotoImage object
        imgtk = ImageTk.PhotoImage(image=img)

        # grid the image label at the center of the window
        self.cap_lbl.grid(column=1, row=1)

        # Set it to the photo image
        self.cap_lbl.imgtk = imgtk

        # Configure the photo image as the displayed image
        self.cap_lbl.configure(image=imgtk)

        # Update the video stream label with the current frame
        # by recursively calling the method itself with a delay.
        self.cap_lbl.after(5, self.video_stream)

    # Method for cleaning up resources
    def cleanup(self) -> None:
        try:
            # Release any resources
            print("Cleaning up resources...")
            # Ensure to set the camera direction back to forward if not.
            if self.camera_down:
                self.drone.set_video_direction(self.drone.CAMERA_FORWARD)
            self.drone.end()
            self.root.quit()  # Quit the Tkinter main loop
            exit()
        except Exception as e:
            print(f"Error performing cleanup: {e}")


if __name__ == "__main__":
    # Initialize the GUI
    gui = DroneController()
    # Call the run_app method to run tkinter mainloop
    gui.run_app()
