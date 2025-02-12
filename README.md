# Bonsai Scanner User Input Script

This repository contains a Python script designed to interact with a user, collect specific input values, and save them for future use. The script creates a simple graphical user interface (GUI) using the `tkinter` library to capture user preferences related to a bonsai scanning process. The user inputs include height values, number of photos per loop, and the number of loops to perform. 

## Other Repos
Scanning is meant to be used with these two other repositories:
https://github.com/tedtheturtlenz/PointCloud_Prep
https://github.com/tedtheturtlenz/PointStack


## Features
- **User Input for Z Value**: The user can either use a default stool height or input a custom height value.
- **Number of Photos**: Allows the user to specify how many photos to take per loop.
- **Number of Loops**: The user can also define how many loops to perform during the process.
- **Error Handling**: If the user inputs invalid data (e.g., non-numeric values), an error message is shown.
- **Output**: The input values are saved to a text file (`user_inputs.txt`) and also displayed as a confirmation message.
- **3D Model**: A 3D model is reconstructed using Reality Capture.

---

## Python Script Breakdown

### 1. **GUI Creation**
   The script uses `tkinter` to create a window where the user can input:
   - **Z value (Height)**: A default value can be used if the user is using a stool, or a custom height value can be entered.
   - **Number of Photos**: The number of photos to take per loop.
   - **Number of Loops**: The number of loops to complete.

### 2. **Input Validation**
   The script validates the user input and ensures that the following conditions are met:
   - The Z value is either set to a default or a valid custom value.
   - The number of photos and the number of loops are integers.

### 3. **Output File**
   The input values are saved to a text file located at: D:\Bonsai\Code\user_inputs.txt
   
### 4. **Confirmation**
Once the user inputs the data and clicks **Submit**, a confirmation dialog is shown displaying the input values.

---



