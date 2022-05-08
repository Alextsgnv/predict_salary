import json
import re
import time

import pandas as pd
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


def get_page(params: dict, vac: str, page: int = 0) -> str:
    """Получает данные с стайта hh.ru и спользованием API
    на основе заданных параметров"""
    params["page"] = page
    params["text"] = vac
    req = requests.get("https://api.hh.ru/vacancies", params)
    data = (req.content.decode())
    req.close()
    return data


def get_additional_information(url: str) -> dict:
    """Выводит дополнительную информацию о вакансии"""
    with requests.get(url) as req:
        data = req.content.decode()
    return json.loads(data)


def get_frame_with_salary(df: pd.DataFrame) -> pd.DataFrame:
    df.loc[(df["salary_to"] != 0) & (df["salary_from"] != 0),
           "salary"] = (df["salary_to"] + df["salary_from"]) // 2
    df.loc[df["salary_to"] != 0, "salary"] = df["salary_to"]
    df.loc[(df["salary_to"] == 0) & (df["salary_from"] != 0),
           "salary"] = df["salary_from"]
    df.loc[(df["salary_to"] == 0) & (df["salary_from"] == 0),
           "salary"] = 0
    df.loc[df["currency"] == "RUR", "currency_coin"] = 1
    df.loc[df["currency"] == "RUB", "currency_coin"] = 1
    df.loc[df["currency"] == "USD", "currency_coin"] = 78
    df.loc[df["currency"] == "EUR", "currency_coin"] = 83
    df.loc[df["currency"] == "KZT", "currency_coin"] = 0.17
    df.loc[df["currency"].isna(), "currency_coin"] = 0
    df["salary"] = df["salary"] * df["currency_coin"] / 1000

    return df[(df["salary"] == 0) | ((df["salary"] >= 80) & (df["salary"] < 400))]


def get_description_vacancies(json_items: list) -> list:
    """Выводит список словарей, описывающих вакансии
        Функция получения списка описания вакансий по заданным параметрам
        Основные параметры:
        id вакансии
        Название вакансии
        Место расположения офиса (по умолчанию выбран регион - Москва)
        Зарплата от
        Зарплата до
        Валюта
        Компания-работодатель
        График работы"""
    description_vacancies = []
    json_copy = json_items.copy()
    for items in json_copy:
        description = {}
        skills = []
        add_info = get_additional_information(items.get("url"))
        if add_info:
            description["id"] = add_info.get("id", 0)
            description["vacancy"] = add_info.get("name", "unknown")
            description["area"] = (
                add_info.get("area").get("name")
                if add_info.get("area", 0)
                else "unknown"
            )
            description["salary_from"] = (
                add_info.get("salary").get("from", 0)
                if add_info.get("salary", 0)
                else 0
            )
            description["salary_from"] = (
                description["salary_from"] if description["salary_from"] is not None else 0
            )
            description["salary_to"] = (
                add_info.get("salary").get(
                    "to", 0) if add_info.get("salary", 0) else 0
            )
            description["salary_to"] = (
                description["salary_to"] if description["salary_to"] is not None else 0
            )
            description["currency"] = (
                add_info.get("salary").get("currency", "RUB")
                if add_info.get("salary", 0)
                else "RUB"
            )
            description["employer"] = (
                add_info.get("employer").get("name")
                if add_info.get("employer", 0)
                else "unknown"
            )
            description["schedule"] = (
                add_info.get("schedule").get("name")
                if add_info.get("schedule", 0)
                else "unknown"
            )
            description["employment"] = (
                add_info.get("employment").get("name")
                if add_info.get("employment", 0)
                else "unknown"
            )
            description["description"] = add_info.get("description", "unknown")
            if add_info.get("key_skills", 0):
                for skill in add_info.get("key_skills"):
                    if skill.get("name", 0):
                        skills.append(skill.get("name"))
            description["skills"] = ", ".join(skills)
        if description:
            description_vacancies.append(description)

    return description_vacancies


def get_vacancies(only_salary: bool) -> list:
    PARAMS = {
        'area': 1,  # Поиск ощуществляется по вакансиям города Москва
        "per_page": 100,  # Кол-во вакансий на 1 странице
        # "only_with_salary": True,  # Показывать вакансии с известной ЗП
    }
    if only_salary:
        PARAMS["only_with_salary"] = True
    else:
        PARAMS["only_with_salary"] = False
    VACANCIES = ["Python"]
    lst_result = []

    for name in VACANCIES:
        vac = f"NAME:{name}"
        for page in range(0, 10):
            json_obj = json.loads(get_page(PARAMS, vac, page))
            lst_result.append(json_obj)
            time.sleep(0.7)
    vacancies = []
    for items in lst_result:
        vacancy = get_description_vacancies(items["items"])
        if vacancy:
            vacancies = vacancies + vacancy
        time.sleep(0.7)

    df = pd.DataFrame(vacancies)
    df = df.drop_duplicates(keep="first")
    df = get_frame_with_salary(df)
    tags = re.compile(r"<[a-zA-Z /]*>")
    df["description"] = df["description"].apply(lambda x: re.sub(tags, "", x))
    df = df.dropna()
    df = df[df["skills"] != ""]
    return df[['id', 'vacancy', 'area', 'employer', 'schedule', 'employment', 'description', 'skills', 'salary']].values
