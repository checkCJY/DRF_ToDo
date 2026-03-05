# from rest_framework.views import APIView    # viewsets 사용으로 안씀.
from rest_framework import viewsets  # viewsets 사용을 위해 추가
from ..models import Todo
from ..serializers import TodoSerializer
from rest_framework.pagination import PageNumberPagination


class TodoViewSet(viewsets.ModelViewSet):
    queryset = Todo.objects.all().order_by("-created_at")
    serializer_class = TodoSerializer


"""
ModelViewSet을 사용하면 아래 기능이 자동 생성됩니다
- list()      : 전체 목록 조회 (GET)
- retrieve()  : 단일 데이터 조회 (GET)
- create()    : 데이터 생성 (POST)
- update()    : 전체 수정 (PUT)
- partial_update() : 부분 수정 (PATCH)
- destroy()   : 삭제 (DELETE)
"""


# Todo 목록 페이지네이션 설정
class TodoListPagination(PageNumberPagination):

    page_size = 3
    page_size_query_param = "page_size"
    max_page_size = 50


"""
page_size=              : 한 페이지에 기본적으로 보여줄 데이터 개수
page_size_query_param   : URL 쿼리 파라미터로 페이지 크기 변경 가능
max_page_size           : 사용자가 설정할 수 있는 최대 페이지 크기 제한
"""

# 아래 내용들은 Viewset 사용으로 인해서 안쓰는 코드
# 삭제해도 무방하나, 에러발생을 방지하기 위해 남겨둠
# class TodoListAPI(APIView):
#     """전체 Todo 목록을 반환하는 API"""

#     def get(self, request):
#         todos = Todo.objects.all()
#         serializer = TodoSerializer(todos, many=True)  # many=True: 복수 객체 직렬화
#         return Response(serializer.data)


# class TodoCreateAPI(APIView):
#     """새 Todo를 생성하는 API"""

#     def post(self, request):
#         serializer = TodoSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)  # 유효하지 않으면 400 자동 반환
#         todo = serializer.save()
#         return Response(TodoSerializer(todo).data, status=status.HTTP_201_CREATED)


# class TodoRetrieveAPI(APIView):
#     """특정 Todo의 상세 정보를 반환하는 API"""

#     def get(self, request, pk):
#         try:
#             todo = Todo.objects.get(pk=pk)
#         except Todo.DoesNotExist:
#             return Response(
#                 {"error": "해당하는 todo가 없습니다."}, status=status.HTTP_404_NOT_FOUND
#             )

#         serializer = TodoSerializer(todo)
#         return Response(serializer.data)


# class TodoUpdateAPI(APIView):
#     """특정 Todo를 수정하는 API (PUT: 전체 수정, PATCH: 부분 수정)"""

#     def put(self, request, pk):
#         try:
#             todo = Todo.objects.get(pk=pk)
#         except Todo.DoesNotExist:
#             return Response(
#                 {"error": "해당하는 todo가 없습니다."}, status=status.HTTP_404_NOT_FOUND
#             )

#         serializer = TodoSerializer(todo, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         todo = serializer.save()
#         return Response(TodoSerializer(todo).data)

#     def patch(self, request, pk):
#         try:
#             todo = Todo.objects.get(pk=pk)
#         except Todo.DoesNotExist:
#             return Response(
#                 {"error": "해당하는 todo가 없습니다."}, status=status.HTTP_404_NOT_FOUND
#             )

#         serializer = TodoSerializer(
#             todo, data=request.data, partial=True
#         )  # partial=True: 일부 필드만 수정 허용
#         serializer.is_valid(raise_exception=True)
#         todo = serializer.save()
#         return Response(TodoSerializer(todo).data)


# class TodoDeleteAPI(APIView):
#     """특정 Todo를 삭제하는 API"""

#     def delete(self, request, pk):
#         try:
#             todo = Todo.objects.get(pk=pk)
#         except Todo.DoesNotExist:
#             return Response(
#                 {"error": "해당하는 todo가 없습니다."}, status=status.HTTP_404_NOT_FOUND
#             )

#         todo.delete()
#         return Response(
#             status=status.HTTP_204_NO_CONTENT
#         )  # 204: 성공했지만 반환 데이터 없음
