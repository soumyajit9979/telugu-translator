# Stage 1: Build dependencies
FROM python:3.10-slim-buster as build

WORKDIR /app

COPY app/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Final image
FROM python:3.10-slim-buster

WORKDIR /app

# Copy installed dependencies from build stage
COPY --from=build /usr/local /usr/local

# Copy the rest of the application
COPY app/ .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
