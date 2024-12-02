from django.urls import path

from . import views

urlpatterns = [
    path("", views.calculation, name="calculation"),
    path('calculation_list/', views.calculation_list, name="calculation_list"),
]
