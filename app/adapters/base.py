from abc import ABC, abstractmethod
from typing import List
from app.models.schemas import JobSchema
from app.config.logging_config import logger

class BaseJobSource(ABC):
    """
    Abstract Base Class for all job sources.
    """
    
    def __init__(self):
        # Every adapter gets its own logger context (e.g., JobAutomation.LinkedInAdapter)
        self.logger = logger.getChild(self.__class__.__name__)

    @abstractmethod
    def fetch_jobs(self, search_config: dict) -> List[JobSchema]:
        """
        Fetch jobs based on configuration and return a normalized list of JobSchema.
        Must be implemented by every child class.
        """
        pass