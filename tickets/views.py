# tickets/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator # [추가] Django의 Paginator를 import 합니다.
from django.db.models import Q, Count # [추가] Count를 import 합니다.
from .models import Ticket, Notice, SiteUpdate
from .forms import UpperTicketForm, TLTicketForm, FootTicketForm
from . import constants
import json
from datetime import datetime # datetime을 import 합니다.
from django.contrib.auth.decorators import login_required

@login_required
def ticket_main_view(request):

    # POST 요청 처리 로직을 GET과 분리하여 명확하게 만듭니다.
    if request.method == 'POST':
        surgery_type = request.POST.get('surgery_type') # 'Upper', 'T&L', 'Foot'
        form = None

        # prefix는 항상 소문자로 일관성 있게 사용
        prefix = surgery_type.lower() if surgery_type else None

        prefix = ''
        if surgery_type == 'Upper':
            prefix = 'upper'
            form = UpperTicketForm(request.POST, prefix=prefix)
        elif surgery_type == 'T&L':
            prefix = 'tl' # '&'를 사용하지 않습니다.
            form = TLTicketForm(request.POST, prefix=prefix)
        elif surgery_type == 'Foot':
            prefix = 'foot'
            form = FootTicketForm(request.POST, prefix=prefix)

        if form and form.is_valid():
            instance = form.save(commit=False)
            instance.part_type = prefix # DB에 'upper', 'tl', 'foot' 으로 저장
            instance.save()
            # 저장 성공 시, 메인 페이지로 리디렉션하여 새로고침
            return redirect('ticket_main')
        else:
            # 유효성 검사 실패 시, 오류 메시지를 포함하여 아래 GET 로직으로 넘어감
            # 이 경우, 사용자가 입력한 데이터가 그대로 남아있는 폼이 화면에 표시됨
            pass

    # 2. GET 요청 처리 (페이지 로드) 또는 POST 실패 시
    # 폼 인스턴스는 여기서 한 번만 생성합니다.
    upper_form = UpperTicketForm(prefix='upper')
    tl_form = TLTicketForm(prefix='tl')
    foot_form = FootTicketForm(prefix='foot')

    # 만약 POST 요청이 실패했다면, 해당 폼을 오류가 포함된 폼으로 교체
    if request.method == 'POST' and form:
        if surgery_type == 'Upper': upper_form = form
        elif surgery_type == 'T&L': tl_form = form
        elif surgery_type == 'Foot': foot_form = form

    tickets = Ticket.objects.all().order_by('-surgery_date', '-id')

    # 자동 채우기 규칙을 JSON으로 변환 (원본 그대로의 방식)
    autofill_rules_for_js = {}

    for key, value in constants.AUTO_FILL_RULES.items():
        string_key = "-".join(key)
        autofill_rules_for_js[string_key] = value

    # [수정] json.dumps를 제거합니다.
    # HTML 템플릿의 |json_script가 알아서 변환해주기 때문에 여기서 변환하면 안 됩니다.
    autofill_rules_json = autofill_rules_for_js

    notices = {notice.part_type: notice.content for notice in Notice.objects.all()}

    latest_update = SiteUpdate.objects.order_by('-update_date').first()

    context = {
        'upper_form': upper_form,
        'tl_form': tl_form,
        'foot_form': foot_form,
        'tickets': tickets,
        'autofill_rules_json': autofill_rules_json,
        'notices': notices,
        'latest_update': latest_update, # <--- 이거 한 줄 추가!
    }
    return render(request, 'tickets/ticket_main.html', context)


