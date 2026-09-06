from pydantic import BaseModel, HttpUrl, Field


class ShortenRequest(BaseModel):
    url: HttpUrl = Field(..., description="Original destination URL")


class ShortenResponse(BaseModel):
    short_code: str
    short_url: str
    original_url: str
    clicks: int = 0


class RedirectStats(BaseModel):
    short_code: str
    original_url: str
    clicks: int
