/**
 * Axios 인스턴스
 * - baseURL: Django 서버와 같은 origin으로 API 요청
 */
const api = axios.create({
  baseURL: "/",
  withCredentials: true,  // 추가해도 기존 코드 영향 없다고함.
});

/**
 * 요청 인터셉터 - CSRF 토큰 자동 주입
 * Django는 POST/PUT/DELETE 요청 시 X-CSRFToken 헤더를 요구하므로,
 * 모든 요청 전에 쿠키에서 csrftoken 값을 꺼내 헤더에 추가한다.
 */
api.interceptors.request.use(config => {
  const csrfToken = document.cookie
    .split("; ")
    .find(row => row.startsWith("csrftoken="))
    ?.split("=")[1];

    // headers 객체가 없으면 생성
    config.headers = config.headers || {};

  if (csrfToken) {
    config.headers["X-CSRFToken"] = csrfToken;
  }
  return config;
});
