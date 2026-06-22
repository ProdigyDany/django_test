from rest_framework import serializers
from .models import CashFlow


class CashFlowSerializer(serializers.ModelSerializer):
    status_name = serializers.CharField(source="status.status", read_only=True)
    sub_category_name = serializers.CharField(
        source="sub_category.sub_category", read_only=True
    )
    category_name = serializers.CharField(
        source="sub_category.category.category", read_only=True
    )
    type_name = serializers.CharField(
        source="sub_category.category.type.type", read_only=True
    )
    created_at = serializers.DateField(format="%d.%m.%Y")
    comments = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    class Meta:
        model = CashFlow
        fields = [
            "id",
            "created_at",
            "status",
            "sub_category",
            "status_name",
            "type_name",
            "category_name",
            "sub_category_name",
            "cash",
            "comments",
        ]

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if instance.sub_category:
            ret["category"] = instance.sub_category.category_id
            if instance.sub_category.category:
                ret["type"] = instance.sub_category.category.type_id
        return ret
