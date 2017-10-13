FROM python:2.7
WORKDIR /code
RUN pip install Django
RUN pip install pyyaml
expose 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
