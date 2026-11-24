FROM python:3.11-slim
WORKDIR /app
COPY requests.py .
CMD ["python", "requests.py"]

# docker build -t car-price-requests:1 .
# docker run --rm -e API_URL=http://host.docker.internal:8001 car-price-requests:1
