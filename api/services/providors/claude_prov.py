from base import (
    BaseLLMProvider,
    LLMBaseError,
    LLMInvalidRequestError,
    LLMRateLimitError,
    LLMServerError,
)
from anthropic import Anthropic
from langfuse import observe
import os
import anthropic


class AnthropicProvidor(BaseLLMProvider):
    def __init__(self):
        self._api_key = os.get("AI_API_KEY")
        self._client = None

        # Pass everything upward. The base class safely manages the parsing logic.
        super().__init__(self._api_key, os.getenv("AI_HOST"))

    @property
    def client(self):
        if not self._client:
            self._client = Anthropic(api_key=self._api_key)

        return self._client

    @observe
    def generate(self, model, system_prompt, user_prompt, response_format):
        try:
            response = self.client.messages.parse(
                model=model,
                system=system_prompt,
                messages=[{"role": "user", "content": user_prompt}],
                output_format=response_format,
                temperature=0.1,
                max_tokens=2000,
            )

            result = response_format.model_validate_json(response.content[0].text)
            return result
        except anthropic.RateLimitError as e:
            raise LLMRateLimitError("OpenAI capacity limit reached.") from e

        except anthropic.BadRequestError as e:
            # Handles context window limits and formatting mistakes
            raise LLMInvalidRequestError(
                "Prompt validation or token limit failed."
            ) from e

        except anthropic.InternalServerError as e:
            # Handles OpenAI downtime
            raise LLMServerError("OpenAI servers are experiencing an outage.") from e

        except anthropic.APIStatusError as e:
            # Dynamically catch other HTTP codes
            if e.status_code == 429:
                raise LLMRateLimitError("Rate limit hit.") from e
            elif e.status_code >= 500:
                raise LLMServerError("Upstream provider failure.") from e
            else:
                raise LLMInvalidRequestError(f"API Error {e.status_code}") from e
