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


```
parser의 출처

create_parser()에서 CommandParser 객체를 생성하고, 마지막에 self.add_arguments(parser)로 넘겨줌
즉 Django가 자동으로 만들어서 전달하는 argparse.ArgumentParser 객체

parser로 할 수 있는 것

add_argument()로 CLI 인자 정의 (--path, --limit, --dry-run 등)
실행 시 python manage.py 커맨드명 --path data.csv 형태로 사용

오버라이딩 구조

BaseCommand는 add_arguments를 비워두고, handle은 NotImplementedError로 강제
add_arguments → 선택적 오버라이딩
handle → 필수 오버라이딩

전체 실행 흐름
python manage.py import_collected_reviews --path data.csv
    ↓
create_parser() → add_arguments(parser) → parser 인자 등록
    ↓
execute() → handle() → 실제 로직 실행
    ↓
options["path"] 로 값 꺼내서 사용
```
