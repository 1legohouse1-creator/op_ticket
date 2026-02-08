# ui_components.py

import tkinter as tk
from tkinter import ttk, font, colorchooser
from tkinter import messagebox
import json
import data_manager
from constants import OPTIONS, UPPER_OPTIONS, TL_OPTIONS, FOOT_OPTIONS


class UpperFormTab:
    def __init__(self, parent, vars_dict, apply_autofill_callback):
        self.vars = vars_dict
        self.apply_autofill_callback = apply_autofill_callback
        self.frame = ttk.Frame(parent)
        self.create_upper_form()
        # self.frame.configure(height=180)

    def create_upper_form(self):
        self.frame.columnconfigure(1, weight=1)

        # --- 1. 수술 날짜 ---
        ttk.Label(self.frame, text="수술 날짜", anchor="w").grid(
            row=0, column=0, sticky="ew", padx=5, pady=3
        )
        date_entry_frame = ttk.Frame(self.frame)
        date_entry_frame.grid(row=0, column=1, sticky="ew", padx=5, pady=3)
        date_entry_frame.columnconfigure(0, weight=1)
        year_entry = ttk.Entry(
            date_entry_frame, textvariable=self.vars["surgery_year"], width=6
        )
        year_entry.grid(row=0, column=1, padx=(0, 2))
        ttk.Label(date_entry_frame, text="년").grid(row=0, column=2)
        month_entry = ttk.Entry(
            date_entry_frame, textvariable=self.vars["surgery_month"], width=4
        )
        month_entry.grid(row=0, column=3, padx=(5, 2))
        ttk.Label(date_entry_frame, text="월").grid(row=0, column=4)
        day_entry = ttk.Entry(
            date_entry_frame, textvariable=self.vars["surgery_day"], width=4
        )
        day_entry.grid(row=0, column=5, padx=(5, 2))
        ttk.Label(date_entry_frame, text="일").grid(row=0, column=6)

        # --- 2. 수술실 ---
        ttk.Label(self.frame, text="수술실", anchor="w").grid(
            row=1, column=0, sticky="ew", padx=5, pady=3
        )
        room_entry_frame = ttk.Frame(self.frame)
        room_entry_frame.grid(row=1, column=1, sticky="ew", padx=5, pady=3)
        room_entry_frame.columnconfigure(0, weight=1)
        ttk.Label(room_entry_frame, text="(").grid(row=0, column=1)
        w_entry = ttk.Entry(
            room_entry_frame, textvariable=self.vars["surgery_room_w"], width=3
        )
        w_entry.grid(row=0, column=2, padx=2)
        ttk.Label(room_entry_frame, text=")W-(").grid(row=0, column=3)
        r_entry = ttk.Entry(
            room_entry_frame, textvariable=self.vars["surgery_room_r"], width=3
        )
        r_entry.grid(row=0, column=4, padx=2)
        ttk.Label(room_entry_frame, text=")R").grid(row=0, column=5)

        # --- 3. 다음 포커스 대상 위젯 생성 ---
        professor_entry = ttk.Entry(
            self.frame, textvariable=self.vars["professor_name"]
        )

        # --- [핵심 수정] 스마트 입력 기능을 위한 콜백 함수 및 바인딩 ---
        def _on_year_write(*args):
            if len(self.vars["surgery_year"].get()) == 2:
                self.vars["surgery_year"].set("20" + self.vars["surgery_year"].get())
                month_entry.focus_set()
                month_entry.select_range(0, "end")

        def _on_month_day_write(var, next_widget):
            if len(var.get()) == 2:
                next_widget.focus_set()
                next_widget.select_range(0, "end")

        def _pad_with_zero(var):
            if len(var.get()) == 1 and var.get().isdigit():
                var.set("0" + var.get())

        def _on_w_room_write(*args):
            if len(self.vars["surgery_room_w"].get()) == 1:
                r_entry.focus_set()
                r_entry.select_range(0, "end")

        # 변수 변경 감지자 및 포커스 아웃 이벤트 연결
        self.vars["surgery_year"].trace_add("write", _on_year_write)
        self.vars["surgery_month"].trace_add(
            "write",
            lambda *a: _on_month_day_write(self.vars["surgery_month"], day_entry),
        )
        self.vars["surgery_day"].trace_add(
            "write", lambda *a: _on_month_day_write(self.vars["surgery_day"], w_entry)
        )
        self.vars["surgery_room_w"].trace_add("write", _on_w_room_write)
        self.vars["surgery_room_r"].trace_add(
            "write",
            lambda *a: _on_month_day_write(
                self.vars["surgery_room_r"], professor_entry
            ),
        )

        month_entry.bind(
            "<FocusOut>", lambda *a: _pad_with_zero(self.vars["surgery_month"])
        )
        day_entry.bind(
            "<FocusOut>", lambda *a: _pad_with_zero(self.vars["surgery_day"])
        )
        r_entry.bind(
            "<FocusOut>", lambda *a: _pad_with_zero(self.vars["surgery_room_r"])
        )

        # --- (이하 나머지 위젯 생성 코드는 기존과 동일) ---
        def validate_number(char):
            return char.isdigit()

        vcmd = (self.frame.register(validate_number), "%S")
        year_entry.config(validate="key", validatecommand=vcmd)
        month_entry.config(validate="key", validatecommand=vcmd)
        day_entry.config(validate="key", validatecommand=vcmd)
        w_entry.config(validate="key", validatecommand=vcmd)
        r_entry.config(validate="key", validatecommand=vcmd)

        self._add_grid_row("담당 교수", professor_entry, 2)  # 위에서 생성한 위젯을 배치
        self._add_grid_row(
            "수술명", ttk.Entry(self.frame, textvariable=self.vars["surgery_name"]), 3
        )
        self._add_grid_row(
            "마취",
            ttk.Combobox(
                self.frame,
                textvariable=self.vars["anesthesia"],
                values=OPTIONS["anesthesia"],
            ),
            4,
        )
        op_side_combobox = ttk.Combobox(
            self.frame,
            textvariable=self.vars["op_side"],
            values=UPPER_OPTIONS["op_side"],
        )
        op_side_combobox.bind("<<ComboboxSelected>>", self.apply_autofill_callback)
        self._add_grid_row("Rt./Lt.", op_side_combobox, 5)
        op_site_combobox = ttk.Combobox(
            self.frame,
            textvariable=self.vars["op_site"],
            values=UPPER_OPTIONS["op_site"],
        )
        op_site_combobox.bind("<<ComboboxSelected>>", self.apply_autofill_callback)
        self._add_grid_row("수술 부위", op_site_combobox, 6)

    def _add_grid_row(self, label_text, widget, row_index):
        # 기본 padding
        pady_val = 3
        # 수술 부위는 아래 여백을 줄이기
        if label_text == "수술 부위":
            pady_val = (2, 0)
        label = ttk.Label(self.frame, text=label_text, anchor="w")
        label.grid(row=row_index, column=0, sticky="ew", padx=5, pady=pady_val)
        widget.grid(row=row_index, column=1, sticky="ew", padx=5, pady=pady_val)


