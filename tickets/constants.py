# constants.py

# 공통 옵션들
OPTIONS = {
    'anesthesia': ['G-OP', 'L-OP', ''], 
    'clothing': ['반팔', '긴팔'], 
    'npo_status': ['O', 'X', '해당 없음'], 
    'ast_result': ['Negative', 'Positive', '해당 없음'],
    'enema_status': ['O', 'X', '해당 없음'], 
    'id_bracelet': ['Rt.arm', 'Lt.arm', '다리', '착용 완료', '해당 없음'],
    'foleys_cath': ['O', 'X'],
}

# Upper 탭 전용 옵션
UPPER_OPTIONS = {
    'op_side': ['Rt.', 'Lt.', 'Both'],
    'op_site': ['Humerus', 'Radius & Ulnar', 'Wrist & Finger', 'Shoulder & Clavicle'],
    'shaving_status': ['Rt.Axillary 이하', 'Lt.Axillary 이하', 'Both Axillary 이하', '필요 없음'],
}

# T&L 탭 전용 옵션
TL_OPTIONS = {
    'spine_region': ['C', 'T&L'],
    'approach': ['Anterior', 'Posterior'],
    'level_count': ['Level 1개', 'Level 2개 이상'],
    'professor': ['서형연', '김성규'],
    'op_name_special': ['ACDF', 'OLIF',''],
    'shaving_status': ['턱수염', '뒷머리', '안함'],
}

# Foot 탭 전용 옵션
FOOT_OPTIONS = {
    'op_side': ['Rt.', 'Lt.', 'Both'],
    'op_site': ['Femur', 'Knee & Tibia, Fibula', 'Ankle & Toes'],
    'shaving_status': ['Rt.ingunal 이하', 'Lt.ingunal 이하', 'Both ingunal 이하', 'Rt.thigh 이하', 'Lt.thigh 이하', 'Both thigh 이하', 'Rt.knee 이하', 'Lt.knee 이하', 'Both knee 이하'],
}

