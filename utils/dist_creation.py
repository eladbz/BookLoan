import pandas as pd
from datetime import datetime, timedelta
import random

# Sample names
first_names = ['אביב', 'עידן', 'שירה', 'נועה', 'יובל', 'עומר', 'מיכל', 'דניאל', 'איתי', 'רועי']
last_names = ['כהן', 'לוי', 'פרץ', 'אברהם', 'שפירא', 'גולן', 'אדרי', 'מזרחי', 'ביטון', 'דהן']
distributors = ['משה דהן', 'רחל כהן', 'דוד לוי', 'שרה פרץ', 'יעקב גולן']

# Generate 50 records
records = []
base_date = datetime.now()

for i in range(50):
    student_id = random.randint(200000000, 399999999)
    student_name = f"{random.choice(last_names)} {random.choice(first_names)}"
    distributor = random.choice(distributors)
    # Random time in the last 24 hours
    random_minutes = random.randint(-1440, 0)  # Up to 24 hours back
    date = (base_date + timedelta(minutes=random_minutes)).strftime('%Y-%m-%d %H:%M:%S')

    records.append({
        'תעודת זהות': student_id,
        'שם תלמיד': student_name,
        'מקבל': distributor,
        'זמן קבלה': date
    })

# Create DataFrame
df = pd.DataFrame(records)

# Sort by date
df = df.sort_values('זמן קבלה', ascending=False)

# Save to CSV
df.to_csv('data/distributions.csv', index=False)