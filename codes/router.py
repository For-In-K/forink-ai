from fastapi import FastAPI
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.executors.pool import ThreadPoolExecutor
import asyncio
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

# 작업 함수
from routers.web_crawling import run_extraction_and_save
from routers.crawled_data_analyze_multimodel import run_analysis_and_save

# 라우터 모듈
from routers import make_roadmap, searching_engine_with_storage_data, home_outline

app = FastAPI(title="통합 AI 서버")

# 스케줄러: 동시 작업은 쓰레드풀 사용, KST 타임존
scheduler = AsyncIOScheduler(
    timezone=ZoneInfo("Asia/Seoul"),
    executors={"default": ThreadPoolExecutor(4)},
)

async def periodic_task_sequence():
    print("주기 작업 시작")
    try:
        # 동기 함수 → 이벤트루프 비블로킹 실행
        await asyncio.to_thread(run_extraction_and_save)
        await asyncio.to_thread(run_analysis_and_save)
        print("주기 작업 완료")
    except Exception as e:
        print(f"주기 작업 오류: {e}")

@app.on_event("startup")
async def startup_event():
    if not scheduler.running:
        scheduler.start()
    # 중복 등록 방지
    if not scheduler.get_job("crawling_and_analysis_task"):
        scheduler.add_job(
            periodic_task_sequence,
            "interval",
            days=3,
            id="crawling_and_analysis_task",
            coalesce=True,                # 밀린 작업 묶기
            misfire_grace_time=3600,      # 1시간 이내 미실행 허용
            next_run_time=datetime.now(ZoneInfo("Asia/Seoul")) + timedelta(seconds=1)  # 즉시 1회
        )
    print("스케줄러 등록 완료")

@app.on_event("shutdown")
def shutdown_event():
    if scheduler.running:
        scheduler.shutdown()
    print("스케줄러 종료")

# API 라우터 연결
app.include_router(make_roadmap.router)
app.include_router(searching_engine_with_storage_data.router)
app.include_router(home_outline.router)

@app.get("/")
def read_root():
    return {"message": "AI 서버가 성공적으로 실행되었습니다."} 