
""" This is a program to move the LK MG4010E-i36v3 motor to rotate a camera around a plant. 
It uses the LK-Motor library along with some custom commands to make the motor work correctly """


print("Starting Program.....")
#There is a difference between "motor off" and "Motor stop". Motor off may turn off the coils and so prevent overheating!
from pypylon import pylon
import cv2
import numpy as np
import time
import pygame
from robot import robot
import serial
import os
import shutil
CMD_HEADER                     = 0x3E
CMD_ASK_MULTI_LOOP_ANGLE       = 0x92        #Read multi -loop Angle command
CMD_ASK_SINGLE_LOOP_ANGLE      = 0x94        #Read single -loop Angle command
CMD_ABS_MULTI_LOOP_ANGLE_SPEED = 0xA4        #MULTI ROTATION ABS ANGLE Multi position closed loop control command 2
CMD_ABS_SINGLE_ANGLE_SPEED     = 0xA6        #Single position closed loop control command 2 Angle 0...359.99 deg Rotation direction is set by outside
CMD_INC_ANGLE_SPEED            = 0xA8        #INCREMENT angle with speed
CMD_SET_ZERO                   = 0x19        #Set current poosition as zero for driver
CMD_MOTOR_SHUTDOWN             = 0x80        #MOTOR stop (but power on coils will keep?)
CMD_MOTOR_STOP                 = 0x81        #MOTOR stop (but power on coils will keep?)
CMD_MOTOR_START                = 0x88        #MOTOR operation
CMD_MOTOR_MODEL                = 0x12        #Read driver and motor model commands




# Initialize pygame mixer
pygame.mixer.init()

# Load the sound file (e.g., MP3 or WAV)
pygame.mixer.music.load("D:\Bonsai\Code\PlaySound\Complete_Notification.mp3")

screen_width = 1920  # Replace with actual screen width
screen_height = 1080  # Replace with actual screen height

# Get image dimensions
img_height = 3648
img_width = 5472

#Camera
# Create an instance of the camera
camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
# camera parameters
gain = 20
exposure_time = 70000


# Calculate scaling factor to fit the image within the screen while preserving aspect ratio
scale_width = screen_width / img_width
scale_height = screen_height / img_height
scale = min(scale_width, scale_height)  # Choose the smaller scale to fit within the screen

# Calculate new dimensions
new_width = int(img_width * scale)
new_height = int(img_height * scale)

x_offset = (screen_width - new_width) // 2
y_offset = (screen_height - new_height) // 2

#Motor Constants
motor_speed = 300 #deg per s at motor
increment_angle = 51840
id = 0x1
tolerance = 0.3
name = "cam"
CW = True
sim_shifts = [0.0, 0.0, 0.0]
sim_rot_plane = "XY"
FORWARD = 1
REVERSE = -1
direction = 1
picture_number = 0
#pictures_per_loop = 60
#sleeptime = 2
#pictures_per_loop = 120
#sleeptime = 0.5

#Defaults
pictures_per_loop = 90
sleeptime = 1


#initializing the serial port for the motor
motor_serial_port_name = "COM9"
motor_serial_port = serial.Serial(
                port        =   motor_serial_port_name,
                baudrate    =   115200, #was 115200
                parity      =   serial.PARITY_NONE,
                stopbits    =   serial.STOPBITS_ONE,
                bytesize    =   serial.EIGHTBITS,
                #timeout=1
            )

cam_motor = robot.Motor(id, motor_serial_port, tolerance, name, CW, sim_shifts, sim_rot_plane)





#Functions

#Motor Functions

# This is a function to interpret the single-loop encoder output
def interpret_angle(data_bytes):
    # Ensure data_bytes is of the correct length (4 bytes)
    if len(data_bytes) != 4:
        raise ValueError("Expected 4 data bytes for the angle")

    # Convert the 4 bytes to a 32-bit integer (assuming little-endian format)
    angle = (int.from_bytes(data_bytes, byteorder='little'))/36
    
    # Print the interpreted angle
    #print(f"Interpreted angle: {angle}")

    return angle

