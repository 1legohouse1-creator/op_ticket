# tickets/forms.py

from django import forms
from .models import Ticket
from . import constants

# constants의 딕셔너리를 Django form choices 형식으로 변환하는 헬퍼 함수
def make_choices(options):
    # 첫 번째는 빈 값으로 ('---------')을 추가하여 선택을 유도
    return [('', '---------')] + [(opt, opt) for opt in options]

class UpperTicketForm(forms.ModelForm):
    # 날짜 입력을 위해 HTML5 date 위젯 사용
    surgery_date = forms.DateField(
        label="수술 날짜",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        required=True
    )

    class Meta:
        model = Ticket
        # Upper 탭에서 보여줄 모든 필드 목록
        fields = [
            'surgery_date', 'professor_name', 'surgery_name', 'anesthesia',
            'op_side', 'op_site',
            # E Section
            'clothing', 'brace', 'op_marking', 'shaving_status', 'npo_status', 'ast_result', 'ast_site',
            # N Section
            'foleys_cath', 'iv_line',
            # D Section
            'supplies', 'supplies2', 'antibiotics', 'id_bracelet', 'memo'
        ]

        # 각 필드에 적절한 위젯과 CSS 클래스 지정
        widgets = {
            'professor_name': forms.TextInput(attrs={'class': 'form-control'}),
            'surgery_name': forms.TextInput(attrs={'class': 'form-control'}),
            'anesthesia': forms.Select(choices=make_choices(constants.OPTIONS['anesthesia']), attrs={'class': 'form-select'}),

            'op_side': forms.Select(choices=make_choices(constants.UPPER_OPTIONS['op_side']), attrs={'class': 'form-select'}),
            'op_site': forms.Select(choices=make_choices(constants.UPPER_OPTIONS['op_site']), attrs={'class': 'form-select'}),

            # E Section
            'clothing': forms.Select(choices=make_choices(constants.OPTIONS['clothing']), attrs={'class': 'form-select'}),
            'brace': forms.TextInput(attrs={'class': 'form-control'}),
            'op_marking': forms.TextInput(attrs={'class': 'form-control'}),
            'shaving_status': forms.Select(choices=make_choices(constants.UPPER_OPTIONS['shaving_status']), attrs={'class': 'form-select'}),
            'npo_status': forms.Select(choices=make_choices(constants.OPTIONS['npo_status']), attrs={'class': 'form-select'}),
            'ast_result': forms.Select(choices=make_choices(constants.OPTIONS['ast_result']), attrs={'class': 'form-select'}),
            'ast_site': forms.TextInput(attrs={'class': 'form-control'}),

            # N Section
            'foleys_cath': forms.Select(choices=make_choices(constants.OPTIONS['foleys_cath']), attrs={'class': 'form-select'}),
            'iv_line': forms.TextInput(attrs={'class': 'form-control'}),

            # D Section
            'supplies': forms.TextInput(attrs={'class': 'form-control'}),
            'supplies2': forms.TextInput(attrs={'class': 'form-control'}),
            'antibiotics': forms.TextInput(attrs={'class': 'form-control'}),
            'id_bracelet': forms.Select(choices=make_choices(constants.OPTIONS['id_bracelet']), attrs={'class': 'form-select'}),
            'memo': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class TLTicketForm(forms.ModelForm):
    surgery_date = forms.DateField(
        label="수술 날짜",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        required=True
    )
    spine_region = forms.ChoiceField(
        label="Spine Region",
        choices=make_choices(constants.TL_OPTIONS['spine_region']),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    approach = forms.ChoiceField(
        label="Approach",
        choices=make_choices(constants.TL_OPTIONS['approach']),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    level_count = forms.ChoiceField(
        label="Level Count",
        choices=make_choices(constants.TL_OPTIONS['level_count']),
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Ticket
        # [수정] fields 리스트에 새로 추가한 모델 필드들을 모두 포함시킵니다.
        fields = [
            'surgery_date', 'professor_name', 'surgery_name', 'anesthesia',
            'spine_region', 'approach', 'level_count',
            'clothing', 'brace', 'op_marking', 'shaving_status', 'npo_status', 'ast_result', 'ast_site',
            # E 섹션에 추가되는 필드들
            'pre_ru_status', 'pre_ru_result', 'enema_status', 'enema_details', 'hair', 'nipple',
            # N, D 섹션 필드들
            'foleys_cath', 'iv_line', 'supplies', 'supplies2', 'antibiotics', 'id_bracelet', 'memo'
        ]
        # [수정] widgets 딕셔너리에 새 필드들의 모양(위젯)을 정의합니다.
        widgets = {
            'professor_name': forms.Select(choices=make_choices(constants.TL_OPTIONS['professor']), attrs={'class': 'form-select'}),
            'surgery_name': forms.TextInput(attrs={'class': 'form-control'}),
            'anesthesia': forms.Select(choices=make_choices(constants.OPTIONS['anesthesia']), attrs={'class': 'form-select'}),
            'clothing': forms.Select(choices=make_choices(constants.OPTIONS['clothing']), attrs={'class': 'form-select'}),
            'brace': forms.TextInput(attrs={'class': 'form-control'}),
            'op_marking': forms.TextInput(attrs={'class': 'form-control'}),
            'shaving_status': forms.Select(choices=make_choices(constants.TL_OPTIONS['shaving_status']), attrs={'class': 'form-select'}),

            # --- E 섹션 위젯 ---
            'npo_status': forms.Select(choices=make_choices(constants.OPTIONS['npo_status']), attrs={'class': 'form-select'}),
            'ast_result': forms.Select(choices=make_choices(constants.OPTIONS['ast_result']), attrs={'class': 'form-select'}),
            'ast_site': forms.TextInput(attrs={'class': 'form-control'}),
            # 새로 추가된 필드들의 위젯 정의
            'pre_ru_status': forms.TextInput(attrs={'class': 'form-control'}),
            'pre_ru_result': forms.TextInput(attrs={'class': 'form-control'}),
            'enema_status': forms.TextInput(attrs={'class': 'form-control'}),
            'enema_details': forms.TextInput(attrs={'class': 'form-control'}),
            'hair': forms.TextInput(attrs={'class': 'form-control'}),
            'nipple': forms.TextInput(attrs={'class': 'form-control'}),

            # --- N, D 섹션 위젯 ---
            'foleys_cath': forms.Select(choices=make_choices(constants.OPTIONS['foleys_cath']), attrs={'class': 'form-select'}),
            'iv_line': forms.TextInput(attrs={'class': 'form-control'}),
            'supplies': forms.TextInput(attrs={'class': 'form-control'}),
            'supplies2': forms.TextInput(attrs={'class': 'form-control'}),
            'antibiotics': forms.TextInput(attrs={'class': 'form-control'}),
            'id_bracelet': forms.Select(choices=make_choices(constants.OPTIONS['id_bracelet']), attrs={'class': 'form-select'}),
            'memo': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


# Foot 폼도 Upper와 필드가 거의 동일하므로 상속을 사용합니다.
class FootTicketForm(UpperTicketForm): # UpperTicketForm을 상속
    class Meta(UpperTicketForm.Meta): # 부모 Meta를 상속
        widgets = UpperTicketForm.Meta.widgets.copy() # 위젯 설정을 복사

        # [핵심 수정] clothing 필드의 위젯을 TextInput으로 덮어씁니다.
        widgets['clothing'] = forms.TextInput(attrs={'class': 'form-control'})

        # Foot에 맞는 op_side, op_site, shaving_status 옵션으로 교체
        widgets['op_side'] = forms.Select(choices=make_choices(constants.FOOT_OPTIONS['op_side']), attrs={'class': 'form-select'})
        widgets['op_site'] = forms.Select(choices=make_choices(constants.FOOT_OPTIONS['op_site']), attrs={'class': 'form-select'})
        widgets['shaving_status'] = forms.Select(choices=make_choices(constants.FOOT_OPTIONS['shaving_status']), attrs={'class': 'form-select'})
