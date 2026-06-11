from abc import ABC, abstractmethod
from pydantic import BaseModel


class LLMBaseError(Exception):
    """Parent exception for all LLM issues. Useful for a final 'catch-all'."""

    pass


class LLMRateLimitError(LLMBaseError):
    """
    What it means: The API key ran out of quota or hit a tokens-per-minute ceiling.
    How your app reacts: Tells the user to wait, or automatically retries after a short delay.
    """

    pass


class LLMInvalidRequestError(LLMBaseError):
    """
    What it means: Context window exceeded, bad prompt syntax, or blocked by content safety filters.
    How your app reacts: Does NOT retry (it will fail again). Logs a critical alert and tells the user to shorten or change their input.
    """

    pass


class LLMServerError(LLMBaseError):
    """
    What it means: OpenAI or Anthropic is having a partial outage (500/503 status codes).
    How your app reacts: Immediately switches the request over to a backup provider (e.g., switches OpenAI -> Anthropic).
    """

    pass


class BaseLLMProvider(ABC):
    """This is an abstract base class for a LLM (Local Language Model) provider."""

    def __init__(self, api_key: str = None, host:str = None):
        self._api_key = api_key
        self.is_local = host and ("localhost" in host or "127.0.0.1" in host)

        if not self.is_local and not self._api_key:
            raise ValueError(
                f"LLM Provider Error: An API key must be supplied or set in your "
                f"environment to initialize '{self.__class__.__name__}'."
            )

    @abstractmethod
    def generate(
        self,
        model: str,
        system_prompt: str,
        user_prompt: str,
        response_format: type[BaseModel],
    ) -> type[BaseModel]:
        """This method must implemented by every LLM Provider"""
        pass

    @abstractmethod
    @property
    def client(self):
        pass
