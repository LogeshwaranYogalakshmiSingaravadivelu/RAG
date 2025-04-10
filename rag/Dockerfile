FROM python:3.10-slim
WORKDIR /app
COPY rag/requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "rag.rag_api:app", "--host", "0.0.0.0", "--port", "8000"]