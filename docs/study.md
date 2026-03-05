### detail.html

// 방식 1: Django 템플릿 태그
window.location.href = "{% url 'todo:list' %}";

// 방식 2: 하드코딩
window.location.href = `/todo/update/${todoId}/`;

실무에서는 상황에 따라 다르게 써요.

JS 변수 없는 고정 URL -> {% URL %}
JS 변수가 포함된 동적 URL -> 하드코딩 or data 속성 활용

{% url %}은 URL이 바뀌어도 자동으로 따라가는 장점이 있지만, JS 변수를 중간에 끼워넣기가 어려워요.
그래서 pk가 포함된 URL은 이런 패턴을 많이 써요.
html<!-- data 속성으로 URL을 미리 렌더링해서 JS에 전달 -->
<div class="btnList"
  data-update-url="{% url 'todo:todo_Update' todo.id %}"
  data-delete-url="{% url 'todo:todo_api_delete' todo.id %}">
javascriptconst updateUrl = document.querySelector(".btnList").dataset.updateUrl;
window.location.href = updateUrl;


### Part 5. 페이지네이션

전체 흐름을 요청-응답 순서로 정리할게요.

1. 클라이언트 요청
브라우저 → GET /todo/viewsets/view/?page=2

2. Django URL → ViewSet 도달
urls.py → TodoViewSet.list() 실행

3. ViewSet에서 페이지네이션 적용
ViewSet
  └─ queryset 전체 조회 (Todo.objects.all())
  └─ settings.py의 DEFAULT_PAGINATION_CLASS 확인
  └─ CustomPageNumberPagination.paginate_queryset() 호출
       └─ ?page=2 파라미터 읽어서 해당 슬라이스만 잘라냄

4. 응답 구조 생성
CustomPageNumberPagination.get_paginated_response() 호출
  └─ OrderedDict로 응답 구조 커스터마이징
       └─ data, total_count, page_count, current_page, next, previous

5. 클라이언트 수신 후 JS 처리
res.data 수신
  └─ renderTodos(data.data)       → DOM 생성
  └─ updatePaginationUI(data)     → 버튼 활성화/비활성화, 페이지 표시
  └─ currentPage = data.current_page → 상태 업데이트

핵심 포인트 한 줄 요약
역할담당몇 개씩 자를지PAGE_SIZE (settings.py)어떻게 자를지paginate_queryset()응답 구조get_paginated_response()UI 제어JS updatePaginationUI()

결국 "settings → ViewSet → pagination.py → JS" 순서로 데이터가 흘러가는 구조

---
#####  페이지네이션 아래같은 로그가 남는 이유

[05/Mar/2026 17:31:16] "GET /.well-known/appspecific/com.chrome.devtools.json HTTP/1.1" 404 2610
[05/Mar/2026 17:31:23] "GET /.well-known/appspecific/com.chrome.devtools.json HTTP/1.1" 404 2610

Chrome 개발자 도구가 열려있을 때 DevTools 설정 파일을 찾으려고 자동으로
/.well-known/appspecific/com.chrome.devtools.json을 요청
-> Django에 해당 URL이 없으니 404 발생.
