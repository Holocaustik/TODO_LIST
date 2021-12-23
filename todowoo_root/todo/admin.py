from django.contrib import admin

from .models import Todo


class TodoAdm(admin.ModelAdmin):
    list_display = ('status', 'user', 'start_date', 'end_date')
    search_fields = ('user', 'status')
    list_filter = ('user', 'status')


admin.site.register(Todo, TodoAdm)
