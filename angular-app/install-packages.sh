#!/bin/bash
# Angular Package Installation Script for Linux/macOS

echo "🚀 Installing Angular packages for Q&A Generator App..."
echo ""

# Check if we're in the angular-app directory
if [ ! -f "package.json" ]; then
    echo "❌ Error: package.json not found. Make sure you're in the angular-app directory."
    echo "Run this script from: angular-app/"
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Error: Node.js is not installed."
    echo "Please install Node.js from: https://nodejs.org/"
    exit 1
fi

echo "✅ Node.js version: $(node --version)"

# Check if npm is available
if ! command -v npm &> /dev/null; then
    echo "❌ Error: npm is not available."
    exit 1
fi

echo "✅ npm version: $(npm --version)"

# Check if Angular CLI is installed globally
if ! command -v ng &> /dev/null; then
    echo "🔧 Angular CLI not found. Installing globally..."
    npm install -g @angular/cli
    if [ $? -ne 0 ]; then
        echo "❌ Error: Failed to install Angular CLI"
        exit 1
    fi
    echo "✅ Angular CLI installed successfully"
else
    echo "✅ Angular CLI version: $(ng version --skip-confirmation 2>/dev/null | grep 'Angular CLI' | head -1)"
fi

# Clean previous installation
echo ""
echo "🧹 Cleaning previous installation..."
if [ -d "node_modules" ]; then
    rm -rf node_modules
    echo "✅ Removed node_modules directory"
fi

if [ -f "package-lock.json" ]; then
    rm package-lock.json
    echo "✅ Removed package-lock.json"
fi

# Install packages
echo ""
echo "📦 Installing Angular packages..."
npm install

if [ $? -ne 0 ]; then
    echo "⚠️  Installation failed. Trying with --legacy-peer-deps..."
    npm install --legacy-peer-deps
    
    if [ $? -ne 0 ]; then
        echo "❌ Error: Failed to install packages even with legacy peer deps"
        echo ""
        echo "Possible solutions:"
        echo "1. Update Node.js to the latest LTS version"
        echo "2. Clear npm cache: npm cache clean --force"
        echo "3. Try using yarn instead: yarn install"
        exit 1
    fi
fi

echo ""
echo "✅ All Angular packages installed successfully!"
echo ""
echo "🎯 Next steps:"
echo "1. Start the Flask API: python app.py (from project root)"
echo "2. Start Angular dev server: ng serve"
echo "3. Open browser: http://localhost:4200"
echo ""