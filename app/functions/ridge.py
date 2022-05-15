import os
import pickle

import numpy as np
import pandas as pd
from django.db.models.query import QuerySet

from .createdf import get_df_predict


def get_predict_lr(vacancies: QuerySet) -> zip:
    df_vacancies = pd.DataFrame(vacancies.values())
    file_path = "./media/ml_models_save/base/lr.save"
    with open(file_path, "rb") as file:
        modellr = pickle.load(file)
    df_predict = get_df_predict(df_vacancies)
    X_predict = df_predict.drop(["salary", "id_hh"], axis=1)
    y_pred = modelRF.predict(X_predict)
    id_hh = df_predict.id_hh.values
    return zip(id_hh, np.round(y_pred))
