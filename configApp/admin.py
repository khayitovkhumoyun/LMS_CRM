from django.contrib import admin

from .models import *


class UserAdmin(admin.ModelAdmin):
    ordering = ['id']
    list_display = (
        ['id', 'phone', 'full_name']
    )


admin.site.register(User, UserAdmin)
admin.site.register(Course)
admin.site.register(Worker)
admin.site.register(Departments)
admin.site.register(Day)
admin.site.register(Rooms)
admin.site.register(Group)
admin.site.register(Student)

