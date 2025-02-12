@echo off





:: Specify the paths for input images and output files


:: start the venv for preprocessing
call "D:\Bonsai\Code\PythonDev\PointCloud_Prep\.venv\Scripts\activate.bat"
python "D:\Bonsai\Code\PythonDev\PointCloud_Prep\Spatial_Segment_Auto.py"
call "D:\Bonsai\Code\PythonDev\PointCloud_Prep\.venv\Scripts\deactivate.bat"

:: start the venv for predicting
call "D:\Bonsai\Code\PythonDev\PointStack\.venv\Scripts\activate.bat"
python "D:\Bonsai\Code\PythonDev\PointStack\PointStack\Predict_Auto.py"
call "D:\Bonsai\Code\PythonDev\PointStack\.venv\Scripts\deactivate.bat"







