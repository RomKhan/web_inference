from fastapi import APIRouter
from utils import prepare_data, predict_price
import torch
from config import image_embedding_size

router = APIRouter()


@router.get('/full_apartment_price', status_code=200)
async def full_apartment_price(request_json: dict):
    X_cat, X_num, image_embedding = prepare_data(request_json, request_json['images'])
    price = predict_price(X_cat, X_num, image_embedding)
    return price


@router.get('/renovation_price', status_code=200)
async def renovation_price(request_json: dict):
    X_cat, X_num, image_embedding = prepare_data(request_json, request_json['images'])
    price = predict_price(X_cat, X_num, image_embedding)
    image_embedding = torch.zeros((1, image_embedding_size))
    price_with_no_renovation = predict_price(X_cat, X_num, image_embedding)
    return price - price_with_no_renovation


@router.get('/apartment_price_with_no_renovation', status_code=200)
async def apartment_price_with_no_renovation(request_json: dict):
    X_cat, X_num, image_embedding = prepare_data(request_json, [])
    price = predict_price(X_cat, X_num, image_embedding)
    return price
