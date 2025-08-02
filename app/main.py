from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app import schemas, database, news, sentiment
from app.sentiment import analyze_sentiment
from datetime import datetime, timedelta
from collections import Counter
import json

app = FastAPI(title="News Sentiment API", version="1.0.0")

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
def get_overall_sentiment(sentiments: list[str]) -> str:
    sentiment_score = {"positive": 1, "neutral": 0, "negative": -1}
    total = sum(sentiment_score.get(s, 0) for s in sentiments)
    avg = total / len(sentiments)

    if avg > 0.2:
        return "positive"
    elif avg < -0.2:
        return "negative"
    else:
        return "neutral"


@app.post("/news-sentiment", response_model=schemas.NewsResponse)
def news_sentiment(req: schemas.NewsRequest, db: Session = Depends(get_db)):
    # Check if we have recent data (within 10 minutes)
    entry = (
        db.query(database.NewsSentiment)
        .filter(database.NewsSentiment.symbol == req.symbol.upper())
        .order_by(database.NewsSentiment.timestamp.desc())
        .first()
    )
    
    if entry and (datetime.utcnow() - entry.timestamp < timedelta(minutes=10)):
        headlines = json.loads(entry.headlines)
        overall = get_overall_sentiment([h["sentiment"] for h in headlines])
        return {
            "symbol": entry.symbol,
            "timestamp": entry.timestamp,
            "headlines": headlines,
            "overall_sentiment": overall,
        }

    # Fetch news headlines
    headlines = news.fetch_news(req.symbol)
    
    # Perform sentiment analysis for each headline
    headline_sentiments = [
        {"title": h, "sentiment": analyze_sentiment(h)} 
        for h in headlines
    ]
    
    overall = get_overall_sentiment([h["sentiment"] for h in headline_sentiments])


    # Store in database
    db_entry = database.NewsSentiment(
        symbol=req.symbol.upper(),
        headlines=json.dumps(headline_sentiments),
    )
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)

    return {
        "symbol": req.symbol.upper(),
        "timestamp": db_entry.timestamp,
        "headlines": headline_sentiments,
        "overall_sentiment": overall
    }
