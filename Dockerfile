FROM python:3.7.2-stretch

WORKDIR /app

# ADD . /app

COPY ./requirements.txt /app
RUN pip install -r requirements.txt

# Copy the source code
COPY . /app

# Set entrypoint
# ENV FLASK_APP=manager.py
# ENV FLASK_RUN_HOST 0.0.0.0
# EXPOSE 8000

# Run Flask command
# CMD ["gunicorn", "--host", "0.0.0.0:4000", "manager:app"]
# CMD ["flask", "run", "--host", "0.0.0.0"]
CMD python manager.py