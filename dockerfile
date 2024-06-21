FROM python:3.12.0

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY package.json .

RUN npm install

COPY . .

WORKDIR /

EXPOSE 8000

CMD ["flask", "--app", "app", "run", "--debug", "--host=0.0.0.0", "--port=8000"]
