from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=450) #Заголовок поста
    author = models.CharField(max_length=32)
    body = models.TextField() #Поле поста

    def __str__(self): #Метод
        return self.title


class Result(models.Model):
    Real_result = models.FloatField
    PL_regression = models.FloatField
    Gradient_boosting = models.FloatField
    RNN = models.FloatField


class Datatesting(models.Model):
    X1 = models.FloatField
    X2 = models.FloatField
    X3 = models.FloatField
    X4 = models.FloatField
    X5 = models.FloatField
    X6 = models.FloatField
    Y = models.FloatField


class Datatraining(models.Model):
    X1 = models.FloatField
    X2 = models.FloatField
    X3 = models.FloatField
    X4 = models.FloatField
    X5 = models.FloatField
    X6 = models.FloatField
    Y = models.FloatField