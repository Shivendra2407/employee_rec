from django.conf.urls import url
from .views import EmployeeView, EmployeeListAPIView, DeleteEmployeAPIView, EmployeeUpdatetView, GenericSearch

urlpatterns = [
    url(r'^$', EmployeeView.as_view(), name='home'),
    url(r'^generic_search/$', GenericSearch.as_view(), name='home'),
    url(r'^api-list/(?P<string>.*)$', EmployeeListAPIView.as_view(), name='employee-list-api'),
    url(r'^delete/$', DeleteEmployeAPIView.as_view(), name='employee-delete-api'),
    url(r'^change/$', EmployeeUpdatetView.as_view(), name='employee-update-api')
]
