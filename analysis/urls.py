from django.urls import path
from . import views

urlpatterns = [
    path(r'index', views.index, name="index"),
    path(r'login', views.login, name="login"),
    path(r'logout', views.logout, name="logout"),
    path(r'check_username', views.check_username, name="check_username"),
    path(r'register', views.register, name="register"),
    path(r'SearchJob', views.SearchJob, name="SearchJob"),
    path(r'jobDetail', views.jobDetail, name="jobDetail"),
    path(r'analyse', views.analyse, name="analyse"),
    path(r'salaryForecast', views.salaryForecast, name="salaryForecast"),
    path(r'jobForecast', views.jobForecast, name="jobForecast"),
    path(r'companies', views.companies, name="companies"),
    path(r'companyDetail', views.companyDetail, name="companyDetail"),
    path(r'associate', views.associate, name="associate"),
    path(r'orientation2position', views.orientation2position, name="orientation2position"),
]