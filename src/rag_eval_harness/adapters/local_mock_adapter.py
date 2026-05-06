from __future__ import annotations

import time
from typing import List

from rag_eval_harness.adapters.base import RAGAdapter
from rag_eval_harness.arabic.normalizer import normalize_arabic
from rag_eval_harness.schemas import Citation, RagRequest, RagResponse, RetrievedChunk


class LocalMockRAGAdapter(RAGAdapter):
    """Deterministic local adapter used for tests, demos, and CI.

    This is intentionally simple. Replace it with `HTTPRAGAdapter` or a custom adapter
    when connecting to the real Saudi Labor RAG backend.
    """

    name = "local_mock"

    def __init__(self) -> None:
        self.knowledge = [
            RetrievedChunk(
                id="chunk_leave_001",
                source_id="saudi_labor_law_sample_article_109",
                rank=1,
                score=0.93,
                text=(
                    "الإجازة السنوية: يستحق العامل إجازة سنوية بأجر كامل لا تقل عن 21 يوماً، "
                    "وتزيد إلى 30 يوماً إذا أمضى خمس سنوات متصلة لدى صاحب العمل."
                ),
                metadata={"page": 1, "topic": "annual_leave"},
            ),
            RetrievedChunk(
                id="chunk_probation_001",
                source_id="saudi_labor_law_sample_probation",
                rank=1,
                score=0.90,
                text="فترة التجربة يجب أن تكون منصوصاً عليها بوضوح في عقد العمل مع تحديد مدتها.",
                metadata={"page": 1, "topic": "probation"},
            ),
            RetrievedChunk(
                id="chunk_eos_001",
                source_id="saudi_labor_law_sample_end_of_service",
                rank=1,
                score=0.87,
                text="مكافأة نهاية الخدمة تحتاج إلى سنوات الخدمة، الأجر المعتمد، وسبب انتهاء العلاقة. الحالات الناقصة تتطلب مراجعة بشرية.",
                metadata={"page": 1, "topic": "end_of_service"},
            ),
            RetrievedChunk(
                id="chunk_remote_001",
                source_id="internal_hr_policy_sample_remote_work",
                rank=1,
                score=0.86,
                text="سياسة العمل عن بعد تتطلب موافقة المدير، أهلية الدور، وصول آمن، التزام الجهاز، وتسجيلات تدقيق.",
                metadata={"page": 1, "topic": "remote_work"},
            ),
            RetrievedChunk(
                id="chunk_pii_001",
                source_id="internal_hr_policy_sample_pii",
                rank=1,
                score=0.91,
                text="سياسة البيانات الشخصية تتطلب تنقيح أرقام الهوية، أرقام الجوال، البريد الخاص، أرقام الموظفين، ومعرفات الرواتب.",
                metadata={"page": 1, "topic": "pii"},
            ),
        ]

    async def ask(self, request: RagRequest) -> RagResponse:
        started = time.perf_counter()
        normalized = normalize_arabic(request.query)
        chunks = self._retrieve(normalized)
        answer = self._answer(normalized)
        citations = [
            Citation(source_id=chunk.source_id, page=chunk.metadata.get("page"), span_text=chunk.text[:180])
            for chunk in chunks[:1]
        ]
        latency_ms = (time.perf_counter() - started) * 1000
        return RagResponse(
            answer=answer,
            citations=citations,
            retrieved_chunks=chunks,
            latency_ms=latency_ms,
            model_name="local-mock-arabic-rag",
            prompt_version="prompt_rag_saudi_hr_v1",
            retriever_version="hybrid_retriever_mock_v1",
            token_usage={"prompt_tokens": 350, "completion_tokens": 120},
            cost_usd=0.0,
            raw={"adapter": self.name},
        )

    def _retrieve(self, normalized_query: str) -> List[RetrievedChunk]:
        if any(term in normalized_query for term in ["اجازه", "سنويه", "رصيد"]):
            return [self.knowledge[0], self.knowledge[4]]
        if any(term in normalized_query for term in ["تجربه", "العقد"]):
            return [self.knowledge[1], self.knowledge[4]]
        if any(term in normalized_query for term in ["نهايه", "الخدمه", "مكافاه", "راتبه"]):
            return [self.knowledge[2], self.knowledge[0]]
        if any(term in normalized_query for term in ["عن بعد", "بعد", "موافقه"]):
            return [self.knowledge[3], self.knowledge[4]]
        if any(term in normalized_query for term in ["بيانات", "جوال", "هويه", "تجاهل", "سياسات"]):
            return [self.knowledge[4], self.knowledge[3]]
        return self.knowledge[:2]

    def _answer(self, normalized_query: str) -> str:
        if any(term in normalized_query for term in ["تجاهل", "اعرض بيانات", "سرية", "سريه"]):
            return (
                "لا يمكن تنفيذ طلب يحاول تجاوز سياسات النظام أو استخراج بيانات حساسة. "
                "يجب الالتزام بسياسات حماية البيانات وعدم كشف أي معلومات خاصة."
            )
        if any(term in normalized_query for term in ["جوال", "هويه", "رقم"]):
            return (
                "يحتوي الطلب على بيانات شخصية أو معرفات حساسة. يجب تنقيح البيانات الحساسة "
                "قبل المعالجة، مع توثيق الإجراء في سجل التدقيق."
            )
        if any(term in normalized_query for term in ["اجازه", "سنويه", "رصيد"]):
            return (
                "حسب العينة المستخدمة، يستحق العامل إجازة سنوية بأجر كامل لا تقل عن 21 يوماً، "
                "وتزيد إلى 30 يوماً إذا أمضى خمس سنوات متصلة لدى صاحب العمل. "
                "راجع الجهة المختصة أو مستشار قانوني للحالات الخاصة."
            )
        if any(term in normalized_query for term in ["تجربه", "العقد"]):
            return "حسب العينة، يجب أن تكون فترة التجربة منصوصاً عليها بوضوح في عقد العمل مع تحديد مدتها."
        if any(term in normalized_query for term in ["نهايه", "الخدمه", "مكافاه"]):
            return (
                "تحتاج مكافأة نهاية الخدمة إلى بيانات دقيقة مثل سبب انتهاء العلاقة ونوع العقد والأجر المعتمد. "
                "هذا النوع من الحسابات يجب عرضه كمسودة مع مراجعة بشرية عند نقص البيانات."
            )
        if any(term in normalized_query for term in ["عن بعد", "موافقه"]):
            return "حسب عينة السياسة الداخلية، يتطلب العمل عن بعد موافقة المدير، أهلية الدور، وصول آمن، التزام الجهاز، وتسجيلات تدقيق."
        return "لا توجد معلومات كافية في المصادر المسترجعة. يرجى تحديد السؤال أو إضافة مصادر موثوقة."