# 더블클릭 시 데이터를 불러오는 기능
def get_ticket_data(request, ticket_id):
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    data = {
        'id': ticket.id, 'part_type': ticket.part_type,
        'surgery_date': ticket.surgery_date.strftime('%Y-%m-%d') if ticket.surgery_date else '',
        'professor_name': ticket.professor_name, 'surgery_name': ticket.surgery_name,
        'anesthesia': ticket.anesthesia, 'op_side': ticket.op_side, 'op_site': ticket.op_site,
        'clothing': ticket.clothing, 'brace': ticket.brace, 'op_marking': ticket.op_marking,
        'shaving_status': ticket.shaving_status, 'npo_status': ticket.npo_status,
        'ast_result': ticket.ast_result, 'ast_site': ticket.ast_site,
        'foleys_cath': ticket.foleys_cath, 'iv_line': ticket.iv_line,
        'supplies': ticket.supplies, 'supplies2': ticket.supplies2,
        'antibiotics': ticket.antibiotics, 'id_bracelet': ticket.id_bracelet, 'memo': ticket.memo,
        'pre_ru_status': ticket.pre_ru_status, 'pre_ru_result': ticket.pre_ru_result,
        'enema_status': ticket.enema_status, 'enema_details': ticket.enema_details,
        'spine_region': ticket.spine_region, 'approach': ticket.approach, 'level_count': ticket.level_count,
        'hair': ticket.hair, 'nipple': ticket.nipple,
    }
    return JsonResponse(data)

# 저장
@require_POST
def create_ticket(request):
    try:
        data = json.loads(request.body)
        part_type = data.get('part_type')
        form_class = {'upper': UpperTicketForm, 'tl': TLTicketForm, 'foot': FootTicketForm}.get(part_type)

        if not form_class:
            return JsonResponse({'status': 'error', 'message': '유효하지 않은 폼 타입입니다.'}, status=400)

        # [수정됨] prefix 옵션을 추가하여 'upper-surgery_date' 같은 데이터를 올바르게 인식하게 함
        form = form_class(data, prefix=part_type)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.part_type = part_type
            instance.save()
            return JsonResponse({'status': 'success', 'message': '티켓이 저장되었습니다.'})
        else:
            return JsonResponse({'status': 'error', 'message': '입력값을 확인해주세요.', 'errors': form.errors}, status=400)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

# 수정
@require_POST
def update_ticket(request, ticket_id):
    try:
        ticket_to_update = get_object_or_404(Ticket, pk=ticket_id)
        data = json.loads(request.body)
        part_type = data.get('part_type', ticket_to_update.part_type)
        form_class = {'upper': UpperTicketForm, 'tl': TLTicketForm, 'foot': FootTicketForm}.get(part_type)

        if not form_class:
            return JsonResponse({'status': 'error', 'message': '유효하지 않은 폼 타입입니다.'}, status=400)

        # --- [핵심 수정] ---
        # 수정 시에도 prefix와 함께 Form에 데이터를 전달합니다.
        form = form_class(data, instance=ticket_to_update, prefix=part_type)

        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'success', 'message': '티켓이 성공적으로 수정되었습니다.'})
        else:
            return JsonResponse({'status': 'error', 'message': '입력값을 확인해주세요.', 'errors': form.errors}, status=400)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

