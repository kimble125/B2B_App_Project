import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import squarify

def create_treemap():
    # 페이지 설정
    st.set_page_config(page_title="국민연금 사업장 업종 분석", layout="wide")
    st.title("국민연금 가입 사업장 업종 분석")

    try:
        # 데이터 로드 (Dummy Data for Portfolio Demo)
        @st.cache_data
        def load_dummy_data():
            # Dummy industries and counts
            data = {
                '사업장업종코드명': ['소프트웨어 개발 및 공급업', '데이터베이스 및 온라인정보 제공업', 
                               '응용 소프트웨어 개발 및 공급업', '컴퓨터 프로그래밍 서비스업', 
                               '경영 컨설팅업', '광고 대행업', '전자상거래 소매업', 
                               '시스템 소프트웨어 개발 및 공급업', '기타 정보기술 및 컴퓨터운영 관련 서비스업', 
                               '포털 및 기타 인터넷 정보매개 서비스업'] * 50
            }
            df = pd.DataFrame(data)
            return df

        df = load_dummy_data()

        # 업종 분석
        top_industries = df['사업장업종코드명'].value_counts().head(10)
        top_industries_pct = (top_industries / len(df) * 100).round(2)
        
        # for display metric
        matched_companies = ["Demo Company " + str(i) for i in range(500)]

        # 시각화
        fig, ax = plt.subplots(figsize=(15, 10))
        # 폰트 설정 (Streamlit Cloud 호환)
        import os
        import matplotlib.font_manager as fm

        # 폰트 설정 (Streamlit Cloud 호환 - FontProperties 직접 사용)
        import os
        import matplotlib.font_manager as fm

        @st.cache_resource
        def get_font_prop():
            # 리눅스(Streamlit Cloud) 환경 등에서 한글 폰트가 없을 경우 다운로드
            font_path = "NanumGothic.ttf"
            if not os.path.exists(font_path):
                import urllib.request
                url = "https://github.com/google/fonts/raw/main/ofl/nanumgothic/NanumGothic-Regular.ttf"
                urllib.request.urlretrieve(url, font_path)
            
            # 폰트 프로퍼티 객체 생성
            return fm.FontProperties(fname=font_path)

        font_prop = get_font_prop()

        # 데이터 준비
        sizes = top_industries_pct.values
        labels = top_industries_pct.index
        percentages = top_industries_pct.values
        labels_with_pct = [f'{label}\n({pct:.1f}%)' for label, pct in zip(labels, percentages)]

        # 색상 정의
        colors = ['#3498db', '#2ecc71', '#9b59b6', '#e74c3c', '#f1c40f', 
                 '#e67e22', '#1abc9c', '#34495e', '#95a5a6', '#16a085']

        # 트리맵 생성
        squarify.plot(sizes=sizes, 
                     label=labels_with_pct,
                     color=colors,
                     alpha=0.8,
                     text_kwargs={'fontsize': 12, 'fontproperties': font_prop})

        plt.title('상위 10개 업종 비율', fontsize=16, pad=20, fontproperties=font_prop)
        plt.axis('off')
        plt.tight_layout()

        # Streamlit에 시각화 표시
        st.pyplot(fig)

        # 데이터 테이블 표시
        st.subheader("상위 10개 업종 상세 정보")
        df_display = pd.DataFrame({
            '업종': labels,
            '비율(%)': percentages
        })
        st.dataframe(df_display)

        # 통계 정보 표시
        col1, col2 = st.columns(2)
        with col1:
            st.metric("분석된 총 회사 수", f"{len(matched_companies):,}개") 
        
        with col2:
            st.metric("상위 10개 업종 비율 합계", f"{sum(percentages):.1f}%")

    except Exception as e:
        st.error(f"오류가 발생했습니다: {str(e)}")

if __name__ == "__main__":
    create_treemap()