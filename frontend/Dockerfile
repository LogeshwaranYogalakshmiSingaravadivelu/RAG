FROM python:3.10-slim
WORKDIR /app
COPY frontend/requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["streamlit", "run", "frontend/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
