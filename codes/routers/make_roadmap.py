import json
from typing import List, Dict, Any, Union

import mysql.connector
from fastapi import FastAPI, HTTPException, APIRouter
from pydantic import BaseModel

# ===============================================================
# 1. 설정 및 데이터 영역
# ===============================================================

# --- 실제 운영 DB 접속 정보를 입력 ---
try:
    from .config import Config      # 패키지 내부에서 실행될 때
except ImportError:
    from config import Config       # 단일 스크립트로 실행할 때 대비

cfg = Config()
DB_CONFIG = cfg.DB_CONFIG

# --- 진단검사 질문-답변 데이터 (수정 불필요) ---
EXAM_QUESTIONS_DATA = [
  {
    "examId": 1,
    "question": { "title": 'Which visa do you have to stay in Korea?' },
    "answer": {
      "mode": 'Dropdown',
      "options": [
        {"answerId": 0, "answer": 'No visa'}, {"answerId": 1, "answer": 'A-1'},
        {"answerId": 2, "answer": 'A-2'}, {"answerId": 3, "answer": 'A-3'},
        {"answerId": 4, "answer": 'B-1'}, {"answerId": 5, "answer": 'B-2'},
        {"answerId": 6, "answer": 'C-1'}, {"answerId": 7, "answer": 'C-3'},
        {"answerId": 8, "answer": 'C-4'}, {"answerId": 9, "answer": 'D-1'},
        {"answerId": 10, "answer": 'D-2'}, {"answerId": 11, "answer": 'D-3'},
        {"answerId": 12, "answer": 'D-4'}, {"answerId": 13, "answer": 'D-5'},
        {"answerId": 14, "answer": 'D-6'}, {"answerId": 15, "answer": 'D-7'},
        {"answerId": 16, "answer": 'D-8'}, {"answerId": 17, "answer": 'D-9'},
        {"answerId": 18, "answer": 'D-10'}, {"answerId": 19, "answer": 'E-1'},
        {"answerId": 20, "answer": 'E-2'}, {"answerId": 21, "answer": 'E-3'},
        {"answerId": 22, "answer": 'E-4'}, {"answerId": 23, "answer": 'E-5'},
        {"answerId": 24, "answer": 'E-6'}, {"answerId": 25, "answer": 'E-7'},
        {"answerId": 26, "answer": 'E-8'}, {"answerId": 27, "answer": 'E-9'},
        {"answerId": 28, "answer": 'E-10'}, {"answerId": 29, "answer": 'F-1'},
        {"answerId": 30, "answer": 'F-2'}, {"answerId": 31, "answer": 'F-3'},
        {"answerId": 32, "answer": 'F-4'}, {"answerId": 33, "answer": 'F-5'},
        {"answerId": 34, "answer": 'F-6'}, {"answerId": 35, "answer": 'G-1'},
        {"answerId": 36, "answer": 'H-1'}, {"answerId": 37, "answer": 'H-2'},
      ],
    },
  },
  {
  "examId": 2,
  "question": {
    "title": "What is your intended length of stay in Korea?"
  },
  "answer": {
    "mode": "Dropdown",
    "options": [],
    "conditionalOptions": {
      "No visa": [
        {
          "answerId": 0,
          "answer": "초단기 체류"
        },
        {
          "answerId": 1,
          "answer": "단기 체류"
        },
        {
          "answerId": 2,
          "answer": "장기 관광"
        }
      ],
      "A-1": [
        {
          "answerId": 0,
          "answer": "단기 체류"
        },
        {
          "answerId": 1,
          "answer": "중기 체류"
        },
        {
          "answerId": 2,
          "answer": "장기 체류"
        }
      ],
      "A-2": [
        {
          "answerId": 0,
          "answer": "단기 체류"
        },
        {
          "answerId": 1,
          "answer": "중기 체류"
        },
        {
          "answerId": 2,
          "answer": "장기 체류"
        }
      ],
      "A-3": [
        {
          "answerId": 0,
          "answer": "단기 체류"
        },
        {
          "answerId": 1,
          "answer": "중기 체류"
        },
        {
          "answerId": 2,
          "answer": "장기 체류"
        }
      ],
      "B-1": [
        {
          "answerId": 0,
          "answer": "초단기 체류"
        },
        {
          "answerId": 1,
          "answer": "단기 체류"
        },
        {
          "answerId": 2,
          "answer": "장기 관광"
        }
      ],
      "B-2": [
        {
          "answerId": 0,
          "answer": "초단기 체류"
        },
        {
          "answerId": 1,
          "answer": "단기 체류"
        },
        {
          "answerId": 2,
          "answer": "장기 관광"
        }
      ],
      "C-1": [
        {
          "answerId": 0,
          "answer": "단기 체류"
        },
        {
          "answerId": 1,
          "answer": "중기 체류"
        }
      ],
      "C-3": [
        {
          "answerId": 0,
          "answer": "초단기 체류"
        },
        {
          "answerId": 1,
          "answer": "단기 체류"
        },
        {
          "answerId": 2,
          "answer": "장기 관광/출장"
        }
      ],
      "C-4": [
        {
          "answerId": 0,
          "answer": "단기 프로젝트"
        },
        {
          "answerId": 1,
          "answer": "중기 프로젝트"
        }
      ],
      "D-1": [
        {
          "answerId": 0,
          "answer": "단기 프로젝트"
        },
        {
          "answerId": 1,
          "answer": "중기 활동"
        },
        {
          "answerId": 2,
          "answer": "장기 활동"
        }
      ],
      "D-2": [
        {
          "answerId": 0,
          "answer": "단기 학기"
        },
        {
          "answerId": 1,
          "answer": "정규과정"
        },
        {
          "answerId": 2,
          "answer": "학위과정"
        }
      ],
      "D-3": [
        {
          "answerId": 0,
          "answer": "단기 훈련"
        },
        {
          "answerId": 1,
          "answer": "표준 훈련"
        }
      ],
      "D-4": [
        {
          "answerId": 0,
          "answer": "단기 어학연수"
        },
        {
          "answerId": 1,
          "answer": "정규 어학과정"
        }
      ],
      "D-5": [
        {
          "answerId": 0,
          "answer": "단기 기획취재"
        },
        {
          "answerId": 1,
          "answer": "상주 취재"
        }
      ],
      "D-6": [
        {
          "answerId": 0,
          "answer": "단기 선교"
        },
        {
          "answerId": 1,
          "answer": "장기 선교"
        }
      ],
      "D-7": [
        {
          "answerId": 0,
          "answer": "단기 파견"
        },
        {
          "answerId": 1,
          "answer": "정규 파견"
        }
      ],
      "D-8": [
        {
          "answerId": 0,
          "answer": "설립 준비"
        },
        {
          "answerId": 1,
          "answer": "초기 운영"
        },
        {
          "answerId": 2,
          "answer": "사업 운영"
        }
      ],
      "D-9": [
        {
          "answerId": 0,
          "answer": "시장 조사/준비"
        },
        {
          "answerId": 1,
          "answer": "영업 개시"
        },
        {
          "answerId": 2,
          "answer": "사업 운영"
        }
      ],
      "D-10": [
        {
          "answerId": 0,
          "answer": "초기 구직"
        },
        {
          "answerId": 1,
          "answer": "연장 구직"
        }
      ],
      "E-1": [
        {
          "answerId": 0,
          "answer": "단기 체류"
        },
        {
          "answerId": 1,
          "answer": "중기 체류"
        },
        {
          "answerId": 2,
          "answer": "장기 체류"
        }
      ],
      "E-2": [
        {
          "answerId": 0,
          "answer": "단기 체류"
        },
        {
          "answerId": 1,
          "answer": "중기 체류"
        },
        {
          "answerId": 2,
          "answer": "장기 체류"
        }
      ],
      "E-3": [
        {
          "answerId": 0,
          "answer": "단기 체류"
        },
        {
          "answerId": 1,
          "answer": "중기 체류"
        },
        {
          "answerId": 2,
          "answer": "장기 체류"
        }
      ],
      "E-4": [
        {
          "answerId": 0,
          "answer": "단기 체류"
        },
        {
          "answerId": 1,
          "answer": "중기 체류"
        },
        {
          "answerId": 2,
          "answer": "장기 체류"
        }
      ],
      "E-5": [
        {
          "answerId": 0,
          "answer": "단기 체류"
        },
        {
          "answerId": 1,
          "answer": "중기 체류"
        },
        {
          "answerId": 2,
          "answer": "장기 체류"
        }
      ],
      "E-6": [
        {
          "answerId": 0,
          "answer": "단기 체류"
        },
        {
          "answerId": 1,
          "answer": "중기 체류"
        },
        {
          "answerId": 2,
          "answer": "장기 체류"
        }
      ],
      "E-7": [
        {
          "answerId": 0,
          "answer": "단기 체류"
        },
        {
          "answerId": 1,
          "answer": "중기 체류"
        },
        {
          "answerId": 2,
          "answer": "장기 체류"
        }
      ],
      "E-9": [
        {
          "answerId": 0,
          "answer": "단기 고용"
        },
        {
          "answerId": 1,
          "answer": "중기 고용"
        },
        {
          "answerId": 2,
          "answer": "장기 고용"
        }
      ],
      "F-2": [
        {
          "answerId": 0,
          "answer": "단기 체류"
        },
        {
          "answerId": 1,
          "answer": "중기 체류"
        },
        {
          "answerId": 2,
          "answer": "장기 체류"
        }
      ],
      "F-4": [
        {
          "answerId": 0,
          "answer": "단기 방문"
        },
        {
          "answerId": 1,
          "answer": "중기 거주"
        },
        {
          "answerId": 2,
          "answer": "장기 거주"
        }
      ],
      "F-5": [
        {
          "answerId": 0,
          "answer": "영주 체류"
        }
      ],
      "F-6": [
        {
          "answerId": 0,
          "answer": "단기 체류"
        },
        {
          "answerId": 1,
          "answer": "중기 체류"
        },
        {
          "answerId": 2,
          "answer": "장기 체류"
        }
      ],
      "G-1": [
        {
          "answerId": 0,
          "answer": "출입국 사무소에 문의"
        }
      ],
      "H-1": [
        {
          "answerId": 0,
          "answer": "단기 체류"
        },
        {
          "answerId": 1,
          "answer": "중기 체류"
        }
      ],
      "H-2": [
        {
          "answerId": 0,
          "answer": "단기 방문취업"
        },
        {
          "answerId": 1,
          "answer": "중기 방문취업"
        },
        {
          "answerId": 2,
          "answer": "장기 방문취업"
        }
      ]
    }
  },
  "dependsOn": {
    "examId": 1
  }
  },
  {
    "examId": 3,
    "question": { "title": 'Do you have a place to live in Korea?' },
    "answer": { "mode": 'Button', "options": [{"answerId": 0, "answer": 'No'}, {"answerId": 1, "answer": 'Yes'}] },
  },
  {
    "examId": 4,
    "question": { "title": "What is your intended area of residence? (if 'Yes' to Q3)" },
    "answer": {
      "mode": 'Dropdown',
      "options": [
        {"answerId": 0, "answer": '서울특별시'}, {"answerId": 1, "answer": '부산광역시'},
        {"answerId": 2, "answer": '대구광역시'}, {"answerId": 3, "answer": '인천광역시'},
        {"answerId": 4, "answer": '광주광역시'}, {"answerId": 5, "answer": '대전광역시'},
        {"answerId": 6, "answer": '울산광역시'}, {"answerId": 7, "answer": '세종특별자치시'},
        {"answerId": 8, "answer": '경기도'}, {"answerId": 9, "answer": '강원특별자치도'},
        {"answerId": 10, "answer": '충청북도'}, {"answerId": 11, "answer": '충청남도'},
        {"answerId": 12, "answer": '전라북도'}, {"answerId": 13, "answer": '전라남도'},
        {"answerId": 14, "answer": '경상북도'}, {"answerId": 15, "answer": '경상남도'},
        {"answerId": 16, "answer": '제주특별자치도'},
      ],
    },
    "dependsOn": { "examId": 3, "answerId": 1 }, # 'Yes'
  },
  {
    "examId": 5,
    "question": { "title": 'Do you already have a Korean bank account?' },
    "answer": { "mode": 'Button', "options": [{"answerId": 0, "answer": 'No'}, {"answerId": 1, "answer": 'Yes'}] },
  },
  {
    "examId": 6,
    "question": { "title": 'Do you have access to health insurance in Korea?' },
    "answer": { "mode": 'Button', "options": [{"answerId": 0, "answer": 'No'}, {"answerId": 1, "answer": 'Yes'}] },
  },
  {
    "examId": 7,
    "question": { "title": 'How confident are you in using basic Korean for daily life (e.g., shopping, asking directions)?' },
    "answer": {
      "mode": 'Scale',
      "options": [
        {"answerId": 0, "answer": 'Not at all'}, {"answerId": 1, "answer": 'A little'},
        {"answerId": 2, "answer": 'Moderately'}, {"answerId": 3, "answer": 'Confidently'},
        {"answerId": 4, "answer": 'Fluent'},
      ],
    },
  },
  {
    "examId": 8,
    "question": { "title": 'Do you already have a Korean phone number and mobile phone (already have Korean phone SIM)?' },
    "answer": { "mode": 'Button', "options": [{"answerId": 0, "answer": 'No'}, {"answerId": 1, "answer": 'Yes'}] },
  },
  {
    "examId": 9,
    "question": { "title": 'Do you understand how to register your address at the local immigration office?' },
    "answer": { "mode": 'Button', "options": [{"answerId": 0, "answer": 'No'}, {"answerId": 1, "answer": 'Yes'}] },
  },
  {
    "examId": 10,
    "question": { "title": 'Do you know how to find a job (or enroll in school) in Korea?' },
    "answer": { "mode": 'Button', "options": [{"answerId": 0, "answer": 'No'}, {"answerId": 1, "answer": 'Yes'}] },
  },
  {
    "examId": 11,
    "question": { "title": 'Do you have a support network (friends, community, or help center) in Korea?' },
    "answer": { "mode": 'Button', "options": [{"answerId": 0, "answer": 'No'}, {"answerId": 1, "answer": 'Yes'}] },
  },
  {
    "examId": 12,
    "question": { "title": 'Do you plan to travel with your spouse or children?' },
    "answer": {
      "mode": 'Dropdown',
      "options": [
        {"answerId": 0, "answer": "No, I'm traveling alone"},
        {"answerId": 1, "answer": 'Yes, with my spouse only'},
        {"answerId": 2, "answer": 'Yes, with my children only'},
        {"answerId": 3, "answer": 'Yes, with both my spouse and children'},
      ],
    },
  },
  {
    "examId": 13,
    "question": { "title": 'Do you plan to drive a car or obtain a driver\'s license in Korea?' },
    "answer": { "mode": 'Button', "options": [{"answerId": 0, "answer": 'No'}, {"answerId": 1, "answer": 'Yes'}] },
  },
  {
    "examId": 14,
    "question": { "title": 'Are you going to work in Korea?' },
    "answer": { "mode": 'Button', "options": [{"answerId": 0, "answer": 'No'}, {"answerId": 1, "answer": 'Yes'}] },
  },
  {
    "examId": 15,
    "question": { "title": "What is your main job type/field in Korea? (if 'Yes' to Q14)" },
    "answer": {
      "mode": 'Dropdown',
      "options": [
        {"answerId": 0, "answer": 'Education (e.g., English teacher, university lecturer)'},
        {"answerId": 1, "answer": 'Research / Academia'},
        {"answerId": 2, "answer": 'Business / Administration'},
        {"answerId": 3, "answer": 'IT / Technology'},
        {"answerId": 4, "answer": 'Translation / Interpretation'},
        {"answerId": 5, "answer": 'Arts / Culture / Media'},
        {"answerId": 6, "answer": 'Service Industry (e.g., hospitality, food service)'},
        {"answerId": 7, "answer": 'Manufacturing / Engineering'},
        {"answerId": 8, "answer": 'Student Internship / Research Assistantship'},
        {"answerId": 9, "answer": 'Other Employment (General)'},
      ],
    },
    "dependsOn": { "examId": 14, "answerId": 1 }, # 'Yes'
  },
  {
    "examId": 16,
    "question": { "title": 'Are you going to study in Korea?' },
    "answer": { "mode": 'Button', "options": [{"answerId": 0, "answer": 'No'}, {"answerId": 1, "answer": 'Yes'}] },
  },
  {
    "examId": 17,
    "question": { "title": "What is your education level or course type? (if 'Yes' to Q16)" },
    "answer": {
      "mode": 'Dropdown',
      "options": [
        {"answerId": 0, "answer": 'Undergraduate Student'},
        {"answerId": 1, "answer": 'Graduate Student – Master’s or PhD'},
        {"answerId": 2, "answer": 'Exchange Student'},
        {"answerId": 3, "answer": 'Language Program Student'},
        {"answerId": 4, "answer": 'Non-degree Student / Visiting Student'},
      ],
    },
    "dependsOn": { "examId": 16, "answerId": 1 }, # 'Yes'
  },
  {
    "examId": 18,
    "question": { "title": 'Do you have any plan to start a business or invest in Korea?' },
    "answer": { "mode": 'Button', "options": [{"answerId": 0, "answer": 'No'}, {"answerId": 1, "answer": 'Yes'}] },
  },
  {
    "examId": 19,
    "question": { "title": 'Do you already have an alien registration card?' },
    "answer": { "mode": 'Button', "options": [{"answerId": 0, "answer": 'No'}, {"answerId": 1, "answer": 'Yes'}] },
  },
]

