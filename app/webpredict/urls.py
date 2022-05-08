from django.urls import path

from .views import KnnSet, KnnAdd, KnnDescription, KnnSelect, RandomForestAdd, RFDescription, RFSelect
from .views import RandomForestSet, XGBoostSet, XGBoostAdd, XGBDescription, XGBSelect
from .views import VacancyDescription
from .views import VacancySortId, VacancySortName, VacancySortDate, VacancySortSkills, VacancySortSalary
from .views import VacancyView, VacancyLoad, VacancyPredictRF, VacancyPredictKNN, VacancyPredictXG
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', VacancyView.as_view(), name='index'),
    path('load/', VacancyLoad.as_view(), name='load'),
    path('random_forest/', VacancyPredictRF.as_view(), name='predict_rf'),
    path('knn/', VacancyPredictKNN.as_view(), name='predict_knn'),
    path('xg/', VacancyPredictXG.as_view(), name='predict_xg'),
    path('id/', VacancySortId.as_view(), name='sort_id'),
    path('name/', VacancySortName.as_view(), name='sort_name'),
    path('date/', VacancySortDate.as_view(), name='sort_date'),
    path('salary/', VacancySortSalary.as_view(), name='sort_salary'),
    path('skills/', VacancySortSkills.as_view(), name='sort_skills'),
    path('<int:pk>/', VacancyDescription.as_view(), name='description'),

    path('set_random_forest/', RandomForestSet.as_view(), name='set_rf'),
    path('set_knn/', KnnSet.as_view(), name='set_knn'),
    path('set_xgb/', XGBoostSet.as_view(), name='set_xgb'),

    path('add_rf/', RandomForestAdd.as_view(), name='add_rf'),
    path('add_knn/', KnnAdd.as_view(), name='add_knn'),
    path('add_xgb/', XGBoostAdd.as_view(), name='add_xgb'),

    path('random_forest/<int:pk>', RFDescription.as_view(), name='description_rf'),
    path('knn/<int:pk>/', KnnDescription.as_view(), name='description_knn'),
    path('xgb/<int:pk>', XGBDescription.as_view(), name='description_xgb'),

    path('select_rf/<int:pk>', RFSelect.as_view(), name='select_rf'),
    path('select_knn/<int:pk>', KnnSelect.as_view(), name='select_knn'),
    path('select_xgb/<int:pk>', XGBSelect.as_view(), name='select_xgb'),

]
if bool(settings.DEBUG):
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)