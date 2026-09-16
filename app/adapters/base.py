from abc import ABC, abstractmethod
from app.models.schemas import JobSchema, SearchCriteria
from app.config.logging_config import logger


class BaseJobSource(ABC):
    """Contract implemented by every permitted job source adapter."""

    def __init__(self):
        self.logger = logger.getChild(self.__class__.__name__)

    @property
    @abstractmethod
    def name(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def fetch_jobs(self, search_config: SearchCriteria | dict) -> list[JobSchema]:
        raise NotImplementedError
