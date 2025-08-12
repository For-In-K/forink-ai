#!/usr/bin/env python
# config.py - 환경변수 로드 및 설정 관리
import os
from dotenv import load_dotenv
from typing import Optional

class Config:
    """환경변수 및 설정 관리"""
    
    def __init__(self): # Config 클래스 초기화 : 환경변수 로드 및 설정 초기화(이 클래스의 인스턴스가 만들어질때 마다 자기만의 멤버 변수를 설정.)
          # 1. config.py 파일이 있는 디렉토리의 절대 경로를 찾습니다.
        config_dir = os.path.dirname(os.path.abspath(__file__))
        
        # 2. .env 파일의 절대 경로를 만듭니다. (config.py와 같은 위치에 있다고 가정)
        dotenv_path = os.path.join(config_dir, ".env")
        
        # 3. 명확한 경로를 지정하여 .env 파일을 로드합니다.
        if os.path.exists(dotenv_path):
            load_dotenv(dotenv_path=dotenv_path)
            print(f".env 파일을 성공적으로 로드했습니다: {dotenv_path}")
        else:
            print(f"경고: .env 파일을 찾을 수 없습니다. 경로: {dotenv_path}")
        
        # API 키들
        self.upstage_api_key = self._get_env("UPSTAGE_API_KEY")
        self.pinecone_api_key = self._get_env("PINECONE_API_KEY")
        
        # 임베딩 모델 설정
        self.embedding_model_name = self._get_env("EMBEDDING_MODEL_NAME", "jhgan/ko-sroberta-multitask")
        
        # Pinecone 설정
        self.pinecone_index_name = self._get_env("PINECONE_INDEX_NAME", "forink-documents")
        
        # 청킹 설정
        self.max_chunk_size = int(self._get_env("MAX_CHUNK_SIZE", "1000"))
        self.chunk_overlap = int(self._get_env("CHUNK_OVERLAP", "200"))
        
        # 로그 레벨
        self.log_level = self._get_env("LOG_LEVEL", "INFO")
        
        # API 엔드포인트
        self.upstage_base_url = "https://api.upstage.ai/v1"

        # DB
        self.db_host = os.getenv("DB_HOST", "localhost")
        self.db_user = os.getenv("DB_USER", "")
        self.db_password = os.getenv("DB_PASSWORD", "")
        self.db_name = os.getenv("DB_NAME", "")
        self.db_port = int(os.getenv("DB_PORT", "3306"))
        self.db_charset = os.getenv("DB_CHARSET", "utf8mb4")
        self.db_conn_timeout = int(os.getenv("DB_CONN_TIMEOUT", "60"))
        
        # 검증
        self._validate_config()

    @property
    def DB_CONFIG(self) -> dict:
        return {
            "host": self.db_host,
            "user": self.db_user,
            "password": self.db_password,
            "database": self.db_name,
            "port": self.db_port,
            "charset": self.db_charset,
            "connection_timeout": self.db_conn_timeout,
        }
    
    def _get_env(self, key: str, default: Optional[str] = None) -> str:
        """환경변수 가져오기"""
        value = os.getenv(key, default)
        if value is None:
            raise ValueError(f"환경변수 {key}가 설정되지 않았습니다.")
        return value
    
    def _validate_config(self):
        """필수 설정 검증"""
        required_keys = [
            self.upstage_api_key,
            self.pinecone_api_key
        ]
        
        if any(not key or key == "your_*_api_key_here" for key in required_keys):
            raise ValueError("API 키가 올바르게 설정되지 않았습니다. .env 파일을 확인해주세요.")
    
    def to_dict(self) -> dict:
        """설정을 딕셔너리로 반환 (API 키 제외) 보안을 위해 비밀번호 제외"""
        return {
            "pinecone_index_name": self.pinecone_index_name,
            "embedding_model_name": self.embedding_model_name,
            "max_chunk_size": self.max_chunk_size,
            "chunk_overlap": self.chunk_overlap,
            "log_level": self.log_level
        }

# In[ ]:




