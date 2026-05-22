import time
import numpy as np
import pandas as pd
import streamlit as st

# -----------------------------------------------------------------------------
# 페이지 설정 및 데이터 생성
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Display Gallery",
    page_icon="🖼️",
    layout="wide",
)

# -----------------------------------------------------------------------------
# 사이드바 — 카테고리 선택
# -----------------------------------------------------------------------------
with st.sidebar:
    st.title("🖼️ Display Gallery")
    st.caption("1교시 — Streamlit 출력 API 종합")

    section = st.radio(
        "카테고리",
        [
            "A. write 만능 출력",
            "B. 텍스트 계열",
            "C. 데이터 표시",
            "D. 네이티브 차트",
            "E. 미디어",
            "F. 상태·알림",
        ],
        index=0,
    )


# ==============================
# 2교시 데모 — Widget Playground
import datetime
import pandas as pd
import streamlit as st
# -----------------------------------------------------------------------------
# 페이지 설정
# -----------------------------------------------------------------------------
st.set_page_config(page_title="Widget Playground", page_icon="🎛️", layout="wide")

# 누적 카운터 (콜백 데모용)
if "saved_count" not in st.session_state:
    st.session_state.saved_count = 0
if "callback_log" not in st.session_state:
    st.session_state.callback_log = []

# -----------------------------------------------------------------------------
# 사이드바 — 카테고리 선택
# -----------------------------------------------------------------------------
with st.sidebar:
    st.title("🎛️ Widget Playground")
    st.caption("2교시 — Streamlit Input 위젯 종합")

    section = st.radio(
        "카테고리",
        [
            "A. 클릭형",
            "B. 불리언",
            "C. 선택형",
            "D. 슬라이더",
            "E. 텍스트·숫자",
            "F. 날짜·시간",
            "G. 파일·미디어",
            "H. 기타",
            "I. 콜백 패턴",
        ],
        index=0,
    )

    st.divider()
    st.caption(f"저장 카운터: {st.session_state.saved_count}")

st.title(f"🎛️ {section}")


# =============================================================================
# A. 클릭형
# =============================================================================
if section.startswith("A"):
    st.markdown("### A.1 `st.button` — 기본")
    c1, c2, c3 = st.columns(3)
    if c1.button("측정 기록 저장"):
        st.success("저장 완료")
    if c2.button("🛑 긴급 정지", type="primary", use_container_width=True):
        st.error("라인 정지됨")
    c3.button("비활성", disabled=True, use_container_width=True)

    st.divider()

    st.markdown("### A.2 `st.download_button` — CSV 다운로드")
    df = pd.DataFrame({
        "측정번호": [1, 2, 3],
        "외경(mm)": [50.012, 49.985, 50.108],
        "판정": ["합격", "합격", "합격"],
    })
    csv = df.to_csv(index=False).encode("utf-8-sig")
    st.download_button(
        "📥 측정 데이터 CSV 다운로드",
        data=csv,
        file_name="measurements_sample.csv",
        mime="text/csv",
    )

    st.divider()

    st.markdown("### A.3 `st.link_button` — 외부 링크")
    st.link_button("📊 Streamlit 공식 문서 열기", "https://docs.streamlit.io")

    st.markdown("### A.4 `st.page_link` — 멀티페이지 (5교시에서 활용)")
    st.info("멀티페이지 앱이 있을 때 활성화됩니다. 호출 형태는 다음과 같습니다.")
    st.code('st.page_link("pages/3_📈_SPC.py", label="SPC 페이지", icon="📈")',
            language="python")



# =============================================================================
# B. 불리언
# =============================================================================
elif section.startswith("B"):
    st.markdown("### B.1 `st.checkbox`")
    recheck = st.checkbox("재검사 필요", value=False)
    if recheck:
        st.warning("재검사 항목으로 등록됨")

    qa_agree = st.checkbox("측정 결과를 검토하고 동의합니다")
    pdf_export = st.checkbox("PDF 자동 첨부")
    st.write({"재검사": recheck, "동의": qa_agree, "PDF": pdf_export})

    st.divider()

    st.markdown("### B.2 `st.toggle` — 큰 모드 전환에 적합")
    realtime = st.toggle("실시간 측정 모드", value=False)
    dark = st.toggle("다크 모드 시뮬레이션")
    st.write({"실시간": realtime, "다크": dark})



