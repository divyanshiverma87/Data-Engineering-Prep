# 🎓 Campus Performance Intelligence System

> Python Data Engineering Mini Hackathon — End-to-End Student Performance Analytics Pipeline

## 📌 Overview

The **Campus Performance Intelligence System** is an end-to-end Python data engineering pipeline developed as part of a mini hackathon.

The system integrates student information, attendance records, and department-specific scholarship rules from multiple data sources. It then performs data transformation, statistical analysis, scholarship eligibility evaluation, performance classification, SQL-based analytics, visualization, and management reporting.

The project demonstrates how raw data from different sources can be transformed into meaningful and actionable insights.

---

## 🎯 Problem Statement

The university maintains student information across multiple sources:

- Student information and marks → CSV
- Attendance information → CSV
- Scholarship rules → JSON

These datasets are initially disconnected.

The objective is to build a complete data pipeline that:

1. Loads data from multiple sources
2. Integrates the datasets
3. Performs statistical analysis
4. Determines scholarship eligibility
5. Calculates final marks
6. Classifies student performance
7. Performs analytical queries
8. Stores processed data in SQLite
9. Generates visualizations
10. Produces a management report

---

## 🔄 Data Engineering Pipeline

```text
students.csv
       │
       ├──────────────┐
       │              │
       ▼              ▼
attendance.csv   scholarships.json
       │              │
       └──────┬───────┘
              ▼
       Data Integration
              │
              ▼
       Data Transformation
              │
       ┌──────┼─────────────┐
       ▼      ▼             ▼
     NumPy  Pandas     Scholarship
   Analysis Analytics    Evaluation
       │      │             │
       └──────┼─────────────┘
              ▼
        Final Dataset
              │
       ┌──────┼──────────────┐
       ▼      ▼              ▼
    SQLite  Matplotlib   JSON Report
   Database Visualization