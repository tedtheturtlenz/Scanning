@echo off

::Capture the Images
call "D:\Bonsai\Code\PythonDev\Scanning\.venv\Scripts\activate.bat"
python "D:\Bonsai\Code\PythonDev\Scanning\User_Input.py"
python "D:\Bonsai\Code\PythonDev\Scanning\Capture.py"
call "D:\Bonsai\Code\PythonDev\Scanning\.venv\Scripts\deactivate.bat"



call "D:\Bonsai\Code\Process.bat"

call "D:\Bonsai\Code\Segment.bat"
