from django.contrib import admin
from .models import *
from django.utils.html import format_html
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib import messages

# Register your models here.

def check_code(ecode,scode):
    codebase_upper = '''
vars = [1,2,3]
'''

    codebase_lower = '''
for i in vars:
    if etalon(i)!=solution(i):
        raise Exception('Uncorrect!')
'''
    try:
        exec(codebase_upper + '\n' + ecode + '\n' + scode + '\n' + codebase_lower, {}, {})
    except:
        return False
    return True
    

class TaskCompleteInline(admin.StackedInline):
    model = TaskComplete
    extra = 0
    verbose_name = 'Решенное задание'
    verbose_name_plural = 'Решенные задания'
    

    fields = ['code','task','solve_out','date_out']
    readonly_fields = ['lnk_out','solve_out','date_out']
        
    @admin.display(description='Дата решения')
    def date_out(self,obj):
        return format_html(f'{obj.date.strftime("%c")}')
    
    @admin.display(description='Решено')
    def solve_out(self,obj):
        return format_html(f'<a href="/admin/main/coder/{obj.solved_by.id}">{obj.solved_by.fio}</a>')
    
    @admin.display(description='Ссылка на задание')
    def lnk_out(self,obj):
        return format_html(f'<a href="/admin/main/task/{obj.task.id}">Нажмите здесь</a>')


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
    readonly_fields = ['date_out','link_out']

    @admin.display(description='Ссылка для просмотра')
    def link_out(self,obj):
        return format_html(f'<a href="/admin/main/task/{obj.id}">Нажмите здесь</a>')

    @admin.display(description='Опубликовано')
    def date_out(self,obj):
        return format_html(f'{obj.date.strftime("%c")}')

class UserAdmin(BaseUserAdmin):
    inlines = [CoderInline]

class CoderAdmin(admin.ModelAdmin):
    list_display = ['fio','id']
    exclude = ['user',]
    inlines = [TaskInline, TaskCompleteInline]
    readonly_fields = ['user_out',]

    def save_formset(self, request, obj, formset, change):
        instances = formset.save(commit=False)

        if formset.model==TaskComplete:
            
            for instance in instances:
                print(instance.code)
                print(request.user.username)
                if not instance.task:
                    raise ValidationError('No task given!')
                instance.save()
                formset.save_m2m()

        formset.save()

    @admin.display(description='Юзернейм')
    def user_out(self,obj):
        return format_html(obj.user.username)


class TaskAdmin(admin.ModelAdmin):
    list_display = ['name','date','published_by']
    exclude = ['date','published_by']
    readonly_fields = ['date_out','pub_out']
    inlines = [TaskCompleteInline,]


    def save_formset(self, request, obj, formset, change):
        instances = formset.save(commit=False)

        if formset.model==TaskComplete:
            
            for instance in instances:
                if not check_code(instance.code, instance.task.source_code):
                    messages.error(request,'TASK COMPLETE INCORRECT!')
                    return
                instance.solved_by = request.user.coder
                instance.save()
                formset.save_m2m()

        formset.save()

    def save_model(self, request, obj, form, change):
        try:    
            obj.published_by = request.user.coder
        except:
            pass
        super().save_model(request, obj, form, change) 

    @admin.display(description='Автор')
    def pub_out(self,obj):
        return format_html(f'<a href="/admin/main/coder/{obj.published_by.id}">{obj.published_by.fio}</a>')

    @admin.display(description='Опубликовано')
    def date_out(self,obj):
        return format_html(f'{obj.date.strftime("%c")}')

admin.site.register(Task, TaskAdmin)
admin.site.register(Coder, CoderAdmin)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)