from django.urls import path
from . import views

app_name = 'services'

urlpatterns = [
    path('', views.service_list, name='service_list'),
    # path('services/<int:service_id>/', views.service, name='service'),
    # path('services/<int:service_id>/book/', views.book_service, name='book_service'),
    # path('services/<int:service_id>/book/confirm/', views.confirm_booking, name='confirm_booking'),
    # path('services/<int:service_id>/book/cancel/', views.cancel_booking, name='cancel_booking'),
    # path('services/<int:service_id>/book/complete/', views.complete_booking, name='complete_booking'),
    # path('services/<int:service_id>/book/review/', views.review_booking, name='review_booking'),
    # path('services/<int:service_id>/book/review/submit/', views.submit_review, name='submit_review'),
    # path('services/<int:service_id>/book/review/delete/', views.delete_review, name='delete_review'),
    # path('services/<int:service_id>/book/review/edit/', views.edit_review, name='edit_review'),
    # path('services/<int:service_id>/book/review/update/', views.update_review, name='update_review'),
    # path('services/<int:service_id>/book/review/like/', views.like_review, name='like_review'),
    # path('services/<int:service_id>/book/review/unlike/', views.unlike_review, name='unlike_review'),
    # path('services/<int:service_id>/book/review/report/', views.report_review, name='report_review'),
    # path('services/<int:service_id>/book/review/report/submit/', views.submit_report, name='submit_report'),
    # path('services/<int:service_id>/book/review/report/delete/', views.delete_report, name='delete_report'),
    # path('services/<int:service_id>/book/review/report/edit/', views.edit_report, name='edit_report'),
    # path('services/<int:service_id>/book/review/report/update/', views.update_report, name='update_report'),
    # path('services/<int:service_id>/book/review/report/like/', views.like_report, name='like_report'),
    # path('services/<int:service_id>/book/review/report/unlike/', views.unlike_report, name='unlike_report'),
    # path('services/<int:service_id>/book/review/report/report/', views.report_report, name='report_report'),
    # path('services/<int:service_id>/book/review/report/report/submit/', views.submit_report_report, name='submit_report_report'),
]