# This is a function to read the single loop encoder value. It returns a value that corresponds to the rotation of the
#motor without taking into account the 1:4 ratio ring gear. 
#This is needed because the library equivalent function does not work.
def read_single_loop_angle(self):
    bytes_expect = 10  # Expected response length: 10 bytes
    
    if self.serial_port is not None:
        # Define the frame components with data length 0x00
        CMD = [0x3E, 0x94, 0x01, 0x00]  # Frame head, Command, ID, Data length

        # Calculate the checksum (sum of CMD[0] to CMD[3] & 0xFF to ensure 8 bits)
        checksum = sum(CMD) & 0xFF

        # Append checksum to the frame
        CMD.append(checksum)

        # Convert to byte array
        frame = bytearray(CMD)
        
        self.serial_port.write(frame)
        
        # Get response
        self.serial_port.timeout = 0.1
        res = self.serial_port.read(bytes_expect)

        # Check if the received data is of the expected length (10 bytes)
        if res is None or len(res) != bytes_expect:
            raise TimeoutError(f"Motor did not respond with {bytes_expect} byte(s), result is '{res}'")

        # Extract the 4 data bytes (bytes 6, 7, 8, 9 -> indices 5, 6, 7, 8)
        data_bytes = res[5:9]  # Extract bytes 6, 7, 8, 9 (indexing starts from 0)

        # Print only the extracted data bytes
        print(f"Single-loop angle bytes: {data_bytes}")

        angle_int = interpret_angle(data_bytes)
        print(f"Angle is: {angle_int}")

        return data_bytes  # Return the raw bytes if needed

    else:
        return None
    
#This is a function to read the multiloop angle of the motor encoder. It returns the angle of the arm with the camera taking into
#account the 1:4 gear ratio of the ring gear.
#This is needed because the library equivalent function does not work.
def read_multi_loop_angle(self):
    bytes_expect = 14  # Expected response length: 5 bytes command + 9 bytes data
    
    if self.serial_port is not None:
        # Define the frame components (command 0x92 for multi-loop angle)
        CMD = [0x3E, 0x92, 0x01, 0x00]  # Frame head, Command, ID, Data length

        # Calculate the checksum (sum of CMD[0] to CMD[3] & 0xFF to ensure 8 bits)
        checksum = sum(CMD) & 0xFF

        # Append checksum to the frame
        CMD.append(checksum)

        # Convert to byte array
        frame = bytearray(CMD)
        
        self.serial_port.write(frame)
        
        # Get response
        self.serial_port.timeout = 0.1
        res = self.serial_port.read(bytes_expect)

        # Check if the received data is of the expected length (10 bytes)
        if res is None or len(res) != bytes_expect:
            raise TimeoutError(f"Motor did not respond with {bytes_expect} byte(s), result is '{res}'")

        # Extract the 8 data bytes (representing the int64_t angle)
        data_bytes = res[5:13]  # Extract bytes 6 to 13 (8 bytes of the motor angle)

        # Print the extracted data bytes
        print(f"Multi-loop angle data bytes: {data_bytes}")

        # Convert the 8 data bytes into a 64-bit integer (little-endian)
        motor_angle = int.from_bytes(data_bytes, byteorder='little', signed=True)

        # Convert to degrees with 0.01°/LSB
        motor_angle_degrees = ((motor_angle * 0.01)/4)/36 # and /4 and /36 because of gear ratio
        
        print(f"Interpreted multi-loop angle: {motor_angle} (raw) -> {motor_angle_degrees}° (converted)")

        return motor_angle_degrees  # Return the angle in degrees

    else:
        return None



#This is a function to turn off the motor so that the coils are denergised and the motor stops responding to commands except for "motor on"
#This is needed because the library equivalent function does not work.
def motor_off(self):
    bytes_expect = 5
    if not self.serial_port == None:
        # Define the frame components
        CMD = [0x3E, 0x80, 0x01, 0x00]  # Frame head, Command, ID, Data length

        # Calculate the checksum (sum of CMD[0] to CMD[3] & 0xFF to ensure 8 bits)
        checksum = sum(CMD) & 0xFF

        # Append checksum to the frame
        CMD.append(checksum)

        # Convert to byte array
        frame = bytearray(CMD)
        
        self.serial_port.write(frame)
        
        self.serial_port.timeout = 0.1


        #get response

        res = self.serial_port.read(bytes_expect)

        if (res is None or (len(res) != bytes_expect)): 
            raise TimeoutError(f"Motor does not responded {bytes_expect} byte(s), result is '{res}'")

    
    else:
        res = 1
