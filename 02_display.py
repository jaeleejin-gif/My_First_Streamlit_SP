import streamlit as st
import pandas as pd
import numpy as np

st.title("🏭 QC 측정 대시보드")        # 페이지에 보통 하나만
st.header("1. 라인 A 현황")             # 큰 섹션 구분
st.subheader("외경 측정")               # 작은 섹션 구분

st.markdown(
    """
    ### 오늘의 요약
    - **측정 수**: 120건
    - **불량률**: 2.5%
    - **Cpk**: 1.42

    | 라인 | 합격률 |
    |---|---:|
    | A | 99.2% |
    | B | 96.8% |
    """
)

st.metric("Cpk", "1.42")
st.caption("Cpk ≥ 1.33 이면 공정능력 양호로 판단")


st.latex(r"Cpk = \min\left(\frac{USL - \mu}{3\sigma}, \frac{\mu - LSL}{3\sigma}\right)")

st.divider()


df = pd.DataFrame({
    "측정번호": range(1, 6),
    "라인": ["A"] * 5,
    "외경(mm)": [50.012, 49.985, 50.108, 49.940, 50.205],
    "판정": ["합격", "합격", "합격", "합격", "불합격"],
})

st.dataframe(
    df,
    use_container_width=True,   # 가로 폭 가득
    hide_index=True,            # 왼쪽 인덱스 숨김
    height=300,                 # 세로 픽셀
)


df = pd.DataFrame({
    "로트": ["L-001", "L-002", "L-003"],
    "합격률": [0.992, 0.968, 0.847],
    "외경(mm)": [50.012, 49.985, 50.108],
    "재검사": [False, False, True],
    "리포트": [
        "https://example.com/r/L-001",
        "https://example.com/r/L-002",
        "https://example.com/r/L-003",
    ],
})

st.dataframe(
    df,
    use_container_width=True,
    hide_index=True,
    column_config={
        "합격률": st.column_config.ProgressColumn(
            "합격률",
            format="%.1f%%",
            min_value=0, max_value=1,
        ),
        "외경(mm)": st.column_config.NumberColumn(
            "외경",
            format="%.3f mm",
            help="목표 50.000 mm",
        ),
        "재검사": st.column_config.CheckboxColumn(
            "재검사 필요",
            default=False,
        ),
        "리포트": st.column_config.LinkColumn(
            "리포트 URL",
            display_text="🔗 열기",
        ),
    },
)

st.metric(
    label="불량률",
    value="2.5%",
    delta="-0.3%p",         # 전일 대비
    delta_color="inverse",  # 줄어드는 게 좋은 지표 → 음수가 초록
    help="규격을 벗어난 비율",
    label_visibility="visible",  # "hidden" / "collapsed" 도 가능
)

c1, c2, c3, c4 = st.columns(4)
c1.metric("측정 수", "120건", "+15")
c2.metric("합격", "117건", "+12")
c3.metric("불량률", "2.5%", "-0.3%p", delta_color="inverse")
c4.metric("Cpk", "1.42", "+0.05")

import streamlit as st
import pandas as pd
import numpy as np

# 가짜 측정 데이터 (50건)
np.random.seed(0)
data = pd.DataFrame({
    "측정번호": range(1, 51),
    "외경(mm)": 50 + np.random.randn(50) * 0.08,
    "라인": np.random.choice(["A", "B"], 50),
})

# 1) 라인 차트 — 시계열에 적합
st.line_chart(data, x="측정번호", y="외경(mm)", color="라인")

# 2) 막대 차트 — 카테고리별
defects = pd.DataFrame({
    "유형": ["크기", "스크래치", "이물", "기타"],
    "건수": [12, 8, 5, 2],
})
st.bar_chart(defects, x="유형", y="건수")

# 3) 영역 차트
st.area_chart(data, x="측정번호", y="외경(mm)")

# 4) 산점도 — 1.27+ 신규 API
st.scatter_chart(data, x="측정번호", y="외경(mm)", color="라인", size="외경(mm)")

sites = pd.DataFrame({
    "lat": [37.5665, 35.1796, 35.8714],   # 서울, 부산, 대구
    "lon": [126.9780, 129.0756, 128.6014],
    "공장": ["서울", "부산", "대구"],
})
st.map(sites, latitude="lat", longitude="lon", size=20)

