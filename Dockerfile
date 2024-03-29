FROM python:3.8

WORKDIR /star-wars

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY ./src ./src

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]