class TLFormTab:
    def __init__(self, parent, vars_dict, apply_autofill_callback):
        self.vars = vars_dict
        self.apply_autofill_callback = apply_autofill_callback
        self.frame = ttk.Frame(parent)
        self.create_tl_form()

    def create_tl_form(self):
        self.frame.columnconfigure(1, weight=1)

        # --- 1. 수술 날짜 ---
        ttk.Label(self.frame, text="수술 날짜", anchor="w").grid(
            row=0, column=0, sticky="ew", padx=5, pady=3
        )
        date_entry_frame = ttk.Frame(self.frame)
        date_entry_frame.grid(row=0, column=1, sticky="ew", padx=5, pady=3)
        date_entry_frame.columnconfigure(0, weight=1)
        year_entry = ttk.Entry(
            date_entry_frame, textvariable=self.vars["surgery_year"], width=6
        )
        year_entry.grid(row=0, column=1, padx=(0, 2))
        ttk.Label(date_entry_frame, text="년").grid(row=0, column=2)
        month_entry = ttk.Entry(
            date_entry_frame, textvariable=self.vars["surgery_month"], width=4
        )
        month_entry.grid(row=0, column=3, padx=(5, 2))
        ttk.Label(date_entry_frame, text="월").grid(row=0, column=4)
        day_entry = ttk.Entry(
            date_entry_frame, textvariable=self.vars["surgery_day"], width=4
        )
        day_entry.grid(row=0, column=5, padx=(5, 2))
        ttk.Label(date_entry_frame, text="일").grid(row=0, column=6)

        # --- 2. 수술실 ---
        ttk.Label(self.frame, text="수술실", anchor="w").grid(
            row=1, column=0, sticky="ew", padx=5, pady=3
        )
        room_entry_frame = ttk.Frame(self.frame)
        room_entry_frame.grid(row=1, column=1, sticky="ew", padx=5, pady=3)
        room_entry_frame.columnconfigure(0, weight=1)
        ttk.Label(room_entry_frame, text="(").grid(row=0, column=1)
        w_entry = ttk.Entry(
            room_entry_frame, textvariable=self.vars["surgery_room_w"], width=3
        )
        w_entry.grid(row=0, column=2, padx=2)
        ttk.Label(room_entry_frame, text=")W-(").grid(row=0, column=3)
        r_entry = ttk.Entry(
            room_entry_frame, textvariable=self.vars["surgery_room_r"], width=3
        )
        r_entry.grid(row=0, column=4, padx=2)
        ttk.Label(room_entry_frame, text=")R").grid(row=0, column=5)

        # --- 3. 다음 포커스 대상 위젯 생성 ---
        professor_combobox = ttk.Combobox(
            self.frame,
            textvariable=self.vars["professor_name"],
            values=TL_OPTIONS["professor"],
        )
        professor_combobox.bind("<<ComboboxSelected>>", self.apply_autofill_callback)

        # --- [핵심 수정] 스마트 입력 기능을 위한 콜백 함수 및 바인딩 ---
        def _on_year_write(*args):
            if len(self.vars["surgery_year"].get()) == 2:
                self.vars["surgery_year"].set("20" + self.vars["surgery_year"].get())
                month_entry.focus_set()
                month_entry.select_range(0, "end")

        def _on_month_day_write(var, next_widget):
            if len(var.get()) == 2:
                next_widget.focus_set()
                next_widget.select_range(0, "end")

        def _pad_with_zero(var):
            if len(var.get()) == 1 and var.get().isdigit():
                var.set("0" + var.get())

        def _on_w_room_write(*args):
            if len(self.vars["surgery_room_w"].get()) == 1:
                r_entry.focus_set()
                r_entry.select_range(0, "end")

        # 변수 변경 감지자 및 포커스 아웃 이벤트 연결
        self.vars["surgery_year"].trace_add("write", _on_year_write)
        self.vars["surgery_month"].trace_add(
            "write",
            lambda *a: _on_month_day_write(self.vars["surgery_month"], day_entry),
        )
        self.vars["surgery_day"].trace_add(
            "write", lambda *a: _on_month_day_write(self.vars["surgery_day"], w_entry)
        )
        self.vars["surgery_room_w"].trace_add("write", _on_w_room_write)
        self.vars["surgery_room_r"].trace_add(
            "write",
            lambda *a: _on_month_day_write(
                self.vars["surgery_room_r"], professor_combobox
            ),
        )

        month_entry.bind(
            "<FocusOut>", lambda *a: _pad_with_zero(self.vars["surgery_month"])
        )
        day_entry.bind(
            "<FocusOut>", lambda *a: _pad_with_zero(self.vars["surgery_day"])
        )
        r_entry.bind(
            "<FocusOut>", lambda *a: _pad_with_zero(self.vars["surgery_room_r"])
        )

        # --- (이하 나머지 위젯 생성 코드는 기존과 동일) ---
        def validate_number(char):
            return char.isdigit()

        vcmd = (self.frame.register(validate_number), "%S")
        year_entry.config(validate="key", validatecommand=vcmd)
        month_entry.config(validate="key", validatecommand=vcmd)
        day_entry.config(validate="key", validatecommand=vcmd)
        w_entry.config(validate="key", validatecommand=vcmd)
        r_entry.config(validate="key", validatecommand=vcmd)

        self._add_grid_row("담당 교수", professor_combobox, 2)
        surgery_name_combobox = ttk.Combobox(
            self.frame,
            textvariable=self.vars["surgery_name"],
            values=TL_OPTIONS["op_name_special"],
        )
        surgery_name_combobox.bind("<<ComboboxSelected>>", self.apply_autofill_callback)
        self._add_grid_row("수술명", surgery_name_combobox, 3)
        self._add_grid_row(
            "마취",
            ttk.Combobox(
                self.frame,
                textvariable=self.vars["anesthesia"],
                values=OPTIONS["anesthesia"],
            ),
            4,
        )
        spine_region_combobox = ttk.Combobox(
            self.frame,
            textvariable=self.vars["spine_region"],
            values=TL_OPTIONS["spine_region"],
        )
        spine_region_combobox.bind("<<ComboboxSelected>>", self.apply_autofill_callback)
        self._add_grid_row("척추 부위", spine_region_combobox, 5)
        approach_combobox = ttk.Combobox(
            self.frame,
            textvariable=self.vars["approach"],
            values=TL_OPTIONS["approach"],
        )
        approach_combobox.bind("<<ComboboxSelected>>", self.apply_autofill_callback)
        self._add_grid_row("접근법", approach_combobox, 6)
        level_count_combobox = ttk.Combobox(
            self.frame,
            textvariable=self.vars["level_count"],
            values=TL_OPTIONS["level_count"],
        )
        level_count_combobox.bind("<<ComboboxSelected>>", self.apply_autofill_callback)
        self._add_grid_row("Level 개수", level_count_combobox, 7)

    def _add_grid_row(self, label_text, widget, row_index):
        label = ttk.Label(self.frame, text=label_text, anchor="w")
        label.grid(row=row_index, column=0, sticky="ew", padx=5, pady=3)
        widget.grid(row=row_index, column=1, sticky="ew", padx=5, pady=3)


