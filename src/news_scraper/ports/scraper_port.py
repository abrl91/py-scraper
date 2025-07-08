from typing import Protocol

from ..domain import Article, Source


class WebScraperPort(Protocol):
    async def scrape_articles(
        self, sources: Source, tags: list[str], max_articles: int = 50
    ) -> list[Article]: ...

    async def is_source_available(self, source: Source) -> bool: ...

    async def validate_source_config(self, source: Source) -> None: ...
