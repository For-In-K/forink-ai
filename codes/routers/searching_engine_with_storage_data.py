from .config import Config
import requests
from pinecone import Pinecone

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


# In[4]:


from typing import Dict, Any, List, Union 

def get_answer_value(exam_id: int, answer_id: int, all_user_responses: Dict[int, Any]) -> Any:
    """ examId와 answerId를 통해 해당 질문의 실제 응답 값을 찾습니다. """
    for exam in EXAM_QUESTIONS_DATA:
        if exam['examId'] == exam_id:
            if exam_id == 2: # Q2는 conditionalOptions를 가짐
                q1_answer_id = all_user_responses.get(1) # Q1의 answerId
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

# internal_key 매핑 (DB 스키마의 conditional_rules와 매칭)
INTERNAL_KEY_MAPPING = {
    1: "visa_type", 2: "stay_duration_categories", 3: "has_place_to_live", 4: "intended_residence_area",
    5: "has_korean_bank_account", 6: "has_health_insurance", 7: "korean_proficiency_level",
    8: "has_korean_phone", 9: "understands_address_registration", 10: "understands_job_school_search",
    11: "accompanying_family", 12: "plan_to_drive", 13: "is_working_in_korea", 14: "job_type",
    16: "is_studying_in_korea", 17: "study_level", 18: "plan_to_business_invest",
    19: "already_have_alien_registration_card"
}

def get_user_profile_from_exam(exam_responses: List[Dict[str, int]]) -> Dict[str, Any]:
    """ 진단 결과를 분석하여 사용자의 프로필 딕셔너리를 생성합니다. """
    user_answers_map = {res['examId']: res['answerId'] for res in exam_responses}
    user_profile = {}
    
    for exam_id, answer_id in user_answers_map.items():
        internal_key = INTERNAL_KEY_MAPPING.get(exam_id)
        if internal_key:
            exam_data = next((e for e in EXAM_QUESTIONS_DATA if e['examId'] == exam_id), None)
            if exam_data:
                if exam_data['answer']['mode'] == 'Button':
                    user_profile[internal_key] = (answer_id == 1)
                else:
                    user_profile[internal_key] = get_answer_value(exam_id, answer_id, user_answers_map)
    
    print(f"생성된 사용자 프로필: {user_profile}")
    return user_profile
    
# db open 되면 이 코드 적용
import mysql.connector
from typing import List, Dict

# --- DB 연결 정보 설정 ---
cfg = Config()
DB_CONFIG = cfg.DB_CONFIG

def get_chat_history(chat_id: int) -> List[Dict[str, str]]:
    """
    [수정된 버전]
    chat_message 테이블에서 특정 chat_id의 AI와 USER 양쪽의
    모든 대화 기록을 시간순으로 가져옵니다.
    """
    print(f"🔍 DB에서 chat_id '{chat_id}'의 전체 대화 기록을 조회합니다...")
    
    cnx = None
    cursor = None
    
    try:
        cnx = mysql.connector.connect(**DB_CONFIG)
        cursor = cnx.cursor(dictionary=True)
        
        # --- SQL 쿼리 수정 ---
        # 1. type, content 컬럼을 함께 선택 (누가, 무슨 말을 했는지)
        # 2. WHERE 절에서 type='USER' 조건 제거 (AI, USER 메시지 모두 가져오기)
        # 3. chat_message 테이블의 컬럼명 'type'으로 수정
        sql_query = """
            SELECT type, content 
            FROM chat_message 
            WHERE chat_id = %s
            ORDER BY created_at ASC
        """
        
        cursor.execute(sql_query, (chat_id,))
        
        # fetchall()은 [{'type': 'USER', 'content': '...'}, {'type': 'AI', 'content': '...'}] 형태의 리스트를 반환합니다.
        history = cursor.fetchall()
        
        print(f"DB에서 추출된 전체 메시지: {len(history)}개")
        return history

    except mysql.connector.Error as err:
        print(f"데이터베이스 오류 발생: {err}")
        return []

    finally:
        if cursor:
            cursor.close()
        if cnx and cnx.is_connected():
            cnx.close()
            print("🔌 데이터베이스 연결이 종료되었습니다.")