#This is a function to turn off the motor so that the coils are energised and the motor starts responding to commands
#This is needed because the library equivalent function does not work.
def motor_on(self):
    bytes_expect = 5
    if not self.serial_port == None:
        # Define the frame components
        CMD = [0x3E, 0x88, 0x01, 0x00]  # Frame head, Command, ID, Data length

        # Calculate the checksum (sum of CMD[0] to CMD[3] & 0xFF to ensure 8 bits)
        checksum = sum(CMD) & 0xFF

        # Append checksum to the frame
        CMD.append(checksum)

        # Convert to byte array
        frame = bytearray(CMD)
        
        self.serial_port.write(frame)
        
        #get response
        self.serial_port.timeout = 0.1
        
        res = self.serial_port.read(bytes_expect)

        if (res is None or (len(res) != bytes_expect)): 
            raise TimeoutError(f"Motor does not responded {bytes_expect} byte(s), result is '{res}'")

    
    else:
        res = 1
#This is a function to stop the motor from moving.
#This is needed because the library equivalent function does not work.
def motor_stop(self):
    bytes_expect = 5
    if not self.serial_port == None:
        # Define the frame components
        CMD = [0x3E, 0x81, 0x01, 0x00]  # Frame head, Command, ID, Data length

        # Calculate the checksum (sum of CMD[0] to CMD[3] & 0xFF to ensure 8 bits)
        checksum = sum(CMD) & 0xFF

        # Append checksum to the frame
        CMD.append(checksum)

        # Convert to byte array
        frame = bytearray(CMD)
        
        self.serial_port.write(frame)

        #get response
        self.serial_port.timeout = 0.1
        
        res = self.serial_port.read(bytes_expect)

        if (res is None or (len(res) != bytes_expect)): 
            raise TimeoutError(f"Motor does not responded {bytes_expect} byte(s), result is '{res}'")

    
    else:
        res = 1

    return res




#This is a function to cleanup the motor, stopping it and turning it off
def Cleanup(motor):
    #stopping the motor and turning it off.
    motor_stop(motor)
    motor_off(motor)
    print("Program Quitting.......")

#This is a function to delete all the old contents of the folder where the images from the camera are going to be stored.
def clear_output_folder(folder_path="D:\Bonsai\Pictures\Basler_Images\Input_Images"):
    """Clears the Basler Images folder before starting"""
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
    os.makedirs(folder_path)



# This function pops up a window showing a live feed from the camera so that the user can set the camera position and focus.
def SetFocus(camera):
    # Start the camera
    camera.Open()

    #Set the Exposure
    camera.PixelFormat.SetValue("BGR8")
    camera.GainAuto.SetValue('Continuous')
    camera.ExposureAuto.SetValue("Off")
    #camera.Gain.SetValue(gain)
    camera.ExposureTime.SetValue(exposure_time)
    # Start grabbing frames
    camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)

    # Loop to continuously capture and display images
    while camera.IsGrabbing():
        grab_result = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

        if grab_result.GrabSucceeded():
            # Convert the image to an OpenCV format
            image = grab_result.GetArray()

            
            # Resize the image
            resized_image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)

            # Create a black canvas of the screen size
            canvas = np.zeros((screen_height, screen_width, 3), dtype=np.uint8)

            # Center the resized image on the canvas
            canvas[y_offset:y_offset + new_height, x_offset:x_offset + new_width] = resized_image

            # Create a named window and set it to full screen
            window_name = "Set Focus, Press Q to exit"
            cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)  # Create a resizable window
            cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_NORMAL)  # Set to fullscreen

            # Display the centered image on the canvas
            cv2.imshow(window_name, canvas)

            # Check for key press to exit (press 'q' to quit)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cv2.destroyAllWindows()  # Ensure the window is closed
                break

        # Release the grab result
        grab_result.Release()

    #Finish Setting Focus
    cv2.destroyAllWindows()
    camera.Close()

