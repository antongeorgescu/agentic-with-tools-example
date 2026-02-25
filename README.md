# Q&A Generator with Tools - Flask API + Angular Frontend

This project provides a comprehensive Q&A generation system for financial domain queries with:
- **Flask API**: Generates question/answer pairs using Azure OpenAI and LangChain tools
- **Angular Frontend**: Interactive web interface to view Q&A pairs, topics, and tools  
- **LangChain Integration**: Intelligent tool selection for financial domain queries
- **Agentic Architecture**: Tool-based AI agents with specialized financial expertise

## Project Statistics

- **Total Lines of Code**: 2,521
  - **Python Backend**: 1,738 lines (69.0%)
  - **Angular Frontend**: 783 lines (31.0%)
- **Files**: 5 Python modules + Complete Angular 18 application
- **Tools**: 10 specialized financial tools with LangChain integration
- **Topics**: 17 predefined mortgage/loan scenarios

## Features

- **Q&A Generation**: Configurable number of question/answer pairs (1-100)
- **Tool Integration**: 10 specialized financial tools (balance, payments, refinancing, etc.)
- **Topic Management**: 17 predefined financial scenarios from mortgage domain
- **Web Interface**: Modern Angular 18 UI with real-time generation
- **API Endpoints**: RESTful API for programmatic access
- **Fallback Support**: Works with or without Azure OpenAI configuration

## Quick Start

### Option 1: Automated Setup (Windows)
```bash
# Run the automated setup script
.\start-app.ps1
```

### Option 2: Manual Setup

#### 1. Backend Setup (Flask API)
```bash
python -m venv .venv
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and set values:
- `AZURE_OPENAI_ENDPOINT`
- `AZURE_OPENAI_API_KEY` 
- `AZURE_OPENAI_API_VERSION` (default `2024-02-01`)
- `AZURE_OPENAI_DEPLOYMENT_NAME` (e.g., `gpt-35-turbo`)

#### 2. Start Flask API
```bash
python app.py
```
Server starts on `http://localhost:5000`

#### 3. Frontend Setup (Angular)
```bash
cd angular-app
npm install
ng serve
```
Frontend opens at `http://localhost:4200`

## How to Launch the Complete System

### Step 1: Setup Python Environment and Dependencies

```powershell
# Navigate to project directory
cd "C:\Users\ag4488\OneDrive - Finastra\Architecture\Agentic Sample"

# Create and activate Python virtual environment (if not already done)
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install Python dependencies
pip install flask flask-cors openai python-dotenv pydantic langchain langchain-openai langchain-community langchain-core
```

### Step 2: Launch Flask API Backend

```powershell
# Start Flask API server (from project root directory)
.\.venv\Scripts\python.exe app.py

# Expected output:
# * Running on http://127.0.0.1:5000
# * Debug mode: on
```

**Flask API will be available at:** `http://localhost:5000`

### Step 3: Setup Angular Frontend Dependencies  

```powershell
# Navigate to Angular app directory
cd angular-app

# Install Node.js dependencies (if not already done)
npm install

# Note: Requires Node.js 18+ and Angular CLI
# Install Angular CLI globally if needed: npm install -g @angular/cli
```

### Step 4: Launch Angular Frontend

```powershell
# Start Angular development server (from angular-app directory)
ng serve

# Expected output:
# ✔ Browser application bundle generation complete.
# ** Angular Live Development Server is listening on localhost:4200 **
```

**Angular Frontend will be available at:** `http://localhost:4200`

### Step 5: Test the Complete System

1. **Open browser** to `http://localhost:4200`
2. **Select number of Q&A pairs** (1-10) using the input field
3. **Click "Run Generator"** button
4. **Watch results appear** in three sections:
   - **Top Section**: Generated Q&A pairs with questions and answers
   - **Middle Section**: Topics used in generation
   - **Bottom Section**: Tools used with usage statistics

### Troubleshooting

**Port Conflicts:**
- If port 5000 is busy, modify `app.py`: `app.run(port=5001)`
- If port 4200 is busy, use: `ng serve --port 4201`

**Flask API Not Responding:**
```powershell
# Check if Flask is running
Invoke-WebRequest -Uri "http://localhost:5000/run_new_caller/1" -Method Get
```

