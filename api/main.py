from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from .database import SessionLocal
from .crud import *
from .schemas import *

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/api/reports/top-products", response_model=list[TopProduct])
def top_products(limit: int = 10, db: Session = Depends(get_db)):
    return [{"product": p[0], "count": p[1]} for p in get_top_products(db, limit)]

@app.get("/api/channels/{channel_name}/activity", response_model=ChannelActivity)
def channel_activity(channel_name: str, db: Session = Depends(get_db)):
    result = get_channel_activity(db, channel_name)
    return {"channel": result[0], "post_count": result[1]}

@app.get("/api/search/messages", response_model=list[SearchMessage])
def search(query: str, db: Session = Depends(get_db)):
    return [{"message": m.message, "date": m.date} for m in search_messages(db, query)]
