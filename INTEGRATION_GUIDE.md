# GitHub - SonarCloud - Jira 연동 완료 가이드

## ✅ 완료된 항목

1. ✅ Git 설치 확인 (2.51.0)
2. ✅ SonarCloud 프로젝트: `logos-1_sonargit`
3. ✅ Jira 프로젝트: `BTS`
4. ✅ GitHub Secrets: `SONAR_TOKEN` 등록
5. ✅ GitHub Actions 워크플로우 생성
6. ✅ Jira 연동 스크립트 생성

---

## 🔐 추가로 필요한 GitHub Secrets (2개)

GitHub Actions가 Jira에 이슈를 생성하려면 2개의 추가 Secret이 필요합니다:

### 1️⃣ JIRA_API_TOKEN 생성

**단계:**
1. https://id.atlassian.com/manage-profile/security/api-tokens 접속
2. **"Create API token"** 클릭
3. Label 입력: `github-actions`
4. **"Create"** 클릭
5. 토큰 복사 (다시 볼 수 없으니 저장!)

### 2️⃣ JIRA_EMAIL 확인

본인의 Jira 로그인 이메일 주소입니다.
예: `yjlee@logossoft.co.kr` 또는 `yjlee32333@gmail.com`

---

## 🔒 GitHub Secrets에 등록하기

### 방법 1: 링크 직접 접속
https://github.com/logos-1/sonargit/settings/secrets/actions

### 방법 2: 수동으로 찾아가기
1. https://github.com/logos-1/sonargit 접속
2. **Settings** 탭 클릭
3. 왼쪽 메뉴: **Secrets and variables** → **Actions**
4. **"New repository secret"** 클릭

### 등록할 Secrets (2개):

#### Secret 1:
```
Name: JIRA_API_TOKEN
Secret: (위에서 생성한 Jira API 토큰 붙여넣기)
```

#### Secret 2:
```
Name: JIRA_EMAIL
Secret: (본인의 Jira 이메일 주소, 예: yjlee@logossoft.co.kr)
```

---

## 🚀 코드를 GitHub에 푸시하기

터미널에서 실행:

```bash
cd C:\Users\YEJI\sonargit
git add .
git commit -m "Add SonarCloud and Jira integration"
git push origin main
```

또는 main이 아니라 master 브랜치인 경우:
```bash
git push origin master
```

---

## 🎯 작동 방식

1. **코드를 GitHub에 푸시**
   ↓
2. **GitHub Actions 자동 실행**
   - SonarCloud 분석 수행
   ↓
3. **코드 품질 이슈 발견**
   ↓
4. **Jira에 자동으로 티켓 생성**
   - 프로젝트: BTS
   - 이슈 타입: 작업
   - SonarCloud 이슈 정보 포함

---

## 📊 확인 방법

### GitHub Actions 실행 확인:
https://github.com/logos-1/sonargit/actions

### Jira 티켓 확인:
https://yjlee32333.atlassian.net/jira/software/projects/BTS/boards/1

### SonarCloud 대시보드:
https://sonarcloud.io/project/overview?id=logos-1_sonargit

---

## 🔔 다음 단계

1. Jira API 토큰 생성 및 GitHub Secrets 등록
2. 이메일 주소 GitHub Secrets에 등록
3. 코드를 GitHub에 푸시
4. GitHub Actions 실행 확인
5. Jira에 자동 생성된 티켓 확인

---

## 💡 추가 정보

- **워크플로우 파일**: `.github/workflows/sonar-jira.yml`
- **Jira 스크립트**: `.github/scripts/sonar_to_jira.py`
- **실행 조건**: main 또는 master 브랜치에 푸시할 때마다
- **중복 방지**: 같은 SonarCloud 이슈는 한 번만 Jira 티켓 생성

---

## 🆘 문제 해결

### GitHub Actions가 실행 안 되는 경우:
- Settings → Actions → General → "Allow all actions" 확인

### Jira 티켓이 생성 안 되는 경우:
- GitHub Secrets 3개가 모두 등록되었는지 확인
- Jira API 토큰이 유효한지 확인
- Actions 탭에서 에러 로그 확인

---

생성 일시: 2026-01-26
프로젝트: sonargit (logos-1)
