# Base image: Python 3.9 slim version to save space
FROM python:3.9-slim

# Set working directory inside the container
WORKDIR /app

# Copy requirements file first (for caching layers)
COPY requirements.txt .

# Install dependencies
# This avoid to install GPU version of torch that is large in size
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu
# We use --no-cache-dir to keep image small
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source code
COPY src/ ./src/

# Expose the port FastAPI runs on
EXPOSE 7860 

# Command to run the application
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "7860"]