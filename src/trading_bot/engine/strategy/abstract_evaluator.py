import logging
import pysnooper

from abc import ABC, abstractmethod


class AbstractEvaluator(ABC):
    context: dict

    def __init__(self, *args, **context) -> None:
        self.context = context

    @abstractmethod
    def evaluate(self, market_data: dict, **context) -> dict:
        pass

