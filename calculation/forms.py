from django import forms

from core.models import Line


class LineChoiceForm(forms.Form):
    """Форма выбора ЛЭП из выпадающего списка."""

    line = forms.ModelChoiceField(
        queryset=Line.objects.all(),
        widget=forms.Select(attrs={"class": "form-select"}),
        label="Защищаемая ЛЭП",
        empty_label="ЛЭП не выбрана",
    )
