FROM python:3.12-alpine

RUN pip install --no-cache-dir kubernetes requests

WORKDIR /app

COPY controller.py .

CMD ["python", "controller.py"]