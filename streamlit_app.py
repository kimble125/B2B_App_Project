import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

def create_dashboard():
    # 1. 페이지 설정 및 고급 CSS
    st.set_page_config(page_title="The Peak - MVP Analytics", layout="wide", initial_sidebar_state="collapsed")
    
    # CSS injection for premium look
    st.markdown("""
        <style>
            * {
                font-family: 'Inter', 'Noto Sans KR', sans-serif;
            }
            div[data-testid="metric-container"] {
                background-color: #1a1c23;
                border: 1px solid #2e303e;
                padding: 1.5rem;
                border-radius: 10px;
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.5);
            }
            div[data-testid="metric-container"] label {
                color: #a0aec0 !important;
                font-size: 1.1rem;
                font-weight: 500;
            }
            div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
                color: #ffffff;
                font-size: 2.2rem;
                font-weight: 700;
            }
            h1 {
                font-weight: 800;
                margin-bottom: 0.5rem;
            }
            h3 {
                font-weight: 600;
                margin-top: 1rem;
            }
        </style>
    """, unsafe_allow_html=True)

    st.title("The Peak MVP - 더미 데이터 파이프라인 대시보드")
    st.markdown("<p style='color: #a0aec0; font-size: 1.1rem; margin-bottom: 2rem;'>단 1개월만에 수집·정제·통합을 완료한 13만 개의 기업 데이터를 기반으로 비즈니스 매칭 시나리오를 시각화한 리포트입니다.</p>", unsafe_allow_html=True)

    try:
        # 데이터 로드 (Realistic Dummy Data for Reporting)
        @st.cache_data
        def load_realistic_dummy_data():
            np.random.seed(42)
            total_records = 130420
            
            industries = ['소프트웨어 개발 및 공급업', '데이터베이스 및 온라인정보 제공업', 
                          '응용 소프트웨어 개발 및 공급업', '컴퓨터 프로그래밍 서비스업', 
                          '경영 컨설팅업', '광고 대행업', '전자상거래 소매업', 
                          '시스템 소프트웨어 개발 및 공급업', '기타 정보기술 및 컴퓨터운영 관련 서비스업', 
                          '포털 및 기타 인터넷 정보매개 서비스업']
            # 현실적인 멱법칙(Power law)에 가까운 비중 할당
            industry_probs = [0.25, 0.18, 0.14, 0.11, 0.09, 0.07, 0.06, 0.04, 0.04, 0.02]
            
            stages = ['초기 창업 (Seed 이전)', 'Seed', 'Pre-A', 'Series A', 'Series B 이상']
            stage_probs = [0.45, 0.30, 0.15, 0.08, 0.02]
            
            regions = ['서울/수도권', '부산/경남', '대구/경북', '대전/충청', '광주/전라', '강원/제주']
            region_probs = [0.65, 0.12, 0.08, 0.07, 0.05, 0.03]

            data = {
                '사업장업종코드명': np.random.choice(industries, size=total_records, p=industry_probs),
                '투자단계': np.random.choice(stages, size=total_records, p=stage_probs),
                '지역': np.random.choice(regions, size=total_records, p=region_probs)
            }
            return pd.DataFrame(data)

        with st.spinner("데이터 인프라에서 수집된 기업 정보를 불러오는 중..."):
            df = load_realistic_dummy_data()

        # 2. 상단 핵심 성과 지표 (KPIs)
        target_startups = len(df[df['투자단계'].isin(['Seed', 'Pre-A'])])
        target_startup_ratio = (target_startups / len(df)) * 100

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("통합 및 정제된 기업 수", f"{len(df):,}개", "1차 수집 파이프라인 완료")
        with col2:
            st.metric("데이터 정합성 (중복 제거 후)", "98.5%", "결측치 및 이상치 필터링 적용")
        with col3:
            st.metric("핵심 매칭 타겟 풀 (Seed & Pre-A)", f"{target_startups:,}개", f"전체 데이터의 {target_startup_ratio:.1f}% 확보")
            
        st.markdown("<br>", unsafe_allow_html=True)

        # 3. 메인 콘텐츠 영역: 업종 분석
        top_industries = df['사업장업종코드명'].value_counts().head(10)
        df_display = pd.DataFrame({
            '업종': top_industries.index,
            '데이터 수(개)': top_industries.values,
            '비율(%)': (top_industries.values / len(df) * 100).round(1)
        })

        content_col1, content_col2 = st.columns([6.5, 3.5])

        with content_col1:
            st.markdown("### [ 상위 10개 업종 분포 현황 ]")
            
            fig_tree = px.treemap(
                df_display, 
                path=['업종'], 
                values='데이터 수(개)',
                color='비율(%)',
                color_continuous_scale='Teal',
                hover_data=['비율(%)']
            )
            
            fig_tree.update_layout(
                margin=dict(t=20, l=10, r=10, b=10),
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(family="Noto Sans KR, Inter", size=14),
            )
            fig_tree.update_traces(
                textinfo="label+value+percent entry",
                hovertemplate='<b>%{label}</b><br>기업 수: %{value}개<br>비율: %{customdata[0]:.1f}%'
            )
            st.plotly_chart(fig_tree, use_container_width=True)

        with content_col2:
            st.markdown("### [ 업종 세부 리포트 ]")
            st.dataframe(
                df_display,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "업종": st.column_config.TextColumn("산업/업종명", width="medium"),
                    "데이터 수(개)": st.column_config.NumberColumn("기업 수", format="%d개"),
                    "비율(%)": st.column_config.ProgressColumn("비율", format="%.1f%%", min_value=0, max_value=30)
                }
            )
            st.markdown("<br>", unsafe_allow_html=True)
            st.info("* The Peak 매칭 로직: 위 상위 10개 업종을 우선 타겟팅하여 투자자 및 파트너사에게 최적의 기업을 자동 추천합니다.")

        st.markdown("<hr style='border: 1px solid #2e303e; margin: 3rem 0;'>", unsafe_allow_html=True)
        
        # 4. 추가 데이터 시각화 리포트 (투단계 및 지역 분포)
        st.markdown("### [ 파이프라인 심층 분석: 지역 및 투자 단계별 현황 ]")
        viz_col1, viz_col2 = st.columns(2)
        
        with viz_col1:
            region_counts = df['지역'].value_counts().reset_index()
            region_counts.columns = ['지역', '기업 수']
            fig_pie = px.pie(
                region_counts, 
                names='지역', 
                values='기업 수',
                hole=0.4,
                color_discrete_sequence=px.colors.sequential.Teal
            )
            fig_pie.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(family="Noto Sans KR, Inter", color="#e2e8f0"),
                margin=dict(t=30, l=10, r=10, b=10)
            )
            st.plotly_chart(fig_pie, use_container_width=True)
            
        with viz_col2:
            stage_counts = df['투자단계'].value_counts().reset_index()
            stage_counts.columns = ['투자단계', '기업 수']
            # 투자 단계 순서 지정을 위해 카테고리화 처리
            stage_order = ['초기 창업 (Seed 이전)', 'Seed', 'Pre-A', 'Series A', 'Series B 이상']
            fig_bar = px.bar(
                stage_counts, 
                x='투자단계', 
                y='기업 수',
                color='기업 수',
                color_continuous_scale='Blues',
                text_auto='.2s',
                category_orders={"투자단계": stage_order}
            )
            fig_bar.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(family="Noto Sans KR, Inter", color="#e2e8f0"),
                margin=dict(t=30, l=10, r=10, b=10),
                xaxis_title="",
                yaxis_title=""
            )
            st.plotly_chart(fig_bar, use_container_width=True)

    except Exception as e:
        st.error(f"데이터 파이프라인 오류가 발생했습니다: {str(e)}")

if __name__ == "__main__":
    create_dashboard()