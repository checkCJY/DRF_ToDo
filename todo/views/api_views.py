from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Todo
from ..serializers import TodoSerializer


class TodoListAPI(APIView):
    """전체 Todo 목록을 반환하는 API"""

    def get(self, request):
        todos = Todo.objects.all()
        serializer = TodoSerializer(todos, many=True)  # many=True: 복수 객체 직렬화
        return Response(serializer.data)


class TodoCreateAPI(APIView):
    """새 Todo를 생성하는 API"""

    def post(self, request):
        serializer = TodoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # 유효하지 않으면 400 자동 반환
        todo = serializer.save()
        return Response(TodoSerializer(todo).data, status=status.HTTP_201_CREATED)


class TodoRetrieveAPI(APIView):
    """특정 Todo의 상세 정보를 반환하는 API"""

    def get(self, request, pk):
        try:
            todo = Todo.objects.get(pk=pk)
        except Todo.DoesNotExist:
            return Response(
                {"error": "해당하는 todo가 없습니다."}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = TodoSerializer(todo)
        return Response(serializer.data)


class TodoUpdateAPI(APIView):
    """특정 Todo를 수정하는 API (PUT: 전체 수정, PATCH: 부분 수정)"""

    def put(self, request, pk):
        try:
            todo = Todo.objects.get(pk=pk)
        except Todo.DoesNotExist:
            return Response(
                {"error": "해당하는 todo가 없습니다."}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = TodoSerializer(todo, data=request.data)
        serializer.is_valid(raise_exception=True)
        todo = serializer.save()
        return Response(TodoSerializer(todo).data)

    def patch(self, request, pk):
        try:
            todo = Todo.objects.get(pk=pk)
        except Todo.DoesNotExist:
            return Response(
                {"error": "해당하는 todo가 없습니다."}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = TodoSerializer(
            todo, data=request.data, partial=True
        )  # partial=True: 일부 필드만 수정 허용
        serializer.is_valid(raise_exception=True)
        todo = serializer.save()
        return Response(TodoSerializer(todo).data)


class TodoDeleteAPI(APIView):
    """특정 Todo를 삭제하는 API"""

    def delete(self, request, pk):
        try:
            todo = Todo.objects.get(pk=pk)
        except Todo.DoesNotExist:
            return Response(
                {"error": "해당하는 todo가 없습니다."}, status=status.HTTP_404_NOT_FOUND
            )

        todo.delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT
        )  # 204: 성공했지만 반환 데이터 없음
