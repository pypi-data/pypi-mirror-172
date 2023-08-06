from django.contrib import admin
from django_telemetry.models import WebQuery

from django_telemetry.models import WebTelemetry

class MultiDBModelAdmin(admin.ModelAdmin):

    using = 'django_telemetry'

    def get_queryset(self, request):
        # Tell Django to look for inline objects on the 'other' database.
        return super().get_queryset(request).using(self.using)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Tell Django to populate ForeignKey widgets using a query
        # on the 'other' database.
        return super().formfield_for_foreignkey(db_field, request, using=self.using, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
  
        return super().formfield_for_manytomany(db_field, request, using=self.using, **kwargs)


# Register your models here.
admin.site.register(WebTelemetry,MultiDBModelAdmin)
admin.site.register(WebQuery,MultiDBModelAdmin)