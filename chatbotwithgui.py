import sqlite3
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext

# Database setup
conn = sqlite3.connect('health_data.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS health_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    age INTEGER,
    sugar_level REAL,
    systolic_bp INTEGER,
    diastolic_bp INTEGER,
    timestamp TEXT
)
''')
conn.commit()

# GUI App
class HealthApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🩺 Health Tracker Assistant")
        self.root.geometry("500x500")
        self.name = ""
        self.age = 0

        self.create_main_interface()

    def create_main_interface(self):
        self.name = simpledialog.askstring("Name", "What's your name?")
        try:
            self.age = int(simpledialog.askstring("Age", "What's your age?"))
        except:
            self.age = 0

        tk.Label(self.root, text=f"Welcome, {self.name}!", font=("Helvetica", 16)).pack(pady=10)

        tk.Button(self.root, text="➕ Add Health Record", width=30, command=self.add_record).pack(pady=5)
        tk.Button(self.root, text="📂 View Records", width=30, command=self.view_records).pack(pady=5)
        tk.Button(self.root, text="📊 Show Averages", width=30, command=self.show_averages).pack(pady=5)
        tk.Button(self.root, text="📈 Analyze Diabetes Risk", width=30, command=self.analyze_diabetes_risk).pack(pady=5)
        tk.Button(self.root, text="👨‍💻 Developer Info", width=30, command=self.show_developer).pack(pady=5)
        tk.Button(self.root, text="❌ Exit", width=30, command=self.root.quit).pack(pady=20)

    def add_record(self):
        try:
            sugar = float(simpledialog.askstring("Sugar Level", "Enter blood sugar level (mg/dL):"))
            systolic = int(simpledialog.askstring("Systolic BP", "Enter systolic BP:"))
            diastolic = int(simpledialog.askstring("Diastolic BP", "Enter diastolic BP:"))
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            cursor.execute('''
                INSERT INTO health_records (name, age, sugar_level, systolic_bp, diastolic_bp, timestamp)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (self.name, self.age, sugar, systolic, diastolic, timestamp))
            conn.commit()

            feedback = "\n✅ Record saved!\n"

            # Sugar level feedback
            if sugar < 70:
                feedback += "🔵 Warning: Low blood sugar!\n"
            elif 70 <= sugar <= 99:
                feedback += "🟢 Sugar level is normal.\n"
            elif 100 <= sugar <= 125:
                feedback += "🟡 Prediabetic sugar range.\n"
            else:
                feedback += "🔴 High blood sugar! (Possible Diabetes)\n"

            # BP feedback
            if systolic < 90 or diastolic < 60:
                feedback += "🔵 Low blood pressure.\n"
            elif systolic <= 120 and diastolic <= 80:
                feedback += "🟢 Blood pressure is normal.\n"
            elif 121 <= systolic <= 139 or 81 <= diastolic <= 89:
                feedback += "🟡 Prehypertension.\n"
            else:
                feedback += "🔴 High blood pressure!\n"

            messagebox.showinfo("Health Feedback", feedback)
        except:
            messagebox.showerror("Error", "Invalid input! Please enter valid numbers.")

    def view_records(self):
        cursor.execute('SELECT * FROM health_records WHERE name = ? ORDER BY timestamp DESC', (self.name,))
        records = cursor.fetchall()

        display = scrolledtext.ScrolledText(self.root, width=60, height=20)
        display.pack()
        display.delete(1.0, tk.END)

        if not records:
            display.insert(tk.END, "⚠️ No records found.\n")
        else:
            display.insert(tk.END, f"📂 Health Records for {self.name}:\n\n")
            for rec in records:
                display.insert(tk.END, f"🧾 {rec[6]}\n  Sugar: {rec[3]} mg/dL\n  BP: {rec[4]}/{rec[5]} mmHg\n\n")

    def show_averages(self):
        cursor.execute('''
            SELECT AVG(sugar_level), AVG(systolic_bp), AVG(diastolic_bp)
            FROM health_records
            WHERE name = ?
        ''', (self.name,))
        result = cursor.fetchone()

        if result and all(result):
            messagebox.showinfo("📊 Averages", 
                f"Sugar Level: {round(result[0], 2)} mg/dL\n"
                f"Blood Pressure: {round(result[1], 2)}/{round(result[2], 2)} mmHg")
        else:
            messagebox.showwarning("⚠️", "Not enough data to calculate averages.")

    def analyze_diabetes_risk(self):
        cursor.execute('SELECT AVG(sugar_level) FROM health_records WHERE name = ?', (self.name,))
        result = cursor.fetchone()

        if result and result[0] is not None:
            avg = round(result[0], 2)
            msg = f"📈 Avg Sugar: {avg} mg/dL\n"

            if avg < 70:
                msg += "🔵 Low sugar (Hypoglycemia)."
            elif avg <= 99:
                msg += "🟢 Normal range."
            elif avg <= 125:
                msg += "🟡 Prediabetic range."
            else:
                msg += "🔴 High risk of Diabetes!"

            messagebox.showinfo("Diabetes Risk", msg)
        else:
            messagebox.showwarning("⚠️", "Not enough data to analyze.")

    def show_developer(self):
        messagebox.showinfo("👨‍💻 Developer", "This chatbot was developed by Suraj.\nKeep tracking, stay healthy! 💪")

# Start app
root = tk.Tk()
app = HealthApp(root)
root.mainloop()

# Close DB when GUI is closed
conn.close()
