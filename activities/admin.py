from django.contrib import admin

from activities.models import Activity


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ["title", "start_time", "location"]
    search_fields = ["title","location"]

# Register your models here.
