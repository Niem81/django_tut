from django.contrib import admin

# Register your models here.
from .models import Course, Step

class StepInline(admin.StackedInline):
	model = Step

class CourseAdmin(admin.ModelAdmin):
	inlines = [StepInline,]

admin.site.register(Course, CourseAdmin)
admin.site.register(Step)