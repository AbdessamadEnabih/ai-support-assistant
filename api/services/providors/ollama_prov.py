from base import (
    BaseLLMProvider,
    LLMInvalidRequestError,
    LLMServerError,
    LLMRateLimitError,
)
from langfuse.openai import OpenAI
from langfuse import observe
import openai
import os


class OllamaProvider(BaseLLMProvider):
    def __init__(self):
        self._api_key = os.getenv("OLLAMA_API_KEY")
        self._client = None

    @property
    def client(self):
        if not self._client:
            self._client = OpenAI(
                base_url="http://localhost:11434/v1", api_key=self._api_key
            )

        return self._client

    @observe
    def generate(self, model, system_prompt, user_prompt, response_format):
        try:
            completion = self.client.chat.completions.parse(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                response_format=response_format,
                temperature=0.1,
                max_tokens=2000,
            )

            result = response_format.model_validate_json(
                completion.choices[0].message.content
            )
            return result
        except openai.RateLimitError as e:
            raise LLMRateLimitError("OpenAI capacity limit reached.") from e
        
        except openai.BadRequestError as e:
            # Handles context window limits and formatting mistakes
            raise LLMInvalidRequestError(
                "Prompt validation or token limit failed."
            ) from e
            
        except openai.InternalServerError as e:
            # Handles OpenAI downtime
            raise LLMServerError("OpenAI servers are experiencing an outage.") from e
        
        except openai.APIStatusError as e:
            # Dynamically catch other HTTP codes
            if e.status_code == 429:
                raise LLMRateLimitError("Rate limit hit.") from e
            elif e.status_code >= 500:
                raise LLMServerError("Upstream provider failure.") from e
            else:
                raise LLMInvalidRequestError(f"API Error {e.status_code}") from e