class FootFormTab:
    def __init__(self, parent, vars_dict, apply_autofill_callback):
        self.vars = vars_dict
        self.apply_autofill_callback = apply_autofill_callback
        self.frame = ttk.Frame(parent)
        self.create_foot_form()
        # self.frame.configure(height=180)

    def create_foot_form(self):
        self.frame.columnconfigure(1, weight=1)

        # --- 1. 수술 날짜 ---
        ttk.Label(self.frame, text="수술 날짜", anchor="w").grid(
            row=0, column=0, sticky="ew", padx=5, pady=3
        )
        date_entry_frame = ttk.Frame(self.frame)
        date_entry_frame.grid(row=0, column=1, sticky="ew", padx=5, pady=3)
        date_entry_frame.columnconfigure(0, weight=1)
        year_entry = ttk.Entry(
            date_entry_frame, textvariable=self.vars["surgery_year"], width=6
        )
        year_entry.grid(row=0, column=1, padx=(0, 2))
        ttk.Label(date_entry_frame, text="년").grid(row=0, column=2)
        month_entry = ttk.Entry(
            date_entry_frame, textvariable=self.vars["surgery_month"], width=4
        )
        month_entry.grid(row=0, column=3, padx=(5, 2))
        ttk.Label(date_entry_frame, text="월").grid(row=0, column=4)
        day_entry = ttk.Entry(
            date_entry_frame, textvariable=self.vars["surgery_day"], width=4
        )
        day_entry.grid(row=0, column=5, padx=(5, 2))
        ttk.Label(date_entry_frame, text="일").grid(row=0, column=6)

        # --- 2. 수술실 ---
        ttk.Label(self.frame, text="수술실", anchor="w").grid(
            row=1, column=0, sticky="ew", padx=5, pady=3
        )
        room_entry_frame = ttk.Frame(self.frame)
        room_entry_frame.grid(row=1, column=1, sticky="ew", padx=5, pady=3)
        room_entry_frame.columnconfigure(0, weight=1)
        ttk.Label(room_entry_frame, text="(").grid(row=0, column=1)
        w_entry = ttk.Entry(
            room_entry_frame, textvariable=self.vars["surgery_room_w"], width=3
        )
        w_entry.grid(row=0, column=2, padx=2)
        ttk.Label(room_entry_frame, text=")W-(").grid(row=0, column=3)
        r_entry = ttk.Entry(
            room_entry_frame, textvariable=self.vars["surgery_room_r"], width=3
        )
        r_entry.grid(row=0, column=4, padx=2)
        ttk.Label(room_entry_frame, text=")R").grid(row=0, column=5)

        # --- 3. 다음 포커스 대상 위젯 생성 ---
        professor_entry = ttk.Entry(
            self.frame, textvariable=self.vars["professor_name"]
        )

        # --- [핵심 수정] 스마트 입력 기능을 위한 콜백 함수 및 바인딩 ---
        def _on_year_write(*args):
            if len(self.vars["surgery_year"].get()) == 2:
                self.vars["surgery_year"].set("20" + self.vars["surgery_year"].get())
                month_entry.focus_set()
                month_entry.select_range(0, "end")

        def _on_month_day_write(var, next_widget):
            if len(var.get()) == 2:
                next_widget.focus_set()
                next_widget.select_range(0, "end")

        def _pad_with_zero(var):
            if len(var.get()) == 1 and var.get().isdigit():
                var.set("0" + var.get())

        def _on_w_room_write(*args):
            if len(self.vars["surgery_room_w"].get()) == 1:
                r_entry.focus_set()
                r_entry.select_range(0, "end")

        # 변수 변경 감지자 및 포커스 아웃 이벤트 연결
        self.vars["surgery_year"].trace_add("write", _on_year_write)
        self.vars["surgery_month"].trace_add(
            "write",
            lambda *a: _on_month_day_write(self.vars["surgery_month"], day_entry),
        )
        self.vars["surgery_day"].trace_add(
            "write", lambda *a: _on_month_day_write(self.vars["surgery_day"], w_entry)
        )
        self.vars["surgery_room_w"].trace_add("write", _on_w_room_write)
        self.vars["surgery_room_r"].trace_add(
            "write",
            lambda *a: _on_month_day_write(
                self.vars["surgery_room_r"], professor_entry
            ),
        )

        month_entry.bind(
            "<FocusOut>", lambda *a: _pad_with_zero(self.vars["surgery_month"])
        )
        day_entry.bind(
            "<FocusOut>", lambda *a: _pad_with_zero(self.vars["surgery_day"])
        )
        r_entry.bind(
            "<FocusOut>", lambda *a: _pad_with_zero(self.vars["surgery_room_r"])
        )

        # --- (이하 나머지 위젯 생성 코드는 기존과 동일) ---
        def validate_number(char):
            return char.isdigit()

        vcmd = (self.frame.register(validate_number), "%S")
        year_entry.config(validate="key", validatecommand=vcmd)
        month_entry.config(validate="key", validatecommand=vcmd)
        day_entry.config(validate="key", validatecommand=vcmd)
        w_entry.config(validate="key", validatecommand=vcmd)
        r_entry.config(validate="key", validatecommand=vcmd)

        self._add_grid_row("담당 교수", professor_entry, 2)
        self._add_grid_row(
            "수술명", ttk.Entry(self.frame, textvariable=self.vars["surgery_name"]), 3
        )
        self._add_grid_row(
            "마취",
            ttk.Combobox(
                self.frame,
                textvariable=self.vars["anesthesia"],
                values=OPTIONS["anesthesia"],
            ),
            4,
        )
        op_side_combobox = ttk.Combobox(
            self.frame,
            textvariable=self.vars["op_side"],
            values=FOOT_OPTIONS["op_side"],
        )
        op_side_combobox.bind("<<ComboboxSelected>>", self.apply_autofill_callback)
        self._add_grid_row("Rt./Lt.", op_side_combobox, 5)
        op_site_combobox = ttk.Combobox(
            self.frame,
            textvariable=self.vars["op_site"],
            values=FOOT_OPTIONS["op_site"],
        )
        op_site_combobox.bind("<<ComboboxSelected>>", self.apply_autofill_callback)
        self._add_grid_row("수술 부위", op_site_combobox, 6)

    def _add_grid_row(self, label_text, widget, row_index):
        # 기본 padding
        pady_val = 3
        if label_text == "수술 부위":
            pady_val = (2, 0)
        label = ttk.Label(self.frame, text=label_text, anchor="w")
        label.grid(row=row_index, column=0, sticky="ew", padx=5, pady=pady_val)
        widget.grid(row=row_index, column=1, sticky="ew", padx=5, pady=pady_val)


