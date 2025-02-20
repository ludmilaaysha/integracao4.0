from django.shortcuts import render

def charts(request):
    return render(request, 'charts.html')
