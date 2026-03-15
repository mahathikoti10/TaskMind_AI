import pandas as pd

# --- Load CSVs ---
employees = pd.read_csv("employees_clean.csv")  # Cleaned employees file
tasks = pd.read_csv("tasks.csv")

# --- Ensure numeric columns are correct ---
for col in ["current_workload_percent", "success_score"]:
    if col in employees.columns:
        employees[col] = pd.to_numeric(employees[col], errors="coerce").fillna(0)
    else:
        employees[col] = 0

# --- Prepare employee skills as a list ---
employees["skills_list"] = employees["skills"].fillna("").apply(lambda x: [s.strip().lower() for s in x.split(";")])

results = []

# --- Allocate tasks dynamically with debug prints ---
for _, task in tasks.iterrows():
    best_employee = None
    best_score = -1
    reason = ""

    task_name = task.get("task") or "Unnamed Task"
    # Get all required skills dynamically
    required_skills = {col.replace("required_", "").lower(): task[col] for col in task.index if "required_" in col}

    print(f"\n--- Matching Task: {task_name}, Required Skills: {list(required_skills.keys())} ---")

    for _, emp in employees.iterrows():
        skill_matches = 0
        skill_score = 0

        # Calculate skill score
        for skill, req_val in required_skills.items():
            if skill in emp["skills_list"]:
                skill_score += req_val
                skill_matches += 1

        workload_penalty = emp["current_workload_percent"] * 0.5
        final_score = skill_score + emp["success_score"] * 10 - workload_penalty

        if pd.isna(final_score):
            final_score = -1

        print(f"Employee: {emp['name']}, Skill Matches: {skill_matches}, "
              f"Skill Score: {skill_score}, Workload Penalty: {workload_penalty}, "
              f"Success Score: {emp['success_score']}, Final Score: {round(final_score,2)}")

        if final_score > best_score:
            best_score = final_score
            best_employee = emp["name"]
            reason = f"Best match with score {round(final_score,2)}"

    results.append({
        "Task": task_name,
        "Assigned Employee": best_employee,
        "Match Score": round(best_score,2),
        "Reason": reason
    })

    print(f"-> Assigned Employee: {best_employee}, Match Score: {round(best_score,2)}, Reason: {reason}")

# --- Save results ---
allocation_df = pd.DataFrame(results)
allocation_df.to_csv("task_allocation_results.csv", index=False)
print("\n✅ Task allocation completed. Results saved to task_allocation_results.csv")
