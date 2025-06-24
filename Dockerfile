FROM python:3.11
WORKDIR /project
COPY . .
RUN pip install -r requirements.txt
EXPOSE 8080
CMD [ "python", "-m", "manage.py", "runserver", "0.0.0.0:8080"]
