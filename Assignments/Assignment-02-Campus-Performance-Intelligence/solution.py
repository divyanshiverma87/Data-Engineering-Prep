import pandas as pd
import numpy as np
import json
import sqlite3
import matplotlib.pyplot as plt



# STEP 1: LOAD DATA


students = pd.read_csv("students.csv")

attendance = pd.read_csv("attendance.csv")

with open("scholarships.json", "r") as file:
    scholarships = json.load(file)



# ----------------------- = TASK 1: INSPECT DATA = ---------------------

print("\n--------- DATA INSPECTION ---------")

print(
    "Number of students:",
    len(students)
)

print(
    "Number of departments:",
    students["department"].nunique()
)

print(
    "Unique cities:",
    students["city"].unique()
)

print("\nFirst five student records:")
print(students.head())

print("\nScholarship Rules:")
print(scholarships)

df = pd.merge(
    students,
    attendance,
    on="student_id",
    how="left"
)

#   --------------------------- == TASK 2 : MERGERD DATA == ----------------------
print("\n-------- MERGED DATA ----------")
print(df.head())

missing_attendance = df["attendance"].isna().sum()

print(
    "\nMissing attendance records:",
    missing_attendance
)
print("\nColumns after merge:")
print(df.columns.tolist())


# ------------------------- === Task 3 === ------------------------------

marks = df["marks"].to_numpy()
attendance_values = df["attendance"].to_numpy()
mean_marks = np.mean(marks)
median_marks = np.median(marks)
std_marks = np.std(marks)
max_marks = np.max(marks)
min_marks = np.min(marks)
mean_attendance = np.mean(attendance_values)

print("\n-------------------------- NUMPY STATISTICS ---------------------")

print("Mean marks:", mean_marks)
print("Median marks:", median_marks)
print("Standard deviation:", std_marks)
print("Maximum marks:", max_marks)
print("Minimum marks:", min_marks)
print("Mean attendance:", mean_attendance)


# =========================================
# TASK 4: SCHOLARSHIP RULES
# =========================================

scholarship_rules = {
    rule["department"]: rule
    for rule in scholarships
}

print("\nScholarship rules dictionary:")
print(scholarship_rules)

def check_scholarship(row):

    rule = scholarship_rules[row["department"]]

    if (
        row["marks"] >= rule["minimum_marks"]
        and
        row["attendance"] >= rule["minimum_attendance"]
    ):
        return "Eligible"

    return "Not Eligible"

df["scholarship_status"] = df.apply(
    check_scholarship,
    axis=1
)

print("\n===== SCHOLARSHIP STATUS =====")

print(
    df[
        [
            "student_id",
            "name",
            "department",
            "marks",
            "attendance",
            "scholarship_status"
        ]
    ]
)

def calculate_final_marks(row):

    if row["scholarship_status"] == "Eligible":

        bonus = scholarship_rules[
            row["department"]
        ]["bonus_marks"]

        return row["marks"] + bonus

    return row["marks"]

df["final_marks"] = df.apply(
    calculate_final_marks,
    axis=1
)

print("\n===== FINAL MARKS =====")

print(
    df[
        [
            "student_id",
            "name",
            "department",
            "marks",
            "attendance",
            "scholarship_status",
            "final_marks"
        ]
    ]
)

# =========================================
# TASK 5: PERFORMANCE CATEGORY
# =========================================

def performance_category(marks):

    if marks >= 90:
        return "Outstanding"

    elif marks >= 80:
        return "Excellent"

    elif marks >= 70:
        return "Good"

    elif marks >= 60:
        return "Average"

    else:
        return "Needs Improvement"


df["performance"] = df["final_marks"].apply(
    performance_category
)


print("\n===== PERFORMANCE CATEGORY =====")

print(
    df[
        [
            "student_id",
            "name",
            "final_marks",
            "performance"
        ]
    ]
)

# =========================================
# TASK 6: PANDAS ANALYTICS
# =========================================


# 1. Top 5 students

top_students = df.nlargest(
    5,
    "final_marks"
)

print("\n===== TOP 5 STUDENTS =====")

print(
    top_students[
        [
            "student_id",
            "name",
            "department",
            "final_marks"
        ]
    ]
)


# 2. Department-wise average

department_avg = (
    df.groupby("department")["final_marks"]
      .mean()
)

print("\n===== DEPARTMENT-WISE AVERAGE =====")
print(department_avg)


