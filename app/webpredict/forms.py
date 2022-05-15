from django.forms import ModelForm
from .models import Vacancy, KnnModel, XGBoostModel, RandomForestModel, RidgeModel


class VacancyForm(ModelForm):
    class Meta:
        model = Vacancy
        fields = (
            "name",
            "area",
            "employer",
            "employment",
            "schedule",
            "description",
            "skills",
            "salary",
        )

class RidgeModelForm(ModelForm):
    class Meta:
        model = RidgeModel
        fields = (
            "name",
        )



class KnnModelForm(ModelForm):
    class Meta:
        model = KnnModel
        fields = (
            "name",
            "neighbors",
            "weights",
            "p",
        )


class RandomForestModelForm(ModelForm):
    class Meta:
        model = RandomForestModel
        fields = (
            "name",
            "estimators",
            "max_features",
            "min_samples_split",
            "min_samples_leaf",
        )


class XGBoostModelForm(ModelForm):
    class Meta:
        model = XGBoostModel
        fields = (
            "name",
            "estimators",
            "max_depth",
            "colsample_bytree",
            "alpha",
        )