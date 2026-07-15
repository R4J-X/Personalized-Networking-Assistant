# 🤝 Personalized Networking Assistant

[![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.36-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Hugging Face](https://img.shields.io/badge/🤗%20Transformers-4.42-yellow)](https://huggingface.co/docs/transformers/)
[![Tests](https://img.shields.io/badge/tests-pytest-0A9EDC?logo=pytest&logoColor=white)](https://docs.pytest.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](./LICENSE)
[![CI](https://img.shields.io/badge/CI-GitHub%20Actions-2088FF?logo=githubactions&logoColor=white)](./.github/workflows/ci.yml)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000)](https://github.com/psf/black)

An AI-powered application that helps professionals walk into any networking event with confidence. Give it an **event description** and your **interests**, and it will generate personalized conversation starters, fact-check topics in real time, and keep a history of everything for you.

---
# 📂 Project Folder Structure Guide

This document provides a brief overview of the folders and files present in the project.

---

# Project Structure

personalized-networking-assistant/
├── 1. Brainstorming & Ideation
│   ├── Brainstorming & Idea Prioritization.pdf
│   ├── Define Problem Statements.pdf
│   └── Empathy Map.pdf
│
├── 2. Requirement Analysis
│   ├── Customer Journey Map.pdf
│   ├── Data Flow Diagram.pdf
│   ├── Solution Requirements.pdf
│   └── Technology Stack.pdf
│
├── 3. Project Design Phase
│   ├── Problem-Solution Fit.pdf
│   ├── Proposed Solution.pdf
│   └── Solution Architecture.pdf
│
├── 4. Project Planning Phase
│   └── Project Planning.pdf
│
├── 5. Project Development Phase
│   ├── Code-Layout, Readability and Reusability.pdf
│   ├── Coding & Solution.pdf
│   └── No. of Functional Features Included in the Solution.pdf
│
├── 6.Project Testing
│   └── Performance Testing.pdf
│
├── 7.Project Documentation
│   ├── Project Executable Files.pdf
│   └── Sample Project Documentation.pdf
│
├── 8.Project Demonstration
│   ├── Communication.pdf
│   ├── Demonstration of Proposed Features.pdf
│   ├── Project Demo Planning.pdf
│   ├── Scalability & Future Plan.pdf
│   └── Team Involvement in Demonstration.pdf
│
├── 9.Programmes and codes
│   ├── app
│   │   ├── models
│   │   │   ├── __init__.py
│   │   │   └── schemas.py
│   │   │
│   │   ├── routes
│   │   │   ├── __init__.py
│   │   │   └── conversation.py
│   │   │
│   │   ├── services
│   │   │   ├── __init__.py
│   │   │   ├── event_analyzer.py
│   │   │   ├── fact_checker.py
│   │   │   ├── feedback_logger.py
│   │   │   ├── history_logger.py
│   │   │   └── topic_generator.py
│   │   │
│   │   ├── __init__.py
│   │   └── main.py
│   │
│   ├── data
│   │   ├── .gitkeep
│   │   ├── feedback.json
│   │   └── history.json
│   │
│   ├── docs
│   │   └── ER_DIAGRAM.md
│   │
│   ├── frontend
│   │   └── streamlit_app.py
│   │
│   ├── tests
│   │   ├── __init__.py
│   │   ├── test_event_analyzer.py
│   │   ├── test_fact_checker.py
│   │   ├── test_routes.py
│   │   └── test_topic_generator.py
│   │
│   ├── Dockerfile
│   ├── README.md
│   └── requirements.txt
│
├── 10.Screenshots
│   ├── 1_Swagger_UI.png
│   ├── 2_Homepage.png
│   ├── 3_History.png
│   ├── 4_Feedback.png
│   └── 5_Fact_Check.png
│
├── Video
│   └── DEMOvideo.md
│
└── LICENSE
```

---

# Folder Descriptions

## 📁 1. Brainstorming & Ideation
Contains documents related to idea generation and problem identification.

## 📁 2. Requirement Analysis
Contains requirement gathering and analysis documents.

## 📁 3. Project Design Phase
Contains architecture and solution design documents.

## 📁 4. Project Planning Phase
Contains project planning and scheduling documents.

## 📁 5. Project Development Phase
Contains development and implementation-related documents.

## 📁 6.Project Testing
Contains testing and performance evaluation documents.

## 📁 7.Project Documentation
Contains project reports and supporting documentation.

## 📁 8.Project Demonstration
Contains demo planning and presentation materials.

## 📁 9.Programmes and codes
Contains the complete source code of the project.

### 📁 app
Backend application source code.

### 📁 models
Contains Pydantic schemas and data models.

### 📁 routes
Contains FastAPI API endpoint definitions.

### 📁 services
Contains business logic and AI services.

### 📁 data
Stores application data such as history and feedback.

### 📁 docs
Contains additional technical documentation.

### 📁 frontend
Contains the Streamlit user interface.

### 📁 tests
Contains unit and integration tests.

### 📄 Dockerfile
Docker configuration file.

### 📄 README.md
Project overview and setup instructions.

### 📄 requirements.txt
List of project dependencies.

## 📁 10.Screenshots
Contains screenshots of the application.

## 📁 Video
Contains project demonstration information.

## 📄 LICENSE
Contains licensing information for the project.
