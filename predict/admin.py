from django.contrib import admin

from .models import Game



class GameAdmin(admin.ModelAdmin):
    list_display = ['__str__','gameid','home','visitor','gamedate','date_posted','finished']
    search_fields = ['content','user__username','user__email']
    class Meta:
        model = Game

admin.site.register(Game,GameAdmin)
