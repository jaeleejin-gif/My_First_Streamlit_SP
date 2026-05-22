import streamlit as st 
import pandas as pd 
import numpy as np

st.set_page_config(page_title="Hello QAQC", page_icon="", layout="wide")

TARGET, USL, LSL = 50.000, 50.200, 49.800

np.random.seed(0) 
df = pd.DataFrame({ "측정번호": range(1, 21), "외경(mm)": (50 + np.random.randn(20) * 0.08).round(3), }) 
df["판정"] = df["외경(mm)"].apply( lambda v: "합격" if LSL <= v <= USL else "불합격" )

st.title(" Hello QAQC") 
st.dataframe(df, use_container_width=True, hide_index=True) 
st.line_chart(df, x="측정번호", y="외경(mm)")