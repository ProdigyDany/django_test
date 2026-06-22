from django import forms
from django.utils import timezone

from .models import CashFlow, Type, Category, SubCategory


class CashFlowForm(forms.ModelForm):
    created_at = forms.DateField(
        initial=timezone.now,
        label="Дата создания",
        widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'})
    )

    type = forms.ModelChoiceField(
        queryset=Type.objects.all(),
        label="Тип ДДС",
        required=True,
        widget=forms.Select(attrs={'id': 'id_type'})
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.none(),
        label="Категория ДДС",
        required=True,
        widget=forms.Select(attrs={'id': 'id_category'})
    )

    class Meta:
        model = CashFlow
        fields = ['created_at', 'status', 'type', 'category', 'sub_category', 'cash', 'comments']
        widgets = {
            'sub_category': forms.Select(attrs={'id': 'id_sub_category'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'type' in self.data:
            try:
                type_id = int(self.data.get('type'))
                self.fields['category'].queryset = Category.objects.filter(type_id=type_id)
            except (ValueError, TypeError):
                pass

        if 'category' in self.data:
            try:
                category_id = int(self.data.get('category'))
                self.fields['sub_category'].queryset = SubCategory.objects.filter(category_id=category_id)
            except (ValueError, TypeError):
                pass
        elif self.instance and self.instance.pk and self.instance.sub_category:
            self.fields['category'].queryset = Category.objects.filter(type=self.instance.sub_category.category.type)
            self.fields['category'].initial = self.instance.sub_category.category
            self.fields['type'].initial = self.instance.sub_category.category.type
            self.fields['sub_category'].queryset = SubCategory.objects.filter(
                category=self.instance.sub_category.category)
        else:
            self.fields['sub_category'].queryset = SubCategory.objects.none()
