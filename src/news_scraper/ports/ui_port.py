from typing import Any, Protocol

from ..domain import Article, ScrapingJob, SentimentType, Source


class DashboardServicePort(Protocol):
    async def get_dashboard_summary(self) -> dict[str, Any]: ...

    async def get_latest_articles(self, limit: int = 20) -> list[Article]: ...

    async def get_articles_by_sentiment(
        self, sentiment: SentimentType, limit: int = 20
    ) -> list[Article]: ...

    async def search_articles(
        self,
        query: str,
        tags: list[str] | None = None,
        sources: list[str] | None = None,
        limit: int = 50,
    ) -> list[Article]: ...

    async def get_trending_tags(self, limit: int = 10) -> list[dict[str, Any]]: ...

    async def get_sentiment_distribution(self) -> dict[SentimentType, int]: ...


class ScrapingControlServicePort(Protocol):
    async def start_scraping_job(
        self, source_names: list[str], tags: list[str], max_articles_per_source: int = 50
    ) -> str: ...

    async def get_job_status(self, job_id: str) -> ScrapingJob | None: ...

    async def get_recent_jobs(self, limit: int = 10) -> list[ScrapingJob]: ...

    async def get_available_sources(self) -> list[Source]: ...
