from django.urls import path

from . import views

urlpatterns = [
    path("", views.calculation, name="calculation"),
    path('results/<int:calculation_meta_id>', views.calculation_results, name="results"),
    path('calculation_list/', views.calculation_list, name="calculation_list"),
]