#This is a function to get an image from the basler camera.
def GetImage(camera):
    # Start the camera
    
    camera.Open()
    camera.ExposureAuto.SetValue("Off")
    camera.GainAuto.SetValue('Continuous')
    camera.ExposureTime.SetValue(exposure_time)
    # Grab a single image
    camera.StartGrabbingMax(1)
    grab_result = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

    if grab_result.GrabSucceeded():
        # Access the image data
        img_array = grab_result.GetArray()
        print("Image captured:", img_array.shape)

        

        

        # Release resources
        grab_result.Release()
        camera.Close()
        
        return img_array

    else:
        print("Error: ", grab_result.ErrorCode, grab_result.ErrorDescription)
        # Release resources
        grab_result.Release()
        camera.Close()
        return 0


#This is a function to save an image to the right folder 
def SaveImage(image_array, name):
    file_name = 'D:\Bonsai\Pictures\Basler_Images\Input_Images\image' + str(name) + '.png'
    print(file_name)
    cv2.imwrite(file_name,image_array)  

#This is a function to pop up a message to the user asking the user to reposition the camera
def popMessage(message):
    height, width = 500, 800  # You can adjust the size
    black_image = np.zeros((height, width, 3), dtype=np.uint8)

    # Define the text and font 
    text = message
    font = cv2.FONT_HERSHEY_TRIPLEX    
    font_scale = 2  # Adjust for larger or smaller text
    font_thickness = 2 
    color = (255, 255, 255)  # White text

    # Get the size of the text
    (text_width, text_height), baseline = cv2.getTextSize(text, font, font_scale, font_thickness)

    # Calculate the text position to center it
    text_x = (width - text_width) // 2
    text_y = (height + text_height) // 2

    # Put the text on the image
    cv2.putText(black_image, text, (text_x, text_y), font, font_scale, color, font_thickness, cv2.LINE_AA)
    window_name = "Message"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)  # Create a resizable window
    cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_NORMAL)  # Set to fullscreen
    cv2.imshow(window_name, black_image)

#This is a function to move the motor a set amount of degrees. 
# It has a ramp part to it so that the motor does not jerk too much when starting
def increment_Motor(degrees, direction):
    iterations = 10
    degrees_with_direction = degrees * direction
    ramp_const = 1000 * direction
    #Ramp for a bit
    for loop in range(iterations):
        cam_motor.inc_angle_speed(ramp_const, ((motor_speed/iterations)*(loop+1)))
        time.sleep(0.2)
    full_speed_degrees = degrees_with_direction - (ramp_const*iterations)
   
    
    #Do the rest
    cam_motor.inc_angle_speed(full_speed_degrees, motor_speed)

# Gets the user inputs from the txt file that another python file (User_Input) has created
def extract_user_inputs(file_path):
    try:
        with open(file_path, "r") as file:
            lines = file.readlines()
        
        # Initialize variables
        z_value = None
        pictures_per_loop = None
        num_loops = None

        # Extract values from file
        for line in lines:
            if "Z Value:" in line:
                z_value = float(line.split(":")[1].strip())
            elif "Photos per Loop:" in line:
                pictures_per_loop = int(line.split(":")[1].strip())
            elif "Number of Loops:" in line:
                num_loops = int(line.split(":")[1].strip())

        # Write Z value to z_movement.txt
        if z_value is not None:
            with open(r"D:\Bonsai\Code\z_movement.txt", "w") as z_file:
                z_file.write(str(z_value))

        return pictures_per_loop, num_loops

    except Exception as e:
        print(f"Error reading file: {e}")
        return None, None


#==================================================================================#
#States

#This is a function to initialize the motor and camera ready for the scan.
def Initialization():

    
    print("Using camera:", camera.GetDeviceInfo().GetModelName())
    print("Turning Motor On\n\r")
    motor_on(cam_motor)
    #Clear Folder
    clear_output_folder("D:\Bonsai\Pictures\Basler_Images\Input_Images")


    time.sleep(5)