# --- 엑셀의 VLOOKUP 테이블 역할 (새로운 규칙 적용) ---
AUTO_FILL_RULES = {
    # --- Upper Part Rules ---
    # --- 1행 규칙: ('Rt.', 'Humerus') ---
    ('Rt.', 'Humerus'): {
        'shaving_status': 'Rt.Axillary 이하',
        'op_marking': 'Rt.손등',
        'brace': 'Arm sling',
        'supplies': '솜 베개 2개, 요기, 얼음판',
        'id_bracelet': 'Lt.arm',
        'ast_site': 'Lt.arm',
        'clothing' : '반팔',
    },
    # --- 2행 규칙: ('Lt.', 'Humerus') ---
    ('Lt.', 'Humerus'): {
        'shaving_status': 'Lt.Axillary 이하',
        'op_marking': 'Lt.손등',
        'brace': 'Arm sling',
        'supplies': '솜 베개 2개, 요기, 얼음판',
        'id_bracelet': 'Rt.arm',
        'ast_site': 'Rt.arm',
        'clothing' : '반팔',
    },
    # --- 3행 규칙: ('Both', 'Humerus') ---
    ('Both', 'Humerus'): {
        'shaving_status': 'Both Axillary 이하',
        'op_marking': 'Both 손등',
        'brace': 'Arm sling',
        'supplies': '솜 베개 4개, 요기, 얼음판',
        'id_bracelet': '다리',
        'ast_site': '다리',
        'clothing' : '반팔',
    },
    # --- 4행 규칙: ('Lt.', 'Radius & Ulnar') ---
    ('Lt.', 'Radius & Ulnar'): {
        'shaving_status': 'Lt.Axillary 이하',
        'op_marking': 'Lt.Humerus',
        'brace': 'Arm sling 혹은 L-sling 혹은 Abduction brace',
        'supplies': '솜베개 2개, 요기, 얼음판',
        'id_bracelet': 'Rt.arm',
        'ast_site': 'Rt.arm',
        'clothing' : '반팔',
    },
    # --- 5행 규칙: ('Rt.', 'Radius & Ulnar') ---
    ('Rt.', 'Radius & Ulnar'): {
        'shaving_status': 'Rt.Axillary 이하',
        'op_marking': 'Rt.Humerus',
        'brace': 'Arm sling 혹은 L-sling 혹은 Abduction brace',
        'supplies': '솜베개 2개, 요기, 얼음판',
        'id_bracelet': 'Lt.arm',
        'ast_site': 'Lt.arm',
        'clothing' : '반팔',
    },
    # --- 6행 규칙: ('Both', 'Radius & Ulnar') ---
    ('Both', 'Radius & Ulnar'): {
        'shaving_status': 'Both Axillary 이하',
        'op_marking': 'Both Humerus',
        'brace': 'Arm sling 혹은 L-sling 혹은 Abduction brace',
        'supplies': '솜베개 4개, 요기, 얼음판',
        'id_bracelet': '다리',
        'ast_site': '다리',
        'clothing' : '반팔',
    },
    # --- 7행 규칙: ('Rt.', 'Wrist & Finger') ---
    ('Rt.', 'Wrist & Finger'): {
        'shaving_status': 'Rt.Axillary 이하',
        'op_marking': 'Rt.Elbow lateral',
        'brace': 'Arm sling 혹은 L-sling 혹은 Abduction brace',
        'supplies': '솜베개 2개, 요기, 얼음판',
        'id_bracelet': 'Lt.arm',
        'ast_site': 'Lt.arm',
        'clothing' : '반팔',
    },
    # --- 8행 규칙: ('Lt.', 'Wrist & Finger') ---
    ('Lt.', 'Wrist & Finger'): {
        'shaving_status': 'Lt.Axillary 이하',
        'op_marking': 'Lt.Elbow lateral',
        'brace': 'Arm sling 혹은 L-sling 혹은 Abduction brace',
        'supplies': '솜베개 2개, 요기, 얼음판',
        'id_bracelet': 'Rt.arm',
        'ast_site': 'Rt.arm',
        'clothing' : '반팔',
    },
    # --- 9행 규칙: ('Both', 'Wrist & Finger') ---
    ('Both', 'Wrist & Finger'): {
        'shaving_status': 'Both Axillary 이하',
        'op_marking': 'Both Elbow lateral',
        'brace': 'Arm sling 혹은 L-sling 혹은 Abduction brace',
        'supplies': '솜베개 4개, 요기, 얼음판',
        'id_bracelet': '다리',
        'ast_site': '다리',
        'clothing' : '반팔',
    },
    # --- 10행 규칙: ('Rt.', 'Shoulder & Clavicle') ---
    ('Rt.', 'Shoulder & Clavicle'): {
        'shaving_status': 'Rt.Axillary 이하',
        'op_marking': 'Rt.손등',
        'brace': 'Arm sling 혹은 L-sling 혹은 Abduction brace',
        'supplies': '솜베개 2개, 요기, 얼음판',
        'id_bracelet': 'Lt.arm',
        'ast_site': 'Lt.arm',
        'clothing' : '반팔',
    },
    # --- 11행 규칙: ('Lt.', 'Shoulder & Clavicle') ---
    ('Lt.', 'Shoulder & Clavicle'): {
        'shaving_status': 'Lt.Axillary 이하',
        'op_marking': 'Lt.손등',
        'brace': 'Arm sling 혹은 L-sling 혹은 Abduction brace',
        'supplies': '솜베개 2개, 요기, 얼음판',
        'id_bracelet': 'Rt.arm',
        'ast_site': 'Rt.arm',
        'clothing' : '반팔',
    },
    # --- 12행 규칙: ('Both', 'Shoulder & Clavicle') ---
    ('Both', 'Shoulder & Clavicle'): {
        'shaving_status': 'Both Axillary 이하',
        'op_marking': 'Both 손등',
        'brace': 'Arm sling 혹은 L-sling 혹은 Abduction brace',
        'supplies': '솜베개 4개, 요기, 얼음판',
        'id_bracelet': '다리',
        'ast_site': '다리',
        'clothing' : '반팔',
    },

    # --- Foot Part Rules ---
    # --- 13행 규칙: ('Rt.', 'Femur') ---
    ('Rt.', 'Femur'): {
        'shaving_status': 'Rt.ingunal 이하',
        'op_marking': 'Rt.발등',
        'supplies': '솜베개 4개, 요기, 얼음판, 메디터치 힐 2개',
        'id_bracelet': '손',
        'ast_site': '손',
        'clothing': '옆 트임 바지',
    },

    # --- 14행 규칙: ('Lt.', 'Femur') ---
    ('Lt.', 'Femur'): {
        'shaving_status': 'Lt.ingunal 이하',
        'op_marking': 'Lt.발등',
        'supplies': '솜베개 4개, 요기, 얼음판, 메디터치 힐 2개',
        'id_bracelet': '손',
        'ast_site': '손',
        'clothing': '옆 트임 바지',
    },

    # --- 15행 규칙: ('Both', 'Femur') ---
    ('Both', 'Femur'): {
        'shaving_status': 'Both ingunal 이하',
        'op_marking': 'Both 발등',
        'supplies': '솜베개 8개, 요기, 얼음판, 메디터치 힐 4개',
        'id_bracelet': '손',
        'ast_site': '손',
        'clothing': '양 트임 바지',
    },

    # --- 16행 규칙: ('Rt.', 'Knee & Tibia, Fibula') ---
    ('Rt.', 'Knee & Tibia, Fibula'): {
        'shaving_status': 'Rt.thigh 이하',
        'op_marking': 'Rt.thigh lateral (가능하면 proximal)',
        'supplies': '솜베개 4개, 요기, 얼음판, 메디터치 힐 2개',
        'id_bracelet': '손',
        'ast_site': '손',
        'clothing': '옆 트임 바지',
    },

    # --- 17행 규칙: ('Lt.', 'Knee & Tibia, Fibula') ---
    ('Lt.', 'Knee & Tibia, Fibula'): {
        'shaving_status': 'Lt.thigh 이하',
        'op_marking': 'Lt.thigh lateral (가능하면 proximal)',
        'supplies': '솜베개 4개, 요기, 얼음판, 메디터치 힐 2개',
        'id_bracelet': '손',
        'ast_site': '손',
        'clothing': '옆 트임 바지',
    },

    # --- 18행 규칙: ('Both', 'Knee & Tibia, Fibula') ---
    ('Both', 'Knee & Tibia, Fibula'): {
        'shaving_status': 'Both thigh 이하',
        'op_marking': 'Both thigh lateral (가능하면 proximal)',
        'supplies': '솜베개 8개, 요기, 얼음판, 메디터치 힐 4개',
        'id_bracelet': '손',
        'ast_site': '손',
        'clothing': '양 트임 바지',
    },

    # --- 19행 규칙: ('Rt.', 'Ankle & Toes') ---
    ('Rt.', 'Ankle & Toes'): {
        'shaving_status': 'Rt.knee 이하',
        'op_marking': 'Rt.mid Tibia',
        'supplies': '솜베개 4개, 요기, 얼음판, 메디터치 힐 2개',
        'id_bracelet': '손',
        'ast_site': '손',
        'clothing': '옆 트임 바지',
    },

    # --- 20행 규칙: ('Lt.', 'Ankle & Toes') ---
    ('Lt.', 'Ankle & Toes'): {
        'shaving_status': 'Lt.knee 이하',
        'op_marking': 'Lt.mid Tibia',
        'supplies': '솜베개 4개, 요기, 얼음판, 메디터치 힐 2개',
        'id_bracelet': '손',
        'ast_site': '손',
        'clothing': '옆 트임 바지',
    },

    # --- 21행 규칙: ('Both', 'Ankle & Toes') ---
    ('Both', 'Ankle & Toes'): {
        'shaving_status': 'Both knee 이하',
        'op_marking': 'Both mid Tibia',
        'supplies': '솜베개 8개, 요기, 얼음판, 메디터치 힐 4개',
        'id_bracelet': '손',
        'ast_site': '손',
        'clothing': '양 트임 바지',
    },

     ############################################ --- T&L Part Rules --- ####################################################

    # --- 22행 규칙: ('C', 'Anterior', 'Level 1개', '서형연') ---
    ('C', 'Anterior', 'Level 1개', '서형연'): {
        'shaving_status': '턱수염',
        'op_marking': 'Nipple 사이 Level 기입',
        'brace': '담당의 확인',
        'pre_ru_status': '시행 안함',
        'enema_status': '시행 안함',
        'supplies': '얼음판, 공 2개, 요기',
        'id_bracelet': '상관없음',
        'ast_site': '상관없음',
        'clothing' : '반팔',
    },

    # --- 23행 규칙: ('C', 'Anterior', 'Level 2개 이상', '서형연') ---
    ('C', 'Anterior', 'Level 2개 이상', '서형연'): {
        'shaving_status': '턱수염',
        'op_marking': 'Nipple 사이 Level 기입',
        'brace': 'Soft collar brace',
        'pre_ru_status': '시행 안함',
        'enema_status': '시행 안함',
        'supplies': '얼음판, 공 2개, 요기',
        'id_bracelet': '상관없음',
        'ast_site': '상관없음',
        'clothing' : '반팔',
    },

    # --- 24행 규칙: ('C', 'Anterior', 'Level 1개', '김성규') ---
    ('C', 'Anterior', 'Level 1개', '김성규'): {
        'shaving_status': '턱수염',
        'op_marking': 'Nipple 사이 Level 기입',
        'brace': 'Soft collar brace',
        'pre_ru_status': '시행 안함',
        'enema_status': '시행 안함',
        'supplies': '얼음판, 공 2개, 요기',
        'id_bracelet': '상관없음',
        'ast_site': '상관없음',
        'clothing' : '반팔',
    },

    # --- 25행 규칙: ('C', 'Anterior', 'Level 2개 이상', '김성규') ---
    ('C', 'Anterior', 'Level 2개 이상', '김성규'): {
        'shaving_status': '턱수염',
        'op_marking': 'Nipple 사이 Level 기입',
        'brace': 'P-brace',
        'pre_ru_status': '시행 안함',
        'enema_status': '시행 안함',
        'supplies': '얼음판, 공 2개, 요기',
        'id_bracelet': '상관없음',
        'ast_site': '상관없음',
        'clothing' : '반팔',
    },

        # --- 26행 규칙: ('C', 'Posterior', 'Level 1개', '서형연') ---
    ('C', 'Posterior', 'Level 1개', '서형연'): {
        'shaving_status': '뒷머리',
        'op_marking': 'Intrascapula에 Level 기입',
        'brace': '담당의 확인',
        'pre_ru_status': '시행 안함',
        'enema_status': '시행 안함',
        'hair': '양 갈래',
        'supplies': '얼음판, 공 2개, 요기',
        'supplies2': 'Biatain 7.5*7.5cm 1x, Post OP IPC',
        'id_bracelet': '상관없음',
        'ast_site': '상관없음',
        'clothing': '반팔',
    },

    # --- 27행 규칙: ('C', 'Posterior', 'Level 2개 이상', '서형연') ---
    ('C', 'Posterior', 'Level 2개 이상', '서형연'): {
        'shaving_status': '뒷머리',
        'op_marking': 'Intrascapula에 Level 기입',
        'brace': 'Soft collar brace',
        'pre_ru_status': '시행 안함',
        'enema_status': '시행 안함',
        'hair': '양 갈래',
        'supplies': '얼음판, 공 2개, 요기',
        'supplies2': 'Biatain 7.5*7.5cm 1x, Post OP IPC',
        'id_bracelet': '상관없음',
        'ast_site': '상관없음',
        'clothing': '반팔',
    },

    # --- 28행 규칙: ('C', 'Posterior', 'Level 1개', '김성규') ---
    ('C', 'Posterior', 'Level 1개', '김성규'): {
        'shaving_status': '뒷머리',
        'op_marking': 'Intrascapula에 Level 기입',
        'brace': 'Soft collar brace',
        'pre_ru_status': '시행 안함',
        'enema_status': '시행 안함',
        'hair': '양 갈래',
        'supplies': '얼음판, 공 2개, 요기',
        'supplies2': 'Biatain 7.5*7.5cm 1x, Post OP IPC',
        'id_bracelet': '상관없음',
        'ast_site': '상관없음',
        'clothing': '반팔',
    },

    # --- 29행 규칙: ('C', 'Posterior', 'Level 2개 이상', '김성규') ---
    ('C', 'Posterior', 'Level 2개 이상', '김성규'): {
        'shaving_status': '뒷머리',
        'op_marking': 'Intrascapula에 Level 기입',
        'brace': 'P-brace',
        'pre_ru_status': '시행 안함',
        'enema_status': '시행 안함',
        'hair': '양 갈래',
        'supplies': '얼음판, 공 2개, 요기',
        'supplies2': 'Biatain 7.5*7.5cm 1x, Post OP IPC',
        'id_bracelet': '상관없음',
        'ast_site': '상관없음',
        'clothing': '반팔',
    },

    # --- 30행 규칙: ('T&L', 'Anterior', 'Level 1개', '서형연') ---
    ('T&L', 'Anterior', 'Level 1개', '서형연'): {
        'shaving_status': '안함',
        'op_marking': 'Level에 따라 수술부위 피해 Back에 표시',
        'brace': 'T : 보조기 안함, L : TLSO or LSO',
        'pre_ru_status': '시행함',
        'pre_rU_result': '     cc',
        'enema_status': '시행함',
        'enema_details': 'Dulcorax 가능, 안 나오면 Glycrein enema 50cc 1회',
        'nipple': '가리기',
        'supplies': '요기',
        'supplies2': 'Post OP IPC',
        'id_bracelet': '상관없음',
        'ast_site': '상관없음',
        'clothing': '반팔',
    },

    # --- 31행 규칙: ('T&L', 'Anterior', 'Level 2개 이상', '서형연') ---
    ('T&L', 'Anterior', 'Level 2개 이상', '서형연'): {
        'shaving_status': '안함',
        'op_marking': 'Level에 따라 수술부위 피해 Back에 표시',
        'brace': 'TLSO or LSO',
        'pre_ru_status': '시행함',
        'pre_ru_result': '     cc',
        'enema_status': '시행함',
        'enema_details': 'Dulcorax 가능, 안 나오면 Glycrein enema 50cc 1회',
        'nipple': '가리기',      
        'supplies': '요기',
        'supplies2': 'Post OP IPC',
        'id_bracelet': '상관없음',
        'ast_site': '상관없음',
        'clothing': '반팔',
    },

    # --- 32행 규칙: ('T&L', 'Anterior', 'Level 1개', '김성규') ---
    ('T&L', 'Anterior', 'Level 1개', '김성규'): {
        'shaving_status': '안함',
        'op_marking': 'Level에 따라 수술부위 피해 Back에 표시',
        'brace': 'TLSO',
        'pre_ru_status': '시행함',
        'pre_ru_result': '     cc',
        'enema_status': '시행함',
        'enema_details': 'Dulcorax 가능, 안 나오면 Glycrein enema 50cc 2회(10000cc enema 확인하기)',
        'nipple': '가리기',
        'supplies': '요기',
        'supplies2': 'Post OP IPC',
        'id_bracelet': '상관없음',
        'ast_site': '상관없음',
        'clothing': '반팔',
    },

    # --- 33행 규칙: ('T&L', 'Anterior', 'Level 2개 이상', '김성규') ---
    ('T&L', 'Anterior', 'Level 2개 이상', '김성규'): {
        'shaving_status': '안함',
        'op_marking': 'Level에 따라 수술부위 피해 Back에 표시',
        'brace': 'TLSO',
        'pre_ru_status': '시행함',
        'pre_ru_result': '     cc',
        'enema_status': '시행함',
        'enema_details': 'Dulcorax 가능, 안 나오면 Glycrein enema 50cc 2회(10000cc enema 확인하기)',
        'nipple': '가리기',
        'supplies': '요기',
        'supplies2': 'Post OP IPC',
        'id_bracelet': '상관없음',
        'ast_site': '상관없음',
        'clothing': '반팔',
    },

    # --- 34행 규칙: ('T&L', 'Posterior', 'Level 1개', '서형연') ---
    ('T&L', 'Posterior', 'Level 1개', '서형연'): {
        'shaving_status': '안함',
        'op_marking': 'Level에 따라 수술부위 피해 Back에 표시',
        'brace': 'T: 보조기 안함, L : TLSO or LSO',
        'pre_ru_status': '시행함',
        'pre_ru_result': '     cc',
        'enema_status': '시행 안함',
        'nipple': '가리기',
        'supplies': '요기',
        'supplies2': 'Biatain 7.5*7.5cm 1x, Post OP IPC',
        'id_bracelet': '상관없음',
        'ast_site': '상관없음',
        'clothing': '반팔',
    },

    # --- 35행 규칙: ('T&L', 'Posterior', 'Level 2개 이상', '서형연') ---
    ('T&L', 'Posterior', 'Level 2개 이상', '서형연'): {
        'shaving_status': '안함',
        'op_marking': 'Level에 따라 수술부위 피해 Back에 표시',
        'brace': 'TLSO or LSO',
        'pre_ru_status': '시행함',
        'pre_ru_result': '     cc',
        'enema_status': '시행 안함',
        'hair': '양 갈래',
        'supplies': '요기',
        'supplies2': 'Biatain 7.5*7.5cm 1x, Post OP IPC',
        'id_bracelet': '상관없음',
        'ast_site': '상관없음',
        'clothing': '반팔',
    },


    # --- 36행 규칙: ('T&L', 'Posterior', 'Level 1개', '김성규') ---
    ('T&L', 'Posterior', 'Level 1개', '김성규'): {
        'shaving_status': '안함',
        'op_marking': 'Level에 따라 수술부위 피해 Back에 표시',
        'brace': 'TLSO',
        'pre_ru_status': '시행함',
        'pre_ru_result': '     cc',
        'enema_status': '시행 안함',
        'hair': '양 갈래',
        'supplies': '요기',
        'supplies2': 'Biatain 7.5*7.5cm 1x, Post OP IPC',
        'id_bracelet': '상관없음',
        'ast_site': '상관없음',
        'clothing': '반팔',
    },

    # --- 37행 규칙: ('T&L', 'Posterior', 'Level 2개 이상', '김성규') ---
    ('T&L', 'Posterior', 'Level 2개 이상', '김성규'): {
        'shaving_status': '안함',
        'op_marking': 'Level에 따라 수술부위 피해 Back에 표시',
        'brace': 'TLSO',
        'pre_ru_status': '시행함',
        'pre_ru_result': '     cc',
        'enema_status': '시행 안함',
        'hair': '양 갈래',
        'supplies': '요기',
        'supplies2': 'Biatain 7.5*7.5cm 1x, Post OP IPC',
        'id_bracelet': '상관없음',
        'ast_site': '상관없음',
        'clothing': '반팔',
    },

    # --- 38행 규칙: ('ACDF', 'Level 1개', '서형연') ---
    ('ACDF', 'Level 1개', '서형연'): {
        'op_name': 'ACDF',
        'shaving_status': '턱수염',
        'op_marking': 'Nipple 사이 Level 기입',
        'brace': '담당의 확인',
        'pre_ru_status': '시행 안함',
        'enema_status': '시행함',
        'enema_details': 'Dulcorax 가능, 안 나오면 Glycrein enema 50cc 1회',
        'nipple': '가리기',
        'supplies': '얼음판, 공 2개, 요기',
        'supplies2': 'Post OP IPC',
        'id_bracelet': '상관없음',
        'ast_site': '상관없음',
        'clothing': '반팔',
    },

    # --- 39행 규칙: ('ACDF', 'Level 2개 이상', '서형연') ---
    ('ACDF', 'Level 2개 이상', '서형연'): {
        'op_name': 'ACDF',
        'shaving_status': '턱수염',
        'op_marking': 'Nipple 사이 Level 기입',
        'brace': 'Soft collar brace',
        'pre_ru_status': '시행 안함',
        'enema_status': '시행함',
        'enema_details': 'Dulcorax 가능, 안 나오면 Glycrein enema 50cc 1회',
        'nipple': '가리기',
        'supplies': '얼음판, 공 2개, 요기',
        'supplies2': 'Post OP IPC',
        'id_bracelet': '상관없음',
        'ast_site': '상관없음',
        'clothing': '반팔',
    },

    # --- 40행 규칙: ('ACDF', 'Level 1개', '김성규') ---
    ('ACDF', 'Level 1개', '김성규'): {
        'op_name': 'ACDF',
        'shaving_status': '턱수염',
        'op_marking': 'Nipple 사이 Level 기입',
        'brace': 'Soft collar brace',
        'pre_ru_status': '시행 안함',
        'enema_status': '시행함',
        'enema_details': 'Dulcorax 가능, 안 나오면 Glycrein enema 50cc 2회(10000cc enema 확인)',
        'nipple': '가리기',
        'supplies': '얼음판, 공 2개, 요기',
        'supplies2': 'Post OP IPC',
        'id_bracelet': '상관없음',
        'ast_site': '상관없음',
        'clothing': '반팔',
    },

    # --- 41행 규칙: ('ACDF', 'Level 2개 이상', '김성규') ---
    ('ACDF', 'Level 2개 이상', '김성규'): {
        'op_name': 'ACDF',
        'shaving_status': '턱수염',
        'op_marking': 'Nipple 사이 Level 기입',
        'brace': 'P-brace',
        'pre_ru_status': '시행 안함',
        'enema_status': '시행함',
        'enema_details': 'Dulcorax 가능, 안 나오면 Glycrein enema 50cc 2회(10000cc enema 확인)',
        'nipple': '가리기',
        'supplies': '얼음판, 공 2개, 요기',
        'supplies2': 'Post OP IPC',
        'id_bracelet': '상관없음',
        'ast_site': '상관없음',
        'clothing': '반팔',
    },

    # --- 42행 규칙: ('OLIF', 'Level 1개', '서형연') ---
    ('OLIF', 'Level 1개', '서형연'): {
        'op_name': 'OLIF',
        'shaving_status': '안함',
        'op_marking': 'Intrascapula 해당 Level 기입',
        'brace': 'T : 보조기 안함, L : TLSO or LSO',
        'pre_ru_status': '시행함',
        'pre_ru_result': '     cc',
        'enema_status': '시행함',
        'enema_details': 'Dulcorax 가능, 안 나오면 Glycrein enema 50cc 1회',
        'nipple': '가리기',
        'supplies': '요기',
        'supplies2': 'Post OP IPC',
        'id_bracelet': '상관없음',
        'ast_site': '상관없음',
        'clothing': '반팔',
    },


    # --- 43행 규칙: ('OLIF', 'Level 2개 이상', '서형연') ---
    ('OLIF', 'Level 1개', '서형연'): {
        'op_name': 'OLIF',
        'shaving_status': '안함',
        'op_marking': 'Intrascapula 해당 Level 기입',
        'brace': 'TLSO or LSO',
        'pre_ru_status': '시행함',
        'pre_ru_result': '     cc',
        'enema_status': '시행함',
        'enema_details': 'Dulcorax 가능, 안 나오면 Glycrein enema 50cc 1회',
        'nipple': '가리기',
        'supplies': '요기',
        'supplies2': 'Post OP IPC',
        'id_bracelet': '상관없음',
        'ast_site': '상관없음',
        'clothing': '반팔',
    },


    # --- 44행 규칙: ('OLIF', 'Level 1개', '김성규') ---
    ('OLIF', 'Level 1개', '김성규'): {
        'op_name': 'OLIF',
        'shaving_status': '안함',
        'op_marking': 'Intrascapula 해당 Level 기입',
        'brace': 'TLSO',
        'pre_ru_status': '시행함',
        'pre_ru_result': '     cc',
        'enema_status': '시행함',
        'enema_details': 'Dulcorax 가능, 안 나오면 Glycrein enema 50cc 2회(10000cc enema 확인)',
        'nipple': '가리기',
        'supplies': '요기',
        'supplies2': 'Post OP IPC',
        'id_bracelet': '상관없음',
        'ast_site': '상관없음',
        'clothing': '반팔',
    },


    # --- 45행 규칙: ('OLIF', 'Level 2개 이상', '김성규') ---
    ('OLIF', 'Level 1개', '김성규'): {
        'op_name': 'OLIF',
        'shaving_status': '안함',
        'op_marking': 'Intrascapula 해당 Level 기입',
        'brace': 'TLSO',
        'pre_ru_status': '시행함',
        'pre_ru_result': '     cc',
        'enema_status': '시행함',
        'enema_details': 'Dulcorax 가능, 안 나오면 Glycrein enema 50cc 2회(10000cc enema 확인)',
        'nipple': '가리기',
        'supplies': '요기',
        'supplies2': 'Post OP IPC',
        'id_bracelet': '상관없음',
        'ast_site': '상관없음',
        'clothing': '반팔',
    },


}

