📡 AI PULSE – API Health Monitor
🚀 Overview

AI Pulse is a real-time API monitoring system that tracks the health, response time, and availability of multiple APIs through an interactive dashboard.

❗ Problem Statement

Monitoring APIs manually (e.g., using tools like Postman) is inefficient and does not provide continuous visibility or alerting.

💡 Solution

This project automates API health checks by continuously sending requests, analyzing responses, and displaying real-time status with alert mechanisms.

⚙️ Features
Real-time API monitoring
Status tracking (200, 404, 500, etc.)
Response time measurement
Color-coded health indicators (Green / Yellow / Red)
Email alert system for failures
Concurrent API execution (multithreading)
CSV report download
🧰 Tech Stack
Python
Streamlit
Requests
Pandas
concurrent.futures
streamlit-autorefresh
SMTP (Email alerts)
🧠 How It Works
User adds API endpoints
System sends HTTP requests periodically
Responses are analyzed (status + latency)
Data is stored in session state
Dashboard updates every few seconds
Alerts are triggered on failures
▶️ How to Run Locally
git clone <your-repo-link>
cd <project-folder>
pip install -r requirements.txt
streamlit run app.py
🌐 Live Demo

Deployed on: Streamlit Cloud
https://xvxwxqyd9wskvfvvjotypz.streamlit.app/

⚠️ Limitations
No persistent database (data stored in memory)
Not optimized for large-scale monitoring
Depends on Streamlit refresh model
🔮 Future Improvements
Add database for persistent logging
Implement retry and alert thresholds
Support large-scale API monitoring
Integrate advanced alert systems (Slack, SMS)
