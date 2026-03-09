document.addEventListener("DOMContentLoaded", () => {
  // django 코드는 .js에서 작동하지 않는다. data-* 형식으로 변경
  // const todoId = "{{ todo.id }}";
  const todoId = document.getElementById("page-data").dataset.todoId;
  const LOGIN_PAGE_URL = "/login/";
  const LIST_PAGE_URL  = "/todo/list/";

  if (!window.api) {
    console.error("window.api가 없습니다. base.html에서 static/js/api.js가 로드됐는지 확인하세요.");
    alert("설정 오류: api.js가 로드되지 않았습니다.");
    return;
  }

  // access 토큰 없으면 로그인으로
  const access = localStorage.getItem(ACCESS_KEY);
  if (!access) {
    console.log("ACCESS_KEY 없음 → 로그인 이동");
    window.location.href = LOGIN_PAGE_URL;
    return;
  }

  // 401/403 처리 함수 (세션 기반의 res.status 체크 대체)
  function handleAuthError(err) {
    const status = err.response?.status;
    if (status === 401 || status === 403) {
      alert("로그인이 필요합니다.");

      // ✅ [추가됨] (선택) 토큰 정리
      localStorage.removeItem(ACCESS_KEY);
      localStorage.removeItem(REFRESH_KEY);

      window.location.href = LOGIN_PAGE_URL;
    }
    return Promise.reject(err);
  }


  // 수정 버튼 클릭 이벤트
  document.querySelector(".todoUpdate").addEventListener("click", () => {
    window.location.href = `/todo/update/${todoId}/`;
  });



  // 삭제 버튼 클릭 이벤트 (fetch → axios로만 변경)
  // - 동작은 동일: confirm → DELETE 요청 → 401/403 로그인 이동 → 성공 시 리스트 이동
  document.querySelector(".todoDelete").addEventListener("click", async () => {
    const ok = confirm("정말 삭제하시겠습니까?");
    if (!ok) return;

    try {
      // 변경: fetch → axios(window.api)
      await window.api.delete(`/todo/viewsets/view/${todoId}/`);
      window.location.href = LIST_PAGE_URL;

    } catch (err) {

      // 인증 문제면 로그인으로
      handleAuthError(err).catch(() => {});
      console.error("삭제 실패:", err.response?.data || err.message);
      // 로그 상세화

      alert("삭제 중 오류가 발생했습니다.");
      }
    });


  // 홈으로 버튼 클릭 이벤트
  document.querySelector(".todoHome").addEventListener("click", () => {
    window.location.href = LIST_PAGE_URL;
  });

});
