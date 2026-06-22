from django.contrib import admin

from cash_flow.models import Status, Type, Category, SubCategory


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = "status",


@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = "type",


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = "category",


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = "sub_category",
