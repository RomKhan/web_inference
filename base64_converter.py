import os
import base64
from PIL import Image
from io import BytesIO

def resize_image(image_path, target_size=(224, 224)):
    # Открываем изображение
    with Image.open(image_path) as img:
        # Ресайзим изображение
        resized_img = img.resize(target_size)

    return resized_img


def image_to_base64(image_path):
    # Ресайзим изображение
    resized_img = resize_image(image_path)

    with BytesIO() as output_buffer:
        # Сохраняем ресайзнутое изображение в буфере
        resized_img.save(output_buffer, format="JPEG")

        # Получаем байты из буфера
        image_data = output_buffer.getvalue()

        # Кодируем изображение в строку base64
        base64_string = base64.b64encode(image_data).decode("utf-8")

    return base64_string


def folder_images_to_base64(folder_path, output_file_path):
    with open(output_file_path, "w") as output_file:
        for filename in os.listdir(folder_path):
            if filename.endswith(('.jpg', '.jpeg', '.png', '.gif')):
                # Полный путь к изображению
                image_path = os.path.join(folder_path, filename)

                # Преобразование изображения в строку base64
                base64_string = image_to_base64(image_path)

                # Запись строки base64 в файл
                output_file.write(f"{filename}: {base64_string}\n")


# Пример использования:
folder_path = "images"
output_file_path = "output_base64.txt"
folder_images_to_base64(folder_path, output_file_path)