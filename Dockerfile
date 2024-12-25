FROM python:3
LABEL authors="gosvoh"

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir fastapi[standard]

COPY . .

EXPOSE 8000

ENTRYPOINT ["fastapi", "run", "main.py"]