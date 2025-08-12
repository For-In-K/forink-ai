import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
from typing import List, Dict, Optional
from dataclasses import dataclass
import json
import os
import traceback # 오류 추적을 위해 추가

@dataclass
class ArticleInfo:
    """개별 글 정보"""
    title: str
    link: str
    date: str
    views: str
    content_html: str = ""
    content_type: str = ""
    processed_content: str = ""

class TargetExtractor:
    """BFWC 사이트 타겟 추출기"""
    
    def __init__(self):
        self.base_url = "https://bfwc.or.kr"
        self.main_url = "https://bfwc.or.kr/kr/index.php?pCode=MN0000025&pg=1"
        
        # 요청 헤더 설정
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
    
    def get_page_content(self, url: str) -> Optional[BeautifulSoup]:
        """페이지 내용 가져오기"""
        try:
            print(f"페이지 요청 중: {url}")
            response = requests.get(url, headers=self.headers, timeout=10)
            response.encoding = 'utf-8'
            
            if response.status_code == 200:
                return BeautifulSoup(response.content, 'html.parser')
            else:
                print(f"HTTP 오류: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"페이지 요청 실패: {e}")
            return None
    
    def extract_article_links(self) -> List[ArticleInfo]:
        """메인 페이지에서 글 링크들 추출"""
        print("=== 메인 페이지 글 링크 추출 시작 ===")
        
        soup = self.get_page_content(self.main_url)
        if not soup:
            print("메인 페이지 로드 실패")
            return []
        
        articles = []
        
        # 클래스 이름이 'child_1' 또는 'child_2'인 <tr> 찾기 (기존 'child1'에서 수정)
        article_rows = soup.find_all('tr', class_=['child_1', 'child_2'])
        
        print(f"발견된 글 수: {len(article_rows)}")
        
        for i, row in enumerate(article_rows):
            try:
                # 글 번호 추출
                num_cell = row.find('td', class_='f-num num')
                
                # 제목과 링크 추출
                title_cell = row.find('td', class_='f-tit subject')
                if title_cell:
                    link_tag = title_cell.find('a')
                    if link_tag and link_tag.get('href'):
                        title = link_tag.get_text(strip=True)
                        relative_link = link_tag['href']
                        full_link = urljoin(self.base_url, relative_link)
                        
                        # 날짜 추출
                        date_cell = row.find('td', class_='f-date date')
                        date = date_cell.get_text(strip=True) if date_cell else "날짜 없음"
                        
                        # 조회수 추출
                        views_cell = row.find('td', class_='f-hits read')
                        views = views_cell.get_text(strip=True) if views_cell else "0"
                        
                        article = ArticleInfo(
                            title=title,
                            link=full_link,
                            date=date,
                            views=views
                        )
                        
                        articles.append(article)
                        # print(f"글 {i+1}: {title} | {date} | 조회수: {views}")
                        
            except Exception as e:
                print(f"글 {i+1} 파싱 오류: {e}")
                continue
        
        print(f"총 {len(articles)}개 글 링크 추출 완료")
        return articles
    
    def extract_board_contents(self, article_url: str) -> Optional[str]:
        """개별 글 페이지에서 <div id="boardContents"> 내용 추출"""
        # print(f"글 내용 추출 중: {article_url}")
        
        soup = self.get_page_content(article_url)
        if not soup:
            print("글 페이지 로드 실패")
            return None
        
        # <div id="boardContents"> 찾기
        board_contents = soup.find('div', id='boardContents')
        
        if board_contents:
            content_html = str(board_contents)
            # print(f"boardContents 추출 성공 (크기: {len(content_html)} 문자)")
            return content_html
        else:
            print("boardContents div를 찾을 수 없음")
            # 대안으로 다른 콘텐츠 영역 찾기
            alternatives = [
                soup.find('div', class_='board-view-contents'),
                soup.find('div', class_='content'),
                soup.find('div', class_='view-content')
            ]
            
            for alt in alternatives:
                if alt:
                    print(f"대안 콘텐츠 영역 발견: {alt.get('class')}")
                    return str(alt)
            
            return None
    
    def analyze_content_structure(self, content_html: str) -> Dict[str, any]:
        """콘텐츠 구조 분석"""
        soup = BeautifulSoup(content_html, 'html.parser')
        
        text_content = soup.get_text(strip=True, separator="\n")
        text_length = len(text_content)
        
        images = soup.find_all('img')
        image_count = len(images)
        
        image_info = []
        for img in images:
            src = img.get('src', '')
            full_url = urljoin(self.base_url, src) if src else ''
            
            img_data = {
                'src': src,
                'full_url': full_url
            }
            image_info.append(img_data)
        
        links = soup.find_all('a')
        link_count = len(links)
        
        if image_count == 0:
            content_type = "text_only"
        elif text_length < 100 and image_count > 0:
            content_type = "image_heavy"
        elif text_length > 100 and image_count > 0:
            content_type = "mixed"
        else:
            content_type = "unknown"
        
        analysis = {
            'content_type': content_type,
            'text_content': text_content,
            'text_length': text_length,
            'image_count': image_count,
            'images': image_info,
            'link_count': link_count
        }
        
        return analysis
    
    def process_all_articles(self, max_articles: int = 5) -> List[ArticleInfo]:
        """모든 글 처리 (테스트용으로 최대 개수 제한)"""
        print("=== 전체 글 처리 시작 ===")
        
        articles = self.extract_article_links()
        
        if not articles:
            print("추출할 글이 없습니다")
            return []
        
        if max_articles > 0:
            articles = articles[:max_articles]
            print(f"처리할 글 수를 {len(articles)}개로 제한")
        
        processed_articles = []
        
        for i, article in enumerate(articles):
            print(f"\n--- 글 {i+1}/{len(articles)} 처리 중: {article.title} ---")
            
            content_html = self.extract_board_contents(article.link)
            
            if content_html:
                analysis = self.analyze_content_structure(content_html)
                
                article.content_html = content_html
                article.content_type = analysis['content_type']
                
                print(f"콘텐츠 타입: {analysis['content_type']} | 텍스트 길이: {analysis['text_length']} | 이미지 수: {analysis['image_count']}")
                processed_articles.append(article)
            else:
                print("콘텐츠 추출 실패")
            
            time.sleep(1)
        
        print(f"\n=== 처리 완료: {len(processed_articles)}개 글 성공 ===")
        return processed_articles
    
    def save_results(self, articles: List[ArticleInfo], filename: str = "extracted_articles.json"):
        """결과를 JSON 파일로 저장"""
        results = []
        
        for article in articles:
            if article.content_html:
                analysis = self.analyze_content_structure(article.content_html)
                
                result = {
                    'title': article.title,
                    'link': article.link,
                    'date': article.date,
                    'views': article.views,
                    'content_type': article.content_type,
                    'text_content': analysis['text_content'],
                    'text_length': analysis['text_length'],
                    'image_count': analysis['image_count'],
                    'images': analysis['images'],
                    'link_count': analysis['link_count'],
                    'content_html': article.content_html
                }
            else:
                result = {
                    'title': article.title,
                    'link': article.link,
                    'date': article.date,
                    'views': article.views,
                    'content_type': "extraction_failed",
                    'text_content': "", 'text_length': 0,
                    'image_count': 0, 'images': [],
                    'link_count': 0, 'content_html': ""
                }
            
            results.append(result)
        
        script_dir = os.path.dirname(os.path.abspath(__file__))
        full_path = os.path.join(script_dir, filename)
        
        with open(full_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        print(f"\n결과 저장 완료: {full_path}")
        print(f"저장된 글 수: {len(results)}")
        
        text_only = sum(1 for r in results if r['content_type'] == 'text_only')
        image_heavy = sum(1 for r in results if r['content_type'] == 'image_heavy') 
        mixed = sum(1 for r in results if r['content_type'] == 'mixed')
        
        print(f"콘텐츠 타입 분포: 텍스트만({text_only}) | 이미지위주({image_heavy}) | 혼합({mixed})")

# --------------------------------------------------------------------
# 1. 핵심 실행 로직을 이 함수 안에 모두 넣습니다.
# --------------------------------------------------------------------
def run_extraction_and_save(max_articles: int = 10):
    """
    웹사이트에서 글을 추출하고 분석하여 JSON 파일로 저장하는 전체 과정을 실행합니다.
    """
    print("=" * 50)
    print("웹사이트 글 추출 및 분석 작업을 시작합니다.")
    print("=" * 50)
    
    extractor = TargetExtractor()
    
    try:
        # 1. 전체 처리 (최대 개수 지정)
        processed_articles = extractor.process_all_articles(max_articles=max_articles)
        
        # 2. 결과 저장
        if processed_articles:
            extractor.save_results(processed_articles)
        else:
            print("처리된 글이 없어 저장할 내용이 없습니다.")
            
    except Exception as e:
        print(f"\n[오류] 전체 처리 중 예외 발생: {e}")
        traceback.print_exc()

# --------------------------------------------------------------------
# 2. 이 스크립트를 직접 실행할 때만 아래 코드가 동작합니다.
#    이제 이 파일의 핵심 기능은 위 함수를 통해 어디서든 호출할 수 있습니다.
# --------------------------------------------------------------------
if __name__ == "__main__":
    # 이제 스크립트의 모든 작업은 이 함수 하나를 호출해서 실행할 수 있습니다.
    # 예를 들어 FastAPI의 스케줄러에서 이 함수를 그대로 호출하면 됩니다.
    run_extraction_and_save(max_articles=10)