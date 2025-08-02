# News Sentiment API

A FastAPI-based service that fetches news for Indian stock symbols, analyzes sentiment, and stores results in a database.

## 🎯 Features

- **POST /news-sentiment**: Analyzes news sentiment for stock symbols
- **10-minute caching**: Serves cached results for repeated requests
- **Sentiment Analysis**: Powered by Groq’s LLaMA 3 70B model for contextual accuracy  
- **Database Storage**: SQLite database for result persistence

## 🛠 Setup Instructions(Local)

### 1. Add your GROQ_API_Key
```bash
GROQ_API_KEY=your api key

```
### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Application
```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### 4. Access API Documentation
Open your browser and go to: http://127.0.0.1:8000/docs

## Dockerized Setup

### 1. Build docker image
```bash
docker-compose build
```

### 2. Start the Container
```bash
docker-compose up
```
### 3. Open in Browser
Go to: http://localhost:8000/docs to try the API.

✅ The news.db file is mounted via volume, ensuring data persists across runs.


## 📡 API Usage

### POST /news-sentiment

**Request:**
```json
{
  "symbol": "TCS"
}
```

**Response:**
```json
{
  "symbol": "TCS",
  "timestamp": "2025-01-29T18:00:00Z",
  "headlines": [
    {
      "title": "TCS reports strong Q1 growth",
      "sentiment": "positive"
    },
    {
      "title": "IT sector faces macro uncertainty",
      "sentiment": "negative"
    }
  ]
}
```

## 🔧 Technical Details

### News Fetching
- **Source**: Google News RSS feed
- **Method**: Scraping via feedparser library
- **Scope**: Indian stock symbols with "+stock" query
- **Count**: 2-3 recent headlines per request

### Sentiment Analysis
- **Tool**: llama3-70b-8192 hosted on Groq API
- **Classification**: positive, negative, or neutral
- **Prompt**: Sentiment classification of financial headlines


### Database
- **Type**: SQLite (local file: news.db)
- **Caching**: 10-minute cache for repeated symbol requests
- **Schema**: symbol, timestamp, headlines (JSON)

## 🚀 Performance Features

- **Caching**: Results cached for 10 minutes to avoid repeated API calls
- **Database Indexing**: Optimized queries with indexed symbol column
- **Error Handling**: Graceful handling of network and parsing errors
- **Overall_sentiments**: Using weighted scores overall sentiments were determined

## 📦 Project Structure

```
Diversifi/
├── app/
│   ├── main.py          # FastAPI routes
│   ├── sentiment.py     # LLaMA 3 API call
│   ├── news.py          # RSS fetching logic
│   ├── database.py      # SQLAlchemy DB config
│   └── schemas.py       # Pydantic models
├── news.db              # SQLite DB (persistent)
├── Dockerfile           # Image setup
├── docker-compose.yml   # Local containerization
├── .env                 # API Key for Groq
├── requirements.txt     # Python dependencies
└── README.md            # You are here

```

## 🤖 AI Tools Used

This project was developed with assistance from:
- **Cursor AI**: For code optimization and performance improvements
- **Groq API:** Ultra-fast inference of llama3-70b model



## 🚀 Quick Test

1. **Start the server**: `uvicorn app.main:app --reload`
2. **Go to**: http://127.0.0.1:8000/docs
3. **Try the `/news-sentiment` endpoint** with symbol "TCS"
4. **Check the response format** matches the assignment specification

