FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml README.md requirements.txt ./
COPY src ./src
RUN pip install --upgrade pip && pip install -e .

COPY configs ./configs
COPY data ./data
COPY scripts ./scripts
COPY reports ./reports

EXPOSE 8080
CMD ["uvicorn", "rag_eval_harness.api.main:app", "--host", "0.0.0.0", "--port", "8080"]
