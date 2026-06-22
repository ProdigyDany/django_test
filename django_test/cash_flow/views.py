from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView

from cash_flow.forms import CashFlowForm
from cash_flow.models import CashFlow, Category, SubCategory


class CashFlowListView(ListView):
    template_name = "cash_flow/cash-flow-list.html"
    model = CashFlow
    context_object_name = "objects"
    queryset = CashFlow.objects.all()


class CashFlowCreateView(CreateView):
    template_name = "cash_flow/cash-flow-form.html"
    model = CashFlow
    form_class = CashFlowForm
    success_url = reverse_lazy("cash_flow:general")


def load_categories(request):
    type_id = request.GET.get('type_id')
    categories = Category.objects.filter(type_id=type_id).values('id', 'category')
    return JsonResponse(list(categories), safe=False)

def load_sub_categories(request):
    category_id = request.GET.get('category_id')
    sub_categories = SubCategory.objects.filter(category_id=category_id).values('id', 'sub_category')
    return JsonResponse(list(sub_categories), safe=False)