# =============================================================================
# C. 선택형
# =============================================================================
elif section.startswith("C"):
    st.markdown("### C.1 `st.radio`")
    method = st.radio(
        "판정 방식",
        ["자동 (규격 기준)", "수동 (작업자 입력)"],
        horizontal=True,
        captions=["LSL/USL 자동 비교", "검사자가 직접 입력"],
    )

    st.markdown("### C.2 `st.selectbox`")
    line = st.selectbox("라인 선택", ["A", "B", "C", "D", "E"])

    st.markdown("### C.3 `st.multiselect`")
    defects = st.multiselect(
        "발견된 결점 유형 (복수 선택)",
        options=["크기", "스크래치", "이물", "크랙", "변형", "기타"],
        default=["크기"],
        max_selections=3,
    )

    st.markdown("### C.4 `st.pills` (1.36+)")
    try:
        shifts = st.pills(
            "측정 시간대",
            options=["주간", "야간", "주말"],
            selection_mode="multi",
            default=["주간"],
        )
    except AttributeError:
        st.info("Streamlit 1.36 이상 필요")
        shifts = None

    st.markdown("### C.5 `st.segmented_control` (1.36+)")
    try:
        view_mode = st.segmented_control(
            "보기 모드",
            options=["요약", "상세", "원본"],
            default="요약",
        )
    except AttributeError:
        st.info("Streamlit 1.36 이상 필요")
        view_mode = None

    st.divider()
    st.write({
        "판정방식": method,
        "라인": line,
        "결점": defects,
        "시간대": shifts,
        "보기": view_mode,
    })


# =============================================================================
# D. 슬라이더
# =============================================================================
elif section.startswith("D"):
    st.markdown("### D.1 `st.slider` — 단일 숫자")
    n = st.slider("샘플 수", 1, 100, 30, step=1)

    st.markdown("### D.2 `st.slider` — 범위 (튜플)")
    lsl, usl = st.slider(
        "규격 범위 (mm)",
        min_value=49.0, max_value=51.0,
        value=(49.8, 50.2),
        step=0.001, format="%.3f",
    )
    st.write(f"LSL={lsl}, USL={usl}")

    st.markdown("### D.3 날짜 슬라이더")
    start = datetime.date(2026, 4, 1)
    end = datetime.date(2026, 5, 18)
    period = st.slider("분석 기간", min_value=start, max_value=end, value=(start, end))
    st.write(f"{period[0]} ~ {period[1]}")

    st.markdown("### D.4 `st.select_slider` — 이산 옵션")
    grade = st.select_slider("등급", options=["F", "D", "C", "B", "A", "S"], value="B")
    st.metric("선택 등급", grade)



# =============================================================================
# E. 텍스트·숫자
# =============================================================================
elif section.startswith("E"):
    st.markdown("### E.1 `st.text_input`")
    operator = st.text_input(
        "검사자", value="정00", max_chars=20,
        placeholder="이름을 입력하세요",
        help="사번이 아닌 실명",
    )
    pwd = st.text_input("관리자 비밀번호", type="password")

    st.markdown("### E.2 `st.text_area`")
    note = st.text_area(
        "검사 비고", height=120, max_chars=500,
        placeholder="예) 공구 교체 직후, 신규 작업자 첫 측정 등",
    )

    st.markdown("### E.3 `st.number_input` — 외경 측정값")
    value = st.number_input(
        "외경 측정값 (mm)",
        min_value=48.000, max_value=52.000,
        value=50.000, step=0.001,
        format="%.3f",
        help="단위 mm. 소수점 셋째자리까지",
    )

    st.divider()
    st.write({
        "검사자": operator,
        "비밀번호길이": len(pwd) if pwd else 0,
        "비고": note,
        "측정값": value,
    })



# =============================================================================
# F. 날짜·시간
# =============================================================================
elif section.startswith("F"):
    st.markdown("### F.1 `st.date_input` — 단일")
    d = st.date_input("검사 일자", value=datetime.date.today())

    st.markdown("### F.2 `st.date_input` — 범위")
    period = st.date_input(
        "분석 기간",
        value=(datetime.date(2026, 4, 1), datetime.date.today()),
        min_value=datetime.date(2026, 1, 1),
        max_value=datetime.date.today(),
    )

    st.markdown("### F.3 `st.time_input`")
    shift_start = st.time_input("교대 시작 시각", value=datetime.time(8, 0))

    st.divider()
    st.write({
        "검사일자": str(d),
        "분석기간": str(period),
        "교대시작": str(shift_start),
    })