# 삭제
@require_POST
def delete_ticket(request, ticket_id):
    try:
        ticket_to_delete = get_object_or_404(Ticket, pk=ticket_id)
        ticket_to_delete.delete()
        return JsonResponse({'status': 'success', 'message': '티켓이 성공적으로 삭제되었습니다.'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

@login_required
# '날짜 필터' 기능을 추가하여 ticket_list_view 함수를 업데이트합니다.
def ticket_list_view(request):
    # 1. URL 파라미터에서 모든 필터/정렬 값을 가져옵니다.
    sort_by = request.GET.get('sort', '-surgery_date')
    order = request.GET.get('order', 'desc')
    query = request.GET.get('q', '')
    search_field = request.GET.get('search_field', 'all')
    date_filter = request.GET.get('date', '') # [추가] 날짜 필터 값을 가져옵니다.

    queryset = Ticket.objects.all()

    # 2. [추가] 만약 날짜 값이 있으면, 해당 날짜로 먼저 필터링합니다.
    if date_filter:
        queryset = queryset.filter(surgery_date=date_filter)

    # 3. 텍스트 검색 기능은 그대로 유지합니다.
    if query:
        if search_field == 'surgery_name': queryset = queryset.filter(surgery_name__icontains=query)
        elif search_field == 'professor_name': queryset = queryset.filter(professor_name__icontains=query)
        elif search_field == 'brace': queryset = queryset.filter(brace__icontains=query)
        else: queryset = queryset.filter(Q(surgery_name__icontains=query) | Q(brace__icontains=query) | Q(professor_name__icontains=query))

    # 4. 정렬 순서를 적용합니다.
    if order == 'desc':
        sort_by_query = f'-{sort_by.lstrip("-")}'
    else:
        sort_by_query = sort_by.lstrip('-')

    ordered_tickets = queryset.order_by(sort_by_query, '-id')

    # 5. 페이지네이션 기능은 그대로 유지합니다.
    paginator = Paginator(ordered_tickets, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'current_sort': sort_by.lstrip('-'),
        'current_order': order,
        'query': query,
        'current_search_field': search_field,
        'current_date': date_filter, # [추가] 현재 선택된 날짜를 템플릿에 전달
    }
    return render(request, 'tickets/ticket_list.html', context)


@login_required
# [최종 수정] ticket_stats_view 함수
def ticket_stats_view(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    year = request.GET.get('year')
    month = request.GET.get('month')

    queryset = Ticket.objects.all()
    filter_display_text = "전체 기간"

    if start_date and end_date:
        queryset = queryset.filter(surgery_date__range=[start_date, end_date])
        filter_display_text = f"{start_date} ~ {end_date}"
    elif year and month:
        queryset = queryset.filter(surgery_date__year=year, surgery_date__month=month)
        filter_display_text = f"{year}년 {month}월"
    elif year:
        queryset = queryset.filter(surgery_date__year=year)
        filter_display_text = f"{year}년"

    total_count = queryset.count()
    part_stats = list(queryset.values('part_type').annotate(count=Count('part_type')).order_by('-count'))
    professor_stats = list(queryset.values('professor_name').annotate(count=Count('professor_name')).order_by('-count'))
    anesthesia_stats = list(queryset.values('anesthesia').annotate(count=Count('anesthesia')).order_by('-count'))

    # [핵심] 리스트를 순회하며 데이터를 미리 가공합니다.
    chart_data = {
        'part': {
            'labels': ['Upper' if s['part_type'] == 'upper' else 'T&L' if s['part_type'] == 'tl' else 'Foot' if s['part_type'] == 'foot' else s['part_type'] or '(미지정)' for s in part_stats],
            'data': [s['count'] for s in part_stats],
        },
        'professor': {
            'labels': [s['professor_name'] or '(미지정)' for s in professor_stats],
            'data': [s['count'] for s in professor_stats],
        },
        'anesthesia': {
            'labels': [s['anesthesia'] or '(미지정)' for s in anesthesia_stats],
            'data': [s['count'] for s in anesthesia_stats],
        },
    }

    dates = Ticket.objects.dates('surgery_date', 'month', order='DESC')
    available_years = sorted(list(set(d.year for d in dates)), reverse=True)
    available_months = sorted(list(set(d.month for d in dates)), reverse=True)

    context = {
        'total_count': total_count,
        'part_stats': part_stats,
        'professor_stats': professor_stats,
        'anesthesia_stats': anesthesia_stats,
        'start_date': start_date,
        'end_date': end_date,
        'filter_display_text': filter_display_text,
        'available_years': available_years,
        'available_months': available_months,
        'current_year': int(year) if year else None,
        'current_month': int(month) if month else None,

        # [핵심] 데이터를 여기서 JSON 문자열로 완전히 변환해서 보냅니다.
        'chart_data_json': json.dumps(chart_data, ensure_ascii=False),
    }
    return render(request, 'tickets/ticket_stats.html', context)
