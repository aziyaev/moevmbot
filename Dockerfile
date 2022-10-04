FROM python:3.9

WORKDIR /moevmboat

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]