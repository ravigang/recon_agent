# """Gemini API client wrapper for AI audit intelligence."""

# from typing import Optional
# from google import genai
# from google.genai.errors import APIError

# from recon_agent.config.settings import settings
# from recon_agent.utils.logging import get_logger
# from recon_agent.utils.validators import AIServiceError

# logger = get_logger("infrastructure.gemini_client")


# class GeminiClient:
#     """Encapsulates communication with the Google Gemini API."""

#     def __init__(
#         self,
#         api_key: Optional[str] = None,
#         model_name: Optional[str] = None,
#     ) -> None:
#         self._api_key = api_key or settings.gemini_api_key
#         self._model_name = model_name or settings.gemini_model
#         self._client: Optional[genai.Client] = None

#         if self._api_key:
#             try:
#                 self._client = genai.Client(api_key=self._api_key)
#                 logger.debug("Gemini client initialized with model %s", self._model_name)
#             except Exception as err:
#                 logger.error("Failed to initialize Gemini Client: %s", err)
#                 self._client = None
#         else:
#             logger.warning("Gemini API key is not configured. AI reasoning will be unavailable.")

#     @property
#     def is_configured(self) -> bool:
#         """Return True if Gemini client is initialized and ready."""
#         return self._client is not None

#     def generate_content(self, prompt: str) -> str:
#         """Send prompt to Gemini model and return text response.

#         Args:
#             prompt: Text prompt to send to the model.

#         Returns:
#             Stripped response text.

#         Raises:
#             AIServiceError: Wrapped domain error if Gemini request fails.
#         """
#         if not self.is_configured:
#             raise AIServiceError("Gemini API key is missing or client is not configured.")

#         try:
#             assert self._client is not None
#             from google.genai import types
#             config = types.GenerateContentConfig(temperature=0.2)
#             response = self._client.models.generate_content(
#                 model=self._model_name,
#                 contents=prompt,
#                 config=config,
#             )
#             if not response or not response.text:
#                 raise AIServiceError("Received empty response from Gemini model.")

#             return response.text.strip()

#         except APIError as api_err:
#             err_msg = str(api_err)
#             logger.error("Gemini API error during generation: %s", err_msg)

#             if "429" in err_msg or "RESOURCE_EXHAUSTED" in err_msg or "quota" in err_msg.lower():
#                 raise AIServiceError("API Quota Exceeded: Daily or rate limit reached.") from api_err

#             raise AIServiceError("Gemini service encountered an API error.") from api_err

#         except AIServiceError:
#             raise

#         except Exception as err:
#             logger.error("Unexpected error during Gemini content generation: %s", err)
#             raise AIServiceError("Gemini diagnostic service is temporarily unavailable.") from err


"""Gemini API client wrapper for AI audit intelligence."""

import time
from typing import Optional
from google import genai
from google.genai import types
from google.genai.errors import APIError

from recon_agent.config.settings import settings
from recon_agent.utils.logging import get_logger
from recon_agent.utils.validators import AIServiceError

logger = get_logger("infrastructure.gemini_client")


class GeminiClient:
    """Encapsulates communication with the Google Gemini API."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        model_name: Optional[str] = None,
    ) -> None:
        self._api_key = api_key or settings.gemini_api_key
        self._model_name = model_name or settings.gemini_model
        self._client: Optional[genai.Client] = None

        if self._api_key:
            try:
                self._client = genai.Client(api_key=self._api_key)
                logger.debug("Gemini client initialized with model %s", self._model_name)
            except Exception as err:
                logger.error("Failed to initialize Gemini Client: %s", err)
                self._client = None
        else:
            logger.warning("Gemini API key is not configured. AI reasoning will be unavailable.")

    @property
    def is_configured(self) -> bool:
        """Return True if Gemini client is initialized and ready."""
        return self._client is not None

    def generate_content(self, prompt: str, max_retries: int = 3) -> str:
        """Send prompt to Gemini model with retry logic on rate limits and return text response.

        Args:
            prompt: Text prompt to send to the model.
            max_retries: Maximum number of retries if rate-limited (HTTP 429).

        Returns:
            Stripped response text.

        Raises:
            AIServiceError: Wrapped domain error if Gemini request fails.
        """
        if not self.is_configured:
            raise AIServiceError("Gemini API key is missing or client is not configured.")

        assert self._client is not None
        config = types.GenerateContentConfig(temperature=0.2)

        for attempt in range(max_retries):
            try:
                response = self._client.models.generate_content(
                    model=self._model_name,
                    contents=prompt,
                    config=config,
                )
                if not response or not response.text:
                    raise AIServiceError("Received empty response from Gemini model.")

                return response.text.strip()

            except APIError as api_err:
                err_msg = str(api_err)
                logger.error("Gemini API error during generation (Attempt %d/%d): %s", attempt + 1, max_retries, err_msg)

                # Rate Limit / Quota Exceeded handling
                if "429" in err_msg or "RESOURCE_EXHAUSTED" in err_msg or "quota" in err_msg.lower():
                    if attempt < max_retries - 1:
                        wait_time = (attempt + 1) * 2  # Wait 2s on 1st retry, 4s on 2nd retry
                        logger.warning("Rate limit hit (429). Retrying in %d seconds...", wait_time)
                        time.sleep(wait_time)
                        continue
                    raise AIServiceError("API Quota Exceeded: Daily or rate limit reached.") from api_err

                raise AIServiceError("Gemini service encountered an API error.") from api_err

            except AIServiceError:
                raise

            except Exception as err:
                logger.error("Unexpected error during Gemini content generation: %s", err)
                raise AIServiceError("Gemini diagnostic service is temporarily unavailable.") from err

        raise AIServiceError("Gemini diagnostic service failed after retries.")