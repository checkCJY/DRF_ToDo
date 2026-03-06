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


---


현재 코드에서 과한 부분

# 문제가 없으면 username 반환
return value

# 생성된 user 객체 반환
return user
이런 주석은 코드 자체로 명백한 내용이라 실무에서는 오히려 노이즈로 취급됩니다.

실무 기준
상황	주석 필요 여부
코드만 봐도 명확한 로직	❌ 불필요
비즈니스 규칙 / 도메인 지식	✅ 필요
DRF 같은 프레임워크의 암묵적 동작	✅ 유용
Public API / 라이브러리	✅ 필수
팀 내부 코드	팀 컨벤션 따름
실무에서 가치 있는 주석 예시

def validate_username(self, value):
    # DRF는 validate_<field_name> 형식의 메서드를 자동으로 호출한다
    if User.objects.filter(username=value).exists():
        raise serializers.ValidationError("이미 사용중인 username 입니다.")
    return value
DRF 자동 호출 방식 같은 프레임워크의 숨겨진 동작은 처음 보는 사람이 모를 수 있어서 유용합니다.

결론
지금 코드는 학습/포트폴리오 목적이라면 충분히 좋습니다. 다만 실무 코드에서는:

"왜(Why)" 는 주석으로 → 의도, 비즈니스 규칙, 비직관적 선택
"무엇(What)" 은 코드 자체로 → 깔끔한 네이밍으로 표현
이 원칙을 따르는 게 일반적입니다.
