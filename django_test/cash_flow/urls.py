from django.urls import path, include


app_name = "cash_flow"

urlpatterns = [
    path("general/", include("cash_flow.urls"), name="general"),
]
