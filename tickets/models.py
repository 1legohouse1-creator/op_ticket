# tickets/models.py

from django.db import models
from django.utils import timezone # timezone 임포트
from ckeditor_uploader.fields import RichTextUploadingField     # 관리자페이지 주의사항

class Ticket(models.Model):
    """
    Tkinter 앱의 database.py 스키마를 기반으로 재구성한 Ticket 모델
    """
    # === 기본 정보 ===

    # 이 티켓이 어떤 파트에 속하는지 저장 ---
    part_type = models.CharField(max_length=10, default='upper')

    # surgery_date: 날짜 정보를 저장, NOT NULL 제약조건은 기본값
    surgery_date = models.DateField(verbose_name="수술 날짜")

    # professor_name: 담당 교수 이름
    professor_name = models.CharField(max_length=100, blank=True, verbose_name="담당 교수")

    # surgery_name: 수술명
    surgery_name = models.CharField(max_length=200, blank=True, verbose_name="수술명")

    # surgery_type: 수술 타입, 기본값을 'Upper'로 설정
    surgery_type = models.CharField(max_length=20, default='Upper', verbose_name="수술 타입")

    # anesthesia: 마취 정보
    anesthesia = models.CharField(max_length=100, blank=True, verbose_name="마취")

    # op_side: Rt/Lt 정보
    op_side = models.CharField(max_length=50, blank=True, verbose_name="Rt/Lt")

    # op_site: 수술 부위
    op_site = models.CharField(max_length=100, blank=True, verbose_name="수술 부위")

    # surgery_room_w, surgery_room_r: 수술방 정보
    surgery_room_w = models.CharField(max_length=50, blank=True, verbose_name="수술방(W)")
    surgery_room_r = models.CharField(max_length=50, blank=True, verbose_name="수술방(R)")

    # === E 섹션 (준비 사항) ===
    clothing = models.CharField(max_length=100, blank=True, verbose_name="환의")
    brace = models.CharField(max_length=100, blank=True, verbose_name="보조기")
    op_marking = models.CharField(max_length=100, blank=True, verbose_name="OP Marking")
    shaving_status = models.CharField(max_length=100, blank=True, verbose_name="Shaving")
    npo_status = models.CharField(max_length=100, blank=True, verbose_name="자정 NPO")
    ast_result = models.CharField(max_length=100, blank=True, verbose_name="AST 결과")
    ast_site = models.CharField(max_length=100, blank=True, verbose_name="AST 위치")

    # === N 섹션 (간호 처치) ===
    foleys_cath = models.CharField(max_length=100, blank=True, verbose_name="Foley's cath.")
    iv_line = models.CharField(max_length=100, blank=True, verbose_name="I.V Line")

    # === D 섹션 (기타) ===
    supplies = models.CharField(max_length=200, blank=True, verbose_name="기타 준비물")
    supplies2 = models.CharField(max_length=200, blank=True, verbose_name="기타 준비물 2") # supplies2 추가
    antibiotics = models.CharField(max_length=100, blank=True, verbose_name="Anti")
    id_bracelet = models.CharField(max_length=100, blank=True, verbose_name="인식 팔찌")
    memo = models.TextField(blank=True, verbose_name="메모") # 긴 텍스트를 위해 TextField 사용

    # === T&L 척추 수술 전용 필드 ===
    pre_ru_status = models.CharField(max_length=100, blank=True, verbose_name="Pre RU 여부")
    pre_ru_result = models.CharField(max_length=100, blank=True, verbose_name="Pre RU 결과")
    enema_status = models.CharField(max_length=50, blank=True, verbose_name="Enema 시행")
    enema_details = models.TextField(blank=True, verbose_name="Enema 상세") # 긴 텍스트를 위해 TextField 사용
    spine_region = models.CharField(max_length=100, blank=True, verbose_name="척추 부위")
    approach = models.CharField(max_length=100, blank=True, verbose_name="접근법")
    level_count = models.CharField(max_length=100, blank=True, verbose_name="Level 수")
    hair = models.CharField(max_length=100, blank=True, verbose_name="머리 처리") # 추가
    nipple = models.CharField(max_length=100, blank=True, verbose_name="Nipple 처리") # 추가

    # === 메타 데이터 ===
    # created_at: 데이터 생성 시 자동으로 현재 시간 저장
    created_at = models.DateTimeField(default=timezone.now, verbose_name="생성일시")

    def __str__(self):
        # 객체를 문자열로 표현할 때 사용 (관리자 페이지 등에서 보임)
        return f"[{self.surgery_date}] {self.professor_name} - {self.surgery_name}"

    class Meta:
        verbose_name = "수술 티켓"
        verbose_name_plural = "수술 티켓" # 복수형 이름도 동일하게 설정
        # 모델의 옵션 설정
        ordering = ['-surgery_date', '-id'] # 기본 정렬 순서를 수술날짜 내림차순, ID 내림차순으로 지정

# 새로운 Notice 모델 추가
class Notice(models.Model):
    # 'part_type'으로 'Upper', 'T&L', 'Foot' 등을 구분합니다.
    part_type = models.CharField(max_length=20, unique=True, choices=[
        ('upper', 'Upper'),
        ('tl', 'T&L'),
        ('foot', 'Foot'),
    ])
    # CKEditor 필드 사용. 글자 수 제한 없는 텍스트 필드입니다.
    content = RichTextUploadingField()

    class Meta:
        verbose_name = "주의사항"
        verbose_name_plural = "주의사항"

    def __str__(self):
        return f"{self.get_part_type_display()} 주의사항"

class SiteUpdate(models.Model):
    update_date = models.DateField(verbose_name="업데이트 날짜")
    content = models.CharField(max_length=200, verbose_name="수정 내용")

    def __str__(self):
        return f"{self.update_date} - {self.content}"