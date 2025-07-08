from dataclasses import dataclass, field
from datetime import datetime
from urllib.parse import urlparse

from news_scraper.domain.constants import (
    SENTIMENT_MAX_CONFIDENCE,
    SENTIMENT_MAX_SCORE,
    SENTIMENT_MIN_CONFIDENCE,
    SENTIMENT_MIN_SCORE,
    TAG_MAX_RELEVANCE_SCORE,
    TAG_MIN_RELEVANCE_SCORE,
)
from news_scraper.domain.enums import SentimentType


@dataclass(frozen=True)
class URL:
    value: str

    def __post_init__(self) -> None:
        parsed = urlparse(self.value)
        if not parsed.scheme or not parsed.netloc:
            raise ValueError(f"Invalid URL format: {self.value}")

    @property
    def domain(self) -> str:
        return urlparse(self.value).netloc

    @property
    def base_url(self) -> str:
        parsed = urlparse(self.value)
        return f"{parsed.scheme}://{parsed.netloc}"


@dataclass(frozen=True)
class SentimentScore:
    score: float  # Range: -1.0 (very negative) to 1.0 (very positive)
    confidence: float  # Range: 0.0 (low confidence) to 1.0 (high confidence)

    def __post_init__(self) -> None:
        if not SENTIMENT_MIN_SCORE <= self.score <= SENTIMENT_MAX_SCORE:
            raise ValueError(
                f"Score must be between {SENTIMENT_MIN_SCORE} and {SENTIMENT_MAX_SCORE}, got {self.score}"
            )
        if not SENTIMENT_MIN_CONFIDENCE <= self.confidence <= SENTIMENT_MAX_CONFIDENCE:
            raise ValueError(
                f"Confidence must be between {SENTIMENT_MIN_CONFIDENCE} and {SENTIMENT_MAX_CONFIDENCE}, got {self.confidence}"
            )

    @property
    def sentiment_type(self) -> SentimentType:
        if self.confidence < SENTIMENT_MIN_CONFIDENCE:
            return SentimentType.UNKNOWN
        elif self.score > SENTIMENT_MAX_SCORE:
            return SentimentType.POSITIVE
        elif self.score < SENTIMENT_MIN_SCORE:
            return SentimentType.NEGATIVE
        else:
            return SentimentType.NEUTRAL


@dataclass
class Tag:
    name: str
    category: str | None = None
    relevance_score: float = TAG_MAX_RELEVANCE_SCORE

    def __post_init__(self) -> None:
        if not self.name or not self.name.strip():
            raise ValueError("Tag name cannot be empty")
        if not TAG_MIN_RELEVANCE_SCORE <= self.relevance_score <= TAG_MAX_RELEVANCE_SCORE:
            raise ValueError(
                f"Relevance score must be between {TAG_MIN_RELEVANCE_SCORE} and {TAG_MAX_RELEVANCE_SCORE}, got {self.relevance_score}"
            )

        self.name = self.name.strip().lower()


@dataclass
class AnalysisResult:
    sentiment: SentimentScore | None = None
    keywords: list[str] = field(default_factory=list)
    topics: list[str] = field(default_factory=list)
    word_count: int = 0
    reading_time_in_minutes: float = 0.0
    analysis_timestamp: datetime = field(default_factory=datetime.now)

    def __post_init__(self) -> None:
        if self.word_count < 0:
            raise ValueError("Word count cannot be negative")
        if self.reading_time_in_minutes < 0:
            raise ValueError("Reading time cannot be negative")
        if self.analysis_timestamp > datetime.now():
            raise ValueError("Analysis timestamp cannot be in the future")
