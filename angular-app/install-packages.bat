@echo off
REM Angular Package Installation Script for Windows

echo 🚀 Installing Angular packages for Q&A Generator App...
echo.

REM Check if we're in the angular-app directory
if not exist "package.json" (
    echo ❌ Error: package.json not found. Make sure you're in the angular-app directory.
    echo Run this script from: angular-app\
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: Node.js is not installed.
    echo Please install Node.js from: https://nodejs.org/
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('node --version') do echo ✅ Node.js version: %%i

REM Check if npm is available
npm --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: npm is not available.
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('npm --version') do echo ✅ npm version: %%i

REM Check if Angular CLI is installed globally
ng version --skip-confirmation >nul 2>&1
if errorlevel 1 (
    echo 🔧 Angular CLI not found. Installing globally...
    npm install -g @angular/cli
    if errorlevel 1 (
        echo ❌ Error: Failed to install Angular CLI
        pause
        exit /b 1
    )
    echo ✅ Angular CLI installed successfully
) else (
    echo ✅ Angular CLI is available
)

REM Clean previous installation
echo.
echo 🧹 Cleaning previous installation...
if exist "node_modules" (
    rmdir /s /q "node_modules"
    echo ✅ Removed node_modules directory
)

if exist "package-lock.json" (
    del "package-lock.json"
    echo ✅ Removed package-lock.json
)

REM Install packages
echo.
echo 📦 Installing Angular packages...
npm install

if errorlevel 1 (
    echo ⚠️  Installation failed. Trying with --legacy-peer-deps...
    npm install --legacy-peer-deps
    
    if errorlevel 1 (
        echo ❌ Error: Failed to install packages even with legacy peer deps
        echo.
        echo Possible solutions:
        echo 1. Update Node.js to the latest LTS version
        echo 2. Clear npm cache: npm cache clean --force
        echo 3. Try using yarn instead: yarn install
        pause
        exit /b 1
    )
)

echo.
echo ✅ All Angular packages installed successfully!
echo.
echo 🎯 Next steps:
echo 1. Start the Flask API: python app.py (from project root)
echo 2. Start Angular dev server: ng serve
echo 3. Open browser: http://localhost:4200
echo.
pause