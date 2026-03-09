# 🚀 todoList_Django_to_DRF

이 프로젝트는 Django 기반 Todo 애플리케이션을 시작으로
Django REST Framework, JWT 인증, PostgreSQL 전환,
AI 모델 연동(Hugging Face), Redis/Celery 비동기 처리까지
단계적으로 확장하는 풀스택 학습 프로젝트입니다.

---

## 📌 프로젝트 목표

- Django MVT 구조 이해
- DRF 기반 API 설계
- 인증(JWT) 시스템 구축
- 데이터베이스 전환(SQLite → PostgreSQL)
- 외부 데이터 수집 및 적재
- AI 모델 연동
- Redis/Celery 기반 비동기 처리
- 실무형 프로젝트 구조 설계

---

## 🧭 전체 개발 로드맵

### 1️⃣ Django 기본 세팅

<img src="docs/screenshots/01/01_check.png" width="500"/>
<img src="docs/screenshots/01/01_admin.png" width="500"/>


### 2️⃣ Generic View 기반 CRUD

##### **API 확인**
<img src="docs/screenshots/02/02_get_api.png" width="500"/>

##### **CRUD**
<img src="docs/screenshots/02/02_create.png" width="500"/>
<img src="docs/screenshots/02/02_get_detail.png" width="500"/>
<img src="docs/screenshots/02/02_update.png" width="500"/>
<img src="docs/screenshots/02/02_delete.png" width="500"/>
<img src="docs/screenshots/02/02_delete_check.png" width="500"/>


### 3️⃣ DRF ViewSets로 API 전환
##### **CRUD**
<img src="docs/screenshots/03/03_Create_viewsets.png" width="500"/>
<img src="docs/screenshots/03/03_list_viewsets.png" width="500"/>
<img src="docs/screenshots/03/03_Retrieve_viewsets.png" width="500"/>
<img src="docs/screenshots/03/03_Patch_viewsets.png" width="500"/>
<img src="docs/screenshots/03/03_Delete1_viewsets.png" width="500"/>
<img src="docs/screenshots/03/03_Delete2_viewsets.png" width="500"/>

### 4️⃣ 환경 변수 설정 (.env)

<img src="docs/screenshots/04/04_env.png" width="500"/>

### 5️⃣ Pagination 추가

<img src="docs/screenshots/05/05_pagenation1.png" width="500"/>
<img src="docs/screenshots/05/05_pagenation2.png" width="500"/>
<img src="docs/screenshots/05/05_pagenation3.png" width="500"/>

### 6️⃣ 이미지 업로드 기능 추가

##### **API**

<img src="docs/screenshots/06/06_이미지파일_추가.png" width="500"/>
<img src="docs/screenshots/06/06_image_fales.png" width="500"/>
<img src="docs/screenshots/06/06_image_True.png" width="500"/>

##### **Page**

<img src="docs/screenshots/06/06_image_page.png" width="500"/>
<img src="docs/screenshots/06/06_image_update.png" width="500"/>


### 7️⃣ 회원가입 / 로그인 기능 구현

##### **Page**

<img src="docs/screenshots/07/07_signup.png" width="500"/>
<img src="docs/screenshots/07/07_cookiecheck.png" width="500"/>
<img src="docs/screenshots/07/07_cookiecheck_another_user.png" width="500"/>


### 8️⃣ 템플릿 구조 정리

##### **login/signup Page**

<img src="docs/screenshots/08/08_login.png" width="500"/>
<img src="docs/screenshots/08/08_signup.png" width="500"/>

##### **CRUD Page**

<img src="docs/screenshots/08/08_create.png" width="500"/>
<img src="docs/screenshots/08/08_list.png" width="500"/>
<img src="docs/screenshots/08/08_detail.png" width="500"/>
<img src="docs/screenshots/08/08_update.png" width="500"/>
<img src="docs/screenshots/08/08_delete.png" width="500"/>

### 9️⃣ JWT 인증 도입

##### ** Header 변경 **
<img src="docs/screenshots/09/09_login_header.png" width="500"/>

##### ** localStorage **

<img src="docs/screenshots/09/09_localStorage_access.png" width="500"/>
<img src="docs/screenshots/09/09_localStorage_refresh.png" width="500"/>

##### ** JWT 인증 전환 **

<img src="docs/screenshots/09/09_JWT_settings.png" width="500"/>
<img src="docs/screenshots/09/09_JWT_API.png" width="500"/>
<img src="docs/screenshots/09/09_jwt_io.png" width="500"/>