**Angular Compilation Errors:**
```powershell
# Clear cache and reinstall
rm -rf node_modules
rm package-lock.json
npm install
```

**Azure OpenAI Not Configured:**
- System will use fallback mock responses if Azure OpenAI credentials aren't set
- For full GenAI features, configure `.env` file with Azure OpenAI credentials

### Running Both Services Simultaneously

**Option 1: Two Terminal Windows**
```powershell
# Terminal 1 - Flask API
cd "C:\Users\ag4488\OneDrive - Finastra\Architecture\Agentic Sample"
.\.venv\Scripts\python.exe app.py

# Terminal 2 - Angular App  
cd "C:\Users\ag4488\OneDrive - Finastra\Architecture\Agentic Sample\angular-app"
ng serve
```

**Option 2: Background Processes**
```powershell
# Start Flask API in background
Start-Process powershell -ArgumentList "-Command", "cd 'C:\Users\ag4488\OneDrive - Finastra\Architecture\Agentic Sample'; .\.venv\Scripts\python.exe app.py"

# Start Angular in current terminal
cd angular-app
ng serve
```

## API Endpoints

### Core Generation
- `GET /run_new_caller/<npairs>` - Generate N question/answer pairs
- `POST /run_new_caller` - Generate via JSON body `{"npairs": <int>}`

### Metadata  
- `GET /run_new_caller/tool_list` - Get available tools with descriptions
- `GET /run_new_caller/topics_list` - Get all topics for generation
- `GET /` - API documentation

### Example Usage
```bash
# Generate 5 Q&A pairs
curl http://localhost:5000/run_new_caller/5

# Get available tools
curl http://localhost:5000/run_new_caller/tool_list

# Get topics list
curl http://localhost:5000/run_new_caller/topics_list
```

## Project Structure

```
├── app.py                           # Main Flask API server (146 lines)
├── chat_tools.py                    # LangChain agent with 10 financial tools (1,072 lines)
├── generate_chats.py                # Q&A generation with Azure OpenAI (312 lines)
├── simple_app.py                    # Simplified Flask API for testing (116 lines)
├── test_api.py                      # API testing and validation (92 lines)
├── topics.json                      # 17 financial scenarios configuration
├── requirements.txt                 # Python dependencies
├── pyproject.toml                   # Python project configuration
├── start-app.ps1                    # Windows automated setup script
├── start-app.bat                    # Windows batch startup script
├── angular-app/                     # Angular 18 frontend (783 lines total)
│   ├── src/
│   │   ├── app/
│   │   │   ├── app.component.ts     # Main UI component (305 lines)
│   │   │   ├── app.component.html   # Component template (89 lines)
│   │   │   ├── app.component.css    # Component styles (227 lines)
│   │   │   ├── app-simple.component.html # Simple version (19 lines)
│   │   │   └── api.service.ts       # API communication service (47 lines)
│   │   ├── main.ts                  # Angular bootstrap (10 lines)
│   │   ├── polyfills.ts            # Browser compatibility (6 lines)
│   │   ├── styles.css              # Global styles (35 lines)
│   │   └── index.html              # Main HTML template (30 lines)
│   ├── angular.json                # Angular CLI configuration
│   ├── package.json               # Node.js dependencies
│   ├── tsconfig.json              # TypeScript configuration
│   ├── install-packages.bat       # Dependency installation script  
│   ├── install-packages.sh        # Unix dependency installation
│   └── test.html                  # Unused test file (can be removed)
└── README.md                      # Project documentation
```

## Tools Available

The system includes 10 specialized financial tools:

1. **Balance Tool** - Current loan balance and payment dates
2. **Payment Increase Tool** - Payment modification scenarios  
3. **Lump Sum Tool** - One-time payment options
4. **Interest Rate Tool** - Rate information and calculations
5. **Missed Payment Tool** - Late payment penalties
6. **Pre-approval Tool** - Pre-approval process guidance
7. **Application Tool** - Loan application assistance
8. **Refinancing Tool** - Refinancing options and advice
9. **Hardship Tool** - Financial difficulty programs
10. **Insurance Tool** - Insurance and escrow matters

## Topics Covered (17 Financial Scenarios)

