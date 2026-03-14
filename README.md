<p align="center">
  <img src="https://img.shields.io/badge/GramCare%20AI-Rural%20TeleHealth-0d9488?style=for-the-badge&logo=hospital&logoColor=white" alt="GramCare AI Banner"/>
</p>

<h1 align="center">🏥 GramCare AI — Rural TeleHealth Access System</h1>

<p align="center">
  <strong>Bridging the healthcare gap between rural patients and healthcare providers through a low-bandwidth telemedicine platform</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Hackathon-UAI%20Hawk--A--Thon%202026-blueviolet?style=flat-square" alt="Hackathon"/>
  <img src="https://img.shields.io/badge/Team-The%20DOMinators-orange?style=flat-square" alt="Team"/>
  <img src="https://img.shields.io/badge/Status-Prototype-green?style=flat-square" alt="Status"/>
  <img src="https://img.shields.io/badge/License-MIT-blue?style=flat-square" alt="License"/>
</p>

<p align="center">
  <a href="#-features">Features</a> •
  <a href="#-system-architecture">Architecture</a> •
  <a href="#-tech-stack">Tech Stack</a> •
  <a href="#-installation-guide">Installation</a> •
  <a href="#-how-to-run">How to Run</a> •
  <a href="#-demo">Demo</a>
</p>

---

## 📋 Table of Contents

