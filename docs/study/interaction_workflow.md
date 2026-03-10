```
[클라이언트 요청]

        ↓

[Router → TodoViewSet 연결]

        ↓

[Permission 검사]
AllowAny  → 조회 가능
IsAuthenticated → 좋아요/북마크/댓글 가능

        ↓

[Todo 데이터 조회]
Todo.objects.all()

        ↓

[요청 종류 판단]

 ┌───────────────┬───────────────┬───────────────┬───────────────┐
 │ 목록조회       │ 좋아요         │ 북마크         │ 댓글작성       │
 │ GET /todos/   │ POST /like/   │ POST /bookmark│ POST /comments│
 └───────────────┴───────────────┴───────────────┴───────────────┘

        ↓

[데이터 처리]

목록 → serializer → pagination
좋아요 → get_or_create → 토글
북마크 → get_or_create → 토글
댓글 → content 저장

        ↓

[결과 JSON 반환]

{
  data / like_count / bookmark_count / comment_count
}
```
