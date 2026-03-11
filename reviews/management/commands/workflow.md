CSV/JSONL 파일
    ↓
① 파일 읽기 (_read_csv / _read_jsonl)
    ↓
② 컬럼 매핑 (pick 함수)
   - 파일마다 컬럼명이 달라도 대응 가능
   - name/title/subject → title
   - description/review/content → review
    ↓
③ doc_id 생성
   - 파일에 doc_id 있으면 그대로 사용
   - 없으면 내용 기반 SHA256 해시로 생성
    ↓
④ CollectedReview 객체 생성 (아직 DB 저장 X)
    ↓
⑤ bulk_create로 DB 일괄 저장
   - ignore_conflicts=True → doc_id 중복이면 자동 스킵


실행 명령어
python manage.py import_collected_reviews --path naver_influencer_movie_reviews.csv --source naver
