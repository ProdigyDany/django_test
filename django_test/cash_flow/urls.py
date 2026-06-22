from django.urls import path, include

from .views import (
    CashFlowListView,
    CashFlowCreateView,
    load_categories,
    load_sub_categories,
)

app_name = "cash_flow"

urlpatterns = [
    path("general/", CashFlowListView.as_view(), name="general"),
    path("create_flow/", CashFlowCreateView.as_view(), name="create_flow"),
    path('load-categories/', load_categories, name='load_categories'),
    path('load-subcategories/', load_sub_categories, name='load_subcategories'),
]
