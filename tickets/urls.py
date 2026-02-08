# tickets/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # 기존 "근본파일" URL (그대로 유지)
    path('', views.ticket_main_view, name='ticket_main'),

    # 더블클릭 시 데이터 가져오기
    path('get/<int:ticket_id>/', views.get_ticket_data, name='get_ticket_data'),

    # 저장 API: /tickets/api/create/1/ 와 같은 형식
    path('api/create/', views.create_ticket, name='create_ticket'),

    # 수정 API: /tickets/api/update/2/ 와 같은 형식
    path('api/update/<int:ticket_id>/', views.update_ticket, name='update_ticket'),

    # 삭제 API: /tickets/api/delete/3/ 와 같은 형식
    path('api/delete/<int:ticket_id>/', views.delete_ticket, name='delete_ticket'),

    # [추가] '전체 목록 조회' 페이지를 위한 새로운 주소
    path('list/', views.ticket_list_view, name='ticket_list'),

    # [추가] '통계/리포트' 페이지를 위한 새로운 주소
    path('stats/', views.ticket_stats_view, name='ticket_stats'),
]

