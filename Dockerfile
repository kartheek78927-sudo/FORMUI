FROM python:3.12-slim

# Create a non-root user and app directory
RUN useradd --create-home --shell /bin/bash appuser
WORKDIR /home/appuser/app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .
RUN chown -R appuser:appuser /home/appuser/app

USER appuser

ENV FLASK_ENV=production
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

EXPOSE 8080

CMD ["python", "app.py"]
