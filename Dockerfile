# 1. Slim base image use karni hai lightweight rakhnay ke liye
FROM python:3.10-slim

# 2. Python ko cache files likhnay se rokna hai aur logs ko foran print karna hai
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Working directory set karein
WORKDIR /app

# 4. System dependencies install karein (psycopg2 database driver ke liye zaroori hain)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 5. Pehle requirements copy karein (Layer caching ka faida uthanay ke liye)
COPY requirements.txt .

# 6. Python packages install karein
RUN pip install --no-cache-dir -r requirements.txt

# 7. Baqi ka saara application code copy karein
COPY . .

# 8. Security ke liye non-root user banana (Marks check point!)
RUN useradd -m devopsuser && chown -R devopsuser:devopsuser /app
USER devopsuser

# 9. App ko run karne ki command (Port 8000 par expose hogi)
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]