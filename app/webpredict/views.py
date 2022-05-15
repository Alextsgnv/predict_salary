import datetime

from django.core.files import File
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView, CreateView
from django.views.generic.list import ListView
from functions.knn import get_predict_knn
from functions.loadvacansies import get_vacancies
from functions.ml_models import Knn, RandomForest, XGBoostReg, Ridge_reg
from functions.randomforest import get_predict_rf
from functions.ridge import get_predict_lr
from functions.xgboost import get_predict_xg

from .forms import VacancyForm, KnnModelForm, RandomForestModelForm, XGBoostModelForm, RidgeModelForm
from .models import Vacancy, KnnModel, RandomForestModel, XGBoostModel, RidgeModel


# Create your views here.

def add_new_vacancy(list_vacancies: list):
    for parameter_vacancy in list_vacancies:
        new_vacancy = Vacancy()
        if not Vacancy.objects.filter(id_hh=parameter_vacancy[0]).exists():
            new_vacancy.id_hh = parameter_vacancy[0]
            new_vacancy.name = parameter_vacancy[1]
            new_vacancy.area = parameter_vacancy[2]
            new_vacancy.employer = parameter_vacancy[3]
            new_vacancy.schedule = parameter_vacancy[4]
            new_vacancy.employment = parameter_vacancy[5]
            new_vacancy.description = parameter_vacancy[6]
            new_vacancy.skills = parameter_vacancy[7]
            new_vacancy.salary = parameter_vacancy[8]
            new_vacancy.date = datetime.date.today()
            new_vacancy.save()


def add_predict_salary(predict_salary: zip):
    for id_hh, predict in predict_salary:
        vacancy = Vacancy.objects.get(id_hh=id_hh)
        vacancy.predict_salary = predict
        vacancy.save()


def create_base_model():
    if not RidgeModel.objects.filter(name="base").exists():
        new_lr = RidgeModel()
        new_lr.name = "base"
        with open("./media/ml_models_save/base/lr.save", "rb") as file:
            new_lr.file_model = File(file)
            new_lr.save()
    if not KnnModel.objects.filter(name="base").exists():
        new_knn = KnnModel()
        new_knn.name = "base"
        new_knn.weights = "distance"
        new_knn.neighbors = 11
        new_knn.p = 2
        with open("./media/ml_models_save/base/knn.save", "rb") as file:
            new_knn.file_model = File(file)
            new_knn.save()
    if not RandomForestModel.objects.filter(name="base").exists():
        new_rf = RandomForestModel()
        new_rf.name = "base"
        new_rf.estimators = 100
        new_rf.min_samples_leaf = 1
        new_rf.max_features = 'sqrt'
        with open("./media/ml_models_save/base/rf.save", "rb") as file:
            new_rf.file_model = File(file)
            new_rf.save()
    if not XGBoostModel.objects.filter(name="base").exists():
        new_xgb = XGBoostModel()
        new_xgb.name = "base"
        new_xgb.estimators = "500"
        new_xgb.max_depth = 3
        new_xgb.colsample_bytree = 0.2
        new_xgb.alpha = 0.01
        with open("./media/ml_models_save/base/xgb.save", "rb") as file:
            new_xgb.file_model = File(file)
            new_xgb.save()


class VacancyView(ListView):
    template_name = 'webpredict/index.html'
    model = Vacancy
    success_url = reverse_lazy('index')
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["vacancies"] = Vacancy.objects.order_by('id')
        return context


class VacancyLoad(ListView):
    template_name = 'webpredict/index.html'
    model = Vacancy
    success_url = reverse_lazy('load')
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        create_base_model()
        vacancies = Vacancy.objects.all()
        if not vacancies.exists():
            list_vacancies = get_vacancies(True)
            add_new_vacancy(list_vacancies)
        else:
            list_vacancies = get_vacancies(False)
            add_new_vacancy(list_vacancies)

        context["vacancies"] = Vacancy.objects.order_by('id')
        return context


class VacancyPredictRidge(ListView):
    template_name = "webpredict/index.html"
    model = Vacancy
    success_url = reverse_lazy('predict_lr')
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vacancies = Vacancy.objects.order_by('id')
        predict_salary = get_predict_lr(vacancies)
        add_predict_salary(predict_salary)
        vacancies = Vacancy.objects.order_by('id')
        context["vacancies"] = vacancies
        return context


