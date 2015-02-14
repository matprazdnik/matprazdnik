from flying_rows.models import Transaction
import main_app.models as models

from django.contrib import admin


class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('participant_code', 'test_number', 'surname', 'name', 'gender', 'grade', 'school')


class SchoolAdmin(admin.ModelAdmin):
    list_display = ('nominative',)


# TODO: move somewhere
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('author', 'timestamp', 'type', 'module', 'model', 'rowId', 'column', 'value')


admin.site.register(models.Participant, ParticipantAdmin)
admin.site.register(models.School, SchoolAdmin)
admin.site.register(Transaction, TransactionAdmin)
