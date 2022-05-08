from django.contrib import admin

from .models import Vacancy, KnnModel, RandomForestModel, XGBoostModel


class VacancyAdmin(admin.ModelAdmin):
    list_display = ('id_hh', 'name', 'skills', 'salary', 'predict_salary')
    list_display_links = ('id_hh', 'name')
    search_fields = ('id_hh', 'name', 'salary', 'predict_salary')


admin.site.register(Vacancy, VacancyAdmin)


class KnnAdmin(admin.ModelAdmin):
    list_display = ('name', 'neighbors', 'weights', 'p')
    list_display_links = ('name',)
    search_fields = ('name', 'neighbors', 'weights', 'p')


admin.site.register(KnnModel, KnnAdmin)


class RandomForestAdmin(admin.ModelAdmin):
    list_display = ('name', 'estimators', 'max_features', 'min_samples_split', 'min_samples_leaf')
    list_display_links = ('name',)
    search_fields = ('name', 'estimators', 'max_features', 'min_samples_split', 'min_samples_leaf')


admin.site.register(RandomForestModel, RandomForestAdmin)


class XGBoostAdmin(admin.ModelAdmin):
    list_display = ('name', 'estimators', 'max_depth', 'colsample_bytree', 'alpha')
    list_display_links = ('name',)
    search_fields = ('name', 'estimators', 'max_depth', 'colsample_bytree', 'alpha')


admin.site.register(XGBoostModel, XGBoostAdmin)
