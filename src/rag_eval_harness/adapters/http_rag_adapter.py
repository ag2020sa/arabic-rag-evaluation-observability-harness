from __future__ import annotations

import httpx

from rag_eval_harness.adapters.base import RAGAdapter
from rag_eval_harness.schemas import RagRequest, RagResponse


class HTTPRAGAdapter(RAGAdapter):
    """Adapter for an external RAG backend.

    Expected endpoint contract:

    POST /ask
    {
      "query": "...",
      "user_id": "...",
      "session_id": "...",
      "metadata": {...}
    }

    Response must be compatible with RagResponse fields. If your backend has a different
    schema, modify `_normalize_response` only.
    """

    name = "http_rag_adapter"

    def __init__(self, base_url: str, timeout_seconds: int = 30) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout_seconds = timeout_seconds

    async def ask(self, request: RagRequest) -> RagResponse:
        async with httpx.AsyncClient(timeout=self.timeout_seconds) as client:
            response = await client.post(f"{self.base_url}/ask", json=request.model_dump())
            response.raise_for_status()
            return self._normalize_response(response.json())

    def _normalize_response(self, payload: dict) -> RagResponse:
        return RagResponse.model_validate(payload)
