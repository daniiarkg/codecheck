from django.contrib import admin
from .models import *
from django.utils.html import format_html
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
# Register your models here.

class TaskCompleteInline(admin.StackedInline):
    model = TaskComplete
    extra = 0
    verbose_name = 'Решенное задание'
    verbose_name_plural = 'Решенные задания'

class CoderInline(admin.StackedInline):
    model = Coder
    can_delete = False
    verbose_name = 'Основные данные'
    verbose_name_plural = "Основные данные"

class TaskInline(admin.StackedInline):
    model = Task
    extra = 0
    verbose_name = 'Опубликованное задание'
    verbose_name_plural = 'Опубликованные задания'

    exclude = ['date',]
    readonly_fields = ['date_out',]

    @admin.display(description='Опубликовано')
    def date_out(self,obj):
        return format_html(f'{obj.date.strftime("%c")}')

class UserAdmin(BaseUserAdmin):
    inlines = [CoderInline]

class CoderAdmin(admin.ModelAdmin):
    list_display = ['fio','id']
    inlines = [TaskInline, TaskCompleteInline]


class TaskAdmin(admin.ModelAdmin):
    list_display = ['name','date','published_by']
    exclude = ['date','published_by']
    readonly_fields = ['date_out','pub_out']
    inlines = [TaskCompleteInline,]

    def save_model(self, request, obj, form, change):
        try:    
            obj.published_by = request.user.coder
        except:
            pass
        super().save_model(request, obj, form, change) 

    @admin.display(description='Автор')
    def pub_out(self,obj):
        return format_html(f'<a href=/admin/main/coder/{obj.published_by.id}>{obj.published_by.fio}</a>')

    @admin.display(description='Опубликовано')
    def date_out(self,obj):
        return format_html(f'{obj.date.strftime("%c")}')

admin.site.register(Task, TaskAdmin)
admin.site.register(Coder, CoderAdmin)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)