from django.shortcuts import redirect, render

from core.models import ProtectionHalfSet

from .forms import LineSelectionForm
from .models import CalculationMeta, SettingsCalculation
from .services import SettingsCalculationService


def calculation(request):
    if request.method == 'POST':
        form = LineSelectionForm(request.POST)
        if form.is_valid():
            # Получаем выбранную ЛЭП
            selected_line = form.cleaned_data['line']

            # Получаем параметры выбранной ЛЭП
            selected_line_data = {
                'dispatch_name': selected_line.dispatch_name,
                'pf_name': selected_line.pf_name,
                'current_capacity': selected_line.current_capacity,
                'length': selected_line.length,
            }

            # Получаем полукомплекты, связанные с выбранной ЛЭП
            protection_half_sets = ProtectionHalfSet.objects.filter(
                line=selected_line,
            )

            if 'run_calculation' in request.POST:
                calculation_meta = CalculationMeta.objects.create(
                    line=selected_line,
                )
                service = SettingsCalculationService(
                    calculation_meta=calculation_meta
                )
                service.run()

                return redirect('results', calculation_meta_id=calculation_meta.id)

            return render(
                request,
                'calculation/calculation.html',
                {
                    'form': form,
                    'selected_line': selected_line,
                    'selected_line_data': selected_line_data,
                    'protection_half_sets': protection_half_sets,
                }
            )
    else:
        form = LineSelectionForm()

    return render(
        request,
        'calculation/calculation.html',
        {'form': form}
    )

def calculation_results(request, calculation_meta_id):
    calculation_meta = CalculationMeta.objects.get(id=calculation_meta_id)
    results = SettingsCalculation.objects.filter(
        calculation_meta=calculation_meta
    )
    return render(
        request,
        'calculation/results.html',
        {'results': results, 'calculation_meta': calculation_meta}
    )

def calculation_list(request):
    calculations = CalculationMeta.objects.all().order_by('-calculation_date')
    return render(
        request,
        'calculation/calculation_list.html',
        {'calculations': calculations}
    )