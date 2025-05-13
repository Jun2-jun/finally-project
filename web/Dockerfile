FROM python:3.10-slim

# 1. 시스템 패키지 설치
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 2. 파이썬 패키지 설치
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

# 3. 소스 복사 및 실행
COPY . .
EXPOSE 80
CMD ["python", "app.py"]

