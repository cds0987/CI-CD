# Base image
FROM python:3.11-slim

# Thư mục làm việc trong container
WORKDIR /app

# Copy requirements trước (tận dụng Docker layer cache)
COPY requirements.txt .

# Cài thư viện
RUN pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ source code
COPY . .

# Chạy agent
CMD ["python", "testapi.py"]
