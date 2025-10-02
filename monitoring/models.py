from django.db import models

class SensorData(models.Model):
    waktu = models.DateTimeField(auto_now_add=True)
    suhu = models.FloatField()
    kelembapan = models.FloatField()
    prediksi = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.waktu} - Suhu: {self.suhu}°C"