class VacancyPredictRF(ListView):
    template_name = "webpredict/index.html"
    model = Vacancy
    success_url = reverse_lazy('predict_rf')
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vacancies = Vacancy.objects.order_by('id')
        predict_salary = get_predict_rf(vacancies)
        add_predict_salary(predict_salary)
        vacancies = Vacancy.objects.order_by('id')
        context["vacancies"] = vacancies
        return context


class VacancyPredictKNN(ListView):
    template_name = "webpredict/index.html"
    model = Vacancy
    success_url = reverse_lazy('predict_knn')
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vacancies = Vacancy.objects.order_by('id')
        predict_salary = get_predict_knn(vacancies)
        add_predict_salary(predict_salary)
        vacancies = Vacancy.objects.order_by('id')
        context["vacancies"] = vacancies
        return context


class VacancyPredictXG(ListView):
    template_name = "webpredict/index.html"
    model = Vacancy
    success_url = reverse_lazy('predict_xg')
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vacancies = Vacancy.objects.order_by('id')
        predict_salary = get_predict_xg(vacancies)
        add_predict_salary(predict_salary)
        vacancies = Vacancy.objects.order_by('id')
        context["vacancies"] = vacancies
        return context


class VacancySortId(ListView):
    template_name = "webpredict/index.html"
    model = Vacancy
    success_url = reverse_lazy('sort_id')
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["vacancies"] = Vacancy.objects.order_by('id')
        return context


class VacancySortDate(ListView):
    template_name = "webpredict/index.html"
    model = Vacancy
    success_url = reverse_lazy('sort_date')
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["vacancies"] = Vacancy.objects.order_by('-date')
        return context


class VacancySortName(ListView):
    template_name = "webpredict/index.html"
    model = Vacancy
    success_url = reverse_lazy('sort_name')
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["vacancies"] = Vacancy.objects.order_by('name')
        return context


class VacancySortSkills(ListView):
    template_name = "webpredict/index.html"
    model = Vacancy
    success_url = reverse_lazy('sort_skills')
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["vacancies"] = Vacancy.objects.order_by('skills')
        return context


class VacancySortSalary(ListView):
    template_name = "webpredict/index.html"
    model = Vacancy
    success_url = reverse_lazy('sort_salary')
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["vacancies"] = Vacancy.objects.order_by('salary')
        return context


class VacancyDescription(UpdateView):
    template_name = "webpredict/description.html"
    model = Vacancy
    form_class = VacancyForm
    success_url = reverse_lazy('index')

    def get_queryset(self, **kwargs):
        return Vacancy.objects.filter(id=self.kwargs['pk'])


class RidgeSet(ListView):
    template_name = "webpredict/ridge.html"
    model = RidgeModel
    success_url = reverse_lazy('set_lr')
    fields = "__all__"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ridge_models = RidgeModel.objects.all()
        context["lrs"] = ridge_models
        return context


class KnnSet(ListView):
    template_name = "webpredict/knn.html"
    model = KnnModel
    success_url = reverse_lazy('set_knn')
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        knn_models = KnnModel.objects.all()
        context["knns"] = knn_models
        return context


class RandomForestSet(ListView):
    template_name = "webpredict/randomforest.html"
    model = KnnModel
    success_url = reverse_lazy('set_rf')
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        rf_models = RandomForestModel.objects.all()
        context["rfs"] = rf_models
        return context


class XGBoostSet(ListView):
    template_name = "webpredict/xgboost.html"
    model = KnnModel
    success_url = reverse_lazy('set_xgb')
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        xg_models = XGBoostModel.objects.all()
        context["xgbs"] = xg_models
        return context


class KnnAdd(CreateView):
    template_name = "webpredict/new_knn.html"
    model = KnnModel
    success_url = reverse_lazy('set_knn')
    form_class = KnnModelForm


class RandomForestAdd(CreateView):
    template_name = "webpredict/new_randomforest.html"
    model = RandomForestModel
    success_url = reverse_lazy('set_rf')
    form_class = RandomForestModelForm


class XGBoostAdd(CreateView):
    template_name = "webpredict/new_xgboost.html"
    model = XGBoostModel
    success_url = reverse_lazy('set_xgb')
    form_class = XGBoostModelForm


