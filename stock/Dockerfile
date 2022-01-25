FROM python:latest

WORKDIR /usr/share/app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY ./gen-stock-data.py ./
COPY ./ticker_* ./

ENV PYTHONUNBUFFERED=1
CMD ["python", "gen-stock-data.py"]