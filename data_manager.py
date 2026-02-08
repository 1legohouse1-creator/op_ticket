# data_manager.py

import json
import os
from constants import PRECAUTIONS

DATA_FILE = "precautions_data.json"


def load_precautions_data():
    """JSON 파일에서 주의사항 서식 데이터를 불러옵니다."""
    # [핵심 수정] 파일이 존재하지 않을 때만 기본값으로 새로 생성합니다.
    if not os.path.exists(DATA_FILE):
        print(f"'{DATA_FILE}' 파일이 없어 기본값으로 새로 생성합니다.")
        default_data = {}
        for key, value in PRECAUTIONS.items():
            # 기본 텍스트를 Text 위젯 dump 형식으로 변환
            default_data[key] = [["text", value, "1.0"]]
        save_precautions_data(default_data)
        return default_data

    # 파일이 존재하면, 내용을 읽어서 반환합니다.
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            # 파일이 비어있는 경우를 대비
            content = f.read()
            if not content:
                raise json.JSONDecodeError("파일이 비어있습니다.", "", 0)
            return json.loads(content)
    except json.JSONDecodeError as e:
        print(f"'{DATA_FILE}' 파일 분석 오류: {e}. 파일을 기본값으로 재생성합니다.")
        # 파일이 깨졌을 경우에도 기본값으로 재생성
        os.remove(DATA_FILE)  # 손상된 파일 삭제
        return load_precautions_data()  # 재귀 호출로 다시 생성


def save_precautions_data(data):
    """주의사항 서식 데이터를 JSON 파일에 저장합니다."""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
