from django.urls import path
from . import views

urlpatterns = [
    path('', views.compass_page, name='compass'),
    path('instructions/<int:instruction_id>/', views.instruction_detail, name='instruction_detail'),
]
