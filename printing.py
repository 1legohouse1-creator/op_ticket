# printing.py

import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import cm


def generate_ticket_pdf(ticket_data):
    """
    티켓 데이터를 바탕으로 A4 사이즈의 PDF 파일을 생성합니다.
    파일은 'temp_ticket.pdf'라는 이름으로 저장됩니다.
    """
    file_path = "temp_ticket.pdf"

    try:
        # --- 한글 폰트 등록 (Windows 기준 '맑은 고딕') ---
        # 폰트 경로가 다를 경우 시스템에 맞게 수정해야 합니다.
        font_path = "c:/Windows/Fonts/malgun.ttf"
        if not os.path.exists(font_path):
            # 대체 경로 (macOS 등)
            # font_path = "/System/Library/Fonts/Supplemental/AppleGothic.ttf"
            # 위 경로도 없다면 예외 발생
            raise FileNotFoundError(
                "맑은 고딕 폰트를 찾을 수 없습니다. 폰트 경로를 확인해주세요."
            )

        pdfmetrics.registerFont(TTFont("MalgunGothic", font_path))
    except Exception as e:
        print(f"폰트 로딩 오류: {e}")
        # 폰트 로딩 실패 시, 기본 폰트로 진행 (한글이 깨질 수 있음)
        pass

    c = canvas.Canvas(file_path, pagesize=A4)
    width, height = A4  # 페이지 크기 (가로, 세로)

    # --- 좌표 설정 (좌측 하단이 0,0) ---
    x_margin = 2 * cm
    y_start = height - 2 * cm
    line_height = 0.8 * cm

    def draw_line(y_pos, text1, text2):
        """PDF에 한 줄을 그리는 함수"""
        c.drawString(x_margin, y_pos, f"{text1}:")
        c.drawString(
            x_margin + 3.5 * cm, y_pos, str(text2) if text2 is not None else ""
        )

    # --- 문서 제목 ---
    c.setFont("MalgunGothic", 18)
    c.drawCentredString(
        width / 2, y_start, "■ 수술 준비 티켓 (OP Preparation Ticket) ■"
    )
    y_pos = y_start - 1.5 * cm

    # --- 기본 정보 출력 ---
    c.setFont("MalgunGothic", 11)

    # 날짜와 수술실을 한 줄에 표시
    date_str = ticket_data.get("surgery_date", "날짜 미입력")
    room_w = ticket_data.get("surgery_room_w", "")
    room_r = ticket_data.get("surgery_room_r", "")
    room_str = f"({room_w})W-({room_r})R"
    c.drawString(x_margin, y_pos, f"수술 날짜:  {date_str}")
    c.drawString(width - x_margin - 5 * cm, y_pos, f"수술실:  {room_str}")
    y_pos -= line_height

    draw_line(y_pos, "담당 교수", ticket_data.get("professor_name"))
    y_pos -= line_height
    draw_line(y_pos, "수술명", ticket_data.get("surgery_name"))
    y_pos -= line_height
    draw_line(y_pos, "마취", ticket_data.get("anesthesia"))
    y_pos -= line_height

    # 수술 타입에 따라 다른 필드 출력
    surgery_type = ticket_data.get("surgery_type", "Upper")
    if surgery_type in ["Upper", "Foot"]:
        draw_line(y_pos, "Rt./Lt.", ticket_data.get("op_side"))
        y_pos -= line_height
        draw_line(y_pos, "수술 부위", ticket_data.get("op_site"))
        y_pos -= line_height
    elif surgery_type == "T&L":
        draw_line(y_pos, "척추 부위", ticket_data.get("spine_region"))
        y_pos -= line_height
        draw_line(y_pos, "접근법", ticket_data.get("approach"))
        y_pos -= line_height
        draw_line(y_pos, "Level 개수", ticket_data.get("level_count"))
        y_pos -= line_height

    y_pos -= 0.5 * cm  # 섹션 간격

    # --- 구분선 ---
    c.line(x_margin, y_pos, width - x_margin, y_pos)
    y_pos -= 0.5 * cm

    def draw_section(title, fields, current_y):
        """E, N, D 섹션을 그리는 함수"""
        c.setFont("MalgunGothic", 14)
        c.drawString(x_margin, current_y, title)
        current_y -= line_height * 1.2

        c.setFont("MalgunGothic", 11)
        for label, key in fields.items():
            value = ticket_data.get(key, "")
            if value:  # 값이 있는 항목만 출력
                draw_line(current_y, label, value)
                current_y -= line_height
        return current_y - 0.5 * cm  # 섹션 간의 추가 여백

    # --- E 섹션 ---
    e_fields = {
        "환의": "clothing",
        "보조기": "brace",
        "OP Marking": "op_marking",
        "Shaving": "shaving_status",
        "자정 NPO": "npo_status",
        "AST 결과": "ast_result",
        "AST 위치": "ast_site",
    }
    # T&L 수술일 때만 추가되는 E 섹션 필드
    if surgery_type == "T&L":
        tl_fields = {
            "Pre RU 여부": "pre_ru_status",
            "Pre RU 결과": "pre_ru_result",
            "Enema 시행": "enema_status",
            "Enema 양/횟수": "enema_details",
        }
        # 기존 필드 중간에 삽입 (Shaving 다음)
        e_fields_list = list(e_fields.items())
        e_fields_list.insert(4, list(tl_fields.items())[0])
        e_fields_list.insert(5, list(tl_fields.items())[1])
        e_fields_list.insert(6, list(tl_fields.items())[2])
        e_fields_list.insert(7, list(tl_fields.items())[3])
        e_fields = dict(e_fields_list)

    y_pos = draw_section("E", e_fields, y_pos)

    # --- N 섹션 ---
    n_fields = {"Foley's cath.": "foleys_cath", "I.V Line": "iv_line"}
    y_pos = draw_section("N", n_fields, y_pos)

    # --- D 섹션 ---
    d_fields = {
        "기타 준비물": "supplies",
        "Anti": "antibiotics",
        "인식 팔찌": "id_bracelet",
        "메모": "memo",
    }
    y_pos = draw_section("D", d_fields, y_pos)

    c.save()
    return file_path
