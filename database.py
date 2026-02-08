# database.py 파일

import sqlite3
import json

DB_NAME = "surgery_op_ticket.db"


def create_table():
    """
    데이터베이스에 연결하고 모든 필드가 포함된 'tickets' 테이블을 생성/수정하는 함수.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # --- 수정된 부분: 모든 컬럼을 CREATE TABLE 문에 추가 ---
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS tickets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        surgery_date TEXT NOT NULL,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        surgery_name TEXT,
        surgery_type TEXT DEFAULT 'Upper',
        anesthesia TEXT,
        op_side TEXT,
        op_site TEXT,
        clothing TEXT,
        brace TEXT,
        shaving_status TEXT,
        op_marking TEXT,
        npo_status TEXT,
        pre_ru_status TEXT,
        pre_ru_result TEXT,
        ast_result TEXT,
        ast_site TEXT,
        enema_status TEXT,
        enema_details TEXT,
        supplies TEXT,
        antibiotics TEXT,
        iv_line TEXT,
        id_bracelet TEXT,
        professor_name TEXT,
        memo TEXT,
        surgery_room_w TEXT,
        surgery_room_r TEXT,
        supplies2 TEXT,
        foleys_cath TEXT,
        spine_region TEXT,
        approach TEXT,
        level_count TEXT
    );
    """
    cursor.execute(create_table_sql)

    # --- 수정된 부분: 컬럼 추가 로직을 더 체계적으로 변경 ---

    # 추가할 컬럼과 타입을 딕셔너리로 정의
    columns_to_add = {
        "surgery_type": "TEXT DEFAULT 'Upper'",
        "surgery_room_w": "TEXT",
        "surgery_room_r": "TEXT",
        "supplies2": "TEXT",
        "foleys_cath": "TEXT",
        "spine_region": "TEXT",
        "approach": "TEXT",
        "level_count": "TEXT",
    }

    for col_name, col_type in columns_to_add.items():
        try:
            cursor.execute(f"ALTER TABLE tickets ADD COLUMN {col_name} {col_type}")
            print(f"'{col_name}' 컬럼이 기존 테이블에 추가되었습니다.")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e).lower():
                print(f"'{col_name}' 컬럼이 이미 존재합니다.")
            else:
                print(f"'{col_name}' 컬럼 추가 중 오류 발생: {e}")

    conn.commit()
    conn.close()

    print(
        f"'{DB_NAME}' 데이터베이스 및 수정된 'tickets' 테이블이 성공적으로 준비되었습니다."
    )


# --- CRUD 함수들 ---


def add_ticket(ticket_data):
    """
    새로운 수술 준비 티켓 데이터를 DB에 추가합니다.
    ticket_data는 딕셔너리 형태여야 합니다.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # surgery_type이 없으면 기본값 설정
    if "surgery_type" not in ticket_data:
        ticket_data["surgery_type"] = "Upper"

    columns = ", ".join(ticket_data.keys())
    placeholders = ", ".join("?" for _ in ticket_data)

    sql = f"INSERT INTO tickets ({columns}) VALUES ({placeholders})"

    data_values = []
    for value in ticket_data.values():
        if isinstance(value, list) or isinstance(value, dict):
            data_values.append(json.dumps(value))
        else:
            data_values.append(value)

    cursor.execute(sql, tuple(data_values))
    conn.commit()
    last_id = cursor.lastrowid
    conn.close()
    print("새로운 티켓이 성공적으로 추가되었습니다.")
    return last_id


def get_all_tickets():
    """모든 티켓 데이터를 조회합니다."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tickets ORDER BY surgery_date DESC, id DESC")
    tickets = cursor.fetchall()
    conn.close()

    result = []
    for row in tickets:
        ticket = dict(row)
        # surgery_type이 없는 기존 데이터의 경우 기본값 설정
        if "surgery_type" not in ticket or ticket["surgery_type"] is None:
            ticket["surgery_type"] = "Upper"
        result.append(ticket)

    return result


def get_tickets_by_date(date_str):
    """특정 날짜의 티켓 데이터를 조회합니다."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM tickets WHERE surgery_date = ? ORDER BY created_at DESC",
        (date_str,),
    )
    tickets = cursor.fetchall()
    conn.close()

    result = []
    for row in tickets:
        ticket = dict(row)
        # surgery_type이 없는 기존 데이터의 경우 기본값 설정
        if "surgery_type" not in ticket or ticket["surgery_type"] is None:
            ticket["surgery_type"] = "Upper"
        result.append(ticket)

    return result


def get_tickets_by_surgery_type(surgery_type):
    """특정 수술 타입의 티켓 데이터를 조회합니다."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM tickets WHERE surgery_type = ? ORDER BY surgery_date DESC, id DESC",
        (surgery_type,),
    )
    tickets = cursor.fetchall()
    conn.close()
    return [dict(row) for row in tickets]


def update_ticket(ticket_id, ticket_data):
    """특정 ID의 티켓 데이터를 수정합니다."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # surgery_type이 없으면 기본값 설정
    if "surgery_type" not in ticket_data:
        ticket_data["surgery_type"] = "Upper"

    set_clause = ", ".join(f"{key} = ?" for key in ticket_data)

    sql = f"UPDATE tickets SET {set_clause} WHERE id = ?"

    data_values = []
    for value in ticket_data.values():
        if isinstance(value, list) or isinstance(value, dict):
            data_values.append(json.dumps(value))
        else:
            data_values.append(value)

    params = tuple(data_values) + (ticket_id,)

    cursor.execute(sql, params)
    conn.commit()
    conn.close()
    print(f"티켓 ID {ticket_id}가 성공적으로 수정되었습니다.")


def delete_ticket(ticket_id):
    """특정 ID의 티켓 데이터를 삭제합니다."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM tickets WHERE id = ?", (ticket_id,))
    conn.commit()
    conn.close()
    print(f"티켓 ID {ticket_id}가 성공적으로 삭제되었습니다.")


def update_existing_records_surgery_type():
    """기존 레코드들의 surgery_type을 'Upper'로 업데이트합니다."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    try:
        cursor.execute(
            "UPDATE tickets SET surgery_type = 'Upper' WHERE surgery_type IS NULL"
        )
        updated_count = cursor.rowcount
        conn.commit()
        print(
            f"{updated_count}개의 기존 레코드에 surgery_type='Upper'가 설정되었습니다."
        )
    except sqlite3.OperationalError as e:
        print(f"업데이트 중 오류 발생: {e}")

    conn.close()


# 이 파일이 직접 실행될 때만 create_table() 함수를 호출합니다.
if __name__ == "__main__":
    create_table()
    update_existing_records_surgery_type()
    # 테스트 코드는 여기에서 실행할 수 있습니다.
    # 예: print(get_all_tickets())
