import torch
from PIL import Image
from io import BytesIO
import clip
import base64
import os
import torch.nn.functional as F
from models import ImageModel, CorrectionModel
from sklearn.preprocessing import LabelEncoder
import numpy as np
from dadata import Dadata
from config import device, cat_features, num_features, image_embedding_size,\
    filter_model_path, price_predict_model_path, encoder_name, y_std, y_mean, correct_model_path, token, secret
import __main__
setattr(__main__, "ImageModel", ImageModel)
setattr(__main__, "CorrectionModel", CorrectionModel)


def init_encoder(key):
    encoder = LabelEncoder()
    path = f'{encoder_name}_{key}.npy'
    encoder.classes_ = np.load(path, allow_pickle=True)
    # print(key, encoder.classes_, '\n')
    return encoder

correction_model = torch.load(correct_model_path, map_location=device).to(device)
correction_model.eval()
price_predict_model = torch.load(price_predict_model_path, map_location=device).to(device)
price_predict_model.eval()
clip_model, image_transform = clip.load('ViT-L/14', device=device)
clip_model.eval()
filter_model = torch.load(filter_model_path, map_location=device).to(device)
filter_model.eval()
encoders = {key: init_encoder(key) for key in cat_features}
dadata = Dadata(token, secret)


def prepare_image(base64_data):
    image_data = base64.b64decode(base64_data)
    pil_image = Image.open(BytesIO(image_data))
    return image_transform(pil_image)


def cat_encode(key, value):
    return encoders[key].transform([value])[0]


def prepare_data(json, images=None):
    X_cat = torch.zeros((1, 9), dtype=torch.long)
    X_num = torch.zeros((1, 13))
    for key in json:
        if key in cat_features:
            X_cat[0][cat_features[key]] = cat_encode(key, json[key])
        elif key in num_features:
            X_num[0][num_features[key]] = float(json[key])
    if 'address' in json and len(json['address']) > 0:
        result = dadata.suggest("address", json['address'])
        if len(result) > 0:
            lon, lat = result[0]['data']['geo_lon'], result[0]['data']['geo_lat']
            X_num[0][num_features['latitude']] = float(lat)
            X_num[0][num_features['longitude']] = float(lon)
        else:
            raise Exception('не получилось найти координаты, напишите аддресс в дргой форме')

    image_embedding = torch.zeros(image_embedding_size)
    if len(images) > 0:
        images = torch.stack([prepare_image(file) for file in images], dim=0)
        with torch.no_grad():
            embeddings = F.normalize(clip_model.encode_image(images.to(device)))
            preds = filter_model(embeddings)
        preds, current_classes = torch.max(F.softmax(preds, -1), dim=1)
        inside_idx = np.where(current_classes.numpy() == 1)[0]
        if len(inside_idx) > 0:
            image_embedding = embeddings[inside_idx].mean(0)

    image_embedding = torch.unsqueeze(image_embedding, 0)
    return X_cat, X_num, image_embedding


def predict_price(X_cat, X_num, embedding):
    with torch.no_grad():
        pred = price_predict_model(X_cat.to(device), X_num.to(device)) * y_std + y_mean
        correction = correction_model(X_cat.to(device), X_num.to(device), embedding.to(device))
    pred = pred + correction * pred
    return pred.tolist()[0][0]
