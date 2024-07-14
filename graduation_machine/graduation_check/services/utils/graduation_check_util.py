import pandas as pd

class GraduationCheckUtil:
    def read_report_card(self, excel_file):
        df = pd.read_excel(excel_file, engine='openpyxl')
        
        user_lectures = []
        for index, row in df.iterrows():
            lecture_data = {
                'year': row['년도'],
                'season': row['학기'],
                'code': row['학수강좌번호'],
                'credit': row['학점'],
                'grade': row['등급']
            }
            user_lectures.append(lecture_data)
        
        return user_lectures
