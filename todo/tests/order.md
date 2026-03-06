# 전체 테스트 실행
pytest

# 특정 파일만 실행
pytest ./todo/tests/test_image.py

# 특정 클래스만 실행
pytest ./todo/tests/test_image.py::TestTodoImage

# 특정 테스트만 실행
pytest ./todo/tests/test_image.py::TestTodoImage::test_create_todo_with_image

# 결과 상세하게 보기
pytest ./todo/tests/test_image.py -v
