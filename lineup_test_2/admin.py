from django.contrib import admin
from .models import User, EyewitnessStimuli, Response


class ResponseAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'question_category', 'question_lineup_number', 'statement_type',
                    'statement', 'answer')
    actions = ['download_csv']
    # actions = ['download_csv']
    #
    # def download_csv(self, request, queryset):
    #     import csv

    @staticmethod
    def download_csv(self, request, queryset):
        import csv
        from django.http import HttpResponse
        from io import StringIO

        f = StringIO()
        writer = csv.writer(f)
        writer.writerow(["userid", "category", "lineup_number", "statement_type", "statement", "answer"])
        for s in queryset:
            writer.writerow([s.user.userId, s.question.category, s.question.lineup_number, s.user.StatementType,
                            s.question.statement if s.user.StatementType else s.question.statementOnly, s.answer])
        f.seek(0)
        response = HttpResponse(f, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=response.csv'
        return response

# Register your models here.
admin.site.register(EyewitnessStimuli)
admin.site.register(User)
admin.site.register(Response, ResponseAdmin)
