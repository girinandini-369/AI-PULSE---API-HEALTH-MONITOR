import streamlit as st
import requests
import pandas as pd
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from streamlit_autorefresh import st_autorefresh

# ---------------- PAGE ----------------
st.set_page_config(page_title="API Health Monitor Real-Time Dashboard", layout="wide")
st.title("📡 API Health Monitor – Real-Time Dashboard")

# ---------------- AUTO REFRESH ----------------
st_autorefresh(interval=3000, key="refresh")

# ---------------- SESSION ----------------
if "apis" not in st.session_state:
    st.session_state.apis = []

if "data" not in st.session_state:
    st.session_state.data = []

if "running" not in st.session_state:
    st.session_state.running = False

# ---------------- STYLE ----------------
st.markdown("""
<style>
.card{padding:12px;border-radius:10px;text-align:center;color:white;font-weight:bold;}
.green{background:#2ecc71;}
.yellow{background:#f1c40f;color:black;}
.red{background:#e74c3c;}
.gray{background:#95a5a6;}
</style>
""", unsafe_allow_html=True)

# ---------------- ADD API ----------------
st.subheader("➕ Add API")

api_input = st.text_input("Paste API URL")

if st.button("Add API"):
    if api_input and api_input not in st.session_state.apis:
        st.session_state.apis.append(api_input)
        st.success("API added")

# ---------------- API LIST ----------------
st.write("### 📌 Monitored APIs")

for api in st.session_state.apis:
    c1, c2 = st.columns([8,1])
    c1.write(api)
    if c2.button("❌", key=api):
        st.session_state.apis.remove(api)

# ---------------- CONTROLS ----------------
c1,c2,c3 = st.columns(3)

if c1.button("▶ Start Monitoring"):
    st.session_state.running = True

if c2.button("⏸ Stop Monitoring"):
    st.session_state.running = False

if c3.button("🧹 Clear Data"):
    st.session_state.data = []

# ---------------- API CALL ----------------
def call_api(api):
    try:
        start = datetime.now()
        r = requests.get(api, timeout=10)
        time_ms = round((datetime.now() - start).total_seconds()*1000,2)
        return api, r.status_code, time_ms
    except:
        return api, "ERROR", None

# ---------------- MONITOR LOOP ----------------
if st.session_state.running and st.session_state.apis:

    with ThreadPoolExecutor() as ex:
        results = ex.map(call_api, st.session_state.apis)

        for r in results:
            st.session_state.data.append({
                "Time": datetime.now(),
                "API": r[0],
                "Status": r[1],
                "Response Time (ms)": r[2]
            })

# keep memory small
st.session_state.data = st.session_state.data[-150:]

df = pd.DataFrame(st.session_state.data)

# ---------------- CARDS ----------------
if not df.empty:
    st.subheader("🟢 API Health Cards")

    cols = st.columns(len(st.session_state.apis))

    for i, api in enumerate(st.session_state.apis):
        last = df[df["API"]==api].tail(1)

        if not last.empty:
            s = last["Status"].values[0]
            t = last["Response Time (ms)"].values[0]

            if s != 200:
                color="red"; txt=f"❌ {s}"
            elif t>2000:
                color="red"; txt=f"⚠ {t} ms"
            elif t>1000:
                color="yellow"; txt=f"⚡ {t} ms"
            else:
                color="green"; txt=f"✅ {t} ms"
        else:
            color="gray"; txt="⏳"

        cols[i].markdown(
            f"<div class='card {color}'>{api.split('//')[-1]}<br>{txt}</div>",
            unsafe_allow_html=True
        )

# ---------------- TABLE ----------------
if not df.empty:
    st.subheader("📋 Live API Logs")
    st.dataframe(df.tail(25), use_container_width=True)

# ---------------- GRAPH ----------------
if not df.empty:
    st.subheader("📈 Response Time Graph")

    df["API_SAFE"] = df["API"].str.replace(r"[^A-Za-z0-9]","_",regex=True)
    df["T"] = df["Time"].dt.strftime("%H:%M:%S")

    graph = df.pivot(index="T", columns="API_SAFE", values="Response Time (ms)")
    graph = graph.fillna(method="ffill")

    st.line_chart(graph)   # Streamlit auto gives different colors

# ---------------- DOWNLOAD ----------------
if not df.empty:
    st.download_button("⬇ Download CSV", df.to_csv(index=False), "api_report.csv")
