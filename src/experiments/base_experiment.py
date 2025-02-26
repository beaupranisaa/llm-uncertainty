from abc import ABC, abstractmethod
import logging
from logging_config import logger

class BaseExperiment(ABC):
    """Abstract Base Class for AI-driven experiments."""

    def __init__(self, agent):
        self.agent = agent

    @abstractmethod
    def run(self, agent, config):
        """Each experiment type must define its own run method."""
        pass  # 🚨 This forces subclasses to implement their own version

    def _log_results(self, results):
        """Logs experiment results in a standardized format."""
        logger.info(f"✅ Experiment Completed. Total Results: {len(results)}")
        for idx, res in enumerate(results, start=1):
            logger.debug(f"📊 Result {idx}: {res}")
