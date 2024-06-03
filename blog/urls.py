from django.urls import path
from .views import *

urlpatterns = [
    path('post/<int:pk>/', BlogDetailView.as_view(), name='post_detail'),
    path('about/', AboutPageView.as_view(), name='about'),
    path('', BlogList.as_view(), name='home'),
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('page/', PageView.as_view(), name='page'),
    path('testing/', TestingView.as_view(), name='testing'),
    path('training/', TrainingView.as_view(), name='training'),
    path('result/', ResultView.as_view(), name='result')
]
#, name='register'