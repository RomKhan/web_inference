import torch
import copy
from torch import nn
import torch.nn.functional as F
from tab_transformer_pytorch import TabTransformer

class ImageModel(nn.Module):
    def __init__(self):
        super(ImageModel, self).__init__()

        self.linear1 = torch.nn.Linear(768, 200)
        self.norm = torch.nn.BatchNorm1d(200)
        self.activation = torch.nn.ReLU()
        self.linear2 = torch.nn.Linear(200, 2)

        self.linear1.weight.data.uniform_(-1, 1)
        self.linear2.weight.data.uniform_(-1, 1)

    def forward(self, x):
        x = self.linear1(x)
        x = self.norm(x)
        x = self.activation(x)
        x = self.linear2(x)
        return x


class CorrectionModel(nn.Module):
    def __init__(self, model, device):
        super(CorrectionModel, self).__init__()
        self.num_model = copy.deepcopy(model)
        self.num_model.eval()
        self.num_model.mlp = nn.Identity()
        self.mlp = nn.Sequential(
          nn.Linear(301 + 768, 1024),
          nn.ReLU(),
          nn.Linear(1024, 601),
          nn.ReLU(),
          nn.Linear(601, 1)
        )
        self.device = device

    def forward(self, X_cat, X_num, image_embedding):
        with torch.no_grad():
            features = self.num_model(X_cat, X_num)
        features = torch.cat((features, image_embedding), 1)

        return F.tanh(self.mlp(features))


