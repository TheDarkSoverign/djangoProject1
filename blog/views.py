import pymongo
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import ListView, DetailView, TemplateView, FormView
import pickle
from tensorflow import keras
import pandas as pd

from .models import Post, Result
from .forms import RegisterUserForm, LoginUserForm
from blog.static.Build_Model_Regression import training_rgr, read_data, preprocessing
from blog.static.db_process import db_process


class BlogList(ListView):
    paginate_by = 3
    model = Post
    template_name = 'home.html'
    ordering = ['-id']

    def get_queryset(self):
        return Post.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reg_form'] = RegisterUserForm()
        context['login_form'] = LoginUserForm()
        return context

class BlogDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'


class AboutPageView(TemplateView):
    template_name = 'about.html'


class RegisterUserView(FormView):
    def get(self, request):
        form = RegisterUserForm()
        return render(request, 'register.html', {'form': form})
    def post(self, request):
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            email = form.cleaned_data['email']

            # Создаем пользователя
            user = User.objects.create_user(username=username, email=email, password=password)

            # Авторизуем пользователя
            user = authenticate(username=username, password=password)
            login(request, user)

            # Перенаправляем пользователя на нужную страницу
            return redirect('home')
        return render(request, 'register.html', {'form': form})


class LoginUser(View):
    def get(self, request):
        form1 = LoginUserForm()
        return render(request, 'login.html', {'form': form1})

    def post(self, request):
        form1 = LoginUserForm(data=request.POST)
        if form1.is_valid():
            user = form1.get_user()
            login(request, user)
            return redirect('home')
        return render(request, 'login.html', {'form': form1})

def logout_user(request):
    logout(request)
    return redirect('home')


class PageView(TemplateView):
    template_name = 'page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class TrainingView(View):
    def get(self, request):
        return render(request, 'page.html')

    def post(self, request):
        metrics = training_rgr()
        text_out = [
            "Training model regression complete!!!",
            "Training model gradient regression complete!!!",
            "Training model recurrent neural network complete!!!"
        ]
        return render(request, 'page.html', {'text_out': text_out, 'metrics': metrics})


class TestingView(View):
    def get(self, request):
        return render(request, 'page.html')

    def post(self, request):
        table_name = 'blog_datatesting'
        x_test, y_test = read_data(table_name)
        poly_features = preprocessing(x_test)

        model_rgr = pickle.load(open("blog/static/polymodel.pkl", "rb"))
        y_pred_rgr = model_rgr.predict(poly_features)

        model_bst = pickle.load(open("blog/static/gb_model.pkl", "rb"))
        y_pred_bst = model_bst.predict(poly_features)

        model_rnn = keras.models.load_model("blog/static/rnn_model.h5")
        y_pred_rnn = model_rnn.predict(x_test).flatten()

        db_process(y_test, y_pred_rgr, y_pred_bst, y_pred_rnn)
        return render(request, 'page.html', {'mss': "# Save data successfully"})

class ResultView(View):
    def get(self, request):
        return render(request, 'page.html')

    def post(self, request):
        client = pymongo.MongoClient('mongodb://mongo1:27017')
        db = client["django"]
        collection = db['blog_result']
        results = collection.find()
        return render(request, 'page.html', {'results': results})



