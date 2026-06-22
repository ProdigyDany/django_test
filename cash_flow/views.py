from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django_filters import rest_framework as filters
from rest_framework.generics import (
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
    UpdateAPIView,
)
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer

from cash_flow.forms import CashFlowForm
from cash_flow.models import CashFlow, Category, SubCategory, Status, Type
from cash_flow.serializer import CashFlowSerializer


class CashFlowFilter(filters.FilterSet):
    """
    Класс предназначен для фильтрации данных
    """
    date = filters.DateFromToRangeFilter(
        field_name="created_at", label="Период дат (С / По)"
    )
    status = filters.ModelChoiceFilter(
        field_name="status", queryset=Status.objects.all(), label="Статус"
    )
    type = filters.ModelChoiceFilter(
        field_name="sub_category__category__type",
        queryset=Type.objects.all(),
        label="Тип",
    )
    category = filters.ModelChoiceFilter(
        field_name="sub_category__category",
        queryset=Category.objects.select_related("type"),
        label="Категория",
    )
    sub_category = filters.ModelChoiceFilter(
        field_name="sub_category",
        queryset=SubCategory.objects.select_related("category"),
        label="Подкатегория",
    )


class CashFlowBrowsableAPIRenderer(BrowsableAPIRenderer):
    """
    Класс предназначен для передачи формы на веб страницу
    """
    def get_context(self, data, accepted_media_type, renderer_context):
        context = super().get_context(data, accepted_media_type, renderer_context)
        view = renderer_context["view"]
        if hasattr(view, "filterset_class") and view.filterset_class:
            filterset = view.filterset_class(
                view.request.GET, queryset=view.get_queryset()
            )
            context["custom_filter_form"] = filterset.form
        elif hasattr(view, "get_object"):
            try:
                instance = view.get_object()
                context["django_edit_form"] = CashFlowForm(instance=instance)
            except Exception:
                pass

        return context


class CashFlowDetailAPIView(RetrieveUpdateDestroyAPIView, UpdateAPIView):
    """
    Класс предназначен для вывода детальной информации о записи,
    а также изменении или удалении записи
    """
    queryset = CashFlow.objects.select_related("status", "sub_category__category__type")
    serializer_class = CashFlowSerializer
    renderer_classes = [CashFlowBrowsableAPIRenderer, JSONRenderer]
    http_method_names = ["get", "post", "put", "patch", "delete", "head", "options"]

    def post(self, request, *args, **kwargs):
        """
        Функция предназначена для управления записью (удаление/изменение).
        :param request: Принимаем данные от пользователя.
        :return: Удаляем запись и перенаправляем пользователя либо сохраняем изменения.
        """
        instance = self.get_object()
        if (
            request.data.get("_method") == "DELETE"
            or request.POST.get("_method") == "DELETE"
        ):
            instance.delete()
            return redirect("cash_flow:general")

        if request.accepted_renderer.format == "html":
            sub_category_id = request.data.get("sub_category")
            status_id = request.data.get("status")
            cash_value = request.data.get("cash")
            comments_value = request.data.get("comments")
            created_at_value = request.data.get("created_at")
            if cash_value:
                instance.cash = cash_value
            if status_id:
                instance.status_id = int(status_id)
            if sub_category_id:
                instance.sub_category_id = int(sub_category_id)
            if created_at_value:
                instance.created_at = created_at_value

            instance.comments = comments_value if comments_value else ""
            instance.save()

        return self.update(request, *args, **kwargs)


class CashFlowAPIView(ListAPIView):
    """
    Класс предназначен для вывода списка записей
    """
    queryset = CashFlow.objects.select_related(
        "status", "sub_category__category__type"
    ).order_by("-created_at")
    serializer_class = CashFlowSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = CashFlowFilter
    renderer_classes = [CashFlowBrowsableAPIRenderer, JSONRenderer]


class CashFlowCreateView(CreateView):
    """
    Класс предназначен для создания новой записи
    """
    template_name = "cash_flow/cash-flow-form.html"
    model = CashFlow
    form_class = CashFlowForm
    success_url = reverse_lazy("cash_flow:general")


def load_categories(request):
    """
    Функция предназначена для подгрузки категорий исходя из id типа
    """
    type_id = request.GET.get("type_id")
    categories = Category.objects.filter(type_id=type_id).values("id", "category")
    return JsonResponse(list(categories), safe=False)


def load_sub_categories(request):
    """
    Функция предназначена для подгрузки подкатегорий исходя из id категории
    """
    category_id = request.GET.get("category_id")
    sub_categories = SubCategory.objects.filter(category_id=category_id).values(
        "id", "sub_category"
    )
    return JsonResponse(list(sub_categories), safe=False)
