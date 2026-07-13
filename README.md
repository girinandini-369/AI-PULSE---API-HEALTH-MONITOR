# 📡 AI PULSE – API Health Monitor

![Python](https://img.shields.io/badge/Python-3.x-brightgreen)
![Streamlit](https://img.shields.io/badge/Dashboard-Streamlit-ff4b4b)
![Status](https://img.shields.io/badge/Monitoring-Real--time-blue)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

**🔗 Live Demo:** [xvxwxqyd9wskvfvvjotypz.streamlit.app](https://xvxwxqyd9wskvfvvjotypz.streamlit.app/)

> Note: Streamlit Community Cloud apps sleep after inactivity — the first load may take ~20–30s to wake up, and you may see a "Yes, get this app back up!" button you need to click.

---

## 🚀 Overview

AI Pulse is a real-time API monitoring system that tracks the health, response time, and availability of multiple APIs through an interactive dashboard.

---

## ❗ Problem Statement

Monitoring APIs manually (e.g., using tools like Postman) is inefficient and does not provide continuous visibility or alerting.

---

## 💡 Solution

This project automates API health checks by continuously sending requests, analyzing responses, and displaying real-time status with alert mechanisms.

---

## ⚙️ Features

- ✅ Real-time API monitoring
- 📊 Status tracking (200, 404, 500, etc.)
- ⏱️ Response time measurement
- 🟢 Color-coded health indicators (Green / Yellow / Red)
- 📧 Email alert system for failures
- ⚡ Concurrent API execution (multithreading)
- 📥 CSV report download

---

## 🧰 Tech Stack

| Tool                   | Purpose                     |
| ----------------------- | ----------------------------- |
| Python                   | Core language                  |
| Streamlit                | Dashboard UI                   |
| Requests                 | HTTP health checks             |
| Pandas                   | Data handling & CSV export     |
| concurrent.futures        | Multithreaded API polling      |
| streamlit-autorefresh     | Auto-refresh dashboard         |
| SMTP                      | Email alert system             |

---

## 🧠 How It Works

1. User adds API endpoints to monitor
2. System sends HTTP requests periodically
3. Responses are analyzed (status code + latency)
4. Data is stored in Streamlit session state
5. Dashboard updates every few seconds
6. Alerts are triggered on failures

---

## 📁 Project Structure

```
ai-pulse/
├── app.py               # Main Streamlit app
├── monitor.py           # API health check logic
├── alert.py             # Email alert system
├── utils.py             # Helper functions
├── requirements.txt     # Python dependencies
└── README.md
```

---

## ▶️ How to Run Locally

```
git clone <your-repo-link>
cd ai-pulse
pip install -r requirements.txt
streamlit run app.py
```

### requirements.txt

```
streamlit
requests
pandas
streamlit-autorefresh
```

---

## 📸 Screenshots

> *(Add dashboard screenshots here)*

---

## ⚠️ Limitations

- No persistent database — data is stored in memory only
- Not optimized for large-scale or high-frequency monitoring
- Dependent on Streamlit's refresh model

---

## 🔮 Future Improvements

- [ ] Add database (SQLite / PostgreSQL) for persistent logging
- [ ] Implement retry logic and configurable alert thresholds
- [ ] Support large-scale API monitoring
- [ ] Integrate advanced alert channels (Slack, SMS, webhooks)
- [ ] Add uptime percentage and SLA tracking
- [ ] Historical trend charts and analytics

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you'd like to change.
