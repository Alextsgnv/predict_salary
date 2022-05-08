import os
import pickle

import numpy as np
import pandas as pd
from django.db.models.query import QuerySet

from .createdf import get_df_predict


def get_predict_knn(vacancies: QuerySet, file_path: str = "") -> zip:
    path = os.getcwd()
    df_vacancies = pd.DataFrame(vacancies.values())
    if not file_path:
        file_path = "./media/ml_models_save/base/knn.save"
    else:
        file_path = os.path.join(path, file_path)
    with open(file_path, "rb") as file:
        knn = pickle.load(file)
    df_predict = get_df_predict(df_vacancies)
    X_predict = df_predict.drop(["salary", "id_hh"], axis=1)
    y_pred = knn.predict(X_predict)
    id_hh = df_predict.id_hh.values
    return zip(id_hh, np.round(y_pred))
