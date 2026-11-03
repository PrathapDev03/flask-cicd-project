
# 1. Use Python base image
FROM python:3.12-slim

# 2. Set working directory
WORKDIR /app

# 3. Copy dependency file
COPY requirements.txt .

# 4. Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy application source code
COPY app.py .

# 6. Create a non-root application user
RUN useradd -m appuser

# 7. Run application as non-root user
USER appuser

# 8. Document application port
EXPOSE 5000

# 9. Start Flask using Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