### 🔟 인터랙티브 기능 추가 (Ajax / Axios)

##### ** Page **

<img src="docs/screenshots/10/10_liketest.png" width="500"/>
<img src="docs/screenshots/10/10_로그아웃이후_북마크시도.png" width="500"/>
##### ** develop Tool **

<img src="docs/screenshots/10/10_like.png" width="500"/>
<img src="docs/screenshots/10/10_bookmark.png" width="500"/>
<img src="docs/screenshots/10/10_context.png" width="500"/>

### 1️⃣1️⃣ CSS 및 UI 정리


##### ** CSS 적용 확인 **

<img src="docs/screenshots/11/11_signup.png" width="500"/>
<img src="docs/screenshots/11/11_login.png" width="500"/>

<img src="docs/screenshots/11/11_create.png.png" width="500"/>
<img src="docs/screenshots/11/11_list.png" width="500"/>
<img src="docs/screenshots/11/11_detail.png" width="500"/>
<img src="docs/screenshots/11/11_update.png" width="500"/>

### 1️⃣2️⃣ 다른 사용자 글 조회 기능

<img src="docs/screenshots/12/12_비로그인상태_목록조회와 is_public 확인.png" width="500"/>

### 1️⃣3️⃣ SQLite → PostgreSQL 전환

### 1️⃣4️⃣ 웹 크롤링 → CSV / JSONL 데이터 정제

### 1️⃣5️⃣ DBeaver → DRF 데이터 적재

### 1️⃣6️⃣ DRF에 Hugging Face 모델 연동

### 1️⃣8️⃣ Redis + Celery 비동기 처리 및 캐시 적용

---

## 🛠 사용 기술

### Backend
- Python
- Django
- Django REST Framework
- Django ORM
- JWT (SimpleJWT)

### Database
- SQLite3 (개발 초기)
- PostgreSQL (확장 단계)

### AI / Data
- Hugging Face
- Pandas
- CSV / JSONL 데이터 처리

### Async / Cache
- Redis
- Celery

### Frontend
- Django Template
- HTML5 / CSS3
- JavaScript
- Axios

### DevOps
- Git / GitHub
- pre-commit
- Docker (예정)
- AWS EC2 (예정)

---

## 📂 프로젝트 구조
```
DRF_todoList/
├── mysite/                    # Django 프로젝트 설정 (settings, urls 등)
├── todo/                      # Todo CRUD 앱
│   ├── views/
│   │   ├── api_views.py       # DRF ViewSet 기반 API
│   │   └── templates_views.py # 템플릿 렌더링 뷰 (CBV)
│   ├── tests/                 # 테스트 모음
│   ├── models.py              # Todo 모델 (제목, 내용, 이미지, 완료 여부 등)
│   ├── serializers.py         # Todo 직렬화
│   ├── pagination.py          # 커스텀 페이지네이션
│   ├── admin.py
│   └── urls.py
├── accounts/                  # 인증 앱 (회원가입, 로그인, JWT)
├── interaction/               # 좋아요 / 북마크 / 댓글 앱
│   ├── tests/                 # Interaction 관련 테스트
│   ├── models.py              # Like, Bookmark, Comment 모델
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
├── templates/                 # HTML 템플릿 (accounts/, todo/)
├── static/                    # 정적 파일 (JS, CSS)
├── media/                     # 업로드된 이미지
├── docs/                      # 문서 및 스크린샷
│   ├── guide.md
│   ├── question.md
│   ├── study.md
│   ├── interaction_workflow.md  # Interaction 앱 설계 문서
│   └── screenshots/           # 단계별 스크린샷 (01/ ~ 10/)
├── manage.py
├── pyproject.toml             # 패키지 및 도구 설정 (ruff, pytest 등)
├── requirements.txt
├── Commit_Rules.md
└── .pre-commit-config.yaml    # pre-commit 훅 설정
```

---

## ⚙ 실행 방법

```bash
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt

python manage.py migrate
python manage.py runserver

---

## 📈 확장 방향

- REST API 기반 프론트엔드 분리
- Docker 기반 배포
- CI/CD 구성
- AI 추천 기능 확장
- 모니터링 시스템(Prometheus/Grafana)


---

## 🎯 프로젝트 성격

이 프로젝트는 단순 Todo 앱이 아닌
"실무 확장형 Django → DRF → AI → 비동기 구조 학습 프로젝트"입니다.
