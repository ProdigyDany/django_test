from django.urls import path

from .views import (
    CashFlowAPIView,
    CashFlowCreateView,
    CashFlowDetailAPIView,
    load_categories,
    load_sub_categories,
)

app_name = "cash_flow"

urlpatterns = [
    path("general/", CashFlowAPIView.as_view(), name="general"),
    path("create_flow/", CashFlowCreateView.as_view(), name="create_flow"),
    path("detail_flow/<int:pk>/", CashFlowDetailAPIView.as_view(), name="detail_flow"),
    path("load-categories/", load_categories, name="load_categories"),
    path("load-subcategories/", load_sub_categories, name="load_subcategories"),
]
