from django.urls import path
from . import views

urlpatterns = [
    path('orders/', views.orders, name='orders'),
    # path('orders/<int:order_id>/', views.order, name='order'),
    # path('orders/<int:order_id>/cancel/', views.cancel_order, name='cancel_order'),
    # path('orders/<int:order_id>/complete/', views.complete_order, name='complete_order'),
    # path('orders/<int:order_id>/review/', views.review_order, name='review_order'),
    # path('orders/<int:order_id>/review/submit/', views.submit_review, name='submit_review'),
    # path('orders/<int:order_id>/review/delete/', views.delete_review, name='delete_review'),
    # path('orders/<int:order_id>/review/edit/', views.edit_review, name='edit_review'),
    # path('orders/<int:order_id>/review/update/', views.update_review, name='update_review'),
    # path('orders/<int:order_id>/review/like/', views.like_review, name='like_review'),
    # path('orders/<int:order_id>/review/unlike/', views.unlike_review, name='unlike_review'),
    # path('orders/<int:order_id>/review/report/', views.report_review, name='report_review'),
    # path('orders/<int:order_id>/review/report/submit/', views.submit_report, name='submit_report'),
    # path('orders/<int:order_id>/review/report/delete/', views.delete_report, name='delete_report'),
    # path('orders/<int:order_id>/review/report/edit/', views.edit_report, name='edit_report'),
    # path('orders/<int:order_id>/review/report/update/', views.update_report, name='update_report'),
    # path('orders/<int:order_id>/review/report/like/', views.like_report, name='like_report'),
    # path('orders/<int:order_id>/review/report/unlike/', views.unlike_report, name='unlike_report'),
    # path('orders/<int:order_id>/review/report/report/', views.report_report, name='report_report'),
    # path('orders/<int:order_id>/review/report/report/submit/', views.submit_report_report, name='submit_report_report'),
]