HIGHLIGHT_KEYWORDS = {
    'Upper': {
        'surgery_name': [
            "RC tear & A/S OP", "A/S SAD OP", "Elbow(Humerous) OP", 
            "Dislocation, Bankart OP", "Cuff repair OP", "RC tear"
        ],
        'item_name': [
            "Abduction Brace", "Arm Sling", "Arm sling", "L-sling", 
            "Compression stocking & IPC sleeves"
        ]
    },
    'T&L': {
        'surgery_name': [
            "ACDF", "OLIF"
        ],
        'item_name': [
            "Soft collar brace", "P-brace", "TLSO", "LSO", "Post OP IPC"
        ]
    },
    'Foot': {
        'surgery_name': [
            # 예시: 필요에 따라 Foot 관련 수술명을 추가하세요.
            "TKR", "Total Knee Replacement" 
        ],
        'item_name': [
            # 예시: Foot 관련 보조기나 준비물을 추가하세요.
            "메디터치 힐", "옆 트임 바지", "양 트임 바지"
        ]
    }
}


# --- [핵심 수정] 각 탭별 주의사항 기본 "텍스트"만 남겨둡니다. ---
PRECAUTIONS = {
    'Upper': "Upper 수술 관련 주의사항의 기본 내용을 여기에 입력하세요.",
    'T&L': "T&L 수술 관련 주의사항의 기본 내용을 여기에 입력하세요.",
    'Foot': "Foot 수술 관련 주의사항의 기본 내용을 여기에 입력하세요."
}