class KnnDescription(UpdateView):
    template_name = "webpredict/description_knn.html"
    model = KnnModel
    success_url = reverse_lazy('description_knn')
    form_class = KnnModelForm

    # def get_context_data(self, **kwargs):

    def get_queryset(self, **kwargs):
        return KnnModel.objects.filter(id=self.kwargs['pk'])

    def post(self, request, *args, **kwargs):
        id_model = self.kwargs['pk']
        name = request.POST['name']
        neighbors = int(request.POST['neighbors'])
        weights = request.POST['weights']
        p = int(request.POST['p'])
        method = request.POST['radiomethod']
        knn_model = Knn(neighbors, weights, p, id_model, name)
        vacancy = Vacancy.objects.exclude(salary=0)
        file_path = ""
        if method == "cross":
            knn_model.set_traindata(vacancy)
            knn_model.get_cross()
            knn_model.train()
        elif method == "split":
            knn_model.set_traindata(vacancy)
            knn_model.get_split()
            knn_model.train()
            knn_model.save_to_file()
            file_path = knn_model.filepath
        elif method == "all":
            knn_model.set_traindata(vacancy)
            knn_model.set_all()
            knn_model.train()
            knn_model.save_to_file()
            file_path = knn_model.filepath
        knn = KnnModel.objects.get(id=id_model)
        knn.mae = knn_model.mae
        knn.mse = knn_model.mse
        if file_path:
            with open(knn_model.filepath, "rb") as file:
                knn.file_model = File(file)
                knn.save()

        else:
            knn.save()
        knns = KnnModel.objects.all()
        return render(request, 'webpredict/knn.html', {"knns": knns})


class RidgeDescription(UpdateView):
    template_name = "webpredict/description_lr.html"
    model = RidgeModel
    success_url = reverse_lazy('description_lr')
    form_class = RidgeModelForm

    def get_queryset(self, **kwargs):
        return RidgeModel.objects.filter(id=self.kwargs['pk'])

    def post(self, request, *args, **kwargs):
        id_model = self.kwargs['pk']
        name = request.POST['name']
        method = request.POST['radiomethod']
        lr_model = Ridge_reg(name=name, id_model=id_model)
        vacancy = Vacancy.objects.exclude(salary=0)
        file_path = ""
        if method == "cross":
            lr_model.set_traindata(vacancy)
            lr_model.get_cross()
            lr_model.train()
        elif method == "split":
            lr_model.set_traindata(vacancy)
            lr_model.get_split()
            lr_model.train()
            lr_model.save_to_file()
            file_path = lr_model.filepath
        elif method == "all":
            lr_model.set_traindata(vacancy)
            lr_model.set_all()
            lr_model.train()
            lr_model.save_to_file()
            file_path = lr_model.filepath
        ridge = RidgeModel.objects.get(id=id_model)
        ridge.mae = lr_model.mae
        ridge.mse = lr_model.mse
        if file_path:
            with open(lr_model.filepath, "rb") as file:
                ridge.file_model = File(file)
                ridge.save()

        else:
            ridge.save()
        ridges = RidgeModel.objects.all()
        return render(request, 'webpredict/ridge.html', {"lrs": ridges})


class RFDescription(UpdateView):
    template_name = "webpredict/description_rf.html"
    model = RandomForestModel
    success_url = reverse_lazy('description_rf')
    form_class = RandomForestModelForm

    # def get_context_data(self, **kwargs):

    def get_queryset(self, **kwargs):
        return RandomForestModel.objects.filter(id=self.kwargs['pk'])

    def post(self, request, *args, **kwargs):
        id_model = self.kwargs['pk']
        name = request.POST['name']
        estimators = int(request.POST['estimators'])
        max_features = request.POST['max_features']
        min_samples_split = int(request.POST['min_samples_split'])
        min_samples_leaf = int(request.POST['min_samples_leaf'])
        method = request.POST['radiomethod']
        rf_model = RandomForest(estimators=estimators, max_features=max_features, min_samples_split=min_samples_split,
                                min_samples_leaf=min_samples_leaf, id_model=id_model, name=name)
        vacancy = Vacancy.objects.exclude(salary=0)
        file_path = ""
        if method == "cross":
            rf_model.set_traindata(vacancy)
            rf_model.get_cross()
            rf_model.train()
        elif method == "split":
            rf_model.set_traindata(vacancy)
            rf_model.get_split()
            rf_model.train()
            rf_model.save_to_file()
            file_path = rf_model.filepath
        elif method == "all":
            rf_model.set_traindata(vacancy)
            rf_model.set_all()
            rf_model.train()
            rf_model.save_to_file()
            file_path = rf_model.filepath
        rf = RandomForestModel.objects.get(id=id_model)
        rf.mae = rf_model.mae
        rf.mse = rf_model.mse
        if file_path:
            with open(rf_model.filepath, "rb") as file:
                rf.file_model = File(file)
                rf.save()

        else:
            rf.save()
        rfs = RandomForestModel.objects.all()
        return render(request, 'webpredict/randomforest.html', {"rfs": rfs})


