FROM python:3.7-slim
WORKDIR /app
COPY requirements.txt .
RUN pip3 install -r requirements.txt --no-cache-dir
COPY . .
RUN chmod ugo+x run.sh
CMD sh run.sh
#  CMD ["gunicorn", "api_yamdb.wsgi:application", "--bind", "0:8000" ]
