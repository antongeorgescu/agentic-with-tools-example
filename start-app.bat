@echo off
echo Starting Q&A Generator Application...
echo.

REM Check if we're in the right directory
if not exist "app.py" (
    echo Error: app.py not found. Make sure you're in the project root directory.
    pause
    exit /b 1
)

echo Step 1: Installing Python dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo Error: Failed to install Python dependencies
    pause
    exit /b 1
)

echo.
echo Step 2: Starting Flask API server...
start "Flask API" cmd /k "python app.py"

echo.
echo Step 3: Setting up Angular app...
cd angular-app

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo Error: Node.js is not installed. Please install Node.js from https://nodejs.org/
    pause
    exit /b 1
)

REM Check if Angular CLI is available
ng version --skip-confirmation >nul 2>&1
if errorlevel 1 (
    echo Installing Angular CLI globally...
    npm install -g @angular/cli
    if errorlevel 1 (
        echo Error: Failed to install Angular CLI
        pause
        exit /b 1
    )
)

echo Installing Node.js dependencies...
REM Clean install to ensure all packages are properly installed
if exist "node_modules" rmdir /s /q "node_modules"
if exist "package-lock.json" del "package-lock.json"

call npm install
if errorlevel 1 (
    echo Error: Failed to install Node.js dependencies
    echo Trying with --legacy-peer-deps flag...
    call npm install --legacy-peer-deps
    if errorlevel 1 (
        echo Error: Failed to install Node.js dependencies even with legacy peer deps
        pause
        exit /b 1
    )
)

echo.
echo Step 4: Starting Angular development server...
echo.
echo The application will open in your browser at http://localhost:4200
echo Make sure the Flask API is running at http://localhost:5000
echo.
call ng serve --open

pause