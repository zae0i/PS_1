# Python 공식 이미지
FROM python:3.10-slim-bullseye

ENV PYTHONUNBUFFERED=1
WORKDIR /app

# 빌드 의존성 (psycopg2 빌드 및 최적화)
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential libpq-dev gcc && \
    rm -rf /var/lib/apt/lists/*

# 요구사항 설치 (캐시 활용)
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# 앱 코드 복사
COPY . /app/

# 포트
EXPOSE 8000

# Gunicorn 실행
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application"]
