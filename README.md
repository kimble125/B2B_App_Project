# The Peak: B2B Data Pipeline & Dashboard

본 레포지토리는 B2B 매칭 플랫폼 MVP 구동을 위해 필요한 코어 기업 데이터(약 13만 개)를 수집, 정제하고 이를 Streamlit 애플리케이션 대시보드로 경영진에게 시각화하여 보고하기까지의 데이터 파이프라인 소스코드를 담고 있습니다.

## 📂 폴더 구조 및 파일 설명

- `streamlit_app.py`: Streamlit 프레임워크를 기반으로 구성된 경영진 보고용 (Data Analysis Report) 메인 대시보드 파일입니다. 
- `crawling/`
  - `innoforest_crawler.py`: 이노포레스트 웹사이트 대상 셀레니움 기반 동적 크롤링 스크립트. (Headless 렌더링 및 봇 우회 로직 포함)
  - `sminfo_crawler.py`: 중소벤처기업부 기업 정보 크롤링 파이프라인. (SSL 회피, Requests Session 유지 및 랜덤 User-Agent 배포 포함)
- `erd/`
  - `The_Peak_Data_Model.md`: Mermaid.js 구조로 작성된 최종 파이프라인 데이터 모델링 명세서.

## 🚀 로컬 환경 기동 가이드 (How to run)

### 1. 사전 요구사항 (Requirements)
Python 3.9+ 이상의 환경이 권장됩니다. 아래 명령어로 필요한 핵심 패키지를 설치하십시오.
```bash
pip install streamlit pandas numpy plotly beautifulsoup4 requests fake-useragent selenium webdriver-manager
```

### 2. 백그라운드 크롤러 구동 (Data Acquisition)
크롤링 스크립트는 `crawling/` 폴더 내에 백그라운드 구동(Headless)으로 작동하도록 최적화되어 있습니다.
```bash
# 이노포레스트 보안 우회 크롤러 (Selenium)
python crawling/innoforest_crawler.py

# 공공기관 등 세션 기반 크롤러 (BS4 + Requests)
python crawling/sminfo_crawler.py
```
> ※ 주의: 스크립트 내부의 `email` 및 `password` 등 자격 증명(Credentials) 변수는 실행 시 본인의 환경에 맞게 수정해야 정상 동작합니다.

### 3. 스트림릿 대시보드 렌더링 (Reporting Dashboard)
단일 커맨드로 웹 브라우저에서 대시보드를 로드할 수 있습니다.
```bash
python3 -m streamlit run streamlit_app.py
```
> **💡 디스크 용량 이슈 안내 (Dummy Distribution)**
> 대시보드 작동 시 수십메가의 CSV를 읽어오는 병목(I/O 리소스 소모)을 막기 위해, `streamlit_app.py` 내부의 `load_realistic_dummy_data()` 함수가 멱법칙 기반(Power Law)으로 실제와 똑같은 13만 개의 랜덤 기업 데이터를 **메모리 상에서 실시간으로 생성**하도록 아키텍처를 구현해 두었습니다. 데이터를 별도로 다운로드할 필요가 없습니다.

---

## 🧠 부록: RAG & HyDE 추천 매칭 아키텍처 로드맵
이 데이터 파이프라인 위에서 검색의 질을 높이기 위한 인턴쉽 갈무리 리포트로, 향후 추천 시스템 고도화(AI 서비스)를 위한 아키텍처 방법론을 작성했습니다.
- [HyDE 로 RAG 향상시키기: 이론과 적용 방안 (공동 저자 전문 링크)](https://www.koreaodm.com/인공지능/hyde로-rag-향상시키기-이론과-적용-방안/)