# =============================================================================
# G. 파일·미디어 입력
# =============================================================================
elif section.startswith("G"):
    st.markdown("### G.1 `st.file_uploader`")
    uploaded = st.file_uploader("측정 데이터 파일", type=["csv", "xlsx"])
    if uploaded is not None:
        if uploaded.name.endswith(".csv"):
            df = pd.read_csv(uploaded)
        else:
            df = pd.read_excel(uploaded)
        st.success(f"{uploaded.name} — {len(df)}행")
        st.dataframe(df.head(), use_container_width=True)

    st.divider()

    st.markdown("### G.2 `st.camera_input` — 결점 사진 촬영")
    photo = st.camera_input("결점 부위 촬영 (카메라 권한 필요)")
    if photo is not None:
        st.image(photo, caption="촬영된 사진")

    st.divider()

    st.markdown("### G.3 `st.audio_input` — 음성 메모 (1.31+)")
    try:
        voice = st.audio_input("음성 메모 녹음")
        if voice:
            st.audio(voice)
    except AttributeError:
        st.info("Streamlit 1.31 이상 필요")

    st.divider()

    st.markdown("### G.4 `st.data_editor` — 편집 가능한 표")
    base = pd.DataFrame({
        "측정번호": [1, 2, 3],
        "외경(mm)": [50.012, 49.985, 50.108],
        "재검사": [False, False, True],
    })
    edited = st.data_editor(
        base,
        num_rows="dynamic",
        use_container_width=True,
        column_config={
            "외경(mm)": st.column_config.NumberColumn(
                format="%.3f mm",
                min_value=48.0, max_value=52.0,
                step=0.001,
            ),
            "재검사": st.column_config.CheckboxColumn(),
        },
        key="editor_demo",
    )
    st.caption("표 우하단의 ➕ 버튼으로 행 추가, 셀 우클릭으로 삭제")
    st.write("편집 결과:", edited)



# =============================================================================
# H. 기타
# =============================================================================
elif section.startswith("H"):
    st.markdown("### H.1 `st.color_picker`")
    color = st.color_picker("관리도 라인 색상", value="#1f77b4")
    st.markdown(
        f"<div style='background:{color}; padding:20px; border-radius:6px; color:white;'>"
        f"선택된 색: {color}</div>",
        unsafe_allow_html=True,
    )

    st.divider()

    st.markdown("### H.2 `st.feedback` (1.34+)")
    try:
        c1, c2, c3 = st.columns(3)
        with c1:
            st.write("별점")
            stars = st.feedback(options="stars")
        with c2:
            st.write("표정")
            faces = st.feedback(options="faces")
        with c3:
            st.write("좋/싫")
            thumbs = st.feedback(options="thumbs")
        st.write({"별점": stars, "표정": faces, "좋싫": thumbs})
    except AttributeError:
        st.info("Streamlit 1.34 이상 필요")


# =============================================================================
# I. 콜백 패턴
# =============================================================================
elif section.startswith("I"):
    st.markdown("### I.1 `key=` 와 `session_state` 자동 연결")
    st.text_input("검사자 (key='operator')", key="operator", value="정강민")
    st.write(f"`st.session_state.operator` = `{st.session_state.operator}`")

    st.divider()

    st.markdown("### I.2 `on_change` 콜백 — 규격 이탈 시 토스트")

    def alert_out_of_spec():
        v = st.session_state.measure_val
        if v > 50.2 or v < 49.8:
            st.toast(f"⚠️ 규격 이탈! {v:.3f} mm", icon="⚠️")
            st.session_state.callback_log.append(f"OOS: {v:.3f}")
        else:
            st.session_state.callback_log.append(f"OK: {v:.3f}")

    st.number_input(
        "외경 측정값",
        min_value=48.0, max_value=52.0,
        value=50.0, step=0.001, format="%.3f",
        key="measure_val",
        on_change=alert_out_of_spec,
        help="값을 49.8 미만 또는 50.2 초과로 바꿔보세요",
    )

    st.divider()

    st.markdown("### I.3 `args` / `kwargs` — 콜백에 인자 전달")

    def log_change(widget_name, source):
        st.session_state.callback_log.append(f"{widget_name}({source}) 변경")
        st.toast(f"{widget_name} 변경됨", icon="🔄")

    st.selectbox(
        "라인",
        ["A", "B", "C"],
        key="line_select",
        on_change=log_change,
        args=("라인",),
        kwargs={"source": "selectbox"},
    )

    st.divider()

    st.markdown("### I.4 `on_click` — 버튼 전용")

    def save_record():
        st.session_state.saved_count += 1
        st.session_state.callback_log.append(f"저장 #{st.session_state.saved_count}")

    st.button("측정 저장 (on_click 콜백)", on_click=save_record)
    st.metric("누적 저장", st.session_state.saved_count)

    st.divider()

    st.markdown("### 콜백 호출 로그 (최근 10건)")
    st.code("\n".join(st.session_state.callback_log[-10:][::-1]) or "(없음)")
    if st.button("로그 초기화"):
        st.session_state.callback_log = []
        st.rerun()


# 푸터
st.divider()

