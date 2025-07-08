class NewsScrapeException(Exception):
    def __init__(self, message: str, details: str = "") -> None:
        self.message = message
        self.details = details
        super().__init__(f"{message}. {details}" if details else message)


class InvalidArticleException(NewsScrapeException):
    pass


class InvalidSourceException(NewsScrapeException):
    pass


class InvalidTagException(NewsScrapeException):
    pass


class DuplicateArticleException(NewsScrapeException):
    def __init__(self, article_id: str, existing_source: str = "") -> None:
        self.article_id = article_id
        self.existing_source = existing_source
        details = f"from source: {existing_source}" if existing_source else ""
        super().__init__(f"Article with ID '{article_id}' already exists", details)


class ScrapingJobException(NewsScrapeException):
    def __init__(self, job_id: str, message: str, details: str = "") -> None:
        self.job_id = job_id
        super().__init__(f"Job {job_id}: {message}", details)


class AnalysisException(NewsScrapeException):
    pass


class SourceConfigurationException(InvalidSourceException):
    def __init__(self, source_name: str, missing_config: str) -> None:
        self.source_name = source_name
        self.missing_config = missing_config
        super().__init__(
            f"Source '{source_name}' is missing required configuration",
            f"Missing: {missing_config}",
        )
