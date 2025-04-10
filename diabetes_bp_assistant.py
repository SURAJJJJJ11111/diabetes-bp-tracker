import sqlite3
from datetime import datetime


# Connect to SQLite database (or create if it doesn't exist)
conn = sqlite3.connect('health_data.db')
cursor = conn.cursor()

# Create health records table
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

# Add new record and give feedback
def add_record(name, age):
    try:
        sugar = float(input("Enter your blood sugar level (mg/dL): "))
        systolic = int(input("Enter systolic BP (upper number): "))
        diastolic = int(input("Enter diastolic BP (lower number): "))
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute('''
            INSERT INTO health_records (name, age, sugar_level, systolic_bp, diastolic_bp, timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (name, age, sugar, systolic, diastolic, timestamp))

        conn.commit()
        print("\n✅ Record saved successfully!")

        # --- Blood Sugar Feedback ---
        if sugar < 70:
            print("🔵 Warning: Low blood sugar!")
        elif 70 <= sugar <= 99:
            print("🟢 Sugar level is normal.")
        elif 100 <= sugar <= 125:
            print("🟡 Prediabetic sugar range.")
        else:
            print("🔴 High blood sugar! (Possible Diabetes)")

        # --- Blood Pressure Feedback ---
        if systolic < 90 or diastolic < 60:
            print("🔵 Low blood pressure.")
        elif systolic <= 120 and diastolic <= 80:
            print("🟢 Blood pressure is normal.")
        elif 121 <= systolic <= 139 or 81 <= diastolic <= 89:
            print("🟡 Prehypertension range.")
        else:
            print("🔴 High blood pressure!")

    except ValueError:
        print("❌ Invalid input! Please enter numerical values.")

# View all records for the user
def view_records(name):
    cursor.execute('SELECT * FROM health_records WHERE name = ? ORDER BY timestamp DESC', (name,))
    records = cursor.fetchall()

    if not records:
        print("⚠️ No records found.")
    else:
        print(f"\n📂 Health Records for {name}:")
        for record in records:
            print(f"\n🧾 Date: {record[6]}")
            print(f"   Sugar Level: {record[3]} mg/dL")
            print(f"   BP: {record[4]}/{record[5]} mmHg")

# Show average sugar and BP
def show_averages(name):
    cursor.execute('''
        SELECT AVG(sugar_level), AVG(systolic_bp), AVG(diastolic_bp)
        FROM health_records
        WHERE name = ?
    ''', (name,))
    result = cursor.fetchone()

    if result and all(result):
        avg_sugar = round(result[0], 2)
        avg_sys = round(result[1], 2)
        avg_dia = round(result[2], 2)

        print("\n📊 Averages:")
        print(f"   Sugar Level: {avg_sugar} mg/dL")
        print(f"   Blood Pressure: {avg_sys}/{avg_dia} mmHg")
    else:
        print("⚠️  Not enough data to calculate averages.")
def analyze_diabetes_risk(name):
    cursor.execute('''
        SELECT AVG(sugar_level)
        FROM health_records
        WHERE name = ?
    ''', (name,))
    result = cursor.fetchone()

    if result and result[0] is not None:
        avg_sugar = round(result[0], 2)
        print(f"\n📈 Diabetes Risk Analysis for {name}")
        print(f"   Average Sugar Level: {avg_sugar} mg/dL")

        if avg_sugar < 70:
            print("🔵 Risk: Low sugar (Hypoglycemia). You may feel dizzy or weak.")
        elif 70 <= avg_sugar <= 99:
            print("🟢 Your sugar levels are within the normal range.")
        elif 100 <= avg_sugar <= 125:
            print("🟡 Warning: Prediabetic range. Keep monitoring and maintain a healthy diet.")
        else:
            print("🔴 Alert: High risk of Diabetes! Please consult a doctor.")
    else:
        print("⚠️ Not enough data to analyze risk.")

# Main chatbot function
def chatbot():
    print("👋 Welcome to the Diabetes & BP Tracker Assistant")
    name = input("What's your name? ").strip()
    print("Welcome", name,"nice to see you!")
    try:
        age = int(input("What's your age? "))
    except ValueError:
        print("❌ Invalid age. Defaulting to 0.")
        age = 0

    while True:
        print("\nWhat would you like to do?")
        print("1. Add new health record")
        print("2. View past records")
        print("3. Show average sugar & BP")
        print("4. Analyze diabetes risk")
        print("5. Exit")
        choice = input("> ").strip()

        if choice == "1":
            add_record(name, age)
        elif choice == "2":
            view_records(name)
        elif choice == "3":
            show_averages(name)
        elif choice == "4":
            analyze_diabetes_risk(name)
        elif choice == "5":
            print("👋 Goodbye! Stay healthy.")
            break
        elif choice =="suraj" or "Suraj" or "SURAJ":
            print("\nDeveloper of the chatbot")
        else:
            print("❌ Invalid option. Please try again.")

# Start the chatbot
if __name__ == "__main__":
    chatbot()
    conn.close()
