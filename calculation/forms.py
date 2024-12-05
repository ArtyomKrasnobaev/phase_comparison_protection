from django import forms

from core.models import Line


class LineSelectionForm(forms.Form):
    """Форма выбора ЛЭП из выпадающего списка."""

    line = forms.ModelChoiceField(
        queryset=Line.objects.all(),
        label="Защищаемая ЛЭП",
        empty_label="ЛЭП не выбрана",
    )
