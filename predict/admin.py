from django.contrib import admin

from .models import Game, TensorflowModel,PermaGame,Retrain,ModelReset,ArbLoad



class GameAdmin(admin.ModelAdmin):
    list_display = ['__str__','gameid','home','visitor','gamedate','date_posted','finished']
    search_fields = ['content','user__username','user__email']
    class Meta:
        model = Game

admin.site.register(Game,GameAdmin)


class TensorflowModelAdmin(admin.ModelAdmin):
    list_display = ['author','ip',]
    search_fields = ['user__username','user__email']
    class Meta:
        model = TensorflowModel

admin.site.register(TensorflowModel,TensorflowModelAdmin)



class PermaGameAdmin(admin.ModelAdmin):
    list_display = ['author','ip',]
    search_fields = ['user__username','user__email']
    class Meta:
        model = PermaGame

admin.site.register(PermaGame,PermaGameAdmin)








class RetrainAdmin(admin.ModelAdmin):
    list_display = ['author','ip',]
    search_fields = ['user__username','user__email']
    readonly_fields = ('author', 'game','ip')

    class Meta:
        model = Retrain

admin.site.register(Retrain,RetrainAdmin)




class ModelResetAdmin(admin.ModelAdmin):
    list_display = ['author','ip',]
    search_fields = ['user__username','user__email']
    readonly_fields = ('author','ip')

    class Meta:
        model = ModelReset

admin.site.register(ModelReset,ModelResetAdmin)



class ArbAdmin(admin.ModelAdmin):
    list_display = ['author','ip',]
    search_fields = ['user__username','user__email']
    readonly_fields = ('author','ip')

    class Meta:
        model = ArbLoad

admin.site.register(ArbLoad,ArbAdmin)
