
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from users import views as user_views
from django.conf import settings
from django.conf.urls.static import static
from predict import views as predict_views



from .sitemaps import GameSitemap,sitemap_index,custom_sitemap_view


sitemaps = {
    'Posts': GameSitemap,
}



urlpatterns = [
    path('autoshop/', user_views.shop, name='auto-shop'),
    path('', include('etc.urls')),
    path('shop/', user_views.shop, name='shop'),
    path('community/', user_views.community , name='community'),
    path('new-message/<str:m>', user_views.newMessage , name='new-message'),
    path('public-profile/<str:u>', user_views.publicProfile , name='public-profile'),
    path('export/', predict_views.exportGames , name='export-games'),
    path('admin/', admin.site.urls),
    path('predict/', include('predict.urls')),
    path('register/', user_views.register, name='register'),
    path('profile/', user_views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'), name='password_reset'),
    path('password-reset/done', auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), name='password_reset_complete'),
    
    path('sitemap_index.xml', sitemap_index, name='sitemap-index'),
    path('sitemap-<str:sitemap_name>.xml', custom_sitemap_view, name='custom-sitemap-view'),


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
