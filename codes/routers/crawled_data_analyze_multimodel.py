import requests
import json
import time
from typing import Dict, List, Optional
from dataclasses import dataclass
import os
import io
import base64
import traceback
import hashlib
from urllib.parse import urlparse
# crawled_data_analyze_multimodel.py (상단 근처)
from pathlib import Path

FILE_DIR = Path(__file__).resolve().parent  # 이 파일이 있는 디렉토리

# This assumes you have a config.py file to load the API key.
# If not, you can assign the key directly.
try:
    from config import Config
except ImportError:
    # Create a dummy Config class if config.py doesn't exist
    class Config:
        upstage_api_key = os.environ.get("UPSTAGE_API_KEY", None)

@dataclass
class ProcessedContent:
    """처리된 콘텐츠 결과"""
    original_title: str
    original_url: str
    content_type: str
    final_text: str
    processing_method: str
    image_analysis_results: Optional[List[Dict]] = None
    chunk_ready: bool = False
    error_message: str = ""

class ContentAnalyzer:
    """콘텐츠 분석 및 처리 에이전트"""

    def __init__(self, upstage_api_key: Optional[str] = None):
        self.upstage_api_key = upstage_api_key
        self.upstage_doc_url = "https://api.upstage.ai/v1/document-digitization"
        self.api_url = "https://api.upstage.ai/v1/solar/chat/completions"

        self.content_type_criteria = {
            "text_only": "이미지 0개 - 텍스트만 있는 콘텐츠",
            "image_heavy": "텍스트 100자 미만 + 이미지 1개 이상 - 주로 이미지로 구성",
            "mixed": "텍스트 100자 이상 + 이미지 1개 이상 - 텍스트와 이미지 혼합"
        }
        
        if self.upstage_api_key:
            self.headers = {
                'Authorization': f'Bearer {self.upstage_api_key}',
                'Content-Type': 'application/json'
            }
        else:
            self.headers = {}

    def select_essential_data(self, article_json: Dict) -> Dict:
        """전체 JSON에서 필수 정보만 선별"""
        selected = {
            "title": article_json.get("title", ""),
            "content_type": article_json.get("content_type", "unknown"),
            "content_type_criteria": self.content_type_criteria.get(
                article_json.get("content_type", "unknown"),
                "알 수 없는 타입"
            ),
            "link" : article_json.get("link",""),
            "text_content": article_json.get("text_content", ""),
            "text_length": article_json.get("text_length", 0),
            "image_count": article_json.get("image_count", 0),
            "images": article_json.get("images", [])
        }
        print(f"선별된 데이터: {selected['title']} ({selected['content_type']})")
        return selected

    def _document_parse_file(self, fp: str) -> str:
        """Upstage Document Parse로 이미지/문서를 텍스트로 추출"""
        headers = {"Authorization": f"Bearer {self.upstage_api_key}"}
        data = {"model": "document-parse", "output_formats": '["text"]'}
        with open(fp, "rb") as f:
            files = {"document": (os.path.basename(fp), f)}
            resp = requests.post(self.upstage_doc_url, headers=headers, files=files, data=data, timeout=60)
        resp.raise_for_status()
        j = resp.json()
        container = j.get("content") or j.get("result") or {}
        text = container.get("text") or container.get("plain_text") or ""
        if not text and isinstance(container.get("pages"), list):
            text = "\n".join(p.get("text", "") for p in container["pages"])
        return (text or "").strip()

    def _download_and_parse_images(self, images, save_dir : str | Path = "temp_images" , max_chars=1200):
        """이미지 URL들을 로컬에 저장하고, Document Parse로 텍스트를 뽑아 합쳐서 반환"""
        if not images:
            return "(이미지 없음)", [], []

        save_dir = Path(save_dir)
        
        if not save_dir.is_absolute():
            # 상대 경로로 들어오면 파일 기준으로 붙인다
            save_dir = FILE_DIR / save_dir

        save_dir.mkdir(parents=True, exist_ok=True)

        combined_texts, local_paths, analysis_results = [], [], []

        for i, img_data in enumerate(images, start=1):
            img_url = img_data.get("full_url")
            if not img_url:
                combined_texts.append(f"[이미지 {i}] (URL 누락)")
                continue

            ext = os.path.splitext(urlparse(img_url).path)[1] or ".jpg"
            name = f"img_{i}_{hashlib.md5(img_url.encode()).hexdigest()[:8]}{ext}"
            local_fp = os.path.join(save_dir, name)

            try:
                r = requests.get(img_url, timeout=30)
                r.raise_for_status()
                with open(local_fp, "wb") as f:
                    f.write(r.content)
                local_paths.append(local_fp)

                text = self._document_parse_file(local_fp) or "(텍스트 추출 없음)"
                text = text.replace("\r", " ").strip()
                if len(text) > max_chars:
                    text = text[:max_chars] + "…(생략)"

                combined_texts.append(f"[이미지 {i} 내용]\n{text}")
                analysis_results.append({"image_url": img_url, "extracted_text": text})

            except Exception as e:
                error_msg = f"[이미지 {i}] (다운로드/파싱 실패: {e})"
                combined_texts.append(error_msg)
                analysis_results.append({"image_url": img_url, "error": str(e)})

        return "\n\n".join(combined_texts), local_paths, analysis_results
        
    def create_unified_prompt(self, data: Dict) -> tuple[str, list | None]:
        """통합 프롬프트 생성 (OCR 결과와 함께)"""
        image_text_block = "(이미지 없음)"
        image_analysis_results = None
        
        if self.upstage_api_key and data.get("images"):
            try:
                image_text_block, _, image_analysis_results = self._download_and_parse_images(data["images"])
            except Exception as e:
                print(f"이미지 파싱 실패(무시하고 진행): {e}")
                image_text_block = f"(이미지 처리 중 오류 발생: {e})"

        prompt = f"""당신은 웹사이트 게시글을 분석해서 검색 가능한 텍스트로 변환하는 전문가입니다. 주어진 가이드라인과 게시글 정보를 바탕으로 내용을 변환해주세요.

=== 콘텐츠 타입별 처리 가이드 ===
- text_only: 텍스트만 있는 콘텐츠 → 핵심 내용 요약/정리
- image_heavy: 주로 이미지로 구성된 콘텐츠 → 이미지 정보를 설명 텍스트로 변환, 중요 텍스트가 있으면 포함
- mixed: 텍스트 + 이미지 혼합 → 텍스트와 이미지 정보를 자연스럽게 결합하여 종합적으로 설명

=== 분석할 게시글 정보 ===
제목: {data['title']}
콘텐츠 타입: {data['content_type']} ({data.get('content_type_criteria')})
텍스트 내용:
{data['text_content'] if data.get('text_content') else '(텍스트 없음)'}

이미지에서 추출된 내용:
{image_text_block}

=== 요청사항 ===
1. 위 정보를 바탕으로, 게시글의 핵심 내용을 자연스러운 문장으로 설명해주세요.
2. 이미지가 있다면 그 내용과 의미(중요 수치, 지명, 인물, 행사명 등)를 본문에 녹여내세요.
3. 마지막에 검색에 도움 될 키워드를 5개 이상 쉼표로 구분하여 제시해주세요. (예: 키워드: 부산, 외국인, 지원, 행사, 안내)

결과는 위 요청사항을 반영한 최종 텍스트만 생성해주세요.
"""
        return prompt, image_analysis_results

    def fallback_processing(self, data: Dict) -> ProcessedContent:
        """Upstage Solar API 사용 불가 시 대체 처리"""
        print("📝 대체 처리 방식 사용 중...")
        final_text = f"제목: {data['title']}\n\n내용:\n{data['text_content']}"
        return ProcessedContent(
            original_title=data['title'],
            original_url=data['images'][0]['full_url'] if data['images'] else None,
            content_type=data['content_type'],
            final_text=final_text.strip(),
            processing_method="fallback_rule_based",
            chunk_ready=True
        )

    def analyze_content_with_llm(self, selected_data: Dict) -> ProcessedContent:
        """통합 Upstage Solar 에이전트가 모든 타입을 판단해서 처리"""
        print(f"🤖 Upstage Solar 에이전트로 처리 중: {selected_data['title']}")
        if not self.upstage_api_key:
            print("key is not proper")
            return self.fallback_processing(selected_data)

        prompt, image_analysis_results = self.create_unified_prompt(selected_data)
        
        try:
            payload = {
                "model": "solar-1-mini-chat",
                "messages": [
                    {"role": "system", "content": "당신은 웹사이트 게시글을 분석해서 검색 가능한 텍스트로 변환하는 전문가입니다."},
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 1024, "temperature": 0.2
            }
            response = requests.post(self.api_url, headers=self.headers, json=payload, timeout=90)
            response.raise_for_status()
            result = response.json()

            if 'choices' in result and result['choices']:
                final_text = result['choices'][0]['message']['content'].strip()
                print(f"Solar API 처리 완료: {len(final_text)} 문자")
                return ProcessedContent(
                    original_title=selected_data['title'],
                    original_url=selected_data['link'],
                    content_type=selected_data['content_type'],
                    final_text=final_text,
                    processing_method="upstage_solar_agent",
                    image_analysis_results=image_analysis_results,
                    chunk_ready=True
                )
            else:
                print("Solar API 응답에 문제가 있습니다")
                return self.fallback_processing(selected_data)

        except requests.exceptions.RequestException as e:
            print(f"Solar API 요청 실패: {e}")
            return self.fallback_processing(selected_data)
        except Exception as e:
            print(f"Solar API 처리 중 오류: {e}")
            return self.fallback_processing(selected_data)

    def process_articles_batch(self, articles_json: List[Dict]) -> List[ProcessedContent]:
        """여러 게시글을 일괄 처리"""
        print(f"=== 일괄 처리 시작: {len(articles_json)}개 게시글 ===")
        processed_results = []
        for i, article in enumerate(articles_json):
            print(f"\n--- 게시글 {i+1}/{len(articles_json)} 처리 중 ---")
            selected_data = self.select_essential_data(article)
            result = self.analyze_content_with_llm(selected_data)
            processed_results.append(result)
            if self.upstage_api_key:
                time.sleep(1) # API Rate Limit 방지
        print(f"\n=== 일괄 처리 완료: {len(processed_results)}개 완료 ===")
        return processed_results

    def save_processed_results(self, results: List[ProcessedContent], filename: str):
        """처리 결과 저장 및 통계 출력"""
        output_data = [result.__dict__ for result in results]
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
        print(f"처리 결과 저장 완료: {filename}")
        self.show_processing_stats(results)

    def show_processing_stats(self, results: List[ProcessedContent]):
        """처리 결과 통계"""
        total = len(results)
        success = sum(1 for r in results if r.chunk_ready)
        
        print("\n=== 처리 결과 통계 ===")
        print(f"총 처리: {total}개, 성공: {success}개, 실패: {total - success}개")
        
        methods = {}
        for result in results:
            methods[result.processing_method] = methods.get(result.processing_method, 0) + 1
        print("\n처리 방법별 분포:")
        for method, count in methods.items():
            print(f"  {method}: {count}개")

# --------------------------------------------------------------------
# 1. 핵심 실행 로직을 이 함수 안에 모두 넣습니다.
# --------------------------------------------------------------------
def run_analysis_and_save(input_filename: str, output_filename: str, api_key: Optional[str]):
    """
    추출된 게시글 JSON을 읽어 분석하고, 처리된 결과를 새 JSON 파일로 저장합니다.
    """
    print("=" * 50)
    print("추출된 게시글 분석 및 처리 작업을 시작합니다.")
    print("=" * 50)

    analyzer = ContentAnalyzer(upstage_api_key=api_key)
    
    # --- 여기가 핵심 ---
    # 이 스크립트 파일이 있는 'routers' 폴더의 절대 경로를 찾습니다.
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 위 경로를 기준으로 입력/출력 파일의 전체 경로를 만듭니다.
    input_filepath = os.path.join(script_dir, input_filename)
    output_filepath = os.path.join(script_dir, output_filename)
    # ------------------
    
    try:
        # 수정된 경로를 사용합니다.
        with open(input_filepath, 'r', encoding='utf-8') as f:
            articles_data = json.load(f)
        
        print(f"불러온 게시글 수: {len(articles_data)} (from {input_filepath})")
        
        processed_results = analyzer.process_articles_batch(articles_data)
        # 수정된 경로에 저장합니다.
        analyzer.save_processed_results(processed_results, output_filepath)

    except FileNotFoundError:
        print(f"오류: 입력 파일 '{input_filepath}'을 찾을 수 없습니다.")
        print("크롤링 스크립트를 먼저 실행하여 데이터를 생성해주세요.")
    except Exception as e:
        print(f"\n[오류] 전체 처리 중 예외 발생: {e}")
        traceback.print_exc()

# if __name__ == "__main__": 부분도 base_path 없이 호출하도록 수정합니다.
if __name__ == "__main__":
    config = Config()
    upstage_key = config.upstage_api_key
    
    run_analysis_and_save(
        input_filename="extracted_articles.json",
        output_filename="processed_content.json",
        api_key=upstage_key
    )