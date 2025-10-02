from django.shortcuts import render
from .models import SensorData

def dashboard_view(request):
    data = SensorData.objects.all().order_by('-waktu')[:10]  # ambil 10 data terbaru
    return render(request, 'monitoring/dashboard.html', {'data': data})
