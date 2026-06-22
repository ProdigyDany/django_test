from django import forms
from django.utils import timezone

from .models import CashFlow, Type, Category, SubCategory, Status


class CashFlowForm(forms.ModelForm):
    created_at = forms.DateField(
        initial=timezone.now,
        label="Дата создания",
        widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
    )
    status = forms.ModelChoiceField(
        queryset=Status.objects.all(),
        label="Статус",
        required=True,
    )
    type = forms.ModelChoiceField(
        queryset=Type.objects.all(),
        label="Тип ДДС",
        required=True,
        widget=forms.Select(attrs={"id": "id_type"}),
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        label="Категория ДДС",
        required=True,
        widget=forms.Select(attrs={"id": "id_category"}),
    )
    sub_category = forms.ModelChoiceField(
        queryset=SubCategory.objects.all(),
        label="Подкатегория ДДС",
        required=True,
        widget=forms.Select(attrs={"id": "id_sub_category"}),
    )
    cash = forms.DecimalField(
        label="Итоговая сумма",
        required=True,
    )
    comments = forms.CharField(
        widget=forms.Textarea(
            attrs={"rows": 6, "cols": 30, "placeholder": "Ваше сообщение..."}
        ),
        label="Комментарий",
        required=False,
    )

    class Meta:
        model = CashFlow
        fields = [
            "created_at",
            "status",
            "type",
            "category",
            "sub_category",
            "cash",
            "comments",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "comments" in self.fields:
            self.fields["comments"].required = False
        if self.data:
            try:
                type_id = int(self.data.get("type"))
                self.fields["category"].queryset = Category.objects.filter(
                    type_id=type_id
                )
            except (ValueError, TypeError):
                self.fields["category"].queryset = Category.objects.none()
            try:
                category_id = int(self.data.get("category"))
                self.fields["sub_category"].queryset = SubCategory.objects.filter(
                    category_id=category_id
                )
            except (ValueError, TypeError):
                self.fields["sub_category"].queryset = SubCategory.objects.none()
        elif (
            self.instance
            and self.instance.pk
            and getattr(self.instance, "sub_category", None)
        ):
            current_sub = self.instance.sub_category
            current_cat = current_sub.category
            current_type = current_cat.type
            self.fields["category"].queryset = Category.objects.filter(
                type=current_type
            )
            self.fields["sub_category"].queryset = SubCategory.objects.filter(
                category=current_cat
            )
            self.fields["type"].initial = current_type
            self.fields["category"].initial = current_cat
            self.fields["sub_category"].initial = current_sub
        else:
            self.fields["category"].queryset = Category.objects.none()
            self.fields["sub_category"].queryset = SubCategory.objects.none()

    def clean_category(self):
        category_id = self.data.get("category")
        if category_id:
            return Category.objects.filter(id=category_id).first()
        return None

    def clean_sub_category(self):
        sub_category_id = self.data.get("sub_category")
        if sub_category_id:
            return SubCategory.objects.filter(id=sub_category_id).first()
        return None
