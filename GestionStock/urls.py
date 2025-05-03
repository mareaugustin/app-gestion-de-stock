from django.contrib import admin
from django.urls import path, include
from stock.views import dashboard
#from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('', auth_views.LoginView.as_view(template_name='authentifications/login.html'), name='user-login'),
    path('dashboard/', dashboard, name='dashboard'),
    path('', include('stock.urls')),
    path('staff/', include('authentifications.urls')),
    path('transactions/', include('transactions.urls')),
    path('authentifications/', include('authentifications.urls')),
    path('facture/', include('facture.urls')),
    path('notes/', include('notes.urls'))
]
