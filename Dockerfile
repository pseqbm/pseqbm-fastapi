#first layer
FROM python:3.9.7
#second layer
WORKDIR /usr/src/app
#third layer
COPY requirements.txt ./
#fourth layer
RUN pip install --no-cache-dir -r requirements.txt
#fifth layer
COPY . .
#sixth layer
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]