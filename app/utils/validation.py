from pydantic import BaseModel, Field


class CreateJobRequest(BaseModel):
    query: str = Field(..., min_length=2, max_length=300, description="Search text like 'dentists in Chicago'")
    location: str = Field(default="", max_length=120, description="Optional location hint (text)")
    max_results: int | None = Field(default=None, ge=1, le=500)
    max_pages: int | None = Field(default=None, ge=1, le=10)
    include_reviews: bool = Field(default=True)
    language: str | None = Field(default=None, max_length=8)


def clamp_int(value: int, low: int, high: int) -> int:
    return max(low, min(high, int(value)))
