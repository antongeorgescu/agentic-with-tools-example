# Q&A Generator with Tools - Flask API + Angular Frontend

This project provides a comprehensive Q&A generation system with:
- **Flask API**: Generates question/answer pairs using Azure OpenAI and LangChain tools
- **Angular Frontend**: Interactive web interface to view Q&A pairs, topics, and tools
- **LangChain Integration**: Intelligent tool selection for financial domain queries

## Features

- **Q&A Generation**: Configurable number of question/answer pairs
- **Tool Integration**: 10+ specialized financial tools (balance, payments, refinancing, etc.)
- **Topic Management**: 17 predefined financial topics
- **Web Interface**: Modern Angular UI with real-time generation
- **API Endpoints**: RESTful API for programmatic access

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
ng serve --port 4202

# Expected output:
# ✔ Browser application bundle generation complete.
# ** Angular Live Development Server is listening on localhost:4202 **
```

**Angular Frontend will be available at:** `http://localhost:4202`

### Step 5: Test the Complete System

1. **Open browser** to `http://localhost:4202`
2. **Select number of Q&A pairs** (1-10) using the input field
3. **Click "Run Generator"** button
4. **Watch results appear** in three sections:
   - **Top Section**: Generated Q&A pairs with questions and answers
   - **Middle Section**: Topics used in generation
   - **Bottom Section**: Tools used with usage statistics

### Troubleshooting

**Port Conflicts:**
- If port 5000 is busy, modify `app.py`: `app.run(port=5001)`
- If port 4202 is busy, use: `ng serve --port 4203`

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
ng serve --port 4202
```

**Option 2: Background Processes**
```powershell
# Start Flask API in background
Start-Process powershell -ArgumentList "-Command", "cd 'C:\Users\ag4488\OneDrive - Finastra\Architecture\Agentic Sample'; .\.venv\Scripts\python.exe app.py"

# Start Angular in current terminal
cd angular-app
ng serve --port 4202
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
├── app.py                    # Flask API server
├── generate_chats.py         # Q&A generation logic
├── chat_tools.py            # LangChain agent with financial tools
├── topics.json              # Financial topics configuration
├── requirements.txt         # Python dependencies
├── angular-app/             # Angular frontend
│   ├── src/app/            
│   │   ├── app.component.*  # Main UI component
│   │   └── api.service.ts   # API communication
│   └── package.json        # Node.js dependencies
├── start-app.ps1           # Automated setup script
└── README.md              # This file
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

## Topics Covered

17 financial topics including:
- Balance and payment date inquiries
- Payment increase scenarios
- Lump-sum payments
- Interest rates and calculations
- Missed payments and penalties
- Pre-approval processes
- Loan applications
- Refinancing options
- Financial hardship programs
- Insurance and escrow management
- And more...

## Angular Frontend Features

- **Interactive UI**: Modern, responsive interface
- **Real-time Generation**: Click "Run" to generate new Q&A pairs
- **Three-Layer Layout**:
  - **Top**: Current question and answer (read-only text boxes)
  - **Middle**: All available topics grid
  - **Bottom**: Tools used in current generation + all available tools
- **Auto-refresh**: Loads initial data and Q&A pair on startup

## Development

### Testing the API
```bash
python test_api.py
```

### Running Individual Components
```bash
# Just generate Q&A pairs (console output)
python generate_chats.py --npairs 3

# Test chat tools directly  
python chat_tools.py
```

### Building Angular for Production
```bash
cd angular-app
ng build --prod
```

## Dependencies

### Python (Flask API)
- Flask 3.1.0 + Flask-CORS
- Azure OpenAI SDK
- LangChain + LangChain-OpenAI
- Pydantic for data validation

### Node.js (Angular Frontend) 
- Angular 17+
- RxJS for HTTP communication
- TypeScript 5.2+

## Environment Variables

Required in `.env` file:
```env
AZURE_OPENAI_ENDPOINT=https://your-instance.openai.azure.com/
AZURE_OPENAI_API_KEY=your-api-key-here
AZURE_OPENAI_API_VERSION=2024-02-01
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-35-turbo
```

## License

This project is for demonstration purposes.