# --- 내부 키 매핑 (수정 불필요) ---
INTERNAL_KEY_MAPPING = {
    1: "visa_type", 2: "stay_duration_categories", 3: "has_place_to_live", 4: "intended_residence_area",
    5: "has_korean_bank_account", 6: "has_health(or_travel)_insurance", 7: "korean_proficiency_level",
    8: "has_korean_phone", 9: "understands_address_registration", 10: "understands_job_school_search", 11:"has_support_network",
    12: "accompanying_family", 13: "plan_to_drive", 14: "is_working_in_korea", 15: "job_type",
    16: "is_studying_in_korea", 17: "study_level", 18: "plan_to_business_invest",
    19: "already_have_alien_registration_card"
}

# ===============================================================
# 2. Pydantic 모델 영역 (API 입출력 형식 정의)
# ===============================================================

class StepResponse(BaseModel):
    stepNumber: int
    answer: int

class RoadmapRequest(BaseModel):
    memberId: int
    memberRoleType: str
    examId: int
    responses: List[StepResponse]

# ===============================================================
# 3. 헬퍼 함수 영역 (사용자 응답 분석)
# ===============================================================

def get_answer_value(exam_id: int, answer_id: int, all_user_responses: Dict[int, Any]) -> Any:
    """examId와 answerId를 실제 응답 값(문자열)으로 변환합니다."""
    for exam in EXAM_QUESTIONS_DATA:
        if exam['examId'] == exam_id:
            if exam_id == 2: # Q2는 Q1의 응답에 따라 옵션이 바뀜
                q1_answer_id = all_user_responses.get(1)
                if q1_answer_id is not None:
                    q1_answer_text = get_answer_value(1, q1_answer_id, all_user_responses)
                    if q1_answer_text and q1_answer_text in exam['answer']['conditionalOptions']:
                        for opt in exam['answer']['conditionalOptions'][q1_answer_text]:
                            if opt['answerId'] == answer_id:
                                return opt['answer']
            elif 'options' in exam['answer']:
                for opt in exam['answer']['options']:
                    if opt['answerId'] == answer_id:
                        return opt['answer']
    return None

