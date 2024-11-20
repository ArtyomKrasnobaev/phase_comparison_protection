from django.shortcuts import render

from core.models import Line
from .models import CalculationProtocol


def calculation(request):
    return render(request, "calculation/calculation.html")

# prot = CalculationProtocol.objects.first()
# print(prot)