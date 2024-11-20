# Stage 1: Build dependencies
FROM python:3.10-slim

WORKDIR /app

COPY app/requirements.txt . 

RUN pip install --no-cache-dir -r requirements.txt


# Copy installed dependencies from build stage
COPY --from=build /usr/local /usr/local

# Copy the rest of the application
COPY app/ .  

EXPOSE 8000

# Run app.py
CMD ["python", "app.py"]
