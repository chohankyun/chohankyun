from django.contrib import admin
from index.models import Header, Footer


@admin.register(Header)
class HeaderAdmin(admin.ModelAdmin):
    readonly_fields = ['created_datetime', 'updated_datetime']
    list_display = [field.name for field in Header._meta.fields]


@admin.register(Footer)
class FooterAdmin(admin.ModelAdmin):
    readonly_fields = ['created_datetime', 'updated_datetime']
    list_display = [field.name for field in Footer._meta.fields]


