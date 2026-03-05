from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status  # 추가, HTTP 상태코드를 담고있음
from ..models import Todo  # 경로변경
from ..serializers import TodoSerializer  # 경로변경


# 전체보기
class TodoListAPI(APIView):
    def get(self, request):
        # GET 요청이 들어오면 실행되는 함수

        todos = Todo.objects.all()
        # Todo 모델의 모든 데이터 조회 (QuerySet)

        serializer = TodoSerializer(todos, many=True)
        # 조회한 Todo 객체들을 Serializer로 JSON 변환 준비
        # many=True → 여러 개의 객체를 변환한다는 의미

        return Response(serializer.data)
        # serializer.data를 JSON 형태로 변환하여 API 응답으로 반환


# 생성하기
class TodoCreateAPI(APIView):

    def post(self, request):
        # POST 요청이 들어오면 실행되는 함수 (데이터 생성 요청)

        serializer = TodoSerializer(data=request.data)
        # 요청(request)으로 들어온 JSON 데이터를 Serializer에 전달

        serializer.is_valid(raise_exception=True)
        # 데이터 유효성 검사 수행
        # 잘못된 데이터가 있으면 자동으로 400 에러 발생

        todo = serializer.save()
        # 검증된 데이터를 Todo 모델에 저장 (DB에 새로운 데이터 생성)

        return Response(TodoSerializer(todo).data, status=status.HTTP_201_CREATED)
        # 생성된 Todo 객체를 다시 Serializer로 JSON 변환 후 응답
        # HTTP 상태코드 201 (생성 성공)


# 상세보기 API
class TodoRetrieveAPI(APIView):

    def get(self, request, pk):
        # GET 요청이 들어오면 실행되는 함수
        # pk는 URL에서 전달된 Todo의 기본키(id)

        try:
            todo = Todo.objects.get(pk=pk)
            # pk 값에 해당하는 Todo 데이터를 DB에서 조회

        except Todo.DoesNotExist:
            # 해당 pk의 Todo가 존재하지 않을 경우 실행

            return Response(
                {"error": "해당하는 todo가 없습니다."},
                # 에러 메시지를 JSON 형태로 반환
                status=status.HTTP_404_NOT_FOUND,
                # HTTP 상태코드 404 (데이터 없음)
            )

        serializer = TodoSerializer(todo)
        # 조회한 Todo 객체를 Serializer로 JSON 변환 준비

        return Response(serializer.data)
        # 변환된 데이터를 JSON 응답으로 반환