def get_user_profile_from_exam(exam_responses: List[Dict[str, int]]) -> Dict[str, Any]:
    """사용자 응답 리스트를 분석하여 내부 로직에서 사용할 프로필 딕셔너리를 생성합니다."""
    user_answers_map = {res['examId']: res['answerId'] for res in exam_responses}
    user_profile = {}
    for exam_id, answer_id in user_answers_map.items():
        internal_key = INTERNAL_KEY_MAPPING.get(exam_id)
        if internal_key:
            exam_data = next((e for e in EXAM_QUESTIONS_DATA if e['examId'] == exam_id), None)
            if exam_data:
                if exam_data['answer']['mode'] == 'Button':
                    user_profile[internal_key] = (answer_id == 1) # Yes: True, No: False
                else:
                    user_profile[internal_key] = get_answer_value(exam_id, answer_id, user_answers_map)
    
    print(f"✅ 생성된 사용자 프로필: {user_profile}")
    return user_profile

# ===============================================================
# 4. 핵심 로직 영역 (로드맵 생성)
# 아래 함수로 기존 generate_roadmap 함수를 완전히 교체하세요.
# ===============================================================

def generate_roadmap(user_responses_list: List[Dict[str, int]]) -> List[Dict[str, Any]]:
    """
    [수정됨] 사용자 응답을 기반으로 필터링 및 새로운 규칙에 따라 그룹화하여
    최종 로드맵 데이터를 생성합니다.
    """
    try:
        # --- 1, 2, 3단계는 이전과 동일 (프로필 생성 및 데이터 필터링) ---
        user_profile = get_user_profile_from_exam(user_responses_list)
        visa_type = user_profile.get("visa_type")
        stay_duration = user_profile.get("stay_duration_categories")

        if not visa_type or not stay_duration:
            return []

        initial_chunks = []
        try:
            cnx = mysql.connector.connect(**DB_CONFIG)
            cursor = cnx.cursor(dictionary=True)
            query = """
                SELECT * FROM roadmap_chunks 
                WHERE 
                    (JSON_CONTAINS(visa_types, %s, '$') OR JSON_LENGTH(visa_types) = 0)
                AND
                    (JSON_CONTAINS(stay_duration_categories, %s, '$') OR JSON_LENGTH(stay_duration_categories) = 0)
                ORDER BY default_order ASC;
            """
            params = (json.dumps(visa_type), json.dumps(stay_duration))
            cursor.execute(query, params)
            initial_chunks = cursor.fetchall()
        finally:
            if 'cursor' in locals() and cursor: cursor.close()
            if 'cnx' in locals() and cnx.is_connected(): cnx.close()

        final_chunks = []
        print(initial_chunks)
        for chunk in initial_chunks:
            is_match = True
            rules_str = chunk.get("conditional_rules_json", "{}")
            rules = json.loads(rules_str) if rules_str else {}
            if rules:
                for key, required_value in rules.items():
                    user_value = user_profile.get(key)
                    if isinstance(required_value, list):
                        if user_value not in required_value:
                            is_match = False; break
                    elif user_value != required_value:
                        is_match = False; break
            if is_match:
                final_chunks.append(chunk)

        # --- 4단계: [수정됨] 새로운 규칙에 따라 그룹화 및 재구성 ---
        
        # 1. 그룹핑 기준을 major_category_name만 사용하도록 변경
        grouped_chunks = {}
        for chunk in final_chunks:
            key = chunk["major_category_name"] # <-- 그룹핑 기준 변경
            if key not in grouped_chunks:
                grouped_chunks[key] = []
            grouped_chunks[key].append(chunk)

        # 2. 새로운 매핑 규칙에 따라 최종 Response 데이터 재구성
        response_data = []
        for i, (major_cat, chunks) in enumerate(grouped_chunks.items()):
            steps = []
            # 같은 그룹 내에서는 default_order로 정렬
            sorted_chunks = sorted(chunks, key=lambda c: c.get('default_order', 0))
            
            for j, chunk in enumerate(sorted_chunks):
                steps.append({
                    "stepNumber": j + 1,
                    # [수정] stepTitle: minor_category_name
                    "stepTitle": chunk.get("minor_category_name", "기타"), 
                    # [수정] stepDescription: chunk_title
                    "stepDescription": chunk.get("chunk_title"),
                    # [유지] contents.stepContent: chunk_description
                    "contents": [{"stepContent": chunk.get("chunk_description")}]
                })
            
            response_data.append({
                # [수정] type: "ADMINISTRATION"으로 고정
                "type": "ADMINISTRATION", 
                "order": i + 1,
                # [수정] title: major_category_name
                "title": major_cat,
                "steps": steps
            })
            
        return response_data

    except Exception as e:
        print(f"❌ 로드맵 생성 중 심각한 오류 발생: {e}")
        raise HTTPException(status_code=500, detail=f"로드맵 생성 중 서버 오류 발생: {e}")

# ===============================================================
# 5. FastAPI 앱 및 라우터 영역
# ===============================================================

app = FastAPI(title="개인화 로드맵 AI 서버")
router = APIRouter()

@router.post("/roadmaps", status_code=201)
def create_roadmap_endpoint(request: RoadmapRequest):
    """사용자 진단 결과를 받아 개인화된 로드맵을 생성하여 반환합니다."""
    print(f"🚀 /roadmaps 요청 수신 (Member ID: {request.memberId})")
    
    # "번역기": 백엔드의 요청 형식(stepNumber)을 내부 로직 형식(examId)으로 변환
    responses_for_logic = [
        {"examId": r.stepNumber, "answerId": r.answer} for r in request.responses
    ]
    
    # 핵심 로직 호출
    roadmap_data = generate_roadmap(responses_for_logic)
    
    print(f"로드맵 생성 완료. {len(roadmap_data)}개 카테고리 반환.")
    return roadmap_data

app.include_router(router)
