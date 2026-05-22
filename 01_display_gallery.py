"""
1교시 데모 — Display Gallery
============================

실행:
    cd ~/Desktop/QAQC_streamlit
    streamlit run app/01_display_gallery.py

목적:
    1교시에서 배운 Display API 들을 한 페이지에서 카테고리별로 시연.
    예제 데이터는 모두 자동차 부품 외경 측정 시나리오 사용.

다루는 API:
    write / markdown / title / header / subheader / caption / code / latex
    divider / dataframe (+ column_config) / table / json / metric
    line_chart / bar_chart / area_chart / scatter_chart / map
    image / audio / video / logo
    success / info / warning / error / exception / toast / balloons / snow
    progress / spinner
"""

import time
import numpy as np
import pandas as pd
import streamlit as st

# -----------------------------------------------------------------------------
# 페이지 설정
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Display Gallery",
    page_icon="🖼️",
    layout="wide",
)

# 공통 예제 데이터
np.random.seed(0)
TARGET, USL, LSL = 50.000, 50.200, 49.800

measurements = pd.DataFrame({
    "측정번호": range(1, 51),
    "라인": np.random.choice(["A", "B"], 50),
    "외경(mm)": (50 + np.random.randn(50) * 0.08).round(3),
})
measurements["판정"] = measurements["외경(mm)"].apply(
    lambda v: "합격" if LSL <= v <= USL else "불합격"
)