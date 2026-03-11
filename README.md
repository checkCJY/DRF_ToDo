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

<img src="docs/screenshots/11/11_create.png" width="500"/>
<img src="docs/screenshots/11/11_list.png" width="500"/>
<img src="docs/screenshots/11/11_detail.png" width="500"/>
<img src="docs/screenshots/11/11_update.png" width="500"/>

### 1️⃣2️⃣ 다른 사용자 글 조회 기능

<img src="docs/screenshots/12/12_비로그인상태_목록조회와 is_public 확인.png" width="500"/>

### 1️⃣3️⃣ SQLite → PostgreSQL 전환


<img src="docs/screenshots/13/13_sqlite3_backup.png" width="500"/>
<img src="docs/screenshots/13/13_postgreSQL_migrate.png" width="500"/>
<img src="docs/screenshots/13/13_shell_check.png" width="500"/>
<img src="docs/screenshots/13/13_postgreSQL_DBeaver.png" width="500"/>
<img src="docs/screenshots/13/13_DBeaver_check.png" width="500"/>


### 1️⃣4️⃣ 웹 크롤링 → CSV / JSONL 데이터 정제

<img src="docs/screenshots/14_15/14_디비버_데이터확인.png" width="500"/>

### 1️⃣5️⃣ DBeaver → DRF 데이터 적재

<img src="docs/screenshots/14_15/15_curl_check.png" width="500"/>
<img src="docs/screenshots/14_15/15_admin_data_check1.png" width="500"/>
<img src="docs/screenshots/14_15/15_admin_data_check2.png" width="500"/>

### 1️⃣6️⃣ DRF에 Hugging Face 모델 연동

<img src="docs/screenshots/16/16_hf_model_check.png" width="500"/>
<img src="docs/screenshots/16/16_hf_model_curl.png" width="500"/>
<img src="docs/screenshots/16/16_텍스트 감정분석 추론_1.png" width="500"/>
<img src="docs/screenshots/16/16_텍스트 감정분석 추론_2.png" width="500"/>
<img src="docs/screenshots/16/16_텍스트 감정분석 추론_get.png" width="500"/>

### 1️⃣7️⃣ Redis / Celery로 비동기 적용하기

<img src="docs/screenshots/17/17_감정추론_동기식(처음 추론).png" width="500"/>
<img src="docs/screenshots/17/17_감정추론_비동기식.png" width="500"/>

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
DRF_ToDo/
├── mysite/                    # Django 프로젝트 설정 (settings, urls 등)
│   ├── celery.py              # Celery 설정
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── todo/                      # Todo CRUD 앱
│   ├── views/
│   │   ├── api_views.py       # DRF ViewSet 기반 API
│   │   ├── templates_views.py # 템플릿 렌더링 뷰 (CBV)
│   │   └── permissions.py     # 커스텀 권한
│   ├── tests/                 # 테스트 모음
│   │   ├── conftest.py
│   │   ├── test_crud.py
│   │   ├── test_auth.py
│   │   ├── test_image.py
│   │   ├── test_model.py
│   │   ├── test_pagination.py
│   │   ├── test_serializer.py
│   │   ├── test_admin.py
│   │   ├── test_template_views.py
│   │   └── test_viewset_crud.py
│   ├── models.py              # Todo 모델 (제목, 내용, 이미지, 완료 여부 등)
│   ├── serializers.py         # Todo 직렬화
│   ├── pagination.py          # 커스텀 페이지네이션
│   ├── admin.py
│   └── urls.py
├── accounts/                  # 인증 앱 (회원가입, 로그인, JWT)
│   ├── views.py               # API 뷰
│   ├── views_page.py          # 템플릿 렌더링 뷰
│   ├── serializers.py
│   ├── models.py
│   └── urls.py
├── interaction/               # 좋아요 / 북마크 / 댓글 앱
│   ├── tests/                 # Interaction 관련 테스트
│   ├── models.py              # Like, Bookmark, Comment 모델
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
├── reviews/                   # 네이버 영화 리뷰 앱 (크롤링 + 감정분석)
│   ├── management/commands/
│   │   └── import_collected_reviews.py  # 리뷰 데이터 적재 커맨드
│   ├── tests/
│   │   ├── conftest.py
│   │   └── test_reviews_async.py        # 비동기 처리 테스트
│   ├── models.py              # Review 모델
│   ├── serializers.py
│   ├── services.py            # 감정분석 서비스 로직
│   ├── tasks.py               # Celery 비동기 태스크
│   ├── views.py
│   └── urls.py
├── templates/                 # HTML 템플릿
│   ├── accounts/              # 로그인, 회원가입
│   ├── todo/                  # Todo 목록, 상세, 생성, 수정
│   ├── reviews/               # 리뷰 페이지
│   ├── base.html
│   ├── auth_base.html
│   ├── header.html
│   └── footer.html
├── static/                    # 정적 파일
│   ├── css/                   # 페이지별 스타일시트
│   └── js/                    # Todo / Reviews 관련 JS
├── media/                     # 업로드된 이미지
├── docs/                      # 문서 및 스크린샷
│   ├── guide/
│   │   ├── guide.md
│   │   └── Commit_Rules.md
│   ├── study/
│   │   ├── study.md
│   │   ├── question.md
│   │   ├── interaction_workflow.md
│   │   └── order.md
│   └── screenshots/           # 단계별 스크린샷 (01/ ~ 16/)
├── .github/workflows/
│   └── django.yml             # CI 워크플로우
├── manage.py
├── main.py                    # Celery 워커 진입점
├── docker-compose.yml         # Docker 구성
├── pyproject.toml             # 패키지 및 도구 설정 (ruff, pytest 등)
├── pytest.ini                 # pytest 설정
├── requirements.txt
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
