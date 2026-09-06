import secrets
from typing import Optional

from sqlalchemy.orm import Session

from app.models.url import URLRecord


class URLService:
    @staticmethod
    def normalize_original_url(url: str) -> str:
        if url.endswith("/") and url.count("/") == 3:
            return url.rstrip("/")
        return url

    @staticmethod
    def generate_short_code(length: int = 7) -> str:
        alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        return "".join(secrets.choice(alphabet) for _ in range(length))

    @staticmethod
    def create_short_url(db: Session, original_url: str) -> URLRecord:
        normalized_url = URLService.normalize_original_url(original_url)
        code = URLService.generate_short_code()
        while db.query(URLRecord).filter(URLRecord.short_code == code).first():
            code = URLService.generate_short_code()

        record = URLRecord(original_url=normalized_url, short_code=code)
        db.add(record)
        db.commit()
        db.refresh(record)
        return record

    @staticmethod
    def get_record_by_code(db: Session, short_code: str) -> Optional[URLRecord]:
        return db.query(URLRecord).filter(URLRecord.short_code == short_code, URLRecord.is_active.is_(True)).first()

    @staticmethod
    def increment_click(db: Session, record: URLRecord) -> None:
        record.clicks += 1
        db.commit()
