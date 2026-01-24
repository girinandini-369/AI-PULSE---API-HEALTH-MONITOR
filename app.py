import streamlit as st
import requests
import pandas as pd
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
import smtplib
from email.mime.text import MIMEText

# ---------------- PAGE ----------------
st.set_page_config(page_title="AI PULSE – API Health Monitor", layout="wide")
st.title("📡 AI PULSE – API Health Monitor")

# ---------------- AUTO REFRESH (CRITICAL) ----------------
from streamlit_autorefresh import st_autorefresh
st_autorefresh(interval=3000, key="pulse")  # 3 seconds

# ---------------- EMAIL CONFIG ----------------
SENDER_EMAIL = "richiesgarden333@gmail.com"
SENDER_PASSWORD = "pktf uuas udwn lrib"   # App password
RECEIVER_EMAIL = "richiesgarden333@gmail.com"

# ---------------- SESSION ----------------
if "apis" not in st.session_state:
    st.session_state.apis = []
if "data" not in st.session_state:
    st.session_state.data = []
if "running" not in st.session_state:
    st.session_state.running = False
if "alert_sent" not in st.session_state:
    st.session_state.alert_sent = set()

# ---------------- STYLE ----------------
st.markdown("""
<style>
.card{padding:14px;border-radius:12px;text-align:center;color:white;font-weight:bold;}
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

# ---------------- API LIST ----------------
st.write("### 📌 Monitored APIs")
for i, api in enumerate(st.session_state.apis):
    c1, c2 = st.columns([8,1])
    c1.write(api)
    if c2.button("❌", key=f"del_{i}"):
        st.session_state.apis.pop(i)

# ---------------- CONTROLS ----------------
c1,c2,c3 = st.columns(3)
if c1.button("▶ Start Monitoring"):
    st.session_state.running = True
if c2.button("⏸ Stop Monitoring"):
    st.session_state.running = False
if c3.button("🧹 Clear Data"):
    st.session_state.data = []
    st.session_state.alert_sent.clear()

# ---------------- STATUS MAP ----------------
STATUS_MAP = {
    200: "OK – API working normally",
    400: "Bad Request",
    401: "Unauthorized",
    403: "Forbidden",
    404: "Not Found",
    408: "Timeout",
    429: "Rate Limited",
    500: "Internal Server Error",
    502: "Bad Gateway",
    503: "Service Unavailable",
    504: "Gateway Timeout"
}

# ---------------- EMAIL ALERT ----------------
def send_alert(api, status, issue):
    if api in st.session_state.alert_sent:
        return
    try:
        body = f"""
API FAILURE ALERT

API: {api}
Status: {status}
Issue: {issue}
Time: {datetime.now()}
"""
        msg = MIMEText(body)
        msg["Subject"] = "AI PULSE – API Alert"
        msg["From"] = SENDER_EMAIL
        msg["To"] = RECEIVER_EMAIL

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)

        st.session_state.alert_sent.add(api)
    except:
        pass

# ---------------- API CALL ----------------
def call_api(api):
    try:
        start = datetime.now()
        r = requests.get(api, timeout=10)
        time_ms = round((datetime.now() - start).total_seconds()*1000, 2)
        issue = STATUS_MAP.get(r.status_code, "Unknown status")
        return {
            "Time": datetime.now().strftime("%H:%M:%S"),
            "API": api,
            "Status": r.status_code,
            "Response Time (ms)": time_ms,
            "Issue": issue
        }
    except requests.exceptions.Timeout:
        return {
            "Time": datetime.now().strftime("%H:%M:%S"),
            "API": api,
            "Status": "TIMEOUT",
            "Response Time (ms)": None,
            "Issue": "API did not respond in time"
        }
    except requests.exceptions.ConnectionError:
        return {
            "Time": datetime.now().strftime("%H:%M:%S"),
            "API": api,
            "Status": "CONNECTION ERROR",
            "Response Time (ms)": None,
            "Issue": "Connection failed"
        }

# ---------------- MONITOR LOOP ----------------
if st.session_state.running and st.session_state.apis:
    with ThreadPoolExecutor(max_workers=len(st.session_state.apis)) as executor:
        results = executor.map(call_api, st.session_state.apis)
        for r in results:
            st.session_state.data.append(r)

# ---------------- DATA ----------------
st.session_state.data = st.session_state.data[-300:]
df = pd.DataFrame(st.session_state.data)

# ---------------- HEALTH CARDS ----------------
if not df.empty:
    st.subheader("🟢 API Health Cards")
    cols = st.columns(len(st.session_state.apis))

    for i, api in enumerate(st.session_state.apis):
        last = df[df["API"]==api].tail(1)
        if last.empty:
            cols[i].markdown("<div class='card gray'>Waiting…</div>", unsafe_allow_html=True)
            continue

        s = last["Status"].values[0]
        t = last["Response Time (ms)"].values[0]
        issue = last["Issue"].values[0]

        if not isinstance(s, int) or s != 200:
            color = "red"
            send_alert(api, s, issue)
        elif t and t > 1000:
            color = "yellow"
        else:
            color = "green"

        cols[i].markdown(
            f"<div class='card {color}'>{api.split('//')[-1]}<br>{s} | {issue}<br>⏱ {t} ms</div>",
            unsafe_allow_html=True
        )

# ---------------- LOG TABLE ----------------
if not df.empty:
    st.subheader("📋 Live API Events (Auto-Updating)")
    st.dataframe(df.tail(50), use_container_width=True)

# ---------------- DOWNLOAD ----------------
if not df.empty:
    st.download_button("⬇ Download Report", df.to_csv(index=False), "api_pulse_report.csv")
