"""
3교시 데모 — Layout & Chart
===========================

실행:
    streamlit run app/03_layout_chart.py

내용:
- A. 페이지 레이아웃 (sidebar / columns / empty)
- B. 컨테이너 (container / tabs / expander / popover)
- C. st.form (일괄 제출)
- D. 네이티브 차트 (line / bar / area / scatter / map)
- E. 외부 차트 (Plotly / Matplotlib / Altair) 4종 비교
- F. column_config 심화 (data_editor)
"""

import altair as alt
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# -----------------------------------------------------------------------------
# 페이지 설정 — 가장 먼저
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Layout & Chart",
    page_icon="📐",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": "https://docs.streamlit.io",
        "About": "QA/QC × Streamlit 5시간 강의 — 3교시 데모",
    },
)

# 공통 데이터
np.random.seed(0)
TARGET, USL, LSL = 50.000, 50.200, 49.800
df = pd.DataFrame({
    "측정번호": range(1, 51),
    "외경(mm)": (50 + np.random.randn(50) * 0.08).round(3),
    "라인": np.random.choice(["A", "B"], 50),
})

# -----------------------------------------------------------------------------
# 사이드바 — 섹션 선택
# -----------------------------------------------------------------------------
with st.sidebar:
    st.title("📐 Layout & Chart")
    section = st.radio(
        "섹션",
        [
            "A. 페이지 레이아웃",
            "B. 컨테이너 4종",
            "C. st.form",
            "D. 네이티브 차트",
            "E. 외부 차트 4종 비교",
            "F. column_config 심화",
        ],
    )
    st.divider()
    st.caption(f"규격: {LSL} ~ {USL} mm")

st.title(f"📐 {section}")

# =============================================================================
# A. 페이지 레이아웃
# =============================================================================
if section.startswith("A"):
    st.markdown("### A.1 `st.columns` — 균등 분할")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("측정", "120건")
    c2.metric("합격", "117건")
    c3.metric("불량률", "2.5%", "-0.3%p", delta_color="inverse")
    c4.metric("Cpk", "1.42", "+0.05")

    st.divider()
    st.markdown("### A.2 `st.columns` — 비율 [2,1,1]")
    left, mid, right = st.columns([2, 1, 1])
    left.info("좌측은 비율 2 — 차트를 두기 좋음")
    mid.warning("중간 1")
    right.success("우측 1")

    st.divider()
    st.markdown("### A.3 `st.columns` — gap 옵션 (1.30+)")
    g1, g2, g3 = st.columns(3, gap="large")
    g1.markdown("**gap=large**\n\n넓은 간격")
    g2.markdown("**gap=large**\n\n칸 사이 여유")
    g3.markdown("**gap=large**\n\n시원한 레이아웃")

    st.divider()
    st.markdown("### A.4 `st.empty` — 동적 갱신 자리")
    placeholder = st.empty()
    if st.button("3단계 메시지 시연"):
        import time
        placeholder.info("측정 시작…")
        time.sleep(1)
        placeholder.warning("측정 중…")
        time.sleep(1)
        placeholder.success("측정 완료")
    else:
        placeholder.caption("👆 버튼을 누르면 같은 자리가 덮어쓰여집니다.")


# =============================================================================
# B. 컨테이너 4종
# =============================================================================
elif section.startswith("B"):
    st.markdown("### B.1 `st.container(border=True)`")
    with st.container(border=True):
        st.subheader("이번 측정")
        b1, b2 = st.columns(2)
        b1.metric("외경", "50.012 mm")
        b2.metric("판정", "합격 ✅")

    st.divider()

    st.markdown("### B.2 `st.container(height=...)` — 스크롤 박스")
    with st.container(height=180, border=True):
        for i in range(40):
            st.write(f"측정 #{i+1}: {50 + i*0.005:.3f} mm")

    st.divider()

    st.markdown("### B.3 `st.tabs`")
    tab_s, tab_d, tab_r = st.tabs(["📊 요약", "🔍 상세", "📋 원본"])
    with tab_s:
        st.metric("불량률", "2.5%")
    with tab_d:
        st.write("부분군별 상세 분석…")
        st.bar_chart(df.groupby("라인")["외경(mm)"].mean())
    with tab_r:
        st.dataframe(df.head(10), use_container_width=True, hide_index=True)

    st.divider()

    st.markdown("### B.4 `st.expander`")
    with st.expander("📐 규격 정보 보기"):
        st.write(f"- 목표: **{TARGET} mm**")
        st.write(f"- USL: **{USL} mm**")
        st.write(f"- LSL: **{LSL} mm**")

    st.divider()

    st.markdown("### B.5 `st.popover` (1.32+)")
    with st.popover("🔧 고급 필터"):
        st.text_input("검사자 필터")
        st.selectbox("교대", ["주간", "야간"])
        st.checkbox("이상치 제외")


