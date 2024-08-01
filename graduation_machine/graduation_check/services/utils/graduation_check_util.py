import pandas as pd

class GraduationCheckUtil:
    @staticmethod
    def read_report_card(excel_file):
        df = pd.read_excel(excel_file, engine='openpyxl')
        
        user_lectures = []
        for index, row in df.iterrows():
            number = str(row[df.columns[6]])
            if len(number) == 1 or len(number) == 2:
                lecture_code = f"{row['학수강좌번호']}-{number.zfill(2)}"
            else:
                lecture_code = f"{row['학수강좌번호']}-{number}"
            
            season = ''
            if row['학기'] == '1학기':
                season = '1'
            elif row['학기'] == '2학기':
                season = '2'
            elif row['학기'] == '여름학기':
                season = 'summer'
            elif row['학기'] == '겨울학기':
                season = 'winter'
            else:
                season = row['학기']

            lecture_data = {
                'year': row['년도'],
                'season': season,
                'code': lecture_code,
                'credit': row['학점'],
                'grade': row['등급'],
                'name': row['교과목명']
            }
            user_lectures.append(lecture_data)
        
        return user_lectures
