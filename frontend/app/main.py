import os

import gradio as gr
import requests
from base64_converter import images_to_base64

url = 'http://backend:8081/endpoints/'
# url = 'http://localhost:8081/endpoints/'
# exemple1_folder = os.path.join(os.path.dirname(__file__), 'example1_images')
exemple2_folder = os.path.join(os.path.dirname(__file__), 'example2_images')
exemple3_folder = os.path.join(os.path.dirname(__file__), 'example3_images')
exemple4_folder = os.path.join(os.path.dirname(__file__), 'example4_images')


def greet(residential_complex_name, house_serie, house_type,
          gas_supply_type, is_chute, concierge, flooring_type,
          renovation, is_mortgage_available, address, max_floor,
          passenger_elevator_count, freight_elevator_count,
          end_build_year, room_count, total_area, living_area,
          kitchen_area, apartment_floor, ceiling_height,
          entrance_count, image_paths, precition_type):
    images = []
    if image_paths is not None:
        images = images_to_base64(image_paths=image_paths)

    if len(address) == 0:
        raise gr.Error("Адрес не может быть пустым")
    if len(house_serie) == 0:
        house_serie = 'unknown'
    if len(flooring_type) == 0:
        flooring_type = 'unknown'
    if house_type == 'иной':
        house_type = 'others'
    residential_complex_name = 'есть' if residential_complex_name else 'нет'
    gas_supply_type = 'есть' if gas_supply_type=='да' else 'unknown' if gas_supply_type=='неизвестно' else gas_supply_type
    is_chute = 'unknown' if is_chute == 'неизвестно' else is_chute
    concierge = 'есть' if concierge else 'unknown'
    is_mortgage_available = 'нет'

    params = {
        "address": address,
        "max_floor": max_floor,
        "passenger_elevator_count": passenger_elevator_count,
        "freight_elevator_count": freight_elevator_count,
        "end_build_year": end_build_year,
        "room_count": room_count,
        "total_area": total_area,
        "living_area": living_area,
        "kitchen_area": kitchen_area,
        "apartment_floor": apartment_floor,
        "ceiling_height": ceiling_height,
        "entrance_count": entrance_count,
        "residential_complex_name": residential_complex_name,
        "house_serie": house_serie,
        "house_type": house_type,
        "gas_supply_type": gas_supply_type,
        "is_chute": is_chute,
        "concierge": concierge,
        "flooring_type": flooring_type,
        "renovation": renovation,
        "is_mortgage_available": is_mortgage_available,
        "images": images
    }

    request_text = '0'
    try:
        if precition_type == 'Полная стоимость':
            request_text = requests.get(url + 'full_apartment_price', json=params).text
        elif precition_type == 'Стоимость ремонта':
            request_text = requests.get(url + 'renovation_price', json=params).text
        elif precition_type == 'Стоимость в отсутствии ремонта':
            request_text = requests.get(url + 'apartment_price_with_no_renovation', json=params).text
    except:
        raise gr.Error("Сервер недоступен")
    price = float(request_text.strip('"'))
    return price