# def get_chat_history(chat_id: int) -> List[Dict[str, str]]:
#     """ [모의 함수] DB에서 특정 chat_id의 대화 기록을 가져옵니다. """
#     print(f"DB에서 chat_id '{chat_id}'의 대화 기록을 조회합니다...")
#     # 실제 구현 시 DB 접속 코드로 변경
#     mock_db = {101: [{"sender": "USER", "content": "난 한국에 사업 할려고 들어왔어 아직 직원들을 위한 보험 가입은 하지 않았어"}]}
#     user_messages = [msg for msg in mock_db.get(chat_id, []) if msg["sender"] == "USER"]
#     print(f"추출된 사용자 메시지: {len(user_messages)}개")
#     return user_messages


# --- 2. RAG 시스템 클래스 (이전 코드와 동일, 설명 위해 다시 포함) ---
# 실제 사용 시, 아래 클래스들은 별도 파일로 분리하여 관리하는 것이 좋을 듯 -> 이미 위에서 쓴 코드라서 다시 쓰지 않을 것

class UpstageEmbeddingModel:  #KoreaVisaRAG 에서 인스턴스 생성 및 호출함
    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError("Upstage API 키가 제공되지 않았습니다.")
        self.api_key = api_key
        self.api_url = "https://api.upstage.ai/v1/solar/embeddings"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        print("Upstage Embedding API 클라이언트 초기화 완료.")

    def embed_documents(self, texts):
        """문서 임베딩용 - 데이터 저장시 사용"""
        return self._embed(texts, "embedding-query")
    
    def embed_query(self, text):
        """쿼리 임베딩용 - 검색시 사용"""
        return self._embed(text, "embedding-query")
    
    def _embed(self, texts, model):
        """내부 임베딩 함수"""
        payload = {
            "input": texts,
            "model": model
        }
        try:
            response = requests.post(self.api_url, headers=self.headers, json=payload, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            if 'data' in data and len(data['data']) > 0:
                embeddings = [d['embedding'] for d in data['data']]
                
                # ✅ 모든 값을 float로 변환
                if isinstance(texts, str):
                    return [float(x) for x in embeddings[0]]
                else:
                    return [[float(x) for x in embedding] for embedding in embeddings]
            else:
                raise ValueError("API 응답에서 임베딩 데이터를 찾을 수 없습니다.")
        except requests.exceptions.RequestException as e:
            print(f"❌ 임베딩 API 호출 오류: {e}")
            raise
        except ValueError as e:
            print(f"❌ API 응답 처리 오류: {e}")
            raise


class UpstageChat: #KoreaVisaRAG 에서 인스턴스 생성 및 호출함
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.api_url = "https://api.upstage.ai/v1/solar/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
    # [수정 후]
    def generate_answer(self, current_question: str, user_profile: dict, chat_history: list, context_chunks: list):
        """검색된 문서와 모든 컨텍스트를 바탕으로 최종 답변 생성"""
        
        # 컨텍스트 정보 포맷팅
        profile_context = "\n".join([f"- {key}: {value}" for key, value in user_profile.items()])
        history_context = "\n".join([f"- 과거 질문/답변: {msg['content']}" for msg in chat_history])
        retrieved_docs_context = "\n\n".join([f"문서 {i+1}: {chunk['metadata'].get('output', '')}" for i, chunk in enumerate(context_chunks)])
        prompt_first = f"""당신은 한국 비자 및 체류 관련 전문 상담사에게 현재 사용자의 정보를 일목요연하게 전달해줄 에이전트입니다. 아래 문서들을 참고하여 사용자의 질문에 정확하고 도움이 되는 답변을 제공해주세요.
                    
                    ### 사용자 정보
                    {profile_context}
                    
                    ### 이전 대화 내용
                    {history_context}

                    다음과 같은 내용을 바탕으로 사용자의 정보를 일목요연하게 정리하세요. 

                    ### 이때 몇가지 주의사항이 있어요

                    0. 만약 사용자에게서 들어온 질문의 내용이 "예/응" 등이라면 대화 기록에서 ai가 가장 최근에 한 질문을 기반으로 그 대답의 의미를 추론한 후 사용자의 정보로 인식하세요.

                    ex. 
                      
                      ai 의 질문 : 운전면허를 취득하셨나요 , 사용자의 답변 : 응/예  -> 사용자는 현재 운전면허를 취득한 상태

                      ai 의 질문 : 현재 거주하고 있는 곳이 어디죠? , 사용자의 답변 : 나 부산에서 살고 있어 -> 사용자는 현재 부산에서 거주하고 있는 상태

                    1. 만약 사용자의 정보가 바뀌었다면 절대 놓치지 마세요

                    ex. 
                      
                      ai 의 이전 질문 : 운전면허를 취득하셨나요 , 사용자의 답변 : 아니요  -> 사용자는 현재 운전면허를 취득하지 않은 상태
                      
                      ai 와의 이후 대화에서 사용자의 답변 : 나 지금은 운전면허 땄어 또는 아 나 이제는 부산 아니고 서울에서 살아  -> 사용자는 운전면허를 취득한 상태 / 사용자의 주거지가 부산에서 서울로 바뀜.

                  이 과정에서 사용자에 대한 정보를 잘 모르겠으면 추가적으로 물어보는 질문을 답변으로 만들어되 됩니다 ex. 예전에는 부산에 거주 한다고 하셨는데 지금은 서울로 이사를 가신건가요? / 이제 운전면허를 취득한건가요? 이런 질문!

                  다음과 같은 제약조건을 통해서 밑의 예시와 같은 답변을 만드세요! 

                    ex, 사용자의 이름 : ((대화기록에 혹시 이름이 있다면 여기 넣어!)) , 사용자의 요청사항 : 반드시 답변을 시작할때 이름을 불러야 함 , 사용자는 현재 어떤 비자를 가지고 있고 , 외국인 등록증은 없는 상태

                    등과 같은 표현으로 . 이때 꼭!!!!!!!!!
                    
                    1. 사용자에 대한 정보 + 사용자의 요청사항을 단 하나도 빠짐없이 담되
                     
                    2. 텍스트가 너무 길지 않게 하세요
                    
                """

        payload_first = {
            "model": "solar-1-mini-chat",
            "messages": [
                {"role": "system", "content": "당신은 한국 비자 및 체류 관련 전문 상담사입니다."},
                {"role": "user", "content": prompt_first}
            ],
            "max_tokens": 1000,
            "temperature": 0.3
        }
        
        try:
            response_first = requests.post(self.api_url, headers=self.headers, json=payload_first, timeout=60)
            print("1번쨰 완료")
            response = self.make_final_return_value(response_first.json()['choices'][0]['message']['content'], retrieved_docs_context, current_question)
            response.raise_for_status()
            data = response.json()
            
            if 'choices' in data and len(data['choices']) > 0:
                return data['choices'][0]['message']['content']
            else:
                return "답변 생성 중 오류가 발생했습니다."
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Chat API 호출 오류: {e}")
            return "답변 생성 중 네트워크 오류가 발생했습니다."
        

    def  make_final_return_value(self , summarized_info: str , retrieved_docs_context , current_question):
        
          prompt_last = f"""당신은 한국 비자 및 체류 관련 전문 상담사입니다. 앞의 ai 가 사용자와 ai 가 주고 받은 대화를 바탕으로 정리한 사용자의 정보를 바탕으로 참고하여 사용자의 질문에 정확하고 도움이 되는 답변을 제공해주세요.

                    ### 현재 사용자의 정보
                    {summarized_info}
                    
                    ### 참고 자료 (시스템 검색 결과)
                    {retrieved_docs_context}
                    ---
                    위의 **사용자 정보, 참고 자료**를 모두 종합하여 아래 사용자의 질문에 대해 가장 정확하고 개인화된 답변을 제공해주세요.
                    
                    ### 현재 사용자 질문
                    {current_question}
                    
                    답변 시 주의사항:

                    0. 만약 사용자에게서 들어온 질문의 내용이 마치 어떤 질문이 아닌 잘문에 대한 "답변" 같다면 다음과 같이 답변하세요 "넵 정보를 파악하였습니다" 질문을 계속 하시겠어요? 희망하시면 "예 / 응" 등으로 대답해주세요!
                    
                    1. 만약 추출된 청크들 중 이 정보가 이 사용자한테 전달되기 적절한 정보인지 알기 위해 추가적으로 사용자에게 물어보고 싶은 데이터가 있다면 얼마든지 최대한 많이 물어봐도 됩니다.
                    1-(1). 사용자에게 추가로 물어본 데이터는 대화기록에 저장되며 , 방금 질문에 대해 들어온 답변은 다음 대화에 읽을 수 있게 들어올겁니다 
                    1-(2). 지금 질문 뿐만 아니라 추후 사용자에게 정보를 제공하기 위해 필요한 사용자에 대한 정보를 질문하는건 괭장히 좋습니다. 이렇게 들어온 사용자에 대한 정보를 당신은 질문이 들어올때마다 열람할 수 있습니다.

                    EX> " 위의 정보는 현재 사용자 정보에 포함되어 있지 않으므로, 추가적으로 사용자에게 물어볼 필요가 있습니다 " 와 같이 소극적인 어투가 아닌 적극적 질문을 생성해 사용자에게 질문하세요 
                    예를 들어 , 현재 거주사실 지역은 정하셨나요? 또는 휴대폰 개통은 하셨나요? 하셨다면 잊지말고 로드맵에 체크해주세요 !! 와 같은 표현을 꼭 해주세요
                    

                    마지막 응답을 주기 전 밑의 제약조건을 반드시 하나씩! 평가하고 응답을 수정할지 여부를 판단하세요

                    1. 입력으로 들어온 사용자의 정보 중 응답형태에 관해 요청한 사항이 있다면 반드시 포함시키세요
                    2. 비자 종류, 체류 기간, 필요 서류 등을 구체적으로 명시하세요
                    3. 제공된 문서 내용만을 바탕으로 답변하세요(제공된 청크에 없는 내용을 함부로 넣지 말 것)
                    4. 법적 의무사항은 명확히 구분해서 설명하세요
                    5. 모르는 내용은 추측하지 말고 "제공된 정보로는 확인이 어렵습니다"라고 답하세요
                    6. 혹시 들어온 chunk 들 중 출처와 그 정보의 시간 기준 (ex, 2024.06.07 기준 , 출처 : hikorea) 뭐 이런 거 있으면 반드시 답변에 포함시키세요.
                    7.  "현재 한국어 능력 수준이 중급이라고 하셨는데, 필기시험 준비에 도움이 되실 겁니다 , " -> 이런 사용자에 대한 정보를 인지하고 있음을 알려주는 표현 괭장히 좋습니다
                    8. 질문으로 들어온 문장이 영어라면 영어로 , 한국어면 한국어로 , 중국어면 중국어로 베트남어면 베트남 어로 즉 질문으로 들어온 언어에 맞춰서 답변을 그 언어로 형성해
                    9. 절대 글자수가 750자를 넘지 않게 하고 , 750 자 안에 푀대한 내용을 압축해서 표현해.


                    반드시!!!!!!!! 사용자의 질문으로 들어온 언어에 따라 응답 언어로 번역하세요!!
                    질문이 영어면 영어로!!!!!!!!!!!!!!
                    
                    답변:
                """

          payload_last = {
              "model": "solar-1-mini-chat",
              "messages": [
                  {"role": "system", "content": "당신은 한국 비자 및 체류 관련 전문 상담사입니다."},
                  {"role": "user", "content": prompt_last}
              ],
              "max_tokens": 1000,
              "temperature": 0.3
          }

          response = requests.post(self.api_url, headers=self.headers, json=payload_last, timeout=60)
          
          # ✅ [수정됨] 문자열이 아닌 API 응답 객체(response) 자체를 반환
          return response


class KoreanVisaRAG:
    def __init__(self):
        self.config = Config()
        
        # Pinecone 초기화
        self.pc = Pinecone(api_key=self.config.pinecone_api_key)
        self.index = self.pc.Index(self.config.pinecone_index_name)
        
        # 임베딩 모델 초기화
        self.embedding_model = UpstageEmbeddingModel(api_key=self.config.upstage_api_key)
        
        # Chat 모델 초기화
        self.chat_model = UpstageChat(api_key=self.config.upstage_api_key)
        
        print("✅ 한국 비자 RAG 시스템 초기화 완료!")
    
    def search_similar_documents(self, query: str, top_k: int = 10):
        """사용자 질문과 유사한 문서들을 검색"""
        print(f"🔍 질문 분석 중: {query}")
        
        try:
            # 1. 질문을 임베딩으로 변환 (쿼리용 모델 사용)
            query_embedding = self.embedding_model.embed_query(query)
            print(f"✅ 질문 임베딩 완료 (차원: {len(query_embedding)})")
            
            # 2. Pinecone에서 유사한 벡터 검색
            search_results = self.index.query(
                vector=query_embedding,
                top_k=top_k,
                include_metadata=True,
                include_values=False
            )
            
            print(f"✅ {len(search_results.matches)}개의 관련 문서 검색 완료")
            
            # 3. 결과 정리
            similar_docs = []
            for match in search_results.matches:
                similar_docs.append({
                    'id': match.id,
                    'score': match.score,
                    'metadata': match.metadata
                })
                print(f"  - 문서 ID: {match.id}, 유사도: {match.score:.3f}")
            
            return similar_docs
            
        except Exception as e:
            print(f"❌ 검색 중 오류: {e}")
            return []
    
    def answer_question(self, current_question: str, user_profile: dict, chat_history: list, top_k: int = 10):
        """[수정됨] 전체 RAG 파이프라인 - 모든 컨텍스트를 활용"""
        print(f"\n🤖 질문 처리 시작: {current_question}")
        print("-" * 60)
        
        # 1. 컨텍스트를 종합하여 '검색용 쿼리' 생성
        profile_summary = ", ".join([f"{key}: {value}" for key, value in user_profile.items()])
        history_summary = " ".join([msg['content'] for msg in chat_history])
        composite_query = f"사용자 정보({profile_summary})와 이전 대화({history_summary})를 바탕으로 다음 질문에 답해줘: {current_question}"
        
        print(f"🔍 종합 검색 쿼리: {composite_query}")
        
        # 2. 관련 문서 검색 (종합 쿼리 사용)
        similar_docs = self.search_similar_documents(composite_query, top_k)
        
        if not similar_docs:
            return "죄송합니다. 관련된 정보를 찾을 수 없습니다."
            
        # 3. 최종 답변 생성 (모든 컨텍스트를 LLM에 전달)
        print("🤔 모든 정보를 종합하여 답변 생성 중...")
        final_answer = self.chat_model.generate_answer(
            current_question=current_question,
            user_profile=user_profile,
            chat_history=chat_history,
            context_chunks=similar_docs
        )
        
        print("✅ 답변 생성 완료!")
        print("-" * 60)
        
        return final_answer
    
    def get_index_stats(self):
        """인덱스 상태 확인"""
        try:
            stats = self.index.describe_index_stats()
            print(f"📊 인덱스 통계:")
            print(f"  - 총 벡터 수: {stats.total_vector_count}")
            print(f"  - 차원: {stats.dimension}")
            print(f"  - 네임스페이스: {list(stats.namespaces.keys()) if stats.namespaces else '없음'}")
            return stats
        except Exception as e:
            print(f"❌ 인덱스 상태 확인 오류: {e}")
            return None


# In[ ]:

# routers/main.py 또는 관련 라우터 파일

from fastapi import FastAPI, APIRouter
from pydantic import BaseModel
from typing import List, Dict, Any

# --- Pydantic 모델 정의 ---
class ExamStep(BaseModel):
    stepNumber: int
    stepAnswer: int

class BotMessageRequest(BaseModel):
    message: str
    examSteps: List[ExamStep]

# --- APIRouter 객체 생성 ---
router = APIRouter()

# --- [중요] RAG 시스템 객체를 전역 변수로 한 번만 생성 ---
# 매 요청마다 객체를 생성하면 비효율적이므로, 서버 시작 시 한 번만 초기화합니다.
rag_system = KoreanVisaRAG()

# --- [핵심] 수정된 최종 엔드포인트 ---
@router.post("/bots/{chat_id}/messages")
def process_user_message(chat_id: int, request_body: BotMessageRequest):
    """
    사용자의 메시지와 진단검사 결과를 받아 RAG 시스템을 통해 AI 답변을 생성합니다.
    """
    print(f"새로운 요청 수신: chat_id={chat_id}")

    # 1. 진단검사 결과(examSteps)를 사용자 프로필(user_profile)로 변환
    # 1. [수정됨] 진단검사 결과의 키 이름을 'examId', 'answerId'로 변환
    exam_responses = [
        {"examId": step.stepNumber, "answerId": step.stepAnswer} 
        for step in request_body.examSteps
    ]
    user_profile = get_user_profile_from_exam(exam_responses)
    
    # 2. DB에서 과거 대화 기록 가져오기
    past_history = get_chat_history(chat_id)
    
    # 3. 현재 사용자의 질문 추출
    current_question = request_body.message
    
    # 4. KoreanVisaRAG 시스템을 호출하여 최종 답변 생성 
    final_answer = rag_system.answer_question(
        current_question=current_question,
        user_profile=user_profile,
        chat_history=past_history
    )
    
    # 5. 생성된 답변을 클라이언트에게 반환
    return {"chatAnswer": final_answer}

# # main.py에서 이 라우터를 포함시켜야 합니다.
# from routers import your_router_file
# app.include_router(your_router_file.router)


# Jupyter Notebook 환경에서 FastAPI 서버를 실행하려면 uvicorn 라이브러리가 필요합니다.
# 터미널에서 uvicorn your_file_name:app --reload 와 같이 실행합니다.

# # DB 연결 정보 분리 (DB_CONFIG)

# 서버 IP, 계정 정보 등을 딕셔너리로 분리하여 관리의 편의성을 높였습니다. 나중에 실제 정보를 받으면 이 부분의 값들만 수정하시면 됩니다.

# # 안전한 쿼리 실행 (SQL Injection 방지)

# WHERE chat_id = get_ipython().run_line_magic('s와', '같이 ?나 %s 형태의 플레이스홀더를 사용하고, cursor.execute()에 실제 값을 튜플로 전달했습니다.')

# 이렇게 하면 악의적인 입력값으로 데이터베이스가 공격받는 SQL Injection을 원천적으로 차단할 수 있어 매우 중요합니다.

# # 안정적인 실행 구조 (try...except...finally)

# #try: DB 연결 및 쿼리 실행 코드를 시도합니다.

# except: DB 접속 실패, 쿼리 오류 등 문제가 발생했을 때 프로그램이 멈추지 않고 에러 메시지를 남긴 후, 빈 리스트([])를 반환하여 안정적으로 다음 로직을 처리하도록 합니다.

# finally: 작업이 성공하든 실패하든 반드시 실행되는 부분입니다. 여기에 cursor와 connection을 닫는 코드를 넣어, DB 연결 자원이 소모되거나 남아있지 않도록 항상 깔끔하게 정리해줍니다.

# # 효율적인 데이터 조회

# 이전 코드에서는 모든 대화를 가져와 파이썬에서 sender == 'USER'인지 확인했지만, 이번에는 SQL WHERE 절에 AND sender = 'USER' 조건을 추가했습니다.

# 이렇게 하면 처음부터 DB에서 필요한 데이터만 가져오므로, 불필요한 데이터 전송이 줄어들어 성능이 더 향상됩니다.

