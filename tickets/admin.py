# /home/jasspercoach/op_ticket_project/tickets/admin.py

from django.contrib import admin
from django import forms

# models.py 파일에서 Ticket 모델과 Notice 모델을 가져옵니다.
from .models import Ticket, Notice, SiteUpdate
# ckeditor_uploader 위젯을 가져옵니다.
from ckeditor_uploader.widgets import CKEditorUploadingWidget


# 1. Ticket 모델을 관리자 페이지에 등록합니다.
@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    """
    Ticket 모델이 관리자 페이지에서 어떻게 보이고 관리될지를 정의합니다.
    """
    # 목록 페이지에 표시될 필드들을 지정합니다.
    list_display = ('id', 'surgery_date', 'surgery_name', 'professor_name', 'op_side', 'op_site')

    # 필터링 기능을 추가할 필드들을 지정합니다. (오른쪽에 필터 사이드바 생성)
    list_filter = ('surgery_date', 'professor_name')

    # 검색 기능을 추가할 필드들을 지정합니다. (상단에 검색창 생성)
    search_fields = ('surgery_name', 'professor_name', 'memo')

    # 날짜 계층 탐색 기능을 추가합니다. (목록 상단에 날짜별 링크 생성)
    date_hierarchy = 'surgery_date'

# 2. Notice 모델의 content 필드에 사용할 Form을 먼저 정의합니다.
class NoticeAdminForm(forms.ModelForm):
    # content 필드에 CKEditor 위젯을 사용하도록 명시적으로 지정합니다.
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Notice
        fields = '__all__'


# 3. Notice 모델을 관리자 페이지에 등록하면서 위에서 만든 Form을 사용하도록 지정합니다.
@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    # 이 관리자 클래스는 NoticeAdminForm을 사용하여 폼을 렌더링합니다.
    form = NoticeAdminForm
    list_display = ('part_type',)
    list_filter = ('part_type',)


# 4. SiteUpdate 모델을 관리자 페이지에 등록합니다.
@admin.register(SiteUpdate)
class SiteUpdateAdmin(admin.ModelAdmin):
    # 목록에서 날짜와 내용을 바로 볼 수 있게 설정합니다.
    list_display = ('update_date', 'content')

    # 최신 날짜가 위로 오도록 정렬합니다.
    ordering = ('-update_date',)