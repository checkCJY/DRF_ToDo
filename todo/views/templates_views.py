from ..models import Todo
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from django.urls import reverse_lazy

# ── 뷰 작성 방식 비교 (참고용) ──────────────────────────────
# 1. 함수형 뷰
# def todo_list(request):
#     todos = Todo.objects.all()
#     return render(request, "todo/todo.html", {"todos": todos})

# 2. 클래스형 뷰 (View 상속)
# class TodoListView(View):
#     def get(self, request):
#         todos = Todo.objects.all()
#         return render(request, "todo/todo.html", {"todos": todos})

# 3. 제네릭 뷰 (ListView 상속) - 아래 실제 코드와 동일한 방식
# class TodoListGenericView(ListView):
#     model = Todo
#     template_name = "todo/todo.html"  # 기본값: <app>/<model>_list.html
#     context_object_name = "todos"     # 기본값: object_list
# ──────────────────────────────────────────────────────────────


class TodoListView(ListView):
    """Todo 목록 페이지. 최신 생성순으로 정렬해서 보여줌."""

    model = Todo
    template_name = "todo/list.html"
    context_object_name = "todos"  # 템플릿에서 {{ todos }}로 접근
    ordering = ["-created_at"]
    success_url = reverse_lazy("todo:list")


class TodoCreateView(CreateView):
    """Todo 생성 페이지. 폼 제출 후 목록 페이지로 리다이렉트."""

    model = Todo
    fields = ["name", "description", "complete", "exp"]  # 자동 생성될 HTML form 필드
    template_name = "todo/create.html"
    success_url = reverse_lazy("todo:list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TodoDetailView(DetailView):
    """특정 Todo의 상세 정보 페이지."""

    model = Todo
    template_name = "todo/detail.html"
    context_object_name = "todo"  # 기본값(object) 대신 todo로 템플릿에 전달


class TodoUpdateView(UpdateView):
    """Todo 수정 페이지. 저장 후 목록 페이지로 리다이렉트."""

    model = Todo
    fields = ["name", "description", "complete", "exp"]
    template_name = "todo/update.html"
    context_object_name = "todo"
    success_url = reverse_lazy("todo:list")
