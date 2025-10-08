@echo off
echo Installing YourVision...
echo.
echo Checking Python version...
python --version
echo You need python 3.10 to run the python files properly

echo.
echo Installing required packages...
pip install -r requirements.txt

echo.
echo Installation complete!
echo.
echo Available applications:
echo - python blurface.py     (Face Blur Tool)
echo - python handmouse.py    (Hand Mouse Control)
echo - python dancewithme.py  (Dance with Stickman)
echo - python foodeater.py    (Food Eater Game)
echo - python myavatar.py     (Avatar Creator)
echo - python Red_Light_Green_Light.py  (Red Light Green Light Game)
echo.
pause