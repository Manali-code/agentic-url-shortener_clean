from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.url import URLRecord
from app.schemas import RedirectStats, ShortenRequest, ShortenResponse
from app.services.url_service import URLService

router = APIRouter()


@router.post("/shorten", response_model=ShortenResponse)
def shorten_url(payload: ShortenRequest, db: Session = Depends(get_db)):
    record = URLService.create_short_url(db, str(payload.url))
    return ShortenResponse(
        short_code=record.short_code,
        short_url=f"http://localhost:8000/r/{record.short_code}",
        original_url=record.original_url,
        clicks=record.clicks,
    )


@router.get("/r/{short_code}")
def redirect_to_url(short_code: str, db: Session = Depends(get_db)):
    record = URLService.get_record_by_code(db, short_code)
    if not record:
        raise HTTPException(status_code=404, detail="Short URL not found")

    URLService.increment_click(db, record)
    return Response(status_code=307, headers={"Location": record.original_url})


@router.get("/stats/{short_code}", response_model=RedirectStats)
def get_stats(short_code: str, db: Session = Depends(get_db)):
    record = db.query(URLRecord).filter(URLRecord.short_code == short_code, URLRecord.is_active.is_(True)).first()
    if not record:
        raise HTTPException(status_code=404, detail="Short URL not found")

    return RedirectStats(short_code=record.short_code, original_url=record.original_url, clicks=record.clicks)
