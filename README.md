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
