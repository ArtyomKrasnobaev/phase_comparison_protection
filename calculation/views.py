from django.shortcuts import render


def calculation(request):
    return render(request, "calculation/calculation.html")