- [Problem Statement](#-problem-statement)
- [Solution Overview](#-solution-overview)
- [Features](#-features)
- [System Architecture](#-system-architecture)
- [Tech Stack](#-tech-stack)
- [Dataset Information](#-dataset-information)
- [AI Model Explanation](#-ai-model-explanation)
- [AI Chatbot Explanation](#-ai-chatbot-explanation)
- [Installation Guide](#-installation-guide)
- [How to Run the Project](#-how-to-run-the-project)
- [API Endpoints](#-api-endpoints)
- [Database Setup](#-database-setup)
- [Folder Structure](#-folder-structure)
- [Demo Instructions](#-demo-instructions)
- [Future Improvements](#-future-improvements)
- [Contributors](#-contributors)
- [License](#-license)

---

## 🏥 Problem Statement

Access to healthcare in rural India remains critically limited. **Nabha Civil Hospital** in Punjab serves patients from **173 villages** with only **11 out of 23 sanctioned doctors** — less than 50% staffing. Patients, mostly farmers and daily-wage workers, travel long distances losing an entire day's wages, often to find specialists unavailable or medicines out of stock.

**Key Statistics:**
- 48% doctor vacancy rate at Nabha Civil Hospital
- Only 31% of rural Punjab households have reliable internet
- Patients travel 20–50+ km for basic medical consultations
- Daily-wage workers lose ₹500–₹1000 per hospital visit

### Core Challenges
| Challenge | Impact |
|-----------|--------|
| Doctor Shortage | Long wait times, specialist unavailability |
| Distance & Transport | 20–50 km travel on poor roads |
| Economic Loss | Full day's wages lost per visit |
| Low Internet Access | Only 31% have reliable connectivity |
| Low Digital Literacy | Patients unfamiliar with technology |
| Language Barrier | Primary language is Punjabi; Hindi secondary |
| Medicine Stockouts | Wasted trips when medicines unavailable |

---

## 💡 Solution Overview

**GramCare AI** is a **Progressive Web App (PWA)** based telemedicine platform designed specifically for low-bandwidth, low-literacy rural environments. It enables rural patients to access healthcare remotely through:

- **Teleconsultation** with video, audio, and text chat modes
- **AI-powered symptom checker** for instant health triage
- **AI healthcare chatbot** that communicates in Punjabi/Hindi/English
- **Medicine search** with generic alternative suggestions
- **Digital health records** accessible anytime

> **Impact**: A 15-minute teleconsultation replaces a full lost work day.

---

## ✨ Features

### Patient Module
- 🤖 **AI Symptom Checker** — Select symptoms, get AI-powered disease predictions with severity scores
- 💬 **AI Healthcare Chatbot** — Conversational health assistant in Punjabi/Hindi/English
- 📹 **Teleconsultation** — Video/audio/chat with doctor
- 💊 **Medicine Search** — Search medicines and find affordable generic alternatives
- 📋 **Digital Health Records** — Complete medical history
- 🔐 **Secure Auth** — JWT-based authentication with bcrypt password hashing

### Doctor Module
- 📊 **Patient Queue** — Priority-sorted by severity with AI triage data
- 📝 **Consultation Management** — Complete consultations with diagnosis, prescription, and notes
- 📂 **Patient History** — Instant access to previous health records
- 🟢 **Availability Toggle** — Go online/offline with one click

### AI & Intelligence
- 🧠 **Ensemble ML Model** — Random Forest + Gradient Boosting for 90%+ accuracy disease prediction
- ⚖️ **Severity Scoring** — Weighted symptom analysis for triage levels (Low/Medium/High)
- 🗨️ **Multilingual Chatbot** — Intent classification for healthcare conversations (15 intents)
- 💊 **Medicine Intelligence** — Generic alternative finder from 240MB medicines database

---

## 🏗️ System Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                       CLIENT LAYER                               │
│  ┌──────────────────┐  ┌───────────────────────────────────────┐ │
│  │  React 18 PWA    │  │  Components:                          │ │
│  │  react-router    │  │  SymptomChecker, Chatbot, Dashboard,  │ │
│  │  axios           │  │  MedicineSearch, Consultation, etc.   │ │
│  └────────┬─────────┘  └───────────────────┬───────────────────┘ │
└───────────┼─────────────────────────────────┼────────────────────┘
            │          HTTPS / REST API       │
┌───────────┼─────────────────────────────────┼────────────────────┐
│           ▼                                 ▼                    │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │            Python Flask — API Server (Port 5000)           │  │
│  │            (JWT Auth, CORS, Blueprint Routes)              │  │
│  └─────┬──────────┬──────────┬──────────┬──────────┬─────────┘  │
│        │          │          │          │          │              │
│  ┌─────▼────┐ ┌───▼────┐ ┌──▼───┐ ┌───▼────┐ ┌───▼──────────┐  │
│  │  Auth    │ │Consult │ │Pharm │ │Symptom │ │  Chatbot     │  │
│  │  Routes  │ │ Routes │ │Routes│ │ Routes │ │  Routes      │  │
│  └──────────┘ └────────┘ └──────┘ └───┬────┘ └───┬──────────┘  │
│                                       │          │              │
│  ┌────────────────────────────────────┘          │              │
│  │                                               │              │
│  │  ┌─────────────────────┐  ┌───────────────────▼───────────┐  │
│  └──▶  AI Symptom Checker │  │  Healthcare Chatbot           │  │
│     │  (Ensemble Model:   │  │  (Regex NLP, 15 intents,     │  │
│     │   RF + GBT + Voting)│  │   Multilingual PA/HI/EN)     │  │
│     └──────────┬──────────┘  └───────────────────────────────┘  │
│                │                                                 │
│     ┌──────────▼──────────┐                                     │
│     │  Severity Scorer    │                                     │
│     │  (Weighted Triage)  │                                     │
│     └─────────────────────┘                                     │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │                   MongoDB (Port 27017)                      │ │
│  │  Collections: users, health_records, consultations          │ │
│  └─────────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Frontend** | React 18, React Router 6, Axios | PWA with component-based UI |
| **Styling** | Custom CSS (App.css) | Responsive, mobile-first design |
| **Icons** | react-icons (Font Awesome) | UI iconography |
| **Backend** | Python Flask 3.1 | REST API server |
| **Auth** | flask-jwt-extended, bcrypt | JWT token auth + password hashing |
| **CORS** | flask-cors | Cross-origin request handling |
| **Database** | MongoDB (PyMongo) | Document-based health records |
| **ML Models** | scikit-learn, XGBoost | Ensemble symptom prediction |
| **Model I/O** | joblib | Model serialization |
| **Data** | pandas, numpy | Dataset processing |
| **Chatbot** | Custom regex NLP | 15 healthcare intents, multilingual |

---

## 📊 Dataset Information

All datasets are located in the `datasets/` directory.

| Dataset | File | Size | Description |
|---------|------|------|-------------|
| Disease-Symptom Mapping | `dataset.csv` | 637 KB | Maps diseases to up to 17 symptoms; primary training data |
| Clean Binary Matrix | `clean_dataset.tsv` | 1.3 MB | Binary-encoded symptom-disease matrix |
| Augmented Dataset | `Final_Augmented_dataset_Diseases_and_Symptoms.csv` | 190 MB | 377-symptom augmented data |
| Symptom Severity | `Symptom-severity.csv` | 2.4 KB | Severity weight (1–7) for 133 symptoms |
| Disease Descriptions | `symptom_Description.csv` | 11 KB | Patient-friendly disease descriptions |
| Disease Precautions | `symptom_precaution.csv` | 3.5 KB | 4 precautionary actions per disease |
| Medicine Database | `medicines.csv` | 240 MB | Medicine names, prices, manufacturers, generics |
| EHR Records | `EHR.csv` | 342 KB | Sample electronic health records |
| Lung Cancer Risk | `lung_cancer.csv` | 11 KB | Lung cancer risk factor data |

### Dataset Usage

- **Symptom Checker Training**: `dataset.csv` → binary feature matrix → ensemble model
- **Severity Scoring**: `Symptom-severity.csv` → weighted triage calculation
- **Patient Education**: `symptom_Description.csv` + `symptom_precaution.csv` → shown after prediction
- **Medicine Search**: `medicines.csv` → pharmacy search API (first 5000 records cached)
- **Chatbot Knowledge**: Auto-generated from disease descriptions + precautions

---

## 🧠 AI Model Explanation

### Symptom Checker — ML Pipeline

```
Input: Patient symptoms (e.g., ["fever", "headache", "joint_pain"])
                    │
                    ▼
        ┌─────────────────────┐
        │  Binary Encoding    │  Convert to feature vector
        │  [0,0,1,0,1,...,1]  │  (1 = symptom present)
        └──────────┬──────────┘
                   │
        ┌──────────▼──────────┐
        │  Ensemble Model     │
        │  (VotingClassifier) │
        │  ┌────────────────┐ │
        │  │ Random Forest  │ │  n_estimators=200
        │  │ (200 trees)    │ │  max_depth=30
        │  └────────────────┘ │
        │  ┌────────────────┐ │
        │  │ Gradient       │ │  n_estimators=150
        │  │ Boosting       │ │  learning_rate=0.1
        │  └────────────────┘ │
        │  Soft Voting        │  Averaged probabilities
        └──────────┬──────────┘
                   │
        ┌──────────▼──────────┐
        │  Severity Scoring   │  Σ(symptom weights)
        │  LOW (≤5)           │  from Symptom-severity.csv
        │  MEDIUM (≤10)       │
        │  HIGH (>10)         │
        └──────────┬──────────┘
                   │
                   ▼
        Output: Top 5 diseases with confidence %,
                severity level, description, precautions,
                action recommendation
```

**Model Performance:**
- **Accuracy**: 90%+ (stratified 5-fold cross-validation)
- **Diseases Covered**: 41+ common conditions
- **Symptoms Supported**: 133 symptoms
- **Inference Time**: <100ms per prediction

**Safety**: The model always recommends doctor consultation for HIGH severity predictions. It provides guidance, not diagnosis.

---

## 🤖 AI Chatbot Explanation

### Custom Healthcare Chatbot

```
User Input ("Mujhe 3 din se bukhar hai")
         │
         ▼
┌─────────────────┐
│ Regex Pattern   │  15 intent patterns with
│ Matching        │  multilingual keywords
│ (PA/HI/EN)     │  (Punjabi, Hindi, English)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Intent Match    │  greeting, symptom_check, fever,
│                 │  cold_cough, stomach, headache,
│                 │  emergency, medicine_search,
│                 │  find_doctor, health_tips,
│                 │  diabetes, records, help,
│                 │  thanks, bye
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Response +      │  Contextual reply + optional
│ Action          │  action (navigate_symptoms,
│                 │  navigate_medicines, call_108)
└─────────────────┘
         │
         │  If no intent match:
         ▼
┌─────────────────┐
│ Disease Info    │  Search disease name in
│ Fallback        │  knowledge base
└─────────────────┘
```

### Supported Intents

| Intent | Example | Action |
|--------|---------|--------|
| `greeting` | "Sat Sri Akal" / "Namaste" | Welcome message |
| `symptom_check` | "Mujhe bimaari hai" | Navigate to Symptom Checker |
| `fever` | "Bukhar hai" | Fever advice + triage |
| `emergency` | "Bohot bleeding ho rahi" | Emergency: Call 108 |
| `medicine_search` | "Paracetamol chahiye" | Navigate to Medicine Search |
| `find_doctor` | "Doctor se milna hai" | Find available doctors |
| `health_tips` | "Sehat ke tips batao" | Health advice |
| `diabetes` | "Sugar control kaise karu" | Diabetes management |

---

## 📥 Installation Guide

### Prerequisites

| Software | Version | Download |
|----------|---------|----------|
| **Python** | 3.9 – 3.12 | [python.org](https://python.org/) |
| **Node.js** | 18.x or later | [nodejs.org](https://nodejs.org/) |
| **MongoDB** | 6.0+ | [mongodb.com](https://www.mongodb.com/try/download/community) |
| **Git** | Latest | [git-scm.com](https://git-scm.com/) |

### Clone the Repository

```bash
git clone https://github.com/the-dominators/gramcare-ai.git
cd gramcare-ai
```

---

## 🚀 How to Run the Project

### Step 1: Start MongoDB

```bash
mongod
```

### Step 2: Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (macOS/Linux)
# source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Train the AI model (first time only)
cd ../ai-service
pip install -r ../backend/requirements.txt
python train_model.py
cd ../backend

# Seed demo data
python seed_data.py

# Start the server
python app.py
```

Backend runs on **http://localhost:5000**

### Step 3: Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

Frontend runs on **http://localhost:3000**

### Verify Setup

Open `http://localhost:3000` in your browser. You should see the GramCare AI login page.

**Demo Credentials:**
| Role | Email | Password |
|------|-------|----------|
| Patient | gurpreet@gramcare.in | patient123 |
| Doctor | dr.kaur@gramcare.in | doctor123 |

**Health Check:**
```bash
curl http://localhost:5000/api/health
```

---

## 🔌 API Endpoints

### Authentication
```
POST   /api/auth/register     Register new patient/doctor
POST   /api/auth/login        Login and get JWT token
GET    /api/auth/me           Get current user profile
```

### Symptom Checker
```
POST   /api/symptoms/check    Submit symptoms → AI predictions
GET    /api/symptoms/list     Get all supported symptoms
GET    /api/symptoms/diseases List all diseases
```

### Chatbot
```
POST   /api/chatbot/message   Send message → get reply
GET    /api/chatbot/quick-replies  Get quick reply options
```

### Consultations
```
POST   /api/consultations/            Book consultation
GET    /api/consultations/<id>        Get consultation details
PUT    /api/consultations/<id>        Update (diagnosis, prescription)
GET    /api/consultations/patient     Patient's consultations
GET    /api/consultations/doctor      Doctor's consultations
```

### Medicine / Pharmacy
```
GET    /api/medicines/search?q=<query>      Search medicines
GET    /api/medicines/generic/<name>        Find generic alternatives
GET    /api/medicines/by-disease/<disease>  Medicines for disease
```

### Patient Records
```
GET    /api/patients/records      Get health records
POST   /api/patients/records      Create health record
GET    /api/patients/profile      Get patient profile
PUT    /api/patients/profile      Update patient profile
```

### Doctor
```
GET    /api/doctors/available            List available doctors
GET    /api/doctors/queue                Severity-sorted patient queue
POST   /api/doctors/toggle-availability  Toggle online/offline
```

---

## 🗄️ Database Setup

### MongoDB Collections

**users**
```json
{
  "name": "Gurpreet Singh",
  "email": "gurpreet@gramcare.in",
  "password": "<bcrypt hash>",
  "role": "patient",
  "phone": "+91-98765-43210",
  "age": 42, "gender": "male", "village": "Bhadson",
  "created_at": "2026-01-15T10:00:00Z"
}
```

**consultations**
```json
{
  "patient_id": "<ObjectId>",
  "doctor_id": "<ObjectId>",
  "reason": "Persistent fever and headache",
  "symptoms": ["fever", "headache"],
  "severity": "MEDIUM",
  "status": "scheduled",
  "diagnosis": "", "prescription": "", "notes": "",
  "chat_messages": [],
  "created_at": "2026-01-15T10:30:00Z"
}
```

**health_records**
```json
{
  "patient_id": "<ObjectId>",
  "doctor_name": "Dr. Harpreet Kaur",
  "diagnosis": "Viral Fever",
  "symptoms": ["fever", "headache", "fatigue"],
  "prescription": "Paracetamol 500mg x 3 days",
  "notes": "Rest and hydration",
  "created_at": "2026-01-15T11:00:00Z"
}
```

### Seed Demo Data

```bash
cd backend
python seed_data.py
```

Seeds 3 doctors, 3 patients, 2 consultations, and 2 health records.

---

## 📂 Folder Structure

```
gramcare-ai/
│
├── frontend/                        # React PWA Frontend
│   ├── public/
│   │   ├── index.html               # HTML shell
│   │   └── manifest.json            # PWA manifest
│   ├── src/
│   │   ├── App.js                   # Root component + routing
│   │   ├── App.css                  # Complete stylesheet
│   │   ├── index.js                 # React entry point
│   │   ├── context/
│   │   │   └── AuthContext.js       # Auth state management
│   │   ├── services/
│   │   │   └── api.js               # Axios API client
│   │   └── components/
│   │       ├── Navbar.js            # Navigation bar
│   │       ├── Login.js             # Login page
│   │       ├── Register.js          # Registration page
│   │       ├── PatientDashboard.js  # Patient home
│   │       ├── DoctorDashboard.js   # Doctor home
│   │       ├── SymptomChecker.js    # AI symptom checker
│   │       ├── Chatbot.js           # AI chatbot
│   │       ├── MedicineSearch.js    # Medicine search + generics
│   │       ├── HealthRecords.js     # Health records timeline
│   │       └── Consultation.js      # Teleconsultation page
│   └── package.json
│
├── backend/                         # Python Flask Backend
│   ├── app.py                       # Flask app factory + entry
│   ├── config.py                    # Configuration
│   ├── requirements.txt             # Python dependencies
│   ├── seed_data.py                 # Database seeder
│   └── routes/
│       ├── __init__.py
│       ├── auth_routes.py           # Register, Login, Profile
│       ├── patient_routes.py        # Patient CRUD + records
│       ├── doctor_routes.py         # Doctor queue + availability
│       ├── consultation_routes.py   # Consultation booking + mgmt
│       ├── pharmacy_routes.py       # Medicine search + generics
│       ├── symptom_routes.py        # AI symptom check endpoint
│       └── chatbot_routes.py        # Chatbot message endpoint
│
├── ai-service/                      # AI/ML Service
│   ├── train_model.py               # Model training script
│   ├── symptom_checker.py           # SymptomChecker class
│   ├── severity_scorer.py           # SeverityScorer class
│   ├── chatbot.py                   # HealthcareChatbot class
│   └── models/                      # Trained model files (generated)
│       ├── ensemble_model.pkl
│       ├── label_encoder.pkl
│       ├── symptoms.json
│       ├── disease_info.json
│       └── severity_map.json
│
├── datasets/                        # Raw datasets
│   ├── dataset.csv                  # Primary disease-symptom data
│   ├── clean_dataset.tsv
│   ├── Final_Augmented_dataset_Diseases_and_Symptoms.csv
│   ├── Symptom-severity.csv
│   ├── symptom_Description.csv
│   ├── symptom_precaution.csv
│   ├── medicines.csv
│   ├── EHR.csv
│   └── lung_cancer.csv
│
├── SOLUTION.md                      # Complete technical solution
└── README.md                        # This file
```

---

## 📸 Screenshots

> *Screenshots will be added after the prototype UI is complete.*

| Screen | Description |
|--------|-------------|
| Patient Dashboard | 4-card navigation grid with quick actions |
| AI Symptom Checker | Symptom tag selection + confidence bar results |
| AI Chatbot | Chat bubble interface with quick reply buttons |
| Teleconsultation | Video area + chat panel + doctor completion form |
| Doctor Dashboard | Severity-sorted patient queue + stats |
| Medicine Search | Medicine cards with generic alternative finder |
| Health Records | Timeline view of consultation history |

---

## 🎬 Demo Instructions

### Demo Duration: 10 minutes

### Prerequisites
- MongoDB running, backend + frontend started
- Seed data loaded (`python seed_data.py`)

### Demo Flow

**1. Opening (1 min)**
> Introduce Gurpreet, a farmer from Bhadson who can't afford to lose a work day for a hospital visit.

**2. Patient Login (1 min)**
- Open http://localhost:3000 → Login as `gurpreet@gramcare.in / patient123`
- Show the Patient Dashboard with 4 feature cards

**3. AI Symptom Checker (2 min)**
- Click "Symptom Check" card → Search and select symptoms
- Add: fever, headache, fatigue → Click "Check 3 Symptoms"
- Show AI predictions with confidence percentages
- Show severity triage badge (LOW/MEDIUM/HIGH)
- Show precautions and action recommendations

**4. AI Chatbot (2 min)**
- Navigate to Chatbot → Type "Mujhe bukhar hai"
- Show multilingual response in Hindi
- Try "I have a headache" for English response
- Use quick reply buttons for guided navigation

**5. Medicine Search (1.5 min)**
- Navigate to Medicines → Search "Paracetamol"
- Show medicine results with composition and uses
- Click "Find Generics" to show affordable alternatives

**6. Doctor View (2 min)**
- Open new browser tab → Login as `dr.kaur@gramcare.in / doctor123`
- Show Doctor Dashboard: patient queue sorted by severity
- Click "Start Consult" → Show teleconsultation page
- Fill in diagnosis + prescription → Mark as Completed

**7. Closing (0.5 min)**
> GramCare AI: 15-minute teleconsultation replaces a full lost work day.

---

## 🔮 Future Improvements

- **ABHA Integration** — Link with Ayushman Bharat Health Account
- **WebRTC Video** — Real-time video consultations with bandwidth adaptation
- **IoT Vitals** — Bluetooth BP monitors, glucometers integration
- **Computer Vision** — Image-based skin condition diagnosis
- **SMS Gateway** — Appointment reminders for non-smartphone users
- **Voice Input** — Web Speech API for spoken symptoms in regional language
- **Offline Mode** — Service Worker + IndexedDB for full offline support
- **ASHA Worker Module** — Community health worker interface
- **Multi-Language** — Full i18n for Punjabi, Hindi, English UI
- **Predictive Analytics** — Population health trends and epidemic warnings

---

## 👥 Contributors

### Team: The DOMinators

| Name | Role | Responsibilities |
|------|------|-----------------|
| Shaiikh Ibrahim | Full-Stack Lead | Architecture, Backend APIs, Database |
| Soham | Frontend Developer | React PWA, UI/UX, Components |
| Vishvadeep | AI/ML Engineer | Symptom Checker, Model Training |
| Jeeshan | AI/Integration | Chatbot, API Integration, Testing |

---

## 📄 License

This project is licensed under the **MIT License**.

```
MIT License

Copyright (c) 2026 The DOMinators

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
```

---

<p align="center">
  Built with ❤️ by <strong>The DOMinators</strong> for UAI Hawk-A-Thon 2026
</p>
<p align="center">
  <em>GramCare AI — Bridging healthcare to every village, one connection at a time.</em>
</p>