# =============================================================================
# C. st.form
# =============================================================================
elif section.startswith("C"):
    st.markdown("### `st.form` — 일괄 제출")
    st.caption("위젯을 바꿔도 본문이 재실행되지 않다가, 제출 버튼을 눌렀을 때만 처리됩니다.")

    with st.form("measure_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            operator = st.text_input("검사자")
            line = st.selectbox("라인", ["A", "B", "C"])
        with c2:
            value = st.number_input(
                "외경(mm)", min_value=48.0, max_value=52.0,
                value=50.0, step=0.001, format="%.3f",
            )
            note = st.text_area("비고", height=80)

        submitted = st.form_submit_button("✅ 저장", type="primary")

    if submitted:
        if not operator:
            st.error("검사자를 입력하세요.")
        else:
            pf = "합격" if LSL <= value <= USL else "불합격"
            st.success(f"저장됨 — {operator} / 라인 {line} / {value:.3f} mm / **{pf}**")


# =============================================================================
# D. 네이티브 차트
# =============================================================================
elif section.startswith("D"):
    st.markdown("### D.1 `st.line_chart`")
    st.line_chart(df, x="측정번호", y="외경(mm)", color="라인", height=280)

    st.markdown("### D.2 `st.bar_chart`")
    defects = pd.DataFrame({"유형": ["크기", "스크래치", "이물", "기타"],
                            "건수": [12, 8, 5, 2]})
    st.bar_chart(defects, x="유형", y="건수", height=260)

    st.markdown("### D.3 `st.area_chart`")
    st.area_chart(df, x="측정번호", y="외경(mm)", height=240)

    st.markdown("### D.4 `st.scatter_chart`")
    st.scatter_chart(df, x="측정번호", y="외경(mm)", color="라인", height=280)

    st.markdown("### D.5 `st.map`")
    sites = pd.DataFrame({
        "lat": [37.5665, 35.1796, 35.8714],
        "lon": [126.9780, 129.0756, 128.6014],
    })
    st.map(sites, size=20)


# =============================================================================
# E. 외부 차트 4종 비교
# =============================================================================
elif section.startswith("E"):
    st.markdown("**같은 데이터** 를 4가지 라이브러리로 동시에 그려 비교합니다.")
    st.caption("히스토그램 + USL/LSL 라인 — 어디서 가장 자연스럽게 표현되는지 보세요.")

    c1, c2 = st.columns(2)

    with c1:
        st.markdown("#### 1) 네이티브 — `st.bar_chart`")
        hist, edges = np.histogram(df["외경(mm)"], bins=15)
        hist_df = pd.DataFrame({"bin": edges[:-1].round(3), "건수": hist})
        st.bar_chart(hist_df, x="bin", y="건수", height=280)
        st.caption("⚠️ 규격선 추가 불가, 인터랙티브 제한")

    with c2:
        st.markdown("#### 2) Plotly — `st.plotly_chart` (권장)")
        fig = px.histogram(df, x="외경(mm)", color="라인", nbins=15, opacity=0.7)
        fig.add_vline(x=USL, line_dash="dash", line_color="red",
                      annotation_text="USL")
        fig.add_vline(x=LSL, line_dash="dash", line_color="red",
                      annotation_text="LSL")
        fig.update_layout(height=280, margin=dict(l=0, r=0, t=20, b=0))
        st.plotly_chart(fig, use_container_width=True)
        st.caption("✅ hover, 줌, 규격선, 그룹별 색 모두 자연스러움")

    c3, c4 = st.columns(2)

    with c3:
        st.markdown("#### 3) Matplotlib — `st.pyplot`")
        fig_m, ax = plt.subplots(figsize=(6, 3))
        for line_name, sub in df.groupby("라인"):
            ax.hist(sub["외경(mm)"], bins=15, alpha=0.6, label=line_name)
        ax.axvline(USL, color="red", linestyle="--", label="USL")
        ax.axvline(LSL, color="red", linestyle="--", label="LSL")
        ax.legend()
        ax.set_xlabel("외경(mm)")
        st.pyplot(fig_m, use_container_width=True)
        st.caption("✅ 정적 이미지. 기존 코드 재활용에 강함")

    with c4:
        st.markdown("#### 4) Altair — `st.altair_chart`")
        chart = (
            alt.Chart(df)
            .mark_bar(opacity=0.7)
            .encode(
                alt.X("외경(mm):Q", bin=alt.Bin(maxbins=15)),
                alt.Y("count():Q"),
                color="라인:N",
                tooltip=["라인", "count()"],
            )
            .properties(height=260)
        )
        rule_usl = alt.Chart(pd.DataFrame({"x": [USL]})).mark_rule(
            color="red", strokeDash=[4, 4]
        ).encode(x="x:Q")
        rule_lsl = alt.Chart(pd.DataFrame({"x": [LSL]})).mark_rule(
            color="red", strokeDash=[4, 4]
        ).encode(x="x:Q")
        st.altair_chart((chart + rule_usl + rule_lsl), use_container_width=True)
        st.caption("✅ 선언적, hover 자동, Streamlit 네이티브와 자연스럽게 통합")


# =============================================================================
# F. column_config 심화
# =============================================================================
elif section.startswith("F"):
    st.markdown("### `data_editor` + `column_config` — 표 자체가 입력 폼")
    st.caption("아래 표를 직접 편집해보세요. 우하단 ➕ 로 행 추가, 셀 우클릭으로 삭제.")

    lot_df = pd.DataFrame({
        "로트": ["L-001", "L-002", "L-003", "L-004"],
        "외경평균(mm)": [50.012, 49.985, 50.108, 49.940],
        "합격률": [0.992, 0.968, 0.847, 0.945],
        "재검사": [False, False, True, False],
        "등급": ["A", "B", "C", "B"],
        "리포트": [
            "https://example.com/r/L-001",
            "https://example.com/r/L-002",
            "https://example.com/r/L-003",
            "https://example.com/r/L-004",
        ],
    })

    edited = st.data_editor(
        lot_df,
        num_rows="dynamic",
        use_container_width=True,
        column_config={
            "외경평균(mm)": st.column_config.NumberColumn(
                "외경평균",
                format="%.3f mm",
                min_value=48.0, max_value=52.0,
                step=0.001,
                help="목표 50.000",
            ),
            "합격률": st.column_config.ProgressColumn(
                "합격률",
                format="%.1f%%",
                min_value=0, max_value=1,
            ),
            "재검사": st.column_config.CheckboxColumn(
                "재검사 필요", default=False,
            ),
            "등급": st.column_config.SelectboxColumn(
                "등급", options=["A", "B", "C", "D"], required=True,
            ),
            "리포트": st.column_config.LinkColumn(
                "리포트", display_text="🔗 열기",
            ),
        },
        key="lot_editor",
    )

    st.divider()
    st.markdown("**편집 결과** (실시간 반영)")
    st.dataframe(edited, use_container_width=True, hide_index=True)

    st.caption("✏️ 이 표는 단순 표시가 아니라, 사용자 입력 위젯의 역할까지 합니다.")


# 푸터
st.divider()
st.caption("QA/QC × Streamlit 5시간 강의 · 3교시 데모 · 정강민")
