from datetime import datetime
import pandas as pd
import os
from flask import current_app


def get_path_to_file(filename):
    return os.path.join(current_app.root_path, filename)

def get_student_data(student_id: int, grade: int, class_num: int):
    try:
        file = get_path_to_file('students.csv')
        df = pd.read_csv(file)
        # Split the 'שכבה' column into grade and class_num
        df[['grade', 'class_num']] = df['שכבה'].str.split(expand=True)
        if grade == 0:
            # That is the way the data is stored in the file
            grade = 7
            class_num = 0
        # Convert to numeric values (removes any extra spaces)
        df['grade'] = pd.to_numeric(df['grade'])
        df['class_num'] = pd.to_numeric(df['class_num'])
        student = df[
            ( student_id == df['ת.ז תלמיד']) &
            (  grade == df['grade']) &
            (  class_num == df['class_num'])
        ]

        if student.empty:
            return None

        return {
            'id': student['ת.ז תלמיד'].iloc[0],
            'name': student['שם תלמיד'].iloc[0],
            'grade_str': 'א' if grade == 7 else f"{grade_to_char(student['grade'].iloc[0])}'{student['class_num'].iloc[0]}"
        }

    except Exception as e:
        print(f"Error reading student data: {e}")
        return None


def save_distribution(student_id, student_name, receiver):
    try:
        distributions = get_path_to_file('distributions.csv')
        df = pd.read_csv(distributions)

        new_distribution = {
            'תעודת זהות': student_id,
            'שם תלמיד': student_name,
            'מקבל': receiver,
            'זמן קבלה': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        df = pd.concat([df, pd.DataFrame([new_distribution])], ignore_index=True)
        df.to_csv(distributions, index=False)
        return True

    except Exception as e:
        print(f"Error saving distribution: {e}")
        return False

def get_all_distributions():
    try:
        distributions = get_path_to_file('distributions.csv')
        df = pd.read_csv(distributions)
        column_mapping = {
            'תעודת זהות': 'student_id',
            'שם תלמיד': 'student_name',
            'מקבל': 'receiver',
            'זמן קבלה': 'date'
        }
        # Rename columns
        df = df.rename(columns=column_mapping)

        return df.to_dict('records')

    except Exception as e:
        print(f"Error retrieving distribution: {e}")
        return []

def check_distribution_status(student_id: int) -> (bool, str):
    try:
        distributions = get_path_to_file('distributions.csv')
        df = pd.read_csv(distributions)
        # Use Hebrew column names directly
        student = df[df['תעודת זהות'] == student_id]
        if student.empty:
            return False, ""
        return True, student['מקבל'].iloc[0] if 'מקבל' in student.columns else ""

    except FileNotFoundError:
        return []

def grade_to_char(grade: int) -> str:
    grade_map = {
        7: 'א',
        1: 'ב',
        2: 'ג',
        3: 'ד',
        4: 'ה',
        5: 'ו'
    }
    return grade_map.get(grade, '')