class PrecautionsPanel:
    def __init__(self, parent, on_text_change_callback):
        self.frame = ttk.LabelFrame(parent, text="※ 주의사항")
        self.on_text_change_callback = on_text_change_callback
        self.current_tab = "Upper"
        self.precautions_data = data_manager.load_precautions_data()
        self.create_panel()

    def create_panel(self):
        toolbar_frame = ttk.Frame(self.frame)
        toolbar_frame.pack(fill="x", padx=5, pady=(5, 0))
        self.edit_button = ttk.Button(
            toolbar_frame, text="편집", command=self.enter_edit_mode
        )  # [수정] 함수 연결 변경
        self.edit_button.pack(side="left", padx=(0, 5))
        self.save_button = ttk.Button(
            toolbar_frame, text="저장", command=self.save_precautions, state="disabled"
        )
        self.save_button.pack(side="left", padx=(0, 5))
        self.cancel_button = ttk.Button(
            toolbar_frame, text="취소", command=self.cancel_edit_mode, state="disabled"
        )  # [추가] 취소 버튼
        self.cancel_button.pack(side="left", padx=(0, 10))
        ttk.Button(toolbar_frame, text="굵게", command=self.toggle_bold).pack(
            side="left", padx=1
        )
        ttk.Button(toolbar_frame, text="색상", command=self.apply_color).pack(
            side="left", padx=1
        )
        ttk.Button(
            toolbar_frame, text="크게", command=lambda: self.change_font_size(1)
        ).pack(side="left", padx=1)
        ttk.Button(
            toolbar_frame, text="작게", command=lambda: self.change_font_size(-1)
        ).pack(side="left", padx=1)
        self.notes_text = tk.Text(self.frame, wrap="word", undo=True)
        self.notes_text.pack(fill="both", expand=True, padx=5, pady=5)
        self.font_sizes = [10, 12, 14, 16, 18, 20, 24]
        try:
            default_font = font.Font(font=self.notes_text["font"])
            self.default_font_family = default_font.actual("family")
        except tk.TclError:
            self.default_font_family = "Malgun Gothic"
        self.notes_text.config(font=(self.default_font_family, 16))
        bold_font = font.Font(family=self.default_font_family, size=16, weight="bold")
        self.notes_text.tag_configure("bold", font=bold_font)
        for size in self.font_sizes:
            self.notes_text.tag_configure(
                f"size_{size}", font=(self.default_font_family, size)
            )
        self.is_edit_mode = False
        self.notes_text.config(state="disabled")
        self.update_precautions_display()

    # --- [수정] 편집 모드 진입/취소/저장 함수를 명확하게 분리 ---
    def enter_edit_mode(self):
        """편집 모드로 진입합니다."""
        self.is_edit_mode = True
        self.notes_text.config(state="normal")
        self.edit_button.config(state="disabled")
        self.save_button.config(state="normal")
        self.cancel_button.config(state="normal")

    def cancel_edit_mode(self):
        """편집을 취소하고 원래 상태로 복구합니다."""
        self.is_edit_mode = False
        self.notes_text.config(state="disabled")
        self.edit_button.config(state="normal", text="편집")
        self.save_button.config(state="disabled")
        self.cancel_button.config(state="disabled")
        # 파일에서 데이터를 다시 로드하여 수정 중이던 내용을 되돌립니다.
        self.precautions_data = data_manager.load_precautions_data()
        self.update_precautions_display()

    def save_precautions(self):
        """편집 내용을 저장하고 편집 모드를 종료합니다."""
        try:
            dump_data = self.notes_text.dump("1.0", "end-1c", tag=True, text=True)
            self.precautions_data[self.current_tab] = dump_data
            data_manager.save_precautions_data(self.precautions_data)

            # 수동으로 편집 모드 종료 (데이터 다시 로드 안 함)
            self.is_edit_mode = False
            self.notes_text.config(state="disabled")
            self.edit_button.config(state="normal", text="편집")
            self.save_button.config(state="disabled")
            self.cancel_button.config(state="disabled")

            messagebox.showinfo("저장 완료", "주의사항이 성공적으로 저장되었습니다.")
        except Exception as e:
            messagebox.showerror(
                "저장 오류", f"주의사항 저장 중 오류가 발생했습니다:\n{e}"
            )

    # --- (이하 다른 함수들은 기존과 거의 동일) ---
    def toggle_bold(self):
        try:
            (
                self.notes_text.tag_add("bold", "sel.first", "sel.last")
                if "bold" not in self.notes_text.tag_names("sel.first")
                else self.notes_text.tag_remove("bold", "sel.first", "sel.last")
            )
        except tk.TclError:
            pass

    def apply_color(self):
        try:
            color = colorchooser.askcolor()
            if color and color[1]:
                color_tag = f"fg_{color[1]}"
                self.notes_text.tag_configure(color_tag, foreground=color[1])
                self.notes_text.tag_add(color_tag, "sel.first", "sel.last")
        except tk.TclError:
            pass

    def change_font_size(self, direction):
        try:
            current_tags = self.notes_text.tag_names("sel.first")
            current_size = 16
            for tag in current_tags:
                if tag.startswith("size_"):
                    current_size = int(tag.split("_")[1])
                    self.notes_text.tag_remove(tag, "sel.first", "sel.last")
                    break
            try:
                new_size = self.font_sizes[
                    max(
                        0,
                        min(
                            len(self.font_sizes) - 1,
                            self.font_sizes.index(current_size) + direction,
                        ),
                    )
                ]
            except ValueError:
                new_size = 16
            self.notes_text.tag_add(f"size_{new_size}", "sel.first", "sel.last")
        except tk.TclError:
            pass

    def set_tab(self, tab_name):
        self.current_tab = tab_name
        self.update_precautions_display()

    def update_precautions_display(self):
        current_state = self.notes_text.cget("state")
        if current_state == "disabled":
            self.notes_text.config(state="normal")
        self.notes_text.delete("1.0", "end")
        content = self.precautions_data.get(self.current_tab, [["text", "", "1.0"]])
        if not content:
            content = [["text", "", "1.0"]]
        for item in content:
            if isinstance(item, (list, tuple)) and len(item) >= 3:
                key, value, index = item
                if key == "tagon":
                    self.notes_text.tag_add(value, index)
                elif key == "tagoff":
                    self.notes_text.tag_remove(value, index)
                elif key == "text":
                    self.notes_text.insert(index, value)
                elif key == "mark":
                    self.notes_text.mark_set(value, index)
        if not self.is_edit_mode:
            self.notes_text.config(state="disabled")


