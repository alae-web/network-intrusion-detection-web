from django.urls import path
from . import views
from .views import predict_attack

urlpatterns = [
    path('', views.home, name='home'),
    path("predict/", predict_attack, name="predict")

]
