import os
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, HttpUrl
from typing import List, Optional
import json

# --- 1. 응답 데이터 형식을 위한 Pydantic 모델 정의 ---
# 각 게시글에 대한 응답 모델
class ArticleSummary(BaseModel):
    title: str
    summary: str
    article_url: HttpUrl # URL 형식을 검증
    thumbnail_url: Optional[HttpUrl] = None # 이미지가 없을 수도 있으므로 Optional

# --- APIRouter 객체 생성 ---
router = APIRouter()

# --- 2. 핵심 엔드포인트 코드 ---
@router.post("/home", response_model=List[ArticleSummary])
def get_home_articles():
    """
    저장된 extracted_articles.json 파일을 읽어, 각 게시글의 요약 정보를 목록으로 반환합니다.
    """
    try:
        # 이 파일이 있는 폴더('routers')의 경로를 기준으로 json 파일 경로를 찾습니다.
        current_dir = os.path.dirname(os.path.abspath(__file__))
        json_file_path = os.path.join(current_dir, "processed_content.json")

        with open(json_file_path, 'r', encoding='utf-8') as f:
            articles_data = json.load(f)

    except FileNotFoundError:
        # json 파일을 찾을 수 없는 경우 404 에러를 반환합니다.
        raise HTTPException(status_code=404, detail="게시글 데이터 파일을 찾을 수 없습니다.")
    except Exception as e:
        # 그 외의 오류 발생 시 500 에러를 반환합니다.
        raise HTTPException(status_code=500, detail=f"데이터 처리 중 오류 발생: {str(e)}")

    # --- 3. 응답 데이터 가공 ---
    response_list = []
    for article in articles_data:
        # 대표 이미지 URL 설정 (첫 번째 이미지를 사용, 없으면 None)
        thumbnail = article['image_analysis_results'][0]['image_url'] if article['image_analysis_results'] else None

        # 요약 내용 생성 (text_content가 있으면 50자까지, 없으면 "자세한 내용은 링크를 확인하세요.")
        summary_text = article.get('final_text', '').strip()
        if summary_text and len(summary_text) > 50:
            summary = summary_text[:50] + "..."
        elif summary_text:
            summary = summary_text
        else:
            summary = "자세한 내용은 링크를 확인하세요."
            
        # Pydantic 모델에 맞춰 데이터 추가
        response_list.append(
            ArticleSummary(
                title=article['original_title'],
                summary=summary,
                article_url=article['original_url'],
                thumbnail_url=thumbnail
            )
        )
        
    return response_list