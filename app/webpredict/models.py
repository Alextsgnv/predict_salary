# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Vacancy(models.Model):
    id_hh = models.IntegerField()
    name = models.CharField(max_length=255)
    area = models.CharField(max_length=30, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    skills = models.TextField()
    employer = models.CharField(max_length=255, blank=True, null=True)
    employment = models.CharField(max_length=50, blank=True, null=True)
    schedule = models.CharField(max_length=50, blank=True, null=True)
    salary = models.IntegerField(blank=True, default=0, null=True)
    predict_salary = models.IntegerField(blank=True, default=0, null=True)
    date = models.DateField()

    class Meta:
        db_table = 'vacancy'
        verbose_name_plural = 'Вакансии'
        verbose_name = 'Вакансия'
        ordering = ['id_hh']


class KnnModel(models.Model):
    PARAMS_WEIGHTS = (
        ("uniform", "uniform"),
        ("distance", "distance"),
    )
    PARAMS_P = (
        (1,"manhattan distance"),
        (2,"euclidean distance"),
    )
    name = models.CharField(max_length=10)
    neighbors = models.IntegerField(default=5)
    weights = models.CharField(max_length=10, choices=PARAMS_WEIGHTS, default="U")
    p = models.IntegerField(choices=PARAMS_P, default=2)
    mae = models.FloatField(default=0)
    mse = models.FloatField(default=0)
    file_model = models.FileField(default=None)

    class Meta:
        db_table = 'knn'
        verbose_name_plural = 'Модели К-ближайших соседей'
        verbose_name = 'Модель К-ближайших соседей'
        ordering = ['id']




class RandomForestModel(models.Model):
    PARAMS_FEATURES = (
        ("log2", "log2"),
        ("sqrt", "sqrt"),
        ("auto", "auto"),
    )
    name = models.CharField(max_length=10)
    estimators = models.IntegerField(default=100)
    max_features = models.CharField(max_length=4, choices=PARAMS_FEATURES, default="auto")
    min_samples_split = models.IntegerField(default=2)
    min_samples_leaf = models.IntegerField(default=1)
    mae = models.FloatField(default=0)
    mse = models.FloatField(default=0)
    file_model = models.FileField(default=None)

    class Meta:
        db_table = 'randomforest'
        verbose_name_plural = 'Модели случайного леса'
        verbose_name = 'Модель случайного леса'
        ordering = ['id']


class XGBoostModel(models.Model):
    name = models.CharField(max_length=10)
    estimators = models.IntegerField(default=100)
    max_depth = models.IntegerField(default=6)
    colsample_bytree = models.FloatField(default=1.0)
    alpha = models.FloatField(default=0.01)
    mae = models.FloatField(default=0)
    mse = models.FloatField(default=0)
    file_model = models.FileField(default=None)

    class Meta:
        db_table = 'xgboost'
        verbose_name_plural = 'Модели градиентного бустинга'
        verbose_name = 'Модель градиентного бустинга'
        ordering = ['id']


