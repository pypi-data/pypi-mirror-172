"""DMARC urls."""

from django.urls import path

from . import views

app_name = "kalabash_dmarc"

urlpatterns = [
    path("domains/<int:pk>/", views.DomainReportView.as_view(),
         name="domain_report"),
]
