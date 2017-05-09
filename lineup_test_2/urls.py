from django.conf.urls import url
from . import views

app_name = 'lineup_test_2'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^create_new_user/$', views.create_new_user, name='create_new_user'),
    url(r'^test_dir/(?P<uid>([A-Z]|[0-9]){14})/$', views.test_dir, name='test_dir'),
    # url(r'^generate_question/(?P<uid>([A-Z]|[0-9]){14})/(?P<category>(O1|Omany|R|U1|F))/$', views.generate_question, name='generate_question'),

    url(r'^generate_question/(?P<uid>([A-Z]|[0-9]){14})/$', views.generate_question, name='generate_question'),
    url(r'^detail/(?P<uid>([A-Z]|[0-9]){14})/(?P<category>(O1|Omany|R|U1|F))/$', views.detail, name='detail'),
    url(r'^record/(?P<uid>([A-Z]|[0-9]){14})/(?P<category>(O1|Omany|R|U1|F))/(?P<a>(0|20|40|60|80|100))/$', views.record_answer, name='record_answer'),

    url(r'^instruction/(?P<uid>([A-Z]|[0-9]){14})/(?P<mode>([0-9]))/$', views.instruction, name='instruction'),
    url(r'^example/(?P<uid>([A-Z]|[0-9]){14})/$', views.example, name='example'),

    url(r'^submit/(?P<uid>([A-Z]|[0-9]){14})/$', views.submit_survey, name='submit_survey'),

    url(r'^record_ex/(?P<uid>([A-Z]|[0-9]){14})/(?P<a>(0|20|40|60|80|100))/$',
        views.record_example, name='record_example'),

]