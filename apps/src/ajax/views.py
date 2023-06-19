from django.http import JsonResponse
from django.shortcuts import render


def home(request):
    return render(request, "ajax/index.html")


def compute(request):
    a = request.POST.get("a")
    b = request.POST.get("b")

    return JsonResponse({"operation_result": int(a) + int(b)})
