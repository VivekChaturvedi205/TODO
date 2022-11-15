from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('register/', views.register, name="register"),
    path('login/',views.login,name="login"),
    path('login_process/',views.log_process,name="login_process"),
    path('success/',views.success,name="success"),
    path('error/',views.error,name="error"),
    path('reg_attempt/',views.reg_process,name="reg_process"),
    path('verify/<Token>',views.verify_email,name="verify_email"),
    path('add_task/',views.add_task,name="add_task"),
    path('logout/',views.logout_view,name="logout"),
    path('edit/<int:id>',views.edit_task,name="edit_task"),
    path('update/<int:id>',views.update_task,name="update_task"),
    path('delete/<int:id>',views.delete_task,name="delete")
]
