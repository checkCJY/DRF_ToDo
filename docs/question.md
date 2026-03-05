

##### yml파일

이전 프로젝트에서는 CI 때 더미 장고 key를 넘겨도 넘어갔다.
이번에 env로 설정하고, github action이 작동하지 않아서 찾아보니 2가지 방법이 필요하다고 나온다

1. GitHub 레포 시크릿 등록
GitHub 레포 → Settings → Secrets and variables → Actions → New repository secret

DJANGO_SECRET_KEY 추가

2. yml 파일에 env 추가
Run Migrations 스텝에 이렇게 추가:


더미값으로 충분한 경우 (CI/테스트 환경)
- migrate, pytest 등 테스트만 돌릴 때
- 실제 유저 데이터나 암호화가 필요없을 때

실제 시크릿 키가 필요한 경우
- 배포 환경 (실제 서비스 운영)
- 세션/쿠키 암호화가 필요할 때 (로그인 유지 등)
- JWT 토큰 서명할 때

이러면 DRF는 JWT 토큰, 세션/쿠키 암호화가 필요하니 시크릿 키를 작성해야 하는 것 같다.
- 나중에 CD 추가할 때 수정할 필요 없고
- 더미키가 실수로 운영에 올라가는 사고 방지
- 보안 습관 자체를 가질 수 있다.
