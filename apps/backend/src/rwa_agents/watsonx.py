from __future__ import annotations

import logging
from typing import Any

import httpx
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class WatsonxError(Exception):
    """Base exception for watsonx client errors."""


class WatsonxAuthError(WatsonxError):
    """IBM IAM authentication failed."""


class WatsonxAPIError(WatsonxError):
    """Watsonx API call failed."""


class WatsonxResponseError(WatsonxError):
    """Watsonx response parsing failed."""

    def __init__(
        self,
        message: str,
        *,
        raw_text: str | None = None,
        token_usage: WatsonxTokenUsage | None = None,
    ) -> None:
        super().__init__(message)
        self.raw_text = raw_text
        self.token_usage = token_usage


class WatsonxTokenUsage(BaseModel):
    """Token usage metadata from watsonx response."""

    input_tokens: int = Field(default=0, ge=0)
    output_tokens: int = Field(default=0, ge=0)
    total_tokens: int = Field(default=0, ge=0)


class WatsonxResponse(BaseModel):
    """Structured response from watsonx chat completion."""

    executive_summary: str
    cro_view: str
    cfo_view: str
    token_usage: WatsonxTokenUsage


class WatsonxClient:
    """
    IBM watsonx.ai client for LLM-backed RWA executive commentary.

    Handles IBM IAM token exchange and watsonx.ai /ml/v1/text/chat API calls
    with structured JSON response parsing and token usage tracking.
    """

    def __init__(
        self,
        project_id: str,
        api_key: str,
        url: str,
        model_id: str = "meta-llama/llama-3-3-70b-instruct",
        api_version: str = "2024-03-14",
        max_new_tokens: int = 2048,
        time_limit: int = 60000,
        http_timeout: int = 120,
    ) -> None:
        """
        Initialize watsonx client.

        Args:
            project_id: IBM watsonx.ai project ID
            api_key: IBM Cloud IAM API key
            url: Regional watsonx.ai endpoint (e.g., https://eu-de.ml.cloud.ibm.com)
            model_id: Foundation model ID
            api_version: Watsonx API version
            max_new_tokens: Maximum tokens to generate
            time_limit: Generation time limit in milliseconds
            http_timeout: HTTP request timeout in seconds
        """
        self.project_id = project_id
        self.api_key = api_key
        self.url = url.rstrip("/")
        self.model_id = model_id
        self.api_version = api_version
        self.max_new_tokens = max_new_tokens
        self.time_limit = time_limit
        self.http_timeout = http_timeout
        self._iam_token: str | None = None

        logger.info(
            "WatsonxClient initialized: url=%s, model=%s, project=%s",
            self.url,
            self.model_id,
            self.project_id[:8] + "...",
        )

    def _get_iam_token(self) -> str:
        """
        Exchange IBM Cloud API key for IAM access token.

        Returns:
            IAM access token

        Raises:
            WatsonxAuthError: If token exchange fails
        """
        if self._iam_token:
            return self._iam_token

        logger.debug("Exchanging IBM Cloud API key for IAM token")

        try:
            response = httpx.post(
                "https://iam.cloud.ibm.com/identity/token",
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                data={
                    "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
                    "apikey": self.api_key,
                },
                timeout=30,
            )
            response.raise_for_status()
            token_data = response.json()
            self._iam_token = token_data["access_token"]
            logger.info("IBM IAM token exchange successful")
            return self._iam_token

        except httpx.HTTPStatusError as exc:
            logger.error("IBM IAM token exchange failed: %s", exc)
            raise WatsonxAuthError(f"IAM authentication failed: {exc}") from exc
        except (KeyError, ValueError) as exc:
            logger.error("Failed to parse IAM token response: %s", exc)
            raise WatsonxAuthError(f"Invalid IAM token response: {exc}") from exc
        except Exception as exc:
            logger.error("Unexpected error during IAM token exchange: %s", exc)
            raise WatsonxAuthError(f"IAM token exchange error: {exc}") from exc

    def chat(self, prompt: str) -> WatsonxResponse:
        """
        Call watsonx.ai chat completion API with structured JSON response.

        Args:
            prompt: System prompt with RWA analysis context

        Returns:
            Structured watsonx response with commentary views and token usage

        Raises:
            WatsonxAPIError: If API call fails
            WatsonxResponseError: If response parsing fails
        """
        token = self._get_iam_token()

        # Build chat request with structured JSON response requirement
        messages = [
            {
                "role": "system",
                "content": (
                    "You are an expert RWA analyst. Respond ONLY with valid JSON "
                    "containing exactly these fields: executive_summary, cro_view, cfo_view. "
                    "Do not include any text outside the JSON object."
                ),
            },
            {"role": "user", "content": prompt},
        ]

        payload = {
            "messages": messages,
            "project_id": self.project_id,
            "model_id": self.model_id,
            "parameters": {
                "max_new_tokens": self.max_new_tokens,
                "time_limit": self.time_limit,
                "temperature": 0.7,
                "top_p": 0.9,
                "repetition_penalty": 1.1,
            },
        }

        logger.debug(
            "Calling watsonx chat API: model=%s, max_tokens=%d",
            self.model_id,
            self.max_new_tokens,
        )

        try:
            response = httpx.post(
                f"{self.url}/ml/v1/text/chat?version={self.api_version}",
                headers={
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                },
                json=payload,
                timeout=self.http_timeout,
            )
            response.raise_for_status()
            response_data = response.json()

            # Extract generated text
            generated_text = self._extract_generated_text(response_data)

            # Extract token usage
            token_usage = self._extract_token_usage(response_data)

            # Parse structured JSON response
            try:
                commentary = self._parse_commentary_json(generated_text)
            except WatsonxResponseError as exc:
                if exc.raw_text is None:
                    exc.raw_text = generated_text
                if exc.token_usage is None:
                    exc.token_usage = token_usage
                raise

            logger.info(
                "Watsonx chat completed: tokens=%d",
                token_usage.total_tokens,
            )

            return WatsonxResponse(
                executive_summary=commentary["executive_summary"],
                cro_view=commentary["cro_view"],
                cfo_view=commentary["cfo_view"],
                token_usage=token_usage,
            )

        except httpx.HTTPStatusError as exc:
            error_detail = self._extract_error_detail(exc.response)
            logger.error("Watsonx API call failed: %s - %s", exc, error_detail)
            raise WatsonxAPIError(f"Watsonx API error: {error_detail}") from exc
        except WatsonxResponseError:
            raise
        except Exception as exc:
            logger.error("Unexpected error during watsonx chat: %s", exc)
            raise WatsonxAPIError(f"Watsonx chat error: {exc}") from exc

    def _extract_generated_text(self, response_data: dict[str, Any]) -> str:
        """Extract generated text from watsonx response."""
        try:
            # Watsonx response structure: choices[0].message.content
            choices = response_data.get("choices", [])
            if not choices:
                raise WatsonxResponseError("No choices in watsonx response")

            message = choices[0].get("message", {})
            content = message.get("content", "")

            if not content:
                raise WatsonxResponseError("Empty content in watsonx response")

            return content.strip()

        except (KeyError, IndexError, AttributeError) as exc:
            logger.error("Failed to extract generated text: %s", exc)
            raise WatsonxResponseError(f"Invalid response structure: {exc}") from exc

    def _parse_commentary_json(self, text: str) -> dict[str, str]:
        """
        Parse structured JSON commentary from LLM response.

        Args:
            text: Generated text from watsonx

        Returns:
            Dictionary with executive_summary, cro_view, cfo_view

        Raises:
            WatsonxResponseError: If JSON parsing fails or required fields missing
        """
        import json

        try:
            # Try to extract JSON from text (handle cases where LLM adds extra text)
            json_start = text.find("{")
            json_end = text.rfind("}") + 1

            if json_start == -1 or json_end == 0:
                raise WatsonxResponseError("No JSON object found in response", raw_text=text)

            json_text = text[json_start:json_end]
            commentary = json.loads(json_text)

            # Validate required fields
            required_fields = ["executive_summary", "cro_view", "cfo_view"]
            missing_fields = [f for f in required_fields if f not in commentary]

            if missing_fields:
                raise WatsonxResponseError(
                    f"Missing required fields in JSON response: {missing_fields}",
                    raw_text=text,
                )

            return {
                "executive_summary": str(commentary["executive_summary"]),
                "cro_view": str(commentary["cro_view"]),
                "cfo_view": str(commentary["cfo_view"]),
            }

        except WatsonxResponseError:
            raise
        except json.JSONDecodeError as exc:
            logger.error("Failed to parse JSON from watsonx response: %s", exc)
            logger.debug("Response text: %s", text[:500])
            raise WatsonxResponseError(f"Invalid JSON in response: {exc}", raw_text=text) from exc
        except Exception as exc:
            logger.error("Unexpected error parsing commentary JSON: %s", exc)
            raise WatsonxResponseError(f"Commentary parsing error: {exc}", raw_text=text) from exc

    def _extract_token_usage(self, response_data: dict[str, Any]) -> WatsonxTokenUsage:
        """Extract token usage from watsonx response."""
        try:
            usage = response_data.get("usage", {})
            input_tokens = self._first_int(
                usage,
                (
                    "prompt_tokens",
                    "input_tokens",
                    "input_token_count",
                    "input_tokens_count",
                ),
            )
            output_tokens = self._first_int(
                usage,
                (
                    "completion_tokens",
                    "output_tokens",
                    "generated_tokens",
                    "generated_token_count",
                ),
            )
            total_tokens = self._first_int(
                usage,
                ("total_tokens", "total_token_count", "total_tokens_count"),
            )

            if output_tokens == 0 and response_data.get("results"):
                first_result = response_data["results"][0]
                if isinstance(first_result, dict):
                    output_tokens = self._first_int(
                        first_result,
                        ("generated_token_count", "generated_tokens"),
                    )
                    input_tokens = input_tokens or self._first_int(
                        first_result,
                        ("input_token_count", "input_tokens"),
                    )

            total_tokens = total_tokens or input_tokens + output_tokens

            return WatsonxTokenUsage(
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                total_tokens=total_tokens,
            )

        except Exception as exc:
            logger.warning("Failed to extract token usage, using defaults: %s", exc)
            return WatsonxTokenUsage()

    def _first_int(self, data: dict[str, Any], keys: tuple[str, ...]) -> int:
        """Return the first integer-like usage value for the given keys."""
        for key in keys:
            value = data.get(key)
            if isinstance(value, bool) or value is None:
                continue
            if isinstance(value, int):
                return max(0, value)
            if isinstance(value, float):
                return max(0, int(value))
            if isinstance(value, str) and value.isdigit():
                return int(value)
        return 0

    def _extract_error_detail(self, response: httpx.Response) -> str:
        """Extract error detail from failed watsonx response."""
        try:
            error_data = response.json()
            # Try common error message fields
            for field in ["error", "message", "detail", "errors"]:
                if field in error_data:
                    return str(error_data[field])
            return str(error_data)
        except Exception:
            return response.text[:200]


# Made with Bob
