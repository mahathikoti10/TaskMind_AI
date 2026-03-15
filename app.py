import streamlit as st
import pandas as pd

# =========================
# Page Configuration
# =========================
st.set_page_config(
    page_title="🚀 TaskMind AI - Resource Management",
    layout="wide",
)

# =========================
# Load Data
# =========================
def load_csv(file_name, default_cols=None):
    try:
        df = pd.read_csv(file_name)
    except Exception as e:
        st.warning(f"Error loading {file_name}: {e}")
        df = pd.DataFrame(columns=default_cols if default_cols else [])
    return df

employees = load_csv("employees.csv", ["employee_id", "name", "role", "skills", "experience_years", "current_workload_percent"])
tasks = load_csv("tasks.csv", ["task", "required_ml", "required_backend"])
projects = load_csv("projects.csv", ["project_id", "project_name", "description"])
history = load_csv("history.csv", ["entry_id", "employee_name", "task", "status", "date"])
tools = load_csv("tools.csv", ["tool_id", "tool_name", "category"])

# =========================
# Front Page Banner
# =========================
st.markdown("""
<div style='background-color:#4B0082; padding:15px; border-radius:10px; color:white; text-align:center'>
<h1>🚀 TaskMind AI</h1>
<h4>Smart Resource & Task Management Dashboard</h4>
</div>
""", unsafe_allow_html=True)

# =========================
# Top Metrics Row
# =========================
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Employees", len(employees))
col2.metric("Total Tasks", len(tasks))
col3.metric("Total Projects", len(projects))
col4.metric("History Entries", len(history))

# =========================
# Tab Layout
# =========================
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "👥 Employees", 
    "🗂 Tasks", 
    "📜 History", 
    "🛠 Tools", 
    "➕ Add Data", 
    "🤖 AI Allocation"
])

# =========================
# Tab 1-4
# =========================
with tab1: st.subheader("Employees"); st.dataframe(employees)
with tab2: st.subheader("Project Tasks"); st.dataframe(tasks)
with tab3: st.subheader("Task History"); st.dataframe(history)
with tab4: st.subheader("Tools"); st.dataframe(tools)

# =========================
# Tab 5: Add Data
# =========================
with tab5:
    st.subheader("➕ Add New Entry")
    table_option = st.selectbox("Select Table", ["Employees", "Task", "History", "Tool"])
    if table_option == "Employees":
        name = st.text_input("Employee Name")
        role = st.text_input("Role")
        skills = st.text_input("Skills (semicolon separated)")
        exp = st.number_input("Experience (Years)", 0)
        workload = st.number_input("Current Workload %", 0, 100)
        if st.button("Add Employee"): st.success(f"Employee {name} added!")
    elif table_option == "Task":
        task_name = st.text_input("Task Name")
        req_ml = st.number_input("Required ML Skill", 0)
        req_backend = st.number_input("Required Backend Skill", 0)
        if st.button("Add Task"): st.success(f"Task {task_name} added!")
    elif table_option == "History":
        emp_name = st.text_input("Employee Name")
        task_name = st.text_input("Task")
        status = st.text_input("Status")
        date = st.date_input("Date")
        if st.button("Add History Entry"): st.success("History entry added!")
    elif table_option == "Tool":
        tool_name = st.text_input("Tool Name")
        category = st.text_input("Category")
        if st.button("Add Tool"): st.success(f"Tool {tool_name} added!")

# =========================
# Tab 6: AI Allocation
# =========================
with tab6:
    st.subheader("🤖 AI Allocation")

    if employees.empty or tasks.empty:
        st.warning("Employees or Tasks CSV is empty!")
    else:
        results = []
        for _, task in tasks.iterrows():
            best_score = -1
            best_employee = None
            for _, emp in employees.iterrows():
                emp_skills = str(emp.get("skills", "")).lower().split(";")
                task_skills = []
                if task.get("required_ml", 0) > 0: task_skills.append("ml")
                if task.get("required_backend", 0) > 0: task_skills.append("backend")
                
                skill_matches = len(set(emp_skills) & set(task_skills))
                skill_score = skill_matches * 10  # 10 points per skill match
                workload_penalty = emp.get("current_workload_percent", 0) * 0.5
                success_score = emp.get("experience_years", 0)
                final_score = skill_score + success_score - workload_penalty
                
                if final_score > best_score:
                    best_score = final_score
                    best_employee = emp.get("name")
            
            results.append({
                "Task": task.get("task"),
                "Assigned Employee": best_employee,
                "Match Score": best_score
            })
        
        allocation_df = pd.DataFrame(results)
        st.dataframe(allocation_df)