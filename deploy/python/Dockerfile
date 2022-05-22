FROM python:3.9
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN pip install poetry==1.1.13
COPY poetry.lock pyproject.toml /app/
RUN poetry install

COPY . .

EXPOSE 8000

CMD ["poetry", "run", "alembic", "upgrade", "head"]
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]