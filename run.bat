@echo off
:menu
cls
echo =======================================
echo     YourVision Application Launcher
echo =======================================
echo.
echo Select an application to run:
echo.
echo 1. FaceBlur - Privacy tool
echo 2. HandMouse - Hand gesture mouse control
echo 3. DanceWithMe - Stickman dance mimic
echo 4. FoodEater - Food eating game
echo 5. MyAvatar - Avatar creator
echo 6. RedLightGreenLight - Movement game
echo 7. Exit
echo.

set /p choice="Enter your choice (1-7): "

if "%choice%"=="1" (
    echo Starting FaceBlur...
    python blurface.py
    pause
    goto menu
)
if "%choice%"=="2" (
    echo Starting HandMouse...
    python handmouse.py
    pause
    goto menu
)
if "%choice%"=="3" (
    echo Starting DanceWithMe...
    python dancewithme.py
    pause
    goto menu
)
if "%choice%"=="4" (
    echo Starting FoodEater...
    python foodeater.py
    pause
    goto menu
)
if "%choice%"=="5" (
    echo Starting MyAvatar...
    python myavatar.py
    pause
    goto menu
)
if "%choice%"=="6" (
    echo Starting Red Light Green Light...
    python Red_Light_Green_Light.py
    pause
    goto menu
)
if "%choice%"=="7" (
    echo Goodbye!
    exit
)

echo Invalid choice! Please try again.
pause
goto menu