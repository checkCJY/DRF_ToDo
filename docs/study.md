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
