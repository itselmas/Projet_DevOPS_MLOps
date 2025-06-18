#Base image
FROM python:3.10-slim

#Define work folder in the container
WORKDIR /app

#Copying files
COPY requirements.txt .
COPY training/ ./training/
COPY data/ ./data/

#Installing dependencies
RUN pip install --no-cache-dir -r requirements.txt

#Executing default command
CMD ["python", "training/train.py"]
