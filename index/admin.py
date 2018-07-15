from django.contrib import admin
from index.models import Header, Footer


class HeaderAdmin(admin.ModelAdmin):
    readonly_fields = ['created_datetime', 'changed_datetime']
    list_display = [field.name for field in Header._meta.fields]


admin.site.register(Header, HeaderAdmin)


class FooterAdmin(admin.ModelAdmin):
    readonly_fields = ['created_datetime', 'changed_datetime']
    list_display = [field.name for field in Footer._meta.fields]


admin.site.register(Footer, FooterAdmin)

