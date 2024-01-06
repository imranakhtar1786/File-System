from django.contrib import admin
from django.urls import path
from mainapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.indexPage),
    path('signup/', views.sigupPage),
    path("verify/<int:code>/",views.verifyEmail),
    path("files/",views.listFile),
    path("download-file/<int:id>/",views.download),
    path("downloading-file-request/<int:id>/",views.downloadFile),
    path("login/",views.loginPage),
    path("logout/",views.logout1),
    path("upload-file/",views.UploadFiles)
]