# main_app.py (v4.0 - 최종 수정)

import tkinter as tk
from tkinter import ttk, messagebox
import database as db
from constants import OPTIONS, AUTO_FILL_RULES
from ui_components import (
    UpperFormTab,
    TLFormTab,
    FootFormTab,
    PrecautionsPanel,
    SurgeryListPanel,
)
import printing
import os
import platform
import subprocess

try:
    import win32print  # type: ignore
except ImportError:
    win32print = None


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        db.create_table()
        self.title("OS OP 준비 티켓 프로그램 (v4.2 - 창 크기 조절 기능)")
        self.geometry("1400x950")
        self.minsize(1100, 800)

        self.selected_ticket_id = None
        self.current_surgery_type = "Upper"

        # [핵심 수정] 패널의 상태와 마지막 너비를 저장할 변수
        self.side_panel_visible = True
        self.last_panel_width = 600  # 패널의 너비를 기억할 변수 (기본값)

        self.create_widgets()
        self.load_tickets()
        self.previous_tab_index = 0

    def create_widgets(self):
        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        self.tab1_frame = ttk.Frame(notebook)
        self.tab2_frame = ttk.Frame(notebook)
        self.tab3_frame = ttk.Frame(notebook)
        self.tab4_frame = ttk.Frame(notebook)

        notebook.add(self.tab1_frame, text=" OP 준비 티켓 ")
        notebook.add(self.tab2_frame, text=" 전체 목록 조회 ")
        notebook.add(self.tab3_frame, text=" 통계/리포트 ")
        notebook.add(self.tab4_frame, text=" 설정 ")

        self.create_ticket_tab_widgets(self.tab1_frame)
        self.create_list_tab_widgets(self.tab2_frame)
        self.create_stats_tab_widgets(self.tab3_frame)
        self.create_settings_tab_widgets(self.tab4_frame)

    def create_ticket_tab_widgets(self, parent_tab):
        # [핵심 수정] pack 레이아웃 순서와 옵션을 바로잡습니다.

        # 1. 왼쪽 입력 폼을 먼저 생성하고 왼쪽에 붙입니다.
        #    expand=False로 설정하여 너비가 자동으로 확장되지 않도록 합니다.
        #    fill='y'로 높이는 꽉 채웁니다.
        input_form_frame = ttk.Frame(parent_tab)
        input_form_frame.pack(side="left", fill="y", padx=(0, 10))
        self.create_input_form(input_form_frame)

        # 2. 오른쪽 사이드 패널을 나중에 생성하고, 남은 공간을 모두 채우도록 합니다.
        #    expand=True, fill='both'로 설정합니다.
        self.side_panel_frame = ttk.Frame(parent_tab)
        self.side_panel_frame.pack(side="right", fill="both", expand=True)
        self.create_side_panel(self.side_panel_frame)

    def create_list_tab_widgets(self, parent_tab):
        label = ttk.Label(
            parent_tab,
            text="모든 수술 준비 기록을 검색하고 필터링하는\n전체 목록 화면이 여기에 구성될 예정입니다.",
            font=("Malgun Gothic", 16),
            justify="center",
        )
        label.pack(expand=True)

    def create_stats_tab_widgets(self, parent_tab):
        label = ttk.Label(
            parent_tab,
            text="월별, 수술별 통계 및 리포트 출력 기능이\n여기에 구성될 예정입니다.",
            font=("Malgun Gothic", 16),
            justify="center",
        )
        label.pack(expand=True)

    def create_settings_tab_widgets(self, parent_tab):
        label = ttk.Label(
            parent_tab,
            text="자동 채움 규칙, 사용자 옵션 등을 관리하는\n설정 화면이 여기에 구성될 예정입니다.",
            font=("Malgun Gothic", 16),
            justify="center",
        )
        label.pack(expand=True)

    def _add_grid_row(self, parent, label_text, widget, row_index):
        label = ttk.Label(parent, text=label_text, anchor="w")
        label.grid(row=row_index, column=0, sticky="ew", padx=5, pady=3)
        widget.grid(row=row_index, column=1, sticky="ew", padx=5, pady=3)

    def create_input_form(self, parent):
        top_button_frame = ttk.Frame(parent)
        top_button_frame.pack(fill="x", padx=5, pady=(5, 0))

        self.toggle_button = ttk.Button(
            top_button_frame, text="▶ 주의사항 숨기기", command=self.toggle_side_panel
        )
        self.toggle_button.pack(side="right")

        container = ttk.LabelFrame(parent, text="OP 준비 티켓 입력")
        container.pack(fill="both", expand=True, padx=5, pady=5)

        button_frame = ttk.Frame(container)
        button_frame.pack(side="bottom", fill="x", pady=(10, 5), padx=5)

        scroll_area_container = ttk.Frame(container)
        scroll_area_container.pack(side="top", fill="both", expand=True)

        scroll_area_container.rowconfigure(0, weight=1)
        scroll_area_container.columnconfigure(0, weight=1)

        canvas = tk.Canvas(scroll_area_container)
        scrollbar = ttk.Scrollbar(
            scroll_area_container, orient="vertical", command=canvas.yview
        )
        self.scrollable_frame = ttk.Frame(canvas)
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas_frame = canvas.create_window(
            (0, 0), window=self.scrollable_frame, anchor="nw"
        )

        def _on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        def _on_canvas_configure(event):
            canvas.itemconfig(canvas_frame, width=event.width)

        self.scrollable_frame.bind("<Configure>", _on_frame_configure)
        canvas.bind("<Configure>", _on_canvas_configure)
        canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)
        button_frame.columnconfigure(2, weight=1)
        button_frame.columnconfigure(3, weight=1)
        button_frame.columnconfigure(4, weight=1)
        ttk.Button(button_frame, text="저장", command=self.save_ticket).grid(
            row=0, column=0, sticky="ew", padx=2
        )
        ttk.Button(button_frame, text="수정", command=self.update_ticket).grid(
            row=0, column=1, sticky="ew", padx=2
        )
        ttk.Button(button_frame, text="삭제", command=self.delete_ticket).grid(
            row=0, column=2, sticky="ew", padx=2
        )
        ttk.Button(button_frame, text="프린트", command=self.print_ticket).grid(
            row=0, column=3, sticky="ew", padx=2
        )
        ttk.Button(button_frame, text="초기화", command=self.clear_form).grid(
            row=0, column=4, sticky="ew", padx=2
        )

        form_frame = self.scrollable_frame
        form_frame.columnconfigure(1, weight=1)

        self.vars = {
            "surgery_year": tk.StringVar(),
            "surgery_month": tk.StringVar(),
            "surgery_day": tk.StringVar(),
            "surgery_room_w": tk.StringVar(),
            "surgery_room_r": tk.StringVar(),
            "professor_name": tk.StringVar(),
            "surgery_name": tk.StringVar(),
            "anesthesia": tk.StringVar(),
            "op_side": tk.StringVar(),
            "op_site": tk.StringVar(),
            "clothing": tk.StringVar(),
            "brace": tk.StringVar(),
            "shaving_status": tk.StringVar(),
            "op_marking": tk.StringVar(),
            "npo_status": tk.StringVar(),
            "pre_ru_status": tk.StringVar(),
            "pre_ru_result": tk.StringVar(),
            "ast_result": tk.StringVar(),
            "ast_site": tk.StringVar(),
            "enema_status": tk.StringVar(),
            "supplies": tk.StringVar(),
            "supplies2": tk.StringVar(),
            "antibiotics": tk.StringVar(),
            "iv_line": tk.StringVar(),
            "id_bracelet": tk.StringVar(),
            "memo": tk.StringVar(),
            "foleys_cath": tk.StringVar(),
            "spine_region": tk.StringVar(),
            "approach": tk.StringVar(),
            "level_count": tk.StringVar(),
        }

        row_counter = 0
        surgery_type_notebook = ttk.Notebook(form_frame)
        surgery_type_notebook.grid(
            row=row_counter, column=0, columnspan=2, sticky="ew", padx=5, pady=(5, 0)
        )
        self.upper_tab = UpperFormTab(
            surgery_type_notebook, self.vars, self.apply_autofill_rules
        )
        surgery_type_notebook.add(self.upper_tab.frame, text="Upper")
        self.tl_tab = TLFormTab(
            surgery_type_notebook, self.vars, self.apply_autofill_rules
        )
        surgery_type_notebook.add(self.tl_tab.frame, text="T&L")
        self.foot_tab = FootFormTab(
            surgery_type_notebook, self.vars, self.apply_autofill_rules
        )
        surgery_type_notebook.add(self.foot_tab.frame, text="Foot")
        self.surgery_type_notebook = surgery_type_notebook
        self.surgery_type_notebook.bind(
            "<<NotebookTabChanged>>", self._on_surgery_type_change
        )
        row_counter += 1
        ttk.Label(form_frame, text="E", font=("Helvetica", 12, "bold")).grid(
            row=row_counter, column=0, sticky="w", padx=5, pady=(10, 0)
        )
        self.e_frame = ttk.Frame(form_frame, borderwidth=1, relief="solid")
        self.e_frame.grid(
            row=row_counter + 1, column=0, columnspan=2, sticky="ew", padx=5, pady=5
        )
        self.e_frame.columnconfigure(1, weight=1)
        self._add_grid_row(
            self.e_frame,
            "환의",
            ttk.Combobox(
                self.e_frame,
                textvariable=self.vars["clothing"],
                values=OPTIONS["clothing"],
            ),
            0,
        )
        self._add_grid_row(
            self.e_frame,
            "보조기",
            ttk.Entry(self.e_frame, textvariable=self.vars["brace"]),
            1,
        )
        self._add_grid_row(
            self.e_frame,
            "OP Marking",
            ttk.Entry(self.e_frame, textvariable=self.vars["op_marking"]),
            2,
        )
        self._add_grid_row(
            self.e_frame,
            "Shaving",
            ttk.Combobox(
                self.e_frame,
                textvariable=self.vars["shaving_status"],
                values=[
                    "Rt.Axillary 이하",
                    "Lt.Axillary 이하",
                    "Both Axillary 이하",
                    "필요 없음",
                    "턱수염",
                    "뒷머리",
                    "안함",
                    "Rt.ingunal 이하",
                    "Lt.ingunal 이하",
                    "Both ingunal 이하",
                    "Rt.thigh 이하",
                    "Lt.thigh 이하",
                    "Both thigh 이하",
                    "Rt.knee 이하",
                    "Lt.knee 이하",
                    "Both knee 이하",
                ],
            ),
            3,
        )
        self.tl_pre_ru_label = ttk.Label(self.e_frame, text="Pre RU 여부", anchor="w")
        self.tl_pre_ru_entry = ttk.Entry(
            self.e_frame, textvariable=self.vars["pre_ru_status"]
        )
        self.tl_pre_ru_result_label = ttk.Label(
            self.e_frame, text="Pre RU 결과", anchor="w"
        )
        self.tl_pre_ru_result_entry = ttk.Entry(
            self.e_frame, textvariable=self.vars["pre_ru_result"]
        )
        self.tl_enema_label = ttk.Label(self.e_frame, text="Enema 시행", anchor="w")
        self.tl_enema_combo = ttk.Combobox(
            self.e_frame,
            textvariable=self.vars["enema_status"],
            values=["O", "X", "해당 없음"],
        )
        self.tl_enema_details_label = ttk.Label(
            self.e_frame, text="Enema 양/횟수", anchor="w"
        )
        self.tl_enema_details_text = tk.Text(
            self.e_frame, height=2, wrap="word", font=("Malgun Gothic", 9)
        )
        self._add_grid_row(
            self.e_frame,
            "자정 NPO",
            ttk.Combobox(
                self.e_frame,
                textvariable=self.vars["npo_status"],
                values=OPTIONS["npo_status"],
            ),
            8,
        )
        self._add_grid_row(
            self.e_frame,
            "AST 결과",
            ttk.Combobox(
                self.e_frame,
                textvariable=self.vars["ast_result"],
                values=OPTIONS["ast_result"],
            ),
            9,
        )
        self._add_grid_row(
            self.e_frame,
            "AST 위치",
            ttk.Entry(self.e_frame, textvariable=self.vars["ast_site"]),
            10,
        )
        self.update_e_section_fields()
        row_counter += 2
        ttk.Label(form_frame, text="N", font=("Helvetica", 12, "bold")).grid(
            row=row_counter, column=0, sticky="w", padx=5, pady=(10, 0)
        )
        n_frame = ttk.Frame(form_frame, borderwidth=1, relief="solid")
        n_frame.grid(
            row=row_counter + 1, column=0, columnspan=2, sticky="ew", padx=5, pady=5
        )
        n_frame.columnconfigure(1, weight=1)
        self._add_grid_row(
            n_frame,
            "Foley's cath.",
            ttk.Combobox(
                n_frame,
                textvariable=self.vars["foleys_cath"],
                values=OPTIONS["foleys_cath"],
            ),
            0,
        )
        self._add_grid_row(
            n_frame,
            "I.V Line",
            ttk.Entry(n_frame, textvariable=self.vars["iv_line"]),
            1,
        )
        row_counter += 2
        ttk.Label(form_frame, text="D", font=("Helvetica", 12, "bold")).grid(
            row=row_counter, column=0, sticky="w", padx=5, pady=(10, 0)
        )
        d_frame = ttk.Frame(form_frame, borderwidth=1, relief="solid")
        d_frame.grid(
            row=row_counter + 1, column=0, columnspan=2, sticky="ew", padx=5, pady=5
        )
        d_frame.columnconfigure(1, weight=1)
        self._add_grid_row(
            d_frame,
            "기타 준비물",
            ttk.Entry(d_frame, textvariable=self.vars["supplies"]),
            0,
        )
        self._add_grid_row(
            d_frame,
            "Anti",
            ttk.Entry(d_frame, textvariable=self.vars["antibiotics"]),
            1,
        )
        self._add_grid_row(
            d_frame,
            "인식 팔찌",
            ttk.Combobox(
                d_frame,
                textvariable=self.vars["id_bracelet"],
                values=OPTIONS["id_bracelet"],
            ),
            2,
        )
        self._add_grid_row(
            d_frame, "메모", ttk.Entry(d_frame, textvariable=self.vars["memo"]), 3
        )

    def apply_autofill_rules(self, event=None):
        rules_to_apply = {}
        rule_key = None

        if self.current_surgery_type == "Upper":
            selected_op_side = self.vars["op_side"].get()
            selected_op_site = self.vars["op_site"].get()
            if selected_op_side and selected_op_site:
                rule_key = (selected_op_side, selected_op_site)

        elif self.current_surgery_type == "T&L":
            spine_region = self.vars["spine_region"].get()
            approach = self.vars["approach"].get()
            level_count = self.vars["level_count"].get()
            professor = self.vars["professor_name"].get()
            surgery_name = self.vars["surgery_name"].get()

            key1 = (spine_region, approach, level_count, professor)
            key2 = (surgery_name, level_count, professor)
            if key1 in AUTO_FILL_RULES:
                rule_key = key1
            elif key2 in AUTO_FILL_RULES:
                rule_key = key2

        elif self.current_surgery_type == "Foot":
            selected_op_side = self.vars["op_side"].get()
            selected_op_site = self.vars["op_site"].get()
            if selected_op_side and selected_op_site:
                rule_key = (selected_op_side, selected_op_site)

        if rule_key and rule_key in AUTO_FILL_RULES:
            rules_to_apply = AUTO_FILL_RULES[rule_key]
            for field, value in rules_to_apply.items():
                if field == "enema_details":
                    if hasattr(self, "tl_enema_details_text"):
                        self.tl_enema_details_text.delete("1.0", "end")
                        self.tl_enema_details_text.insert("1.0", value)
                elif field in self.vars:
                    self.vars[field].set(value)

    def _on_surgery_type_change(self, event):
        if hasattr(self, "precautions_panel") and self.precautions_panel.is_edit_mode:
            messagebox.showwarning(
                "편집 중",
                "주의사항을 편집하는 중에는 탭을 이동할 수 없습니다.\n먼저 '저장' 또는 '취소' 버튼을 눌러주세요.",
            )
            self.surgery_type_notebook.select(self.previous_tab_index)
            return

        try:
            current_idx = self.surgery_type_notebook.index(
                self.surgery_type_notebook.select()
            )
        except tk.TclError:
            return

        if self.previous_tab_index != current_idx:
            tab_names = ["Upper", "T&L", "Foot"]
            if current_idx < len(tab_names):
                self.current_surgery_type = tab_names[current_idx]

                self.clear_form()

                if hasattr(self, "precautions_panel") and self.precautions_panel:
                    self.precautions_panel.set_tab(self.current_surgery_type)

                self.update_e_section_fields()

            self.previous_tab_index = current_idx

    def update_e_section_fields(self):
        if hasattr(self, "e_frame") and hasattr(self, "tl_pre_ru_label"):
            if self.current_surgery_type == "T&L":
                self.tl_pre_ru_label.grid(row=4, column=0, sticky="ew", padx=5, pady=3)
                self.tl_pre_ru_entry.grid(row=4, column=1, sticky="ew", padx=5, pady=3)
                self.tl_pre_ru_result_label.grid(
                    row=5, column=0, sticky="ew", padx=5, pady=3
                )
                self.tl_pre_ru_result_entry.grid(
                    row=5, column=1, sticky="ew", padx=5, pady=3
                )
                self.tl_enema_label.grid(row=6, column=0, sticky="ew", padx=5, pady=3)
                self.tl_enema_combo.grid(row=6, column=1, sticky="ew", padx=5, pady=3)
                self.tl_enema_details_label.grid(
                    row=7, column=0, sticky="ew", padx=5, pady=3
                )
                self.tl_enema_details_text.grid(
                    row=7, column=1, sticky="ew", padx=5, pady=3
                )
            else:
                self.tl_pre_ru_label.grid_forget()
                self.tl_pre_ru_entry.grid_forget()
                self.tl_pre_ru_result_label.grid_forget()
                self.tl_pre_ru_result_entry.grid_forget()
                self.tl_enema_label.grid_forget()
                self.tl_enema_combo.grid_forget()
                self.tl_enema_details_label.grid_forget()
                self.tl_enema_details_text.grid_forget()

    def create_side_panel(self, parent):
        side_pane = ttk.PanedWindow(parent, orient=tk.VERTICAL)
        side_pane.pack(fill=tk.BOTH, expand=True)

        self.precautions_panel = PrecautionsPanel(parent, self.on_precautions_change)
        self.surgery_list_panel = SurgeryListPanel(parent, self.on_tree_select)

        side_pane.add(self.precautions_panel.frame, weight=4)
        side_pane.add(self.surgery_list_panel.frame, weight=6)

    def on_precautions_change(self, tab_name, new_text):
        pass

    def load_tickets(self):
        tickets = db.get_all_tickets()
        self.surgery_list_panel.load_tickets(tickets)

    def get_current_form_data(self):
        data = {key: var.get() for key, var in self.vars.items()}
        data["surgery_type"] = self.current_surgery_type

        if self.current_surgery_type == "T&L":
            data["enema_details"] = self.tl_enema_details_text.get("1.0", "end-1c")

        year = data.get("surgery_year", "").strip()
        month = data.get("surgery_month", "").strip()
        day = data.get("surgery_day", "").strip()

        data["surgery_date"] = (
            f"{year}-{month.zfill(2)}-{day.zfill(2)}" if year and month and day else ""
        )
        return data

    def save_ticket(self):
        try:
            data = self.get_current_form_data()
            if not data.get("surgery_date"):
                messagebox.showwarning("입력 오류", "수술 날짜는 필수 항목입니다.")
                return
            data.pop("surgery_year", None)
            data.pop("surgery_month", None)
            data.pop("surgery_day", None)
            db.add_ticket(data)
            messagebox.showinfo("성공", "티켓이 성공적으로 저장되었습니다.")
            self.load_tickets()
            self.clear_form()
        except Exception as e:
            messagebox.showerror(
                "저장 오류", f"데이터 저장 중 예상치 못한 오류가 발생했습니다:\n\n{e}"
            )

    def print_ticket(self):
        data = self.get_current_form_data()
        if not data.get("surgery_date"):
            messagebox.showwarning(
                "입력 오류", "인쇄할 내용이 없습니다. 먼저 수술 날짜를 입력해주세요."
            )
            return
        pdf_path = None
        try:
            pdf_path = printing.generate_ticket_pdf(data)
            current_os = platform.system()
            if current_os == "Windows":
                if not win32print:
                    messagebox.showerror(
                        "모듈 오류",
                        "Windows 인쇄 기능을 사용하기 위한 'pypiwin32' 모듈이 설치되지 않았습니다.",
                    )
                    return
                try:
                    win32print.GetDefaultPrinter()
                    os.startfile(pdf_path, "print")
                except Exception:
                    messagebox.showerror(
                        "프린터 오류",
                        "기본 프린터를 찾을 수 없습니다. [제어판] > [장치 및 프린터]에서 기본 프린터가 올바르게 설정되었는지 확인해주세요.",
                    )
                    return
            elif current_os in ["Darwin", "Linux"]:
                result = subprocess.run(
                    ["lpstat", "-d"], capture_output=True, text=True
                )
                if result.returncode != 0 or not result.stdout.strip():
                    messagebox.showerror(
                        "프린터 오류",
                        "기본 프린터를 찾을 수 없습니다. 시스템 설정에서 프린터가 추가되고 기본 프린터로 지정되었는지 확인해주세요.",
                    )
                    return
                print_cmd = ["lpr" if current_os == "Darwin" else "lp", pdf_path]
                subprocess.run(print_cmd, check=True)
            else:
                messagebox.showerror(
                    "인쇄 오류", f"지원되지 않는 운영체제({current_os})입니다."
                )
                return
            messagebox.showinfo(
                "인쇄",
                f"'{os.path.basename(pdf_path)}' 파일을 기본 프린터로 전송했습니다.",
            )
        except FileNotFoundError as e:
            messagebox.showerror(
                "인쇄 오류",
                f"파일을 찾을 수 없습니다: {e}\n\n특히, c:/Windows/Fonts/malgun.ttf 폰트 파일이 있는지 확인해주세요.",
            )
        except Exception as e:
            messagebox.showerror(
                "인쇄 오류", f"인쇄 중 예상치 못한 오류가 발생했습니다:\n{e}"
            )
        finally:
            if pdf_path and os.path.exists(pdf_path):
                print(
                    f"인쇄를 위해 임시 파일 '{os.path.basename(pdf_path)}'가 생성되었습니다."
                )

    def update_ticket(self):
        if not self.selected_ticket_id:
            messagebox.showwarning("선택 오류", "수정할 티켓을 목록에서 선택해주세요.")
            return
        try:
            data = self.get_current_form_data()
            data.pop("surgery_year", None)
            data.pop("surgery_month", None)
            data.pop("surgery_day", None)
            db.update_ticket(self.selected_ticket_id, data)
            messagebox.showinfo(
                "성공", f"티켓 ID {self.selected_ticket_id}가 수정되었습니다."
            )
            self.load_tickets()
            self.clear_form()
        except Exception as e:
            messagebox.showerror(
                "수정 오류", f"데이터 수정 중 예상치 못한 오류가 발생했습니다:\n\n{e}"
            )

    def delete_ticket(self):
        if not self.selected_ticket_id:
            messagebox.showwarning("선택 오류", "삭제할 티켓을 목록에서 선택해주세요.")
            return
        if messagebox.askyesno(
            "삭제 확인", f"티켓 ID {self.selected_ticket_id}를 정말 삭제하시겠습니까?"
        ):
            db.delete_ticket(self.selected_ticket_id)
            messagebox.showinfo(
                "성공", f"티켓 ID {self.selected_ticket_id}가 삭제되었습니다."
            )
            self.load_tickets()
            self.clear_form()

    def clear_form(self):
        for var in self.vars.values():
            var.set("")
        if hasattr(self, "tl_enema_details_text"):
            self.tl_enema_details_text.delete("1.0", "end")
        self.selected_ticket_id = None
        self.surgery_list_panel.clear_selection()

    def on_tree_select(self, event):
        self.selected_ticket_id = self.surgery_list_panel.get_selected_id()
        if not self.selected_ticket_id:
            return
        all_tickets = db.get_all_tickets()
        ticket_data = next(
            (
                t
                for t in all_tickets
                if str(t.get("id")) == str(self.selected_ticket_id)
            ),
            None,
        )
        if ticket_data:
            surgery_type = ticket_data.get("surgery_type", "Upper")
            tab_index = {"Upper": 0, "T&L": 1, "Foot": 2}.get(surgery_type, 0)
            self.surgery_type_notebook.select(tab_index)
            self.current_surgery_type = surgery_type
            self.precautions_panel.set_tab(surgery_type)
            date_keys = {"surgery_year", "surgery_month", "surgery_day"}
            for key, var in self.vars.items():
                if key not in date_keys:
                    var.set(ticket_data.get(key, ""))
            surgery_date_str = ticket_data.get("surgery_date", "")
            if surgery_date_str and "-" in surgery_date_str:
                try:
                    year, month, day = surgery_date_str.split("-")
                    self.vars["surgery_year"].set(year)
                    self.vars["surgery_month"].set(month)
                    self.vars["surgery_day"].set(day)
                except ValueError:
                    self.vars["surgery_year"].set("")
                    self.vars["surgery_month"].set("")
                    self.vars["surgery_day"].set("")
            else:
                self.vars["surgery_year"].set("")
                self.vars["surgery_month"].set("")
                self.vars["surgery_day"].set("")
            if hasattr(self, "tl_enema_details_text"):
                self.tl_enema_details_text.delete("1.0", "end")
                self.tl_enema_details_text.insert(
                    "1.0", ticket_data.get("enema_details", "")
                )

    def toggle_side_panel(self):
        """오른쪽 사이드 패널을 숨기면서 창 크기를 조절합니다."""

        # 현재 창의 높이를 가져옵니다. 높이는 변하지 않습니다.
        current_win_height = self.winfo_height()

        if self.side_panel_visible:
            # --- 패널 숨기기 ---

            # 1. 숨기기 전, 현재 패널의 너비를 정확히 측정하여 저장합니다.
            #    (winfo_width()는 위젯의 현재 너비를 반환)
            panel_width = self.side_panel_frame.winfo_width()
            # 패널이 정상적인 너비를 가질 때만 값을 업데이트 (초기 실행 오류 방지)
            if panel_width > 1:
                self.last_panel_width = panel_width

            # 2. 현재 전체 창의 너비를 가져옵니다.
            current_win_width = self.winfo_width()

            # 3. 오른쪽 패널을 시야에서 숨깁니다.
            self.side_panel_frame.pack_forget()

            # 4. 새 창의 너비를 계산합니다 (현재 창 너비 - 패널 너비).
            #    padx(여백) 10을 빼주어 더 정확하게 계산합니다.
            new_width = current_win_width - self.last_panel_width - 10

            # 5. geometry를 사용하여 창 크기를 직접 변경합니다.
            self.geometry(f"{new_width}x{current_win_height}")

            # 6. 버튼 텍스트를 변경합니다.
            self.toggle_button.config(text="▶ 패널 보이기")
        else:
            # --- 패널 보이기 ---

            # 1. 현재 (줄어든) 창의 너비를 가져옵니다.
            current_win_width = self.winfo_width()

            # 2. 새 창의 너비를 계산합니다 (현재 창 너비 + 이전에 저장한 패널 너비).
            new_width = current_win_width + self.last_panel_width + 10

            # 3. 창 크기를 먼저 늘립니다.
            self.geometry(f"{new_width}x{current_win_height}")

            # 4. 오른쪽 패널을 다시 화면에 나타나게 합니다.
            self.side_panel_frame.pack(side="right", fill="both", expand=True)

            # 5. 버튼 텍스트를 원래대로 변경합니다.
            self.toggle_button.config(text="◀ 주의사항 숨기기")

        # 6. 현재 상태를 반전시킵니다.
        self.side_panel_visible = not self.side_panel_visible


if __name__ == "__main__":
    app = App()
    app.mainloop()
