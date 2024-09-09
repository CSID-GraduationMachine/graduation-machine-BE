import pandas as pd
import io
import msoffcrypto

class GraduationCheckUtil:

    @staticmethod
    def read_report_card_mdrims(excel_file):
        df = pd.read_excel(excel_file, engine='openpyxl', dtype={6: str})

        user_lectures = []
        for index, row in df.iterrows():
            if pd.notna(row['학수강좌번호']):
                number = str(row[df.columns[6]])
                if len(number) == 1 or len(number) == 2:
                    lecture_code = f"{row['학수강좌번호']}-{number.zfill(2)}"
                else:
                    lecture_code = f"{row['학수강좌번호']}-{number}"
            else:
                lecture_code = ' - '
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
            if row['등급'] == 'F' and row['학점'] == 1:
                grade = 'NP',
                credit = 0
            else:
                grade = row['등급']
                credit = row['학점']
            lecture_data = {
                'year': row['년도'],
                'season': season,
                'code': lecture_code,
                'credit': credit,
                'grade': grade,
                'name': row['교과목명']
            }
            user_lectures.append(lecture_data)
        return user_lectures

    @staticmethod
    def read_report_card_ndrims(excel_file, password):
        try:
            decrypted = io.BytesIO()
            office_file = msoffcrypto.OfficeFile(excel_file)
            office_file.load_key(password=password)
            office_file.decrypt(decrypted)  # 비밀번호 해독한 데이터를 decrypted에 저장

            # 해독된 파일을 BytesIO로 변환하여 pandas로 읽기
            decrypted.seek(0)  # 파일의 시작으로 포인터를 이동
            df = pd.read_excel(decrypted, engine='openpyxl')
        except Exception as e:
            print(f"비밀번호가 걸린 엑셀 파일을 여는 데 문제가 발생했습니다: {e}")
            return None


        user_lectures = []
        for index, row in df.iterrows():
            if pd.notna(row['성적삭제명']):
                continue
            if pd.notna(row['학수번호']):
                number = str(row[df.columns[5]])
                if len(number) == 1 or len(number) == 2:
                    lecture_code = f"{row['학수번호']}-{number.zfill(2)}"
                else:
                    lecture_code = f"{row['학수번호']}-{number}"
            else:
                lecture_code = ' - '
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
            if row['등급'] == 'F' and row['학점'] == 1:
                grade = 'NP',
                credit = 0
            else:
                grade = row['등급']
                credit = row['학점']
            lecture_data = {
                'year': row['년도'],
                'season': season,
                'code': lecture_code,
                'credit': credit,
                'grade': grade,
                'name': row['교과목명']
            }
            user_lectures.append(lecture_data)
        
        return user_lectures