### Step 1: Install Python
Ensure you have the correct Python version environment and all the dependencies from requirements.txt installed on your machine. You can download Python from [here](https://www.python.org/downloads/).

### Step 2: Run the Script
1. These scripts are normally run using the batch file ("Capture_and_Process_and_Segment)



This will open the GUI window, where you can enter your values.

### Step 3: Input and Submit
- Enter the required information in the GUI:
- **Stool Checkbox**: Check if you are using a stool; otherwise, enter a custom Z value.
- **Number of Photos per Loop**: Specify how many photos should be taken per loop.
- **Number of Loops**: Enter the number of loops for the process.
- Click the **Submit** button to confirm and save the values.


# Camera Motor Rotation for Plant Scanning
## Overview
This program controls the LK MG4010E-i36v3 motor to rotate a camera around a plant to take a series of images. It uses the LK-Motor library along with some custom commands to ensure correct motor functionality. The captured images can then be processed, stored, and used for further analysis, such as creating 3D models or monitoring plant growth.

The batch files are used to automate the whole process of capturing the photos and reconstructing the object in 3D using Reality Capture.

The system involves:

A Basler camera to capture images.
A servo motor to rotate the camera around the plant.
Serial communication to control the motor via a connected serial port (e.g., COM9).
Reality Capture to reconstruct the 3D Model


## The Python Program:

Initializes the motor and camera.
Rotates the camera in increments to take images from different angles around the plant.
Saves images to a specified directory.
Provides a live camera feed for focusing and positioning the camera.
Notifies the user when all images have been captured.

## The Batch Files Usage
```

This repository expects the following directory setup:
D:/
  |-- Bonsai
        |-- Code
              |-- Capture_and_Segment.bat
              |-- [All the other batch files]
              |-- PythonDev
                    |--Scanning
                            |-- .venv
                            |--robot
                            |--Capture.py
                            |--README.md
                            |--requirements.txt
                            |--User_Input.py
                    |-- PointStack
                            |-- .venv
                            |-- PointStack
                                    |-- cfgs
                                    |-- core
                                    |-- data
                                          |-- modelnet40
                                                |-- .json files
                                                |-- .txt files
                                          |-- partnormal
                                                |-- dirs
                                                |-- synsetoffset2category.txt
                                          |-- scanobjectnn
                                                |-- dirs
                                          |-- bonsai
                                                |-- dirs
                                                |-- synsetoffset2category.txt
                                    |-- experiments
                            |-- Input_Point_Clouds_Color
                            |-- Output_Predicted_Point_Clouds
                            |-- To_Predict
                            |-- To_Predict_Color
                            |-- Training_Point_Clouds
                    |-- PointCloud_Prep
                            |-- .venv
                            |-- Segmented-Meshes

But by editing the references in the code these can be adjusted.

```
Once this repository is cloned, the batch files should be copied directly into the D:/Bonsai/Code directory 


### April Tags
The Tree-D Scanner uses a visual fiducial system called April Tags to set the reconstruction zone dimensions and scale the model correctly. There are 7 April Tags normally used during scanning, although more can be added if needed. The 7 that are required are comprised of 3 tags for scaling and 4 tags to define the reconstruction zone. The type of April Tags used are 36H11, and the specific tags used are:
Upper Left Corner of Reconstruction Zone: 36H11:05
Upper Right Corner of Reconstruction Zone: 36H11:06
Lower Left Corner of Reconstruction Zone: 36H11:07
Lower Right Corner of Reconstruction Zone: 36H11:08
Upper Left Scale Marker: 36H11:01
Upper Right Scale Marker: 36H11:02
Lower Left Scale Marker: 36H11:03


### Scanning
This section will cover how to actually use the scanner once the previous steps are completed. This is the most user-intensive and involved part of the process. It takes approximately 18 minutes to do a complete image capture. The camera completes 4 full rotations, 2 clockwise and 2 anti-clockwise. The direction of rotation switches after each full rotation. The user is to adjust the camera’s vertical position and tilt between each scan. The entirety of the plant from several different angles should be captured during this process.

### Starting the Scan
Open File Explorer and Navigate to the Scanning Repository and then Scanning/Batch Files
There are 2 main batch files, Capture_and_Process_and_Segment, which is used for Bonsai Trees, and Capture_and_Process_No_Plant, which is used for general scanning. CaPaS will do a full scan, reconstruct the Bonsai, segment the 3D model, and perform the measurements. CaP-NP will omit the last two steps, so it can be used for scanning objects other than Bonsai Trees.

Regardless of which program is chosen, double click the batch file and it will start. CaPaS will output the Reality Capture files and 3D Models etc all into D:\Bonsai\RC_Outputs\Scan_and_Segment. CaP-NP will output into D:\Bonsai\RC_Outputs\No_Plant_Outputs. IMPORTANT: Currently the program does not save these outputs beyond this. BEFORE running the program again the user should save any outputs they want to keep elsewhere on the laptop otherwise they will be OVERWRITTEN.
Follow the On-Screen Prompts to complete the image capturing. When the program asks if it will use a stool, this is asking if the plant has been placed on the grey stool. If it has, then the program will automatically adjust the reconstruction zone upwards to exclude the stool. If not, then the user can enter in a custom value for the reconstruction zone to be moved vertically. The units are metres. The user can also select how many rotations the camera makes, and how many photos per rotation the camera takes. The number of rotations should be even so that the camera does not slowly twist itself and the camera cable excessively.
After every rotation the user will be asked to reposition the camera before the next rotation. Press any key on the prompt screen (“Reposition Camera) to pop up a window that gives a live preview so the user can adjust the camera position and focus. Press “Q” to exit this window and continue the scan once the camera position and focus is set.


4.1 Reconstruction and Segmentation Results
This section will cover how to access the results of the scan.
4.2 Scan Results
After every scan the Reality Capture project is stored in D:/Bonsai/RC_Outputs/<relevant_folder>. Also stored in that folder are .obj and .xyz 3D models of the scan. The .obj file contains the meshed 3D model, and should be used in conjunction with the .mtl and .png files for a textured/coloured mesh. The .xyz file is the point cloud of the 3D model and is what is used in the segmentation and measuring. The photos from the scan are stored in D:/Bonsai/Pictures/Basler_Images/Input_Images. It is VERY important to copy the photos out of this folder and into another folder either on the Laptop or on an external hard drive once the scan is completed. This is because at the start of every scan, EVERYTHING in D:/Bonsai/Pictures/Basler_Images/Input_Images is DELETED.


## Requirements
Before using the system, make sure you have the following installed:

Python 3.7.7
Libraries:
opencv-python
numpy
pygame
pypylon
pyserial
Hardware:
Basler camera acA5472-17uc (for image capturing)
LK MG4010E-i36v3 motor (for rotating the camera)
Computer with a serial port for motor control
You can install the required libraries via pip:

pip install opencv-python numpy pygame pypylon pyserial


## Setup
1. Motor Setup
Connect the motor to your serial port (COM9 by default).
Set up the motor with the appropriate serial parameters (baud rate, timeout, etc.).
2. Camera Setup
Connect your Basler camera to the system.
Ensure that the camera drivers and software are installed for pypylon to interface with the camera.
3. Configure File Paths
Ensure the following paths are set correctly:
D:\Bonsai\Pictures\Basler_Images\Input_Images: Folder where captured images will be saved.
"D:\Bonsai\Code\PlaySound\Complete_Notification.mp3": Sound file for notifications.
You can modify the folder paths and sound file location as needed.

4. Running the Program
To start the program:

Initialization: The motor will be powered on, and the camera will be set up to focus. The program will clear any existing images in the designated folder.

Capture Loop: The program will rotate the camera around the plant in incremental steps, capturing images at each step. It will stop after taking a predefined number of images (set by pictures_per_loop).

Image Saving: After each image is captured, it will be saved to the designated folder with a unique filename.

End of Capture: Once all the images are captured, the program will notify the user and clean up the system (stop the motor and turn it off).

## Usage
This script is usually launched from the batch file "Capture_and_Process_and_Segment"



## Functions
Initialization(): Initializes the motor and camera for scanning. Clears the image folder.
Loop(): Main loop for capturing images while rotating the camera around the plant.
increment_Motor(degrees, direction): Moves the motor by a set number of degrees in the specified direction (CW or CCW).
GetImage(camera): Captures a single image from the Basler camera.
SaveImage(image_array, name): Saves the captured image to the specified folder.
SetFocus(camera): Opens a live feed from the camera to allow focus adjustments.
clear_output_folder(folder_path): Deletes old images in the specified folder before starting a new scan.
motor_on(), motor_off(), motor_stop(): Controls the motor's power and movement.
popMessage(message): Displays a pop-up message on the screen for user notifications.
extract_user_inputs(file_path): Reads user inputs (e.g., number of pictures per loop, number of loops) from a specified text file.
Notes
The motor and camera are controlled using serial communication and the Basler Pylon SDK.
Ensure that the motor and camera are properly connected to the system and configured for communication.

## Troubleshooting

If the camera does not appear to be working, ensure that the pypylon library is properly installed and the camera is recognized by the system. Ensure no other program is using the camera.
If the motor doesn't rotate, check the serial port settings and ensure the motor is powered on. Ensure no other program is using the motor.




