import copy
import pickle

import numpy as np
import pandas as pd
from django.db.models.query import QuerySet
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import Ridge

from xgboost import XGBRegressor
from .createdf import get_df_predict


class MLmodel:
    def __init__(self):
        self.id = None
        self.model = None
        self.X = None
        self.y = None
        self.mae = 0
        self.mse = 0
        self.split = False
        self.cross = False
        self.all_train = True
        self.trained = False
        self.filepath = None

    def set_traindata(self, query: QuerySet):
        df = pd.DataFrame(query.values())
        df_train = get_df_predict(df)
        self.X = df_train.drop(["salary", "id_hh"], axis=1)
        self.y = df_train["salary"]

    def get_split(self):
        self.split = True
        self.cross = False
        self.all_train = False
        return train_test_split(self.X, self.y, test_size=0.2, random_state=11)

    def get_cross(self):
        self.split = False
        self.cross = True
        self.all_train = False
        mae = np.round(np.abs(
            cross_val_score(copy.deepcopy(self.model), self.X, self.y, cv=5, scoring="neg_mean_absolute_error").mean()))
        mse = np.round(np.abs(
            cross_val_score(copy.deepcopy(self.model), self.X, self.y, cv=5, scoring="neg_mean_squared_error").mean()))
        return mae, mse

    def set_all(self):
        self.split = False
        self.cross = False
        self.all_train: True

    def train(self):
        if self.split:
            X_train, X_test, y_train, y_test = self.get_split()
            self.model.fit(X_train, y_train)
            y_pred = self.model.predict(X_test)
            self.mae = np.round(mean_absolute_error(y_test, y_pred))
            self.mse = np.round(mean_squared_error(y_test, y_pred))
            self.trained = True
        elif self.cross:
            self.mae, self.mse = self.get_cross()
        elif self.all_train:
            self.model.fit(self.X, self.y)
            y_pred = self.model.predict(self.X)
            self.mae = np.round(mean_absolute_error(self.y, y_pred))
            self.mse = np.round(mean_squared_error(self.y, y_pred))
            self.trained = True


class Knn(MLmodel):
    def __init__(self, neighbors: int, weights: str, p: int, id_model: int, name: str):
        super().__init__()
        self.id_model = id_model
        self.model = KNeighborsRegressor(n_neighbors=neighbors, weights=weights, p=p)
        self.X = None
        self.y = None
        self.mae = 0
        self.mse = 0
        self.split = False
        self.cross = False
        self.all_train = True
        self.trained = False
        self.filepath = None
        self.name = name

    def save_to_file(self):

        if self.trained:
            if self.name == "base":
                self.filepath = "./media/ml_models_save/base/knn.save"
                print(self.filepath)
                with open(self.filepath, "wb") as file:
                    pickle.dump(self.model, file)
            else:
                self.filepath = "./media/ml_models_save/knn_" + str(self.id_model) + ".save"
                print(self.filepath)
                with open(self.filepath, "wb") as file:
                    pickle.dump(self.model, file)


class RandomForest(MLmodel):
    def __init__(self, estimators: int, max_features: str, min_samples_split: int,
                 min_samples_leaf: int, id_model: int, name: str):
        super().__init__()
        self.id_model = id_model
        self.model = RandomForestRegressor(n_estimators=estimators, max_features=max_features,
                                           min_samples_split=min_samples_split,
                                           min_samples_leaf=min_samples_leaf)
        self.X = None
        self.y = None
        self.mae = 0
        self.mse = 0
        self.split = False
        self.cross = False
        self.all_train = True
        self.trained = False
        self.filepath = None
        self.name = name

    def save_to_file(self):

        if self.trained:
            if self.name == "base":
                self.filepath = "./media/ml_models_save/base/rf.save"
                print(self.filepath)
                with open(self.filepath, "wb") as file:
                    pickle.dump(self.model, file)
            else:
                self.filepath = "./media/ml_models_save/rf_" + str(self.id_model) + ".save"
                with open(self.filepath, "wb") as file:
                    pickle.dump(self.model, file)


class XGBoostReg(MLmodel):
    def __init__(self, estimators: int, max_depth: int, colsample_bytree: float,
                 alpha: float, id_model: int, name: str):
        super().__init__()
        self.id_model = id_model
        self.model = XGBRegressor(n_estimators=estimators, max_depth=max_depth, colsample_bytree=colsample_bytree,
                                  learning_rate=alpha)
        self.X = None
        self.y = None
        self.mae = 0
        self.mse = 0
        self.split = False
        self.cross = False
        self.all_train = True
        self.trained = False
        self.filepath = None
        self.name = name

    def save_to_file(self):

        if self.trained:
            if self.name == "base":
                self.filepath = "./media/ml_models_save/base/xgb.save"
                print(self.filepath)
                with open(self.filepath, "wb") as file:
                    pickle.dump(self.model, file)
            else:
                self.filepath = "./media/ml_models_save/xgb_" + str(self.id_model) + ".save"
                print(self.filepath)
                with open(self.filepath, "wb") as file:
                    pickle.dump(self.model, file)


class Ridge_reg(MLmodel):
    def __init__(self, id_model: int, name: str):
        super().__init__()
        self.id_model = id_model
        self.name = name
        self.model = Ridge()
        if self.trained:
            if self.name == "base":
                self.filepath = "./media/ml_models_save/base/lr.save"
                print(self.filepath)
                with open(self.filepath, "wb") as file:
                    pickle.dump(self.model, file)
