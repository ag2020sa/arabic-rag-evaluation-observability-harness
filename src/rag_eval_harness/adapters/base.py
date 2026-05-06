from __future__ import annotations

from abc import ABC, abstractmethod

from rag_eval_harness.schemas import RagRequest, RagResponse


class RAGAdapter(ABC):
    """Adapter contract for any RAG system under test.

    Implement this interface to wrap an existing FastAPI RAG backend, LangChain app,
    LlamaIndex pipeline, local model, or production API.
    """

    name: str = "base"

    @abstractmethod
    async def ask(self, request: RagRequest) -> RagResponse:
        raise NotImplementedError
