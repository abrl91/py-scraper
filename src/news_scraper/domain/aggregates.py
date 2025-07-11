from dataclasses import dataclass, field
from datetime import datetime

from news_scraper.domain.constants import (
    RELIABILITY_MAX_SCORE,
    RELIABILITY_MIN_SCORE,
)
from news_scraper.domain.enums import ScrapingStatus, SentimentType
from news_scraper.domain.value_objects import URL, AnalysisResult, Tag


@dataclass
class Article:
    title: str
    content: str
    url: URL
    source_name: str
    published_date: datetime | None = None
    tags: list[Tag] = field(default_factory=list)
    analysis: AnalysisResult | None = None
    scraped_at: datetime = field(default_factory=datetime.now)
    id: str | None = None

    def __post_init__(self) -> None:
        if not self.title or not self.title.strip():
            raise ValueError("Title cannot be empty")
        if not self.content or not self.content.strip():
            raise ValueError("Content cannot be empty")
        if not self.url:
            raise ValueError("URL cannot be empty")
        if not self.source_name or not self.source_name.strip():
            raise ValueError("Source name cannot be empty")

        if self.id is None:
            self.id = self._generate_id()

    def _generate_id(self) -> str:
        url_hash = str(hash(self.url.value))
        return f"{self.source_name}_{url_hash}"

    def add_tag(self, tag: Tag) -> None:
        if tag not in self.tags:
            self.tags.append(tag)

    def has_tag(self, tag_name: str) -> bool:
        return any(tag.name == tag_name.lower().strip() for tag in self.tags)

    @property
    def is_analyzed(self) -> bool:
        return self.analysis is not None

    @property
    def sentiment_type(self) -> SentimentType:
        if self.analysis and self.analysis.sentiment:
            return self.analysis.sentiment.sentiment_type
        return SentimentType.UNKNOWN


@dataclass
class Source:
    name: str
    base_url: URL
    description: str | None = None
    is_active: bool = True
    scraping_config: dict[str, str] = field(default_factory=dict)
    reliability_score: float = 1.0
    last_scraped: datetime | None = None

    def __post_init__(self) -> None:
        if not self.name or not self.name.strip():
            raise ValueError("Source name cannot be empty")
        if not self.base_url:
            raise ValueError("Base URL cannot be empty")
        if not RELIABILITY_MIN_SCORE <= self.reliability_score <= RELIABILITY_MAX_SCORE:
            raise ValueError(
                f"Reliability score must be between {RELIABILITY_MIN_SCORE} and {RELIABILITY_MAX_SCORE}, got {self.reliability_score}"
            )

    def update_last_scraped(self) -> None:
        self.last_scraped = datetime.now()

    @property
    def domain(self) -> str:
        return self.base_url.domain


@dataclass
class ScrapingJob:
    job_id: str
    sources: list[Source]
    requested_tags: list[str]
    status: ScrapingStatus = ScrapingStatus.PENDING
    start_time: datetime | None = None
    end_time: datetime | None = None
    articles_found: int = 0
    errors: list[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)

    def start(self) -> None:
        self.status = ScrapingStatus.IN_PROGRESS
        self.start_time = datetime.now()

    def complete(self, articles_count: int) -> None:
        self.status = ScrapingStatus.COMPLETED
        self.end_time = datetime.now()
        self.articles_found = articles_count

    def fail(self, error_message: str) -> None:
        self.status = ScrapingStatus.FAILED
        self.end_time = datetime.now()
        self.errors.append(error_message)

    def add_error(self, error_message: str) -> None:
        self.errors.append(error_message)

    @property
    def duration(self) -> float | None:
        if self.start_time and self.end_time:
            return (self.end_time - self.start_time).total_seconds()
        return None

    @property
    def is_running(self) -> bool:
        return self.status == ScrapingStatus.IN_PROGRESS

    @property
    def is_completed(self) -> bool:
        return self.status == ScrapingStatus.COMPLETED
