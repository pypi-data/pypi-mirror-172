from django.urls import path
from . import views

urlpatterns = [
    # A sample calendar with sample data
    path("sample", views.sample_calendar, name="sample_calendar"),
]
