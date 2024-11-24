from django.shortcuts import render

# from core.models import Line

# from .services import CalculationService


def calculation(request):
    return render(request, "calculation/calculation.html")


# line_name = "ВЛ 500 кВ Ново-Анжерская - Томская"
# line = Line.objects.get(dispatch_name=line_name)
# service = CalculationService(line)
# service.run()
