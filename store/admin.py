from django.contrib import admin

from .models import Category, Product

# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'manufacturer', 'slug', 'price',
                    'count', 'created', 'updated', 'is_active', ]
    list_filter = ['is_active']
    list_editable = ['price', 'count', 'is_active', ]
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
