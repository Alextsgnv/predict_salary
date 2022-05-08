import re
from collections import Counter

import pandas as pd
from sklearn.preprocessing import OneHotEncoder

from .list_feature import get_list_feature


def get_counter(lst_skills: list) -> Counter:
    """Выводит список скилов с частотой их встречаемости"""
    set_skills = []
    for skill in lst_skills:
        set_skills = set_skills + skill.split(", ")
    return Counter(set_skills)


def get_ohe_columns(df: pd.DataFrame, list_columns: list) -> pd.DataFrame:
    """Получение списка перекодированных столбцов
    Расписания и занятости и уровня разработчика"""
    df1 = df.copy()
    columns = []
    columns_encoder = OneHotEncoder()
    schedule_cat = columns_encoder.fit_transform(df1.schedule.values.reshape(-1, 1))
    schedule_cat.todense()
    df1[columns_encoder.categories_[0]] = schedule_cat.todense()
    columns = columns + list(columns_encoder.categories_[0])
    employment_cat = columns_encoder.fit_transform(df1.employment.values.reshape(-1, 1))
    df1[columns_encoder.categories_[0]] = employment_cat.todense()
    columns = columns + list(columns_encoder.categories_[0])
    level_cat = columns_encoder.fit_transform(df1.level.values.reshape(-1, 1))
    level_cat.todense()
    df1[columns_encoder.categories_[0]] = level_cat.todense()
    columns = columns + list(columns_encoder.categories_[0])
    new_columns = list(set(list_columns).difference(columns))
    df1[new_columns] = 0
    return df1[list_columns]


def get_count_skills(str_skills: str, dict_skills: dict, main_skill: str):
    """Возвращает количество входений основного навыка main_skills
    в строке str_skills через отображение всех навыков
    str_skills - строка ключевых навыков вакансии
    dict_skills - словарь навыков отражающих отображение обычных навыков в основные
    main_skills - конкретный основной навык"""

    str_skills = str_skills.lower().split(", ")
    count = 0
    for skill in str_skills:
        if skill and dict_skills.get(skill, 0):
            if main_skill == dict_skills[skill]:
                count += 1
    return count


def get_level(str_vacancy: str, lst_level: list) -> str:
    """Возвращяет уровень разработчика из списка lst_level если он исть в строке str_vacancy
    str_vacancy - название вакансии"""

    for level in lst_level:
        if level in str_vacancy.lower():
            return level
    else:
        return "other"


def get_count_skills_in_description(
        str_skills: str, dict_skills: dict, main_skill: str
):
    """Возвращает количество входений основного навыка main_skills
    в строке str_skills через отображение всех навыков
    str_skills - строка описания вакансии
    dict_skills - словарь навыков отражающих отображение обычных навыков в основные
    main_skills - конкретный основной навык"""
    punct = re.compile("[,.()/]")
    str_skills = re.sub(punct, " ", str_skills)
    str_skills = str_skills.lower().split(" ")
    count = 0
    for skill in str_skills:
        if skill and dict_skills.get(skill, 0):
            if main_skill == dict_skills[skill]:
                count += 1
    return count


def get_df_predict(df: pd.DataFrame) -> pd.DataFrame:
    """Выводит тренировочный DataFrame"""
    df1 = df.copy()
    other, main_skills, dict_skills, lst_level = get_list_feature()
    df1["level"] = df1.name.apply(lambda x: get_level(x, lst_level))
    df1["level1"] = df1.description.apply(lambda x: get_level(x, lst_level))
    df1.loc[(df1["level"] == "other") & (df1["level1"] == "junior"), "level"] = "junior"
    df1.loc[(df1["level"] == "other") & (df1["level1"] == "middle"), "level"] = "middle"
    df1.loc[(df1["level"] == "other") & (df1["level1"] == "senior"), "level"] = "senior"
    df1.loc[(df1["level"] == "other") & (df1["level1"] == "lead"), "level"] = "lead"
    df_oh_columns = get_ohe_columns(df1, other)
    df_predict = df1[["salary", "name", "description", "skills", "id_hh"]].copy()
    for main_skill in main_skills:
        df_predict[main_skill] = df_predict["skills"].apply(
            lambda x: get_count_skills(x, dict_skills, main_skill)
        ) + df_predict["description"].apply(
            lambda x: get_count_skills_in_description(x, dict_skills, main_skill)
        )
    df_predict = pd.concat([df_oh_columns, df_predict], axis=1)
    df_predict = df_predict.dropna()
    return df_predict[other + main_skills + ["salary", "id_hh"]]