class XGBDescription(UpdateView):
    template_name = "webpredict/description_xgb.html"
    model = XGBoostModel
    success_url = reverse_lazy('description_xgb')
    form_class = XGBoostModelForm

    # def get_context_data(self, **kwargs):

    def get_queryset(self, **kwargs):
        return XGBoostModel.objects.filter(id=self.kwargs['pk'])

    def post(self, request, *args, **kwargs):
        id_model = self.kwargs['pk']
        name = request.POST['name']
        estimators = int(request.POST['estimators'])
        max_depth = int(request.POST['max_depth'])
        colsample_bytree = float(request.POST['colsample_bytree'])
        alpha = float(request.POST['alpha'])
        method = request.POST['radiomethod']
        xgb_model = XGBoostReg(estimators=estimators, max_depth=max_depth, colsample_bytree=colsample_bytree,
                               alpha=alpha, id_model=id_model, name=name)
        vacancy = Vacancy.objects.exclude(salary=0)
        file_path = ""
        if method == "cross":
            xgb_model.set_traindata(vacancy)
            xgb_model.get_cross()
            xgb_model.train()
        elif method == "split":
            xgb_model.set_traindata(vacancy)
            xgb_model.get_split()
            xgb_model.train()
            xgb_model.save_to_file()
            file_path = xgb_model.filepath
        elif method == "all":
            xgb_model.set_traindata(vacancy)
            xgb_model.set_all()
            xgb_model.train()
            xgb_model.save_to_file()
            file_path = xgb_model.filepath

        xgb = XGBoostModel.objects.get(id=id_model)
        xgb.mae = xgb_model.mae
        xgb.mse = xgb_model.mse
        if file_path:
            with open(xgb_model.filepath, "rb") as file:
                xgb.file_model = File(file)
                xgb.save()

        else:
            xgb.save()
        xgbs = XGBoostModel.objects.all()
        return render(request, 'webpredict/xgboost.html', {"xgbs": xgbs})


class KnnSelect(ListView):
    template_name = "webpredict/index.html"
    model = Vacancy
    fields = '__all__'
    success_url = reverse_lazy('select_knn')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        knn = KnnModel.objects.get(id=self.kwargs["pk"])
        vacancies = Vacancy.objects.order_by('id')
        predict_salary = get_predict_knn(vacancies, knn.file_model.path)
        add_predict_salary(predict_salary)
        context["vacancies"] = Vacancy.objects.order_by('id')
        return context


class RFSelect(ListView):
    template_name = "webpredict/index.html"
    model = Vacancy
    fields = '__all__'
    success_url = reverse_lazy('select_rf')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        rf = RandomForestModel.objects.get(id=self.kwargs["pk"])

        vacancies = Vacancy.objects.order_by('id')
        predict_salary = get_predict_rf(vacancies, rf.file_model.path)
        add_predict_salary(predict_salary)
        context["vacancies"] = Vacancy.objects.order_by('id')
        return context


class XGBSelect(ListView):
    template_name = "webpredict/index.html"
    model = Vacancy
    fields = '__all__'
    success_url = reverse_lazy('select_rf')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        xgb = XGBoostModel.objects.get(id=self.kwargs["pk"])

        vacancies = Vacancy.objects.order_by('id')
        predict_salary = get_predict_xg(vacancies, xgb.file_model.path)
        add_predict_salary(predict_salary)
        context["vacancies"] = Vacancy.objects.order_by('id')
        return context


class RidgeSelect(ListView):
    template_name = "webpredict/index.html"
    model = Vacancy
    fields = '__all__'
    success_url = reverse_lazy('select_lr')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ridge = RidgeModel.objects.get(id=self.kwargs["pk"])

        vacancies = Vacancy.objects.order_by('id')
        predict_salary = get_predict_lr(vacancies, ridge.file_model.path)
        add_predict_salary(predict_salary)
        context["vacancies"] = Vacancy.objects.order_by('id')
        return context
