FROM python:3.9

ARG GRADIO_SERVER_PORT=7861
ENV GRADIO_SERVER_PORT=${GRADIO_SERVER_PORT}

# Установка зависимостей
COPY ./frontend/requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

# Копирование исходного кода
COPY /frontend/app /app

WORKDIR /app
CMD ["python", "/app/main.py", "--host", "0.0.0.0", "--port", "7861"]