@echo off

:: set the path to the audio file which you want to play when process is finished.
set AudioFile="D:\Bonsai\Code\PlaySound\Complete_SF.mp3"

:: Define the path to VLC
set "vlcPath=C:\Program Files\VideoLAN\VLC\vlc.exe"


:: Define the path to the RealityCapture executable
set RC_PATH="C:\Program Files\Capturing Reality\RealityCapture\RealityCapture.exe"

:: Check if the executable exists
if not exist %RC_PATH% (
    echo Error: RealityCapture executable not found at %RC_PATH%.
    exit /b 1
)

:: Specify the paths for input images and output files
set INPUT_FOLDER="D:\Bonsai\Pictures\Basler_Images\Input_Images"
set OUTPUT_FOLDER="D:\Bonsai\RC_Ouputs\No_Plant_Outputs"
set ModelName=Basler_test
set Model=%OUTPUT_FOLDER%\Basler_test.xyz
set Mesh_Model=%OUTPUT_FOLDER%\Basler_test.obj
set Project=%OUTPUT_FOLDER%\Basler_test.rcproj
set Export_registration_settings="D:\Bonsai\Code\export_registration_params.xml"

:: a name of the first marker.
set FirstMarker="36h11:001"

:: a name of the second marker.
set SecondMarker="36h11:002"

:: a name of the third marker.
set ThirdMarker="36h11:003"


:: a name of the fourth marker.
set FourthMarker="36h11:004"

:: a name of the 5 marker.
set FifthMarker="36h11:005"

:: a name of the 6 marker.
set SixthMarker="36h11:006"

:: a name of the 7 marker.
set SeventhMarker="36h11:007"

:: a name of the 8 marker.
set EighthMarker="36h11:008"



:: A name of the first distance constraint.
set FirstDistance="0.08"

:: A length of the first defined distance constraint.
set FirstDistanceName="distance1"

:: A name of the second distance constraint.
set SecondDistance="0.08"

:: A length of the second defined distance constraint.
set SecondDistanceName="distance2"

:: A path to the settings used for detect markers tool.
set DetectMarkersParams="D:\Bonsai\Code\detectMarkersParams.xml"


:: Read the Z value from a file
set /p Z_VALUE=<z_movement.txt

:: Check if the Z value was read
if "%Z_VALUE%"=="" (
    echo Error: Z value not found in z_movement.txt.
    exit /b 1
)



:: Run RealityCapture with the specified parameters
echo Running RealityCapture with all commands...
%RC_PATH% -addFolder %INPUT_FOLDER% ^
    -detectMarkers %DetectMarkersParams% ^
    -defineDistance %FirstMarker% %SecondMarker% %FirstDistance% %FirstDistanceName% ^
    -defineDistance %FirstMarker% %ThirdMarker% %SecondDistance% %SecondDistanceName% ^
    -align ^
    -selectMaximalComponent ^
    -setReconstructionRegionOnCPs %SeventhMarker% %EighthMarker% %SixthMarker% 1.3 ^
    -moveReconstructionRegion 0 0 %Z_VALUE% ^
    -scaleReconstructionRegion 1.1 1.1 1.1 center factor ^
    -setGroundPlaneFromReconstructionRegion ^
    -calculateNormalModel ^
    -renameSelectedModel %ModelName% ^
    -calculateTexture ^
    -save "%Project%" ^
    -exportModel %ModelName% %Model% ^
    -exportModel %ModelName% %Mesh_Model% ^
    

    

:: Notify the user the operation is complete
echo RealityCapture CLI has finished executing.

:: Play the sound file in VLC minimized and close after playback
start "" /min "%vlcPath%" --intf dummy --play-and-exit "%AudioFile%"


pause

