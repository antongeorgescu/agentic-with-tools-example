# Q&A Generator Application Startup Script
Write-Host "Starting Q&A Generator Application..." -ForegroundColor Green
Write-Host ""

# Check if we're in the right directory
if (-not (Test-Path "app.py")) {
    Write-Host "Error: app.py not found. Make sure you're in the project root directory." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "Step 1: Installing Python dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Failed to install Python dependencies" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "Step 2: Starting Flask API server..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "python app.py"

Write-Host ""
Write-Host "Step 3: Setting up Angular app..." -ForegroundColor Yellow
Set-Location angular-app

# Check if Node.js is installed
try {
    $nodeVersion = node --version
    Write-Host "Node.js version: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "Error: Node.js is not installed. Please install Node.js from https://nodejs.org/" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if Angular CLI is available, install if not
try {
    $ngVersion = ng version --skip-confirmation 2>$null
    Write-Host "Angular CLI is available" -ForegroundColor Green
} catch {
    Write-Host "Installing Angular CLI globally..." -ForegroundColor Cyan
    npm install -g @angular/cli
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Error: Failed to install Angular CLI" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
}

Write-Host "Installing Node.js dependencies..." -ForegroundColor Cyan
# Clean install to ensure all packages are properly installed
if (Test-Path "node_modules") {
    Remove-Item -Recurse -Force "node_modules"
}
if (Test-Path "package-lock.json") {
    Remove-Item -Force "package-lock.json"
}

npm install
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Failed to install Node.js dependencies" -ForegroundColor Red
    Write-Host "Trying with --legacy-peer-deps flag..." -ForegroundColor Yellow
    npm install --legacy-peer-deps
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Error: Failed to install Node.js dependencies even with legacy peer deps" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
}

Write-Host ""
Write-Host "Step 4: Starting Angular development server..." -ForegroundColor Yellow
Write-Host ""
Write-Host "The application will open in your browser at http://localhost:4200" -ForegroundColor Green
Write-Host "Make sure the Flask API is running at http://localhost:5000" -ForegroundColor Green
Write-Host ""

ng serve --open

Read-Host "Press Enter to exit"