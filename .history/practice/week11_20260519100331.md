# Week 11 실습

## 오늘 한 것
PyInstaller 설치 및 빌드
resource_path() 함수 추가
--add-data 옵션으로 에셋 포함
.exe 실행 확인

## resource_path() 를 써야 하는 이유
PyInstaller로 프로그램을 exe 파일로 만들면 이미지나 사운드 파일의 경로가 기존과 달라질 수 있다. 그래서 실행 파일 내부에서도 에셋 파일을 정상적으로 불러오기 위해 resource_path() 함수를 사용한다. 이를 통해 개발 환경과 exe 실행 환경 모두에서 같은 코드로 파일을 불러올 수 있다.

## 빌드 명령어
-## 빌드 명령어

### STEP 1 — 기본
pyinstaller --onefile game.py

### STEP 2 — 터미널 창 숨기기 (배포용)
pyinstaller --onefile --windowed game.py

### STEP 3 — 에셋 포함 + 이름 지정
pyinstaller --onefile --windowed --add-data "assets;assets" --name=MyGame game.py

## AI 활용 내역
PyInstaller 사용 방법 질문
resource_path() 함수 추가 방법 질문
exe 빌드 오류 해결 방법 질문
--add-data 옵션 사용 방법 질문