1. **Balance Inquiries** - Current loan balance and final payment dates
2. **Payment Increases** - Payment modification scenarios and impacts  
3. **Lump-Sum Payments** - One-time payment contributions and limits
4. **Interest Rate Information** - Current rates and total interest calculations
5. **Missed Payments** - Penalties and repercussions for late payments
6. **Pre-Approval Status** - Application processing and requirements
7. **Post Pre-Approval Steps** - Next steps and documentation needed
8. **Loan Application Process** - Required documents and verification
9. **Rate Types & Lock Periods** - Fixed vs variable rates, promotional offers
10. **Application Requirements** - Documentation and verification processes  
11. **Amortization Adjustments** - Term length impacts on interest costs
12. **Term Renewal Options** - End-of-term choices and early renewal
13. **Prepayment Penalties** - IRD calculations and penalty waivers
14. **Annual Prepayment Options** - Prepayment limits and scheduling
15. **Refinancing Scenarios** - Debt consolidation, renovations, equity access
16. **Financial Hardship Programs** - Deferrals and payment restructuring
17. **Insurance & Escrow** - Property tax, home insurance, and payment impacts

## Angular Frontend Features

- **Modern Angular 18**: Standalone components architecture, no NgModules required
- **Interactive UI**: Responsive interface with real-time Q&A generation
- **Multi-Layer Layout**:
  - **Top Section**: Generated Q&A pairs with detailed tool information
  - **Middle Section**: Topics used in current generation  
  - **Bottom Section**: Tools used with usage statistics and descriptions
- **Real-time Generation**: Configurable pairs (1-10) with instant results
- **Tool Visualization**: Shows which financial tools were invoked for each Q&A pair
- **Auto-refresh**: Loads available topics and tools on startup
- **CORS Enabled**: Seamless communication with Flask API
- **Production Ready**: Optimized build configuration for deployment

## Development Notes

### Current Status (February 2026)
- ✅ **Fully Functional**: Both Flask API and Angular frontend are complete and working
- ✅ **Production Ready**: Code is stable with proper error handling and fallbacks  
- ✅ **Well Documented**: Comprehensive README with setup instructions
- 🧹 **Cleanup Available**: `angular-app/test.html` is unused and can be safely removed
- 📊 **Code Metrics**: 2,521 total lines across 15 source files

### Testing the API
```bash
python test_api.py
```

### Running Individual Components  
```bash
# Just generate Q&A pairs (console output)
python generate_chats.py --num-pairs 3

# Test chat tools directly
python chat_tools.py
```

### Building Angular for Production
```bash
cd angular-app
ng build --configuration production
```

### Alternative Flask Apps
- **app.py** - Full-featured API with Azure OpenAI integration
- **simple_app.py** - Simplified mock API for testing without Azure dependencies

## Dependencies

### Python Backend (Flask API)
- **Flask 3.1.0** + Flask-CORS 6.0.1 - Web framework and cross-origin support
- **Azure OpenAI 1.66.3** - Azure OpenAI SDK for Q&A generation
- **LangChain 0.1.0** + LangChain-OpenAI 0.0.5 + LangChain-Community 0.0.12 - Agent framework
- **Pydantic 2.10.6** - Data validation and serialization
- **Python-dotenv 1.0.1** - Environment variable management

### Angular Frontend (Node.js)
- **Angular 18.0.0** - Modern web framework with standalone components
- **TypeScript 5.4+** - Type-safe JavaScript development  
- **RxJS 7.8.0** - Reactive programming for HTTP communication
- **Zone.js 0.14.0** - Change detection and async handling
- **Node.js 18+** - JavaScript runtime (required)

### Development Tools
- **Angular CLI 18.0.0** - Development server and build tools
- **Karma + Jasmine** - Testing framework (configured but optional)

## Environment Variables

Required in `.env` file for full Azure OpenAI functionality:
```env
AZURE_OPENAI_ENDPOINT=https://your-instance.openai.azure.com/
AZURE_OPENAI_API_KEY=your-api-key-here
AZURE_OPENAI_API_VERSION=2024-02-01
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o-mini
```

**Note**: System works with fallback responses if Azure OpenAI is not configured.

## License

This project is for demonstration and educational purposes.
