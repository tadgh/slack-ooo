FROM kennethreitz/pipenv
COPY . /app
WORKDIR .
CMD ["python3", "-u", "main.py"]
