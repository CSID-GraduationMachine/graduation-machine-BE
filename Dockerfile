# 베이스 이미지로 Python 3.12.3 사용
FROM python:3.12.3

# 작업 디렉토리 설정
WORKDIR /usr/src/app

# 종속성 설치
COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 코드 복사
COPY . .

# Django 애플리케이션이 있는 디렉토리로 이동
WORKDIR /usr/src/app/graduation_machine

# 컨테이너 외부에서 접근할 수 있도록 포트 8000 노출
EXPOSE 8000

# Gunicorn을 사용하여 WSGI 서버 실행
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "graduation_machine.wsgi:application"]
