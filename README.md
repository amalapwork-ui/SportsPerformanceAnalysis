Sports Performance Analysis System

An end-to-end **Sports Analytics Platform** that leverages **Machine Learning**, **Deep Learning (YOLOv8)**, and **modern web frameworks** to analyze football player performance, market value, injury risk, and real-time player tracking from match videos.

---

## 📌 Project Overview

Modern football relies heavily on data-driven decision making for:
- Player performance evaluation
- Market value estimation
- Injury prevention
- Match and tactical analysis

This project builds a **production-ready sports analytics system** that combines:
- **Regression-based predictive analytics** (FIFA dataset)
- **Computer Vision-based player tracking** (YOLOv8)
- **FastAPI backend**
- **Streamlit frontend**

---

## 🚀 Key Features

### 🔹 Machine Learning
- Predicts **Overall Player Rating** using **XGBoost Regressor**
- Predicts **Market Value** using **Random Forest Regressor**
- Trained on **FIFA 19 Complete Player Dataset**

### 🔹 Injury Risk Assessment
- Synthetic injury risk classification
- Factors used:
  - Age
  - Stamina
  - Work Rate
- Risk categories:
  - Low
  - Medium
  - High

### 🔹 Deep Learning (Computer Vision)
- Real-time **player detection & tracking** using **YOLOv8**
- Detects players as `person` class
- Assigns **unique tracking IDs** per player
- Outputs annotated match video

### 🔹 Deployment
- RESTful API using **FastAPI**
- Interactive UI using **Streamlit**
- Cross-platform (Windows / Linux)
- Docker-ready architecture

---

## 🧠 Tech Stack

| Layer | Technology |
|----|----|
| Language | Python |
| ML | scikit-learn, XGBoost |
| DL | YOLOv8 (Ultralytics), OpenCV |
| Backend | FastAPI |
| Frontend | Streamlit |
| Dataset | FIFA 19 Complete Player Dataset |

