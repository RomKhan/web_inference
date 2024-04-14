import os

import torch


image_embedding_size = 768
cat_features = {'residential_complex_name': 0, 'house_serie': 1, 'house_type': 2,
                'gas_supply_type': 3, 'is_chute': 4, 'concierge': 5, 'flooring_type': 6,
                'renovation': 7, 'is_mortgage_available': 8}
num_features = {'latitude': 0, 'longitude': 1, 'max_floor': 2, 'passenger_elevator_count': 3,
                'freight_elevator_count': 4, 'end_build_year': 5, 'room_count': 6,
                'total_area': 7, 'living_area': 8, 'kitchen_area': 9, 'apartment_floor': 10,
                'ceiling_height': 11, 'entrance_count': 12}
device = 'cuda' if torch.cuda.is_available() else 'cpu'
dirname = os.path.dirname(__file__)
filter_model_path = os.path.join(dirname, 'files/filter_model.pth')
price_predict_model_path = os.path.join(dirname, 'files/base_model.pt')
correct_model_path = os.path.join(dirname, 'files/final_model.pt')
encoder_name = os.path.join(dirname, os.path.join('files', 'label_encoder'))
y_mean, y_std = (20064978.601985097, 15374011.57400653)
token, secret = ('6dbb03e58a44a30b7f7ddcf27a6bf2711d731a71', '77509879ec5ea38db7cc97554ccbd470dceffdbb')