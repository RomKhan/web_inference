FROM python:3.9

# Установка зависимостей OpenCV
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev
#RUN make clean
#RUN make USE_OPENMP=1
    # Установка зависимостей
COPY ./backend/requirements.txt /requirements.txt
RUN pip3 install torch torchvision torchaudio
RUN pip install -r /requirements.txt

# Копирование исходного кода
COPY backend/app /app

WORKDIR /app
EXPOSE 8081
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8081", "--workers", "1"]