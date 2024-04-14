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
        try:
            resized_img.save(output_buffer, format="JPEG")
        except:
            resized_img = resized_img.convert('RGB')
            resized_img.save(output_buffer, format="JPEG")

        # Получаем байты из буфера
        image_data = output_buffer.getvalue()

        # Кодируем изображение в строку base64
        base64_string = base64.b64encode(image_data).decode("utf-8")

    return base64_string


def images_to_base64(image_paths):
    images = []
    for filename in image_paths:
        if filename.endswith(('.jpg', '.jpeg', '.png', '.gif')):
            base64_string = image_to_base64(filename)
            images.append(base64_string)
    return images