with gr.Blocks() as demo:
    with gr.Row():
        with gr.Column():
            gr.Markdown(value='<h3><b>Информация о доме</b></h3>', line_breaks=True)
            house_serie = gr.Textbox(label='Название серии дома')
            house_type = gr.Dropdown(label='Тип дома', choices=[
                'иной', 'блочный', 'железобетон', 'кирпичный', 'монолитно - кирпичный', 'монолитный', 'панельный'
            ], value='иной')
            gas_supply_type = gr.Radio(label='Есть ли газ в доме?', choices=['да', 'нет', 'неизвестно'], value='неизвестно')
            is_chute = gr.Radio(label='Есть ли мусоропровод?', choices=['да', 'нет', 'неизвестно'], value='неизвестно')
            flooring_type = gr.Dropdown(label='Тип перекрытий', choices=[
                'бетонный', 'деревянный', 'железобетонный', 'иной', 'монолитный', 'нет   информация', 'смешанный'
            ])
            max_floor = gr.Number(label='Количество этажей в доме', minimum=1, value=1)
            end_build_year = gr.Number(label='Год постройки дома', minimum=1800, value=2000)
            entrance_count = gr.Number(label='Количество подьездов', minimum=1, value=1)
        with gr.Column():
            gr.Markdown(value='<h3><b>Информация о квартире</b></h3>', line_breaks=True)
            renovation = gr.Dropdown(label='Тип ремонта', choices=[
                'без   ремонт', 'дизайнерский', 'евроремонт', 'косметический', 'требовать   ремонт'
            ], value='косметический')
            room_count = gr.Number(label='Количество комнат', minimum=0, value=0)
            total_area = gr.Number(label='Общая площаь', minimum=10, value=32)
            living_area = gr.Number(label='Жилая площаь', minimum=0, value=18)
            kitchen_area = gr.Number(label='Площаь кухни', minimum=0, value=9)
            apartment_floor = gr.Number(label='Этаж квартиры', minimum=1, value=1)
            ceiling_height = gr.Number(label='Высота потолков (в метрах)', minimum=1, value=2.7)
        with gr.Column():
            gr.Markdown(value='<h3><b>Прочее</b></h3>', line_breaks=True)
            address = gr.Textbox(label='Адрес', placeholder='Введите адрес в Москве без округов')
            is_mortgage_available = gr.Checkbox(label='Ипотека доступна')
            residential_complex_name = gr.Checkbox(label='ЖК есть название')
            concierge = gr.Checkbox(label='Есть консьерж')
            passenger_elevator_count = gr.Number(label='Количество пассажирских лифтов', minimum=0, value=1)
            freight_elevator_count = gr.Number(label='Количество грузовых лифтов', minimum=0, value=0)
            precition_type = gr.Dropdown(label='Тип предсказания', choices=[
                'Полная стоимость', 'Стоимость ремонта', 'Стоимость в отсутствии ремонта'
            ], value='Полная стоимость')
            images = gr.File(file_count="multiple", label='Изображения квартиры', height=200)
    with gr.Row():
        with gr.Column():
            gr.Markdown(value='<h3><b>Предсказание</b></h3>', line_breaks=True)
            outputs = gr.Textbox(label='Предсказание стоимости', show_label=False)
            btn = gr.Button("Предсказать цену")
            btn.click(greet, inputs=[
              residential_complex_name, house_serie, house_type, gas_supply_type,
              is_chute, concierge, flooring_type, renovation, is_mortgage_available,
              address, max_floor, passenger_elevator_count, freight_elevator_count,
              end_build_year, room_count, total_area, living_area, kitchen_area,
              apartment_floor, ceiling_height, entrance_count, images, precition_type],
                      outputs=[outputs])
            examples = gr.Examples(examples=[
                # [False, 'индивидуальный   проект', 'панельный', 'неизвестно',
                #  'неизвестно', False, 'нет   информация', 'евроремонт', False,
                #  'Москва, Филевский бул., 17', 12, 1, 1,
                #  2014, 2, 52.2, 31, 8.5,
                #  6, 2.75, 12, [os.path.join(exemple1_folder, name) for name in os.listdir(exemple1_folder)], 'Полная стоимость'],
                [False, 'индивидуальный   проект', 'панельный', 'нет',
                'нет', False, 'железобетонный', 'косметический', False,
                'Москва, ул. Мневники, 21', 19, 1, 1,
                1982, 2, 54.9, 29.9, 9.2,
                7, 2.8, 1, [os.path.join(exemple2_folder, name) for name in os.listdir(exemple2_folder)], 'Полная стоимость'],
                [False, 'и - 209а', 'блочный', 'неизвестно',
                 'неизвестно', False, 'железобетонный', 'косметический', False,
                 'Москва, Высотный проезд, 4', 14, 2, 2,
                 1971, 1, 37.8, 22, 9,
                 12, 2.7, 1, [os.path.join(exemple3_folder, name) for name in os.listdir(exemple3_folder)],
                 'Полная стоимость'],
                [True, 'индивидуальный   проект', 'монолитный', 'нет',
                 'да', False, 'нет   информация', 'косметический', False,
                 'Москва, Печорская ул., 7', 25, 1, 2,
                 2022, 2, 60.8, 32, 10,
                 17, 2.8, 1, [os.path.join(exemple4_folder, name) for name in os.listdir(exemple4_folder)],
                 'Полная стоимость']
            ], inputs=[
                residential_complex_name, house_serie, house_type, gas_supply_type,
                is_chute, concierge, flooring_type, renovation, is_mortgage_available,
                address, max_floor, passenger_elevator_count, freight_elevator_count,
                end_build_year, room_count, total_area, living_area, kitchen_area,
                apartment_floor, ceiling_height, entrance_count, images, precition_type])

demo.launch(server_name="0.0.0.0", share=False)
