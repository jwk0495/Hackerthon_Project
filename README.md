#🛸 드론 웹 관제 시스템 프로젝트 매뉴얼

### ***Python과 Pixhawk를 이용한 드론 웹 기반 관제 시스템 프로젝트입니다.***

---
#🌳 Git 협업 규칙 (Git Workflow)
### **★ 모든 작업은 개인 브랜치(Branch)에서 진행하고, main 브랜치에는 직접 커밋하지 말아주세요! ★**

### 작업 시작 전 (매번)
>***목표: 내 개인 브랜치를 팀의 최신 작업 내용(main 브랜치)과 동일한 상태로 만듭니다.***
>
>***1. main 브랜치로 이동하여 최신 내용 가져오기 (Pull)***
>`git checkout main`
>
>`git pull origin main`
>
>2. 본인 개인 브랜치로 이동
>`git checkout 본인브랜치이름`
>
>3. 최신 main 브랜치를 내 개인 브랜치로 병합 (Merge)
>
>+ **`매우 중요: 이 과정을 통해 다른 팀원들의 작업 내용을 내 브랜치에 먼저 반영합니다.`**
>   + `git merge main`
>
>   + 만약 충돌(Conflict)이 발생하면, 충돌 부분을 해결한 후 커밋해야 합니다.
>
>4. 이제 내 개인 브랜치는 팀의 최신 내용을 모두 포함한 상태가 되었습니다. 여기서 새로운 작업을 시작합니다.

### 작업 완료 후
>***목표: 내가 작업한 내용을 팀원들과 공유하기 위해 main 브랜치에 반영 요청을 보냅니다.***

>**1. 내 작업 내용 커밋 (Commit)**
>`git add .`
>`git commit -m "작업 내용 요약"`
>
>**2. 내 브랜치를 GitHub에 푸시 (Push)**
>`git push origin 본인브랜치이름`
>
>**3. Pull Request (PR) 생성**

>GitHub 저장소 페이지로 이동하여 `"Compare & pull request"` 버튼을 클릭합니다.

내 브랜치의 변경 사항을 main 브랜치로 병합해달라는 요청(PR)을 작성합니다.

제목과 내용을 잘 작성한 후 PR을 생성하고, 팀원들에게 리뷰를 요청합니다.

⚙️ 개발 환경 설정 (Development Environment Setup)
1. Python 설치
PC에 파이썬이 설치되어 있지 않다면, python.org에서 최신 버전을 다운로드하여 설치합니다.

설치 시 "Add Python to PATH" 옵션을 반드시 체크해주세요.

2. 가상 환경 생성 및 활성화
터미널(CMD 또는 PowerShell)을 열고 프로젝트 폴더로 이동합니다.

:: 예시: C 드라이브의 프로젝트 폴더로 이동
cd C:\Hackerthon_Project

가상 환경 생성 (최초 한 번만)

python -m venv venv

가상 환경 활성화

venv\Scripts\activate

성공하면 프롬프트 맨 앞에 (venv) 가 표시됩니다.

3. 필수 라이브러리 설치
가상 환경이 활성화된 상태에서, 아래 명령어를 실행하여 필요한 모든 라이브러리를 설치합니다.

pip install flask flask-socketio dronekit pymavlink prompt_toolkit wxPython

▶️ 시스템 실행 방법 (How to Run)
두 개의 터미널 창이 필요합니다. 각 터미널에서 아래 작업을 순서대로 진행하세요.

사전 준비: 드론 연결 및 COM 포트 확인
드론 연결: 픽스호크를 USB 케이블로 PC에 연결합니다.

COM 포트 확인:

**'장치 관리자'**를 실행하고 '포트 (COM & LPT)' 항목을 확인합니다.

ArduPilot 또는 STM32 Virtual COM Port 옆의 COM 포트 번호(예: COM5)를 기억해둡니다.

터미널 1: MAVProxy 실행 (드론 ↔ 서버 연결)
새 터미널을 열고 프로젝트 폴더로 이동 후 가상 환경을 활성화합니다.

cd C:\Hackerthon_Project
venv\Scripts\activate

아래 명령어로 MAVProxy를 실행합니다.

--master=COM5 부분은 위에서 확인한 자신의 COM 포트 번호로 반드시 변경해야 합니다.

python venv\Scripts\mavproxy.py --master=COM5 --out=udp:127.0.0.1:14550 --console

성공하면 STABILIZE> 같은 프롬프트가 나타납니다. 이 창은 끄지 말고 그대로 두세요.

터미널 2: 웹 서버 실행 (app.py)
또 다른 새 터미널을 열고, 마찬가지로 프로젝트 폴더 이동 및 가상 환경을 활성화합니다.

cd C:\Hackerthon_Project
venv\Scripts\activate

아래 명령어로 파이썬 웹 서버를 실행합니다.

python app.py

성공하면 Vehicle Connected!와 Running on http://127.0.0.1:8282 메시지가 나타납니다. 이 창도 끄지 말고 그대로 두세요.

최종 단계: 웹 UI 접속
크롬과 같은 웹 브라우저를 엽니다.

주소창에 http://127.0.0.1:8282 를 입력합니다.

화면에 드론 관제 시스템이 나타나고, '연결 상태'가 '연결됨'으로 바뀌면 성공입니다.

📂 폴더 구조 (Folder Structure)
Hackerthon_Project/

venv/: 파이썬 가상환경 폴더

templates/: HTML 파일 보관

index2.html: 웹 관제 UI

app.py: 웹 서버 로직

README.md: 프로젝트 설명 문서 (현재 파일)