from ..models import Todo
from django.views.generic import ListView
from django.urls import reverse_lazy

# 함수형 list
# def todo_list(request):
#     todos = Todo.objects.all()
#     return render(request, "todo/todo.html", {"todos": todos})

# 클래스형 list
# class TodoListView(View):
#     def get(self, request):
#         todos = Todo.objects.all()
#         return render(request, "todo/todo.html", {"todos": todos})

# 제네릭뷰 list
# class TodoListGenericView(ListView):
#     model = Todo
#     template_name = "todo/todo.html"  # 기본값: todo_list.html
#     context_object_name = "todos"  # 기본값: object_list


class TodoListView(ListView):
    """
    투두 목록을 보여주는 제너릭 뷰.

    model              : 사용할 모델
    template_name      : 렌더링할 HTML 템플릿
    context_object_name: 템플릿에서 사용할 변수 이름 (기본값: object_list)
    ordering           : 최신 생성순 정렬
    success_url        : 작업 성공 후 이동할 URL (ListView에서는 보통 불필요)
    """

    model = Todo
    template_name = "todo/list.html"
    context_object_name = "todos"
    ordering = ["-created_at"]
    success_url = reverse_lazy("todo:list")
