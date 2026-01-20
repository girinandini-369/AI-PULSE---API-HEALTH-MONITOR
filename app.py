import streamlit as st
import requests
import pandas as pd
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

# ---------------- PAGE ----------------
st.set_page_config(page_title="AI PULSE :API Health Monitor", layout="wide")
st.title("📡 Minimal API Health Monitor")

# ---------------- SAFE AUTO REFRESH ----------------
AUTO_REFRESH_INTERVAL = 3  # seconds

# Try using st_autorefresh if available
try:
    from streamlit_autorefresh import st_autorefresh
    st_autorefresh(interval=AUTO_REFRESH_INTERVAL*1000, key="refresh")
    auto_refresh_enabled = True
except ModuleNotFoundError:
    st.warning("streamlit_autorefresh not installed. Using manual refresh instead.")
    auto_refresh_enabled = False

# Manual refresh fallback
if not auto_refresh_enabled:
    if "last_refresh" not in st.session_state:
        st.session_state.last_refresh = datetime.now()
    if st.button("🔄 Refresh API Data"):
        st.session_state.last_refresh = datetime.now()

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
c1, c2 = st.columns([1,1])
with c1:
    if st.button("Add API"):
        if api_input and api_input not in st.session_state.apis:
            st.session_state.apis.append(api_input)
            st.success("API added")
with c2:
    if st.button("Clear All APIs"):
        st.session_state.apis = []
        st.session_state.data = []
        st.success("Cleared all APIs and data!")

# ---------------- API LIST ----------------
st.write("### 📌 Monitored APIs")
for i, api in enumerate(st.session_state.apis):
    c1, c2 = st.columns([8,1])
    c1.write(f"{i+1}. {api}")
    with c2:
        if st.button("❌", key=f"remove_{i}"):
            st.session_state.apis.pop(i)

# ---------------- CONTROLS ----------------
c1,c2,c3 = st.columns(3)
with c1:
    if st.button("▶ Start Monitoring"):
        st.session_state.running = True
with c2:
    if st.button("⏸ Stop Monitoring"):
        st.session_state.running = False
with c3:
    if st.button("🧹 Clear Data"):
        st.session_state.data = []

# ---------------- API CALL FUNCTION ----------------
def call_api(api):
    try:
        start = datetime.now()
        r = requests.get(api, timeout=10)
        response_time = round((datetime.now() - start).total_seconds()*1000, 2)
        if r.status_code == 200:
            message = "✅ Healthy"
        else:
            message = f"❌ Status {r.status_code}"
        status = r.status_code
    except requests.exceptions.Timeout:
        status = "TIMEOUT"
        response_time = None
        message = "⏳ Timeout"
    except requests.exceptions.ConnectionError:
        status = "CONNECTION ERROR"
        response_time = None
        message = "❌ Connection Error"
    except Exception as e:
        status = "ERROR"
        response_time = None
        message = f"❌ {str(e)}"
    return {"Time": datetime.now(), "API": api, "Status": status, "Response Time (ms)": response_time, "Message": message}

# ---------------- MONITOR LOOP ----------------
if st.session_state.running and st.session_state.apis:
    with ThreadPoolExecutor(max_workers=len(st.session_state.apis)) as executor:
        results = executor.map(call_api, st.session_state.apis)
        for r in results:
            st.session_state.data.append(r)

# Keep memory limited
st.session_state.data = st.session_state.data[-1000:]
df = pd.DataFrame(st.session_state.data)

# ---------------- API HEALTH CARDS ----------------
if not df.empty:
    st.subheader("🟢 API Health Cards")
    cols = st.columns(len(st.session_state.apis))
    for i, api in enumerate(st.session_state.apis):
        last = df[df["API"]==api].tail(1)
        if not last.empty:
            s = last["Status"].values[0]
            t = last["Response Time (ms)"].values[0]
            msg = last["Message"].values[0]
            if s != 200 and isinstance(s,int):
                color="red"; txt=f"❌ {s}"
            elif s != 200 and isinstance(s,str):
                color="red"; txt=f"{msg}"
            elif t is None:
                color="gray"; txt="⏳"
            elif t>2000:
                color="red"; txt=f"⚠ {t} ms"
            elif t>1000:
                color="yellow"; txt=f"⚡ {t} ms"
            else:
                color="green"; txt=f"✅ {t} ms"
        else:
            color="gray"; txt="⏳"
        cols[i].markdown(f"<div class='card {color}'>{api.split('//')[-1]}<br>{txt}</div>", unsafe_allow_html=True)

# ---------------- LIVE TABLE ----------------
if not df.empty:
    st.subheader("📋 Live API Logs")
    st.dataframe(df.tail(25), use_container_width=True)

# ---------------- DOWNLOAD ----------------
if not df.empty:
    st.download_button("⬇ Download CSV", df.to_csv(index=False), "api_report.csv")
