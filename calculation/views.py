from django.shortcuts import render


def calculation(request):
    return render(request, "calculation/calculation.html")


fault_currents = {"I1": 1500, "I2": 300, "3I0": None}
