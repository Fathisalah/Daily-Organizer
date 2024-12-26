from django.contrib import admin
from .models import Task, Category, Reminder

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'created_at')
    list_filter = ('user',)
    search_fields = ('name', 'user__username')
    ordering = ('name',)

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'due_date', 'priority', 'status', 'category')
    list_filter = ('status', 'priority', 'category', 'user')
    search_fields = ('title', 'description', 'user__username')
    ordering = ('-due_date',)
    date_hierarchy = 'due_date'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'title', 'description')
        }),
        ('Task Details', {
            'fields': ('category', 'priority', 'status')
        }),
        ('Dates', {
            'fields': ('due_date', 'completed_at')
        }),
    )

@admin.register(Reminder)
class ReminderAdmin(admin.ModelAdmin):
    list_display = ('task', 'reminder_time', 'is_sent')
    list_filter = ('is_sent', 'reminder_time')
    search_fields = ('task__title',)
    ordering = ('-reminder_time',)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('task')