#This is the key function of the program that gets called every time the camera has to rotate around the plant to take pictures.
def Loop():
    global direction
    global picture_number
    global pictures_per_loop
    starting_angle = read_multi_loop_angle(cam_motor)
    # Start Loop, taking pictures.
    increment_Motor(increment_angle, direction)
    # Create a full-screen window
    window_name = "Captured Image"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_NORMAL)

    #These variables are used to determine when to take the photos
    #The angle moved between each picture
    angle_per_picture = 360 / pictures_per_loop
    #The angle moved since the last picture (updates in while loop)
    angle_since_last_picture = 0
    # The angle the last picture was taken at
    angle_at_last_picture = read_multi_loop_angle(cam_motor) - starting_angle
    looping = True
    while(looping):
        #update angle
        angle = read_multi_loop_angle(cam_motor) - starting_angle 
        #print(f"Angle is: {angle}")
        #updating
        angle_since_last_picture = angle - angle_at_last_picture

        #if the motor has moved far enough since the last picture
        if((direction*(angle_since_last_picture / angle_per_picture)) > 1):
            #take a picture
            #Get an image to process
            image_array = GetImage(camera)
            #save image
            SaveImage(image_array, picture_number)

            #Display Image
            # Resize the image
            resized_image = cv2.resize(image_array, (new_width, new_height), interpolation=cv2.INTER_AREA)
            # Create a black canvas of screen size
            canvas = np.zeros((screen_height, screen_width, 3), dtype=np.uint8)
            # Center the resized image on the canvas            
            canvas[y_offset:y_offset + new_height, x_offset:x_offset + new_width] = resized_image
            # Display the centered image on the canvas
            cv2.imshow(window_name, canvas)
            # This is needed so that the window updates
            cv2.waitKey(1)

            #update angle_since_last_picture
            angle_at_last_picture = angle
            
            if(((picture_number + 2)%pictures_per_loop)==0):
                looping = False
            picture_number = picture_number + 1



    

    #update globals
    #take the final picture. This is a workaround because the while loop does not seem to do exactly what I want it to do
    #Get an image to process
    image_array = GetImage(camera)
    #save image
    SaveImage(image_array, picture_number)

    #Display Image
    # Resize the image
    resized_image = cv2.resize(image_array, (new_width, new_height), interpolation=cv2.INTER_AREA)
    # Create a black canvas of screen size
    canvas = np.zeros((screen_height, screen_width, 3), dtype=np.uint8)
    # Center the resized image on the canvas            
    canvas[y_offset:y_offset + new_height, x_offset:x_offset + new_width] = resized_image
    # Display the centered image on the canvas
    cv2.imshow(window_name, canvas)
    # This is needed so that the window updates
    cv2.waitKey(1)
    #move the picture number on ready for the next picture
    picture_number = picture_number + 1

    
    direction = direction * -1
    

#This is a function to get the user to reposition the camera in-between loops.
def Transition():
    # Tell the user to move the camera
    popMessage("Reposition Camera")

    # Wait for a key press and close the window
    # Play the sound
    pygame.mixer.music.play()
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    #Set New Focus
    SetFocus(camera)








#==================================================================================#
    




#main code
try:

    if __name__ == '__main__':
   
        # File path
        input_file_path = r"D:\Bonsai\Code\user_inputs.txt"

        # Extract values
        pictures_per_loop, num_loops = extract_user_inputs(input_file_path)
        

        # Print the extracted values
        print(f"Number of Photos per Loop: {pictures_per_loop}")
        print(f"Number of Loops: {num_loops}")
        


        #Initialize the hardware
        Initialization()
        #Do the right number of loops as asked by the user
        for loop in range(0,num_loops):
            #Adjust camera position and focus for next (or first) loop of photos
            Transition()
            #Start the Loop of Photos
            Loop()
           



       
        #End the Program
        print("Capturing Complete\n\r")
        print("Turning Motor Off\n\r")
        Cleanup(cam_motor)
        
except KeyboardInterrupt:
    Cleanup(cam_motor)
                





