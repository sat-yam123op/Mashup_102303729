# 🎵 Mashup Generator Web Application

A Python-based **Web Service + CLI Tool** that automatically generates a music mashup from YouTube videos of a specified singer and sends the final mashup to the user's email.

The system downloads videos, extracts audio, trims clips, merges them, and delivers the final mashup file — fully automated.

---

## 📌 Project Objective

This project implements:

* ✅ Command-Line Mashup Generator
* ✅ Web-Based Mashup Service (Flask)
* ✅ Automated Audio Processing Pipeline
* ✅ Email Delivery System
* ✅ Production-ready Deployment Setup (Gunicorn compatible)

---

## ⚙️ Methodology

### Step 1 — User Input

The user provides:

* Singer Name
* Number of Videos (**must be > 10**)
* Clip Duration in seconds (**must be > 20**)
* Email ID

---

### Step 2 — Video Download

* YouTube videos fetched using **yt-dlp**
* Automatic search-based retrieval
* Long playlist videos filtered out
* Only valid song-length videos downloaded

---

### Step 3 — Audio Processing

* Audio extracted from downloaded videos
* Processed using **MoviePy + FFmpeg**
* Each clip trimmed to requested duration
* Converted to uniform audio format

---

### Step 4 — Mashup Creation

* Trimmed clips concatenated
* Final mashup exported as `.mp3`
* Clean merge using pydub

---

### Step 5 — Email Delivery

* Output compressed into ZIP file
* Sent via Gmail SMTP using **App Password authentication**
* Implemented using yagmail

---

### Step 6 — Production Setup

* Flask web server
* Gunicorn compatible
* Environment variables for credential security
* `.env` based configuration

---

## 🛠️ Technologies Used

* Python
* Flask
* yt-dlp
* MoviePy
* pydub
* FFmpeg
* yagmail
* Gunicorn

---

## 💻 How to Run Locally

### Install dependencies

```bash
pip install -r requirements.txt
```

---

### Set environment variables

Create `.env` file:

```
email_user=your_email_here
email_pass=your_app_password_here
```

---

### Run the application

```bash
python app.py
```

---

### Open in browser

```
http://127.0.0.1:10000
```

---

## 🖥️ Command Line Usage

You can also run the mashup generator directly:

```bash
python 102303729.py "singer name" <videos> <duration_sec> <output.mp3>
```

Example:

```bash
python 102303729.py "arijit singh" 11 25 mashup.mp3
```

---

## 📊 Features

* Automatically downloads multiple songs
* Filters out long playlists
* Extracts and trims clips
* Merges into final mashup
* Validates user inputs
* Handles download failures gracefully
* Sends final mashup via email
* Works as CLI + Web App

---

## 🔐 Environment Variables Required

For email delivery:

```
email_user
email_pass
```

Use **Gmail App Password** — never your real Gmail password.

---

## 📁 Project Structure

```
app.py
mashup.py
102303729.py
requirements.txt
.env.example
.gitignore
```

---

## 👨‍💻 Author

**Satyam Gupta**
Roll No: **102303729**

---

## 📄 License

Academic Project — Educational Use
