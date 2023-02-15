# syntax=docker/dockerfile:1
   
FROM python:3.9

WORKDIR /musicServer

COPY ./* /musicServer/

RUN pip install --no-cache --upgrade -r /musicServer/requirements.txt

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
