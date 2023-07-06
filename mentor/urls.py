from django.urls import path
from django.shortcuts import redirect
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # home page
    path('', lambda req : redirect('home')),
    path('home', views.home, name='home'),
    path('login', views.login, name='login'),
    path('signup', views.signup, name='signup'),
    path('mentors', views.viewMentors, name='mentors'),
    path('logout', views.user_logout, name='logout'),
    # home page ends

    # admin page
    path('mentors-request', views.view_mentors_request, name='view_mentors_request'),
    path('admin-view-mentors', views.admin_view_mentors, name='admin_view_mentors'),
    path('view-regected-mentors', views.view_regected_mentors, name='view_regected_mentors'),
    path('admin-view-reports', views.admin_view_messages, name='admin_view_messages'),
    path('admin-profile', views.admin_profile, name='admin_profile'),
    path('accept/mentor/<id>', views.accept_mentor, name='accept_mentor'),
    path('reject/mentor/<id>', views.reject_mentor, name='reject_mentor'),
    path('admin-view-patients', views.admin_view_patients, name='admin_view_patients'),
    path('admin-reply-<id>', views.admin_reply_message, name='admin_reply_message'),
    # admin page ends

    # mentor page
    path('patients-request', views.patients_request, name='patient_request'),
    path('accept/<id>', views.accept_patient_request, name='accept_request'),
    path('reject/<id>', views.reject_patient_request, name='reject_request'),
    path('accepted-patients', views.accepted_patients, name='accepted_patients'),
    path('view-diary-writings', views.view_diary_writings, name='view_diary_writings'),
    path('mentor-profile', views.mentor_profile, name='mentor_profile'),
    path('mentor_chat', views.mentor_chat, name='mentor_chat'),
    path("reply-<id>", views.mentor_reply_chat, name='mentor_reply'),
    path('dairy_reply-<id>', views.reply_to_diary_writings, name='reply_to_diary_writings'),
    path('send_motivation', views.send_motivations, name='send_motivation'),
    path('sent_complaints', views.sent_complaints, name='sent_complaints'),
    # mentor page ends

    # user page start
    path('user_profile', views.user_profile, name='user_profile'),
    path('view_mentors', views.user_view_mentors, name='view_mentors'),
    path('request', views.requst_mentor, name='request_mentor'),
    path('view_requested_mentors', views.view_requested_mentors, name='view_requested_mentors'),
    path('view_accepted_mentors', views.view_accepted_mentors, name='view_accepted_mentors'),
    path('write_diary', views.write_diary, name='write_diary'),
    path('chat', views.chat, name='chat'),
    path('report', views.report, name='report'),
    path('view_motivations', views.view_motivations, name='view_motivations')
    # user page ends

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)