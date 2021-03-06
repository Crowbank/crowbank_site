"""crowbank_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^confirm_send', views.send_confirmation, name='confirm_send'),
    url(r'^confirm/(?P<bk_no>[0-9]*)', views.confirm, name='confirm'),
    url(r'^inouts/(?P<io_args>.*)$', views.inouts, name='inouts'),
    url(r'^confirmation/(?P<bk_no>[0-9]+)', views.confirmation, name='confirmation'),
    url(r'^$', views.index, name='index'),
]