class SurgeryListPanel:
    def __init__(self, parent, on_select_callback):
        self.frame = ttk.LabelFrame(parent, text="수술 목록")
        self.on_select_callback = on_select_callback
        self.create_panel()

    def create_panel(self):
        columns = ("id", "surgery_date", "surgery_name", "professor_name", "brace")

        # [수정] 수직/수평 스크롤바를 담을 프레임을 먼저 생성합니다.
        tree_frame = ttk.Frame(self.frame)
        tree_frame.pack(fill="both", expand=True)

        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings")

        self.tree.heading("id", text="ID")
        self.tree.column(
            "id", width=40, anchor="center", stretch=tk.NO
        )  # stretch=NO로 너비 고정

        self.tree.heading("surgery_date", text="수술일")
        self.tree.column("surgery_date", width=100, anchor="center", stretch=tk.NO)

        self.tree.heading("surgery_name", text="수술명")
        self.tree.column("surgery_name", width=200)  # 너비가 변하는 기준 컬럼

        self.tree.heading("professor_name", text="담당교수")
        self.tree.column("professor_name", width=100, anchor="center", stretch=tk.NO)

        self.tree.heading("brace", text="보조기")
        self.tree.column("brace", width=250)  # 보조기 컬럼 너비를 조금 더 넓게 설정

        # --- [수정] 스크롤바 배치 방식 변경 ---
        # 수직 스크롤바
        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        # [추가] 수평 스크롤바
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.tree.xview)

        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        # grid를 사용하여 Treeview와 스크롤바를 배치
        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")

        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

        self.tree.bind("<<TreeviewSelect>>", self.on_select_callback)

    def load_tickets(self, tickets):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for ticket in tickets:
            # --- 수정된 부분 3: values 튜플에 'brace' 데이터 추가 ---
            self.tree.insert(
                "",
                "end",
                values=(
                    ticket.get("id"),
                    ticket.get("surgery_date"),
                    ticket.get("surgery_name"),
                    ticket.get("professor_name"),
                    ticket.get("brace"),  # 보조기 데이터 추가
                ),
            )

    def get_selected_id(self):
        selected_items = self.tree.selection()
        if selected_items:
            return self.tree.item(selected_items[0], "values")[0]
        return None

    def clear_selection(self):
        if self.tree.selection():
            self.tree.selection_remove(self.tree.selection()[0])
