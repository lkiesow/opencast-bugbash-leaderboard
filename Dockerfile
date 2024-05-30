FROM python:3.12-slim
EXPOSE 8000

RUN pip install --no-cache-dir \
  flask \
  gunicorn

COPY leaderboard.py /app/leaderboard.py
COPY static /app/static
WORKDIR /app

CMD [ "gunicorn", "--bind", "0.0.0.0:8000", "leaderboard:app" ]
