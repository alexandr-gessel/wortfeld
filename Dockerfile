FROM python:3.12-slim

# load for spaCy
RUN apt-get update && apt-get install -y \
    gcc \
    build-essential \
    libffi-dev \
    libblas-dev \
    liblapack-dev \
    libpython3-dev \
    python3-dev \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Python
WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# copy all
COPY . .

# start
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
