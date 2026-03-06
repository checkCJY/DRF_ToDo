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

<img src="docs/screenshots/01/01_check.png" width="700"/>
<img src="docs/screenshots/01/01_admin.png" width="700"/>


### 2️⃣ Generic View 기반 CRUD

##### **API 확인**
<img src="docs/screenshots/02/02_get_api.png" width="700"/>

##### **CRUD**
<img src="docs/screenshots/02/02_create.png" width="700"/>
<img src="docs/screenshots/02/02_get_detail.png" width="700"/>
<img src="docs/screenshots/02/02_update.png" width="700"/>
<img src="docs/screenshots/02/02_delete.png" width="700"/>
<img src="docs/screenshots/02/02_delete_check.png" width="700"/>


### 3️⃣ DRF ViewSets로 API 전환
##### **CRUD**
<img src="docs/screenshots/03/03_Create_viewsets.png" width="700"/>
<img src="docs/screenshots/03/03_list_viewsets.png" width="700"/>
<img src="docs/screenshots/03/03_Retrieve_viewsets.png" width="700"/>
<img src="docs/screenshots/03/03_Patch_viewsets.png" width="700"/>
<img src="docs/screenshots/03/03_Delete1_viewsets.png" width="700"/>
<img src="docs/screenshots/03/03_Delete2_viewsets.png" width="700"/>

### 4️⃣ 환경 변수 설정 (.env)

<img src="docs/screenshots/04/04_env.png" width="700"/>

### 5️⃣ Pagination 추가

<img src="docs/screenshots/05/05_pagenation1.png" width="700"/>
<img src="docs/screenshots/05/05_pagenation2.png" width="700"/>
<img src="docs/screenshots/05/05_pagenation3.png" width="700"/>

### 6️⃣ 이미지 업로드 기능 추가

##### **API**

<img src="docs/screenshots/06/06_이미지파일_추가.png" width="700"/>
<img src="docs/screenshots/06/06_image_fales.png" width="700"/>
<img src="docs/screenshots/06/06_image_True.png" width="700"/>

##### **Page**

<img src="docs/screenshots/06/06_image_page.png" width="700"/>
<img src="docs/screenshots/06/06_image_update.png" width="700"/>


### 7️⃣ 회원가입 / 로그인 기능 구현

### 8️⃣ 템플릿 구조 정리

### 9️⃣ JWT 인증 도입

### 🔟 인터랙티브 기능 추가 (Ajax / Axios)

### 1️⃣1️⃣ CSS 및 UI 정리

### 1️⃣2️⃣ 다른 사용자 글 조회 기능

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
├── mysite/                    # Django 프로젝트 설정
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── todo/                      # Todo 앱
│   ├── migrations/
│   ├── tests/
│   │   ├── test_admin.py
│   │   ├── test_crud.py
│   │   ├── test_model.py
│   │   ├── test_pagination.py
│   │   ├── test_serializer.py
│   │   ├── test_template_views.py
│   │   └── test_viewset_crud.py
│   ├── views/
│   │   ├── api_views.py
│   │   └── templates_views.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── pagination.py
│   ├── serializers.py
│   └── urls.py
├── templates/                 # HTML 템플릿
│   ├── base.html
│   └── todo/
│       ├── create.html
│       ├── detail.html
│       ├── list.html
│       ├── todo.html
│       └── update.html
├── static/                    # 정적 파일
│   └── todo/
│       ├── api.js
│       ├── style.css
│       └── todo.html
├── media/                     # 업로드된 이미지
│   └── todo_images/
├── docs/                      # 문서 및 스크린샷
│   ├── guide.md
│   ├── question.md
│   ├── study.md
│   └── screenshots/
│       ├── 01/ ~ 06/
├── db.sqlite3
├── main.py
├── manage.py
├── pyproject.toml
├── pytest.ini
├── requirements.txt
├── Commit_Rules.md
└── .pre-commit-config.yaml
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