# 3. City-wise average

city_avg = (
    df.groupby("city")["final_marks"]
      .mean()
)

print("\n===== CITY-WISE AVERAGE =====")
print(city_avg)


# 4. Best department

best_department = department_avg.idxmax()

print(
    "\nDepartment with highest average:",
    best_department
)


# 5. Highest attendance student

highest_attendance_index = df["attendance"].idxmax()

highest_attendance_student = df.loc[
    highest_attendance_index,
    "name"
]

print(
    "Student with highest attendance:",
    highest_attendance_student
)


# 6. Scholarship count

scholarship_count = (
    df["scholarship_status"] == "Eligible"
).sum()

print(
    "Number of scholarship-eligible students:",
    scholarship_count
)


# 7. Performance distribution

performance_counts = (
    df["performance"]
      .value_counts()
)

print("\n===== PERFORMANCE DISTRIBUTION =====")
print(performance_counts)

# =========================================
# TASK 7: SQLITE DATABASE
# =========================================

conn = sqlite3.connect(
    "student_hackathon.db"
)


# Store final dataframe in database

df.to_sql(
    "student_performance",
    conn,
    if_exists="replace",
    index=False
)


# -----------------------------------------
# QUERY 1
# Scholarship eligible students
# -----------------------------------------

query1 = """
SELECT
    student_id,
    name,
    department,
    final_marks
FROM student_performance
WHERE scholarship_status = 'Eligible';
"""

result1 = pd.read_sql_query(
    query1,
    conn
)

print("\n===== SCHOLARSHIP-ELIGIBLE STUDENTS =====")
print(result1)


# -----------------------------------------
# QUERY 2
# Final marks greater than 85
# -----------------------------------------

query2 = """
SELECT
    student_id,
    name,
    department,
    final_marks
FROM student_performance
WHERE final_marks > 85;
"""

result2 = pd.read_sql_query(
    query2,
    conn
)

print("\n===== FINAL MARKS > 85 =====")
print(result2)

# =========================================
# BONUS: lambda, map(), filter()
# =========================================

# lambda
df["above_85"] = df["final_marks"].apply(
    lambda x: x > 85
)


# map()
bonus_map = {
    rule["department"]: rule["bonus_marks"]
    for rule in scholarships
}

df["bonus_marks"] = df["department"].map(
    bonus_map
)


# filter()
eligible_students = list(
    filter(
        lambda row:
            row["scholarship_status"] == "Eligible",
        df.to_dict("records")
    )
)

print(
    "\nBonus - Eligible students using filter():",
    len(eligible_students)
)


# -----------------------------------------
# QUERY 3
# Department-wise average
# -----------------------------------------

query3 = """
SELECT
    department,
    AVG(final_marks) AS average_final_marks
FROM student_performance
GROUP BY department;
"""

result3 = pd.read_sql_query(
    query3,
    conn
)

print("\n===== DEPARTMENT-WISE AVERAGE =====")
print(result3)


# Close database

conn.close()

# =========================================
# TASK 8: VISUALIZATION
# =========================================

# Chart 1: Department vs Average Final Marks

plt.figure(figsize=(8, 5))

department_avg.plot(kind="bar")

plt.title("Department vs Average Final Marks")
plt.xlabel("Department")
plt.ylabel("Average Final Marks")

plt.xticks(rotation=0)

plt.tight_layout()

plt.savefig("department_performance.png")

plt.close()

# Chart 2: Performance Category Distribution

plt.figure(figsize=(7, 7))

performance_counts.plot(
    kind="pie",
    autopct="%1.1f%%"
)

plt.title("Performance Category Distribution")

plt.ylabel("")

plt.tight_layout()

plt.savefig("performance_distribution.png")

plt.close()


# =========================================
# TASK 9: MANAGEMENT REPORT
# =========================================

report = {
    "total_students": len(df),

    "average_marks": round(
        df["marks"].mean(),
        2
    ),

    "average_attendance": round(
        df["attendance"].mean(),
        2
    ),

    "scholarship_students": int(
        scholarship_count
    ),

    "top_student": df.loc[
        df["final_marks"].idxmax(),
        "name"
    ],

    "best_department": best_department,

    "highest_attendance_student": highest_attendance_student
}


with open("report.json", "w") as file:

    json.dump(
        report,
        file,
        indent=4
    )


print("\n===== MANAGEMENT REPORT =====")
print(json.dumps(report, indent=4))