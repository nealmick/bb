from django.contrib import admin
from .models import Profile,Message
# Register your models here.



class ProfileAdmin(admin.ModelAdmin):
    list_display = ['__str__','predictions','correct','ev_margin3','ev_margin3_count']
    search_fields = []
    class Meta:
        model = Profile

admin.site.register(Profile,ProfileAdmin)

admin.site.register(Message)
