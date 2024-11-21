from django.db.models import Max
from django.shortcuts import render

from core.models import Line

# from .models import CalculationProtocol


def calculation(request):
    return render(request, "calculation/calculation.html")


# line_name = "ВЛ 500 кВ Ново-Анжерская - Томская"
# line = Line.objects.get(dispatch_name=line_name)
# protocols = CalculationProtocol.objects.filter(line=line, component="Тест")
#
# max_result = protocols.aggregate(max_value=Max("result_value"))["max_value"]
# print(max_result)
