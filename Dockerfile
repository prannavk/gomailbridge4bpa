FROM python:3.11-slim

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY . .

# Expose Flask port
# EXPOSE 5050
# Run the app - Dev
# CMD ["python", "run.py"]

# Use Gunicorn to run Flask app (from run.py)
CMD ["gunicorn", "--bind", "0.0.0.0:5050", "run:app"]
