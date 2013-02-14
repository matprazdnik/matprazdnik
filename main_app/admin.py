import main_app.models as models

from django.contrib import admin


class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('number', 'surname', 'name', 'gender', 'grade', 'school')


class SchoolAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'nominative')


admin.site.register(models.Participant, ParticipantAdmin)
admin.site.register(models.School, SchoolAdmin)