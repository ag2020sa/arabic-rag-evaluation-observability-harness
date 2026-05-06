# Arabic RAG Evaluation & Observability Harness

هذا مشروع كامل لتقييم ومراقبة أنظمة RAG العربية، خصوصًا الأنظمة التي تعمل في بيئات سعودية منظمة مثل الموارد البشرية، الامتثال، الأنظمة الداخلية، والأمن السيبراني.

## الهدف

بدل أن يكون مشروع RAG مجرد chatbot يجاوب، هذا المشروع يضيف طبقة هندسية كاملة تقيس:

- جودة الاسترجاع Retrieval Quality
- جودة الإجابة وارتباطها بالمصادر
- صحة الاستشهادات Citations
- جودة اللغة العربية
- مخاطر Prompt Injection وPII Leakage
- سجلات التدقيق Audit Logs
- Telemetry وTracing
- بوابات قرار CI/CD: ترقية، حظر، أو مراجعة بشرية

## التشغيل السريع

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
make evaluate
make report
pytest -q
```

## الملفات المهمة

- `agent.md`: ملف تعليمات كامل للـ coding agent.
- `README.md`: شرح المشروع بالإنجليزية.
- `assets/visuals/`: الفيجوال النهائي للمشروع.
- `src/rag_eval_harness/`: الكود الأساسي.
- `data/golden/`: بيانات الاختبار الذهبية.
- `configs/thresholds.yaml`: thresholds للـ quality gates.
- `reports/latest_release_report.md`: تقرير release جاهز بعد التشغيل.
- `.github/workflows/evaluation.yml`: CI/CD workflow.

## كيف تربطه بمشروع RAG الحالي؟

استخدم `HTTPRAGAdapter` إذا عندك backend شغال مثل FastAPI:

```bash
export RAG_SYSTEM_URL=http://localhost:8000
rag-eval evaluate --adapter http
```

لازم endpoint `/ask` يرجع answer, citations, retrieved_chunks, latency, model_name, prompt_version, retriever_version.
