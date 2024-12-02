# SMINFO_DB_Project

## 프로젝트 설명
중소기업현황시스템 데이터로 크롤링을 통해 데이터베이스를 구축하여 Peak의 DB 구축에 이용합니다.

## 주요 작업 및 최종 결과물
- 중소기업현황시스템에 기제된 정보의 ERD 작성 → 필요 정보 확정 → 최종 ERD 산출
- 회사명, 주소, 업종 데이터 등 크롤링(셀레니움 활용) → 크롤링 코드, raw데이터
- 데이터를 MySQL에 저장 → 최종 DB

SME_DB_Project/
├── README.md           # 프로젝트 설명
├── erd/                # ERD 관련 파일
│   └── schema.png      # ERD 이미지
├── sql/                # 데이터베이스 스키마 및 쿼리
│   └── schema.sql      # 테이블 생성 SQL
├── crawler/            # 크롤링 코드
│   └── main.py         # 크롤링 스크립트
└── data/               # 크롤링 결과 데이터
    └── companies.csv   # CSV 형식 데이터    
