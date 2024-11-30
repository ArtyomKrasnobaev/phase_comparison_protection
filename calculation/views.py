from django.shortcuts import render

from calculation.models import CalculationMeta
from calculation.services.sensitivity_analysis_service import \
    SensitivityAnalysisService


def calculation(request):
    return render(request, "calculation/calculation.html")


# meta = CalculationMeta.objects.get(id=5)
# print(meta)
# service = SensitivityAnalysisService(meta)
# service.run()