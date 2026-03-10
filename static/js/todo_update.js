document.addEventListener("DOMContentLoaded", () => {

  const todoId = document.getElementById("page-data").dataset.todoId;
  const LOGIN_PAGE_URL = "/login/";

  if (!window.api) {
    console.error("window.api가 없습니다. base.html에서 static/js/api.js가 로드됐는지 확인하세요.");
    alert("설정 오류: api.js가 로드되지 않았습니다.");
    return;
  }

  const access = localStorage.getItem(ACCESS_KEY);
  if (!access) {
    console.log("access_token 없음 → 로그인 이동");
    window.location.href = LOGIN_PAGE_URL;
    return;
  }

  // 401/403 처리 로직을 함수로 분리 (기존 interceptor 대체)
  function handleAuthError(err) {
    const status = err.response?.status;
    if (status === 401 ) {
      alert("로그인이 필요합니다.");

      // ✅ [추가됨] (선택) 토큰 정리
      localStorage.removeItem(ACCESS_KEY);
      localStorage.removeItem(REFRESH_KEY);

      window.location.href = LOGIN_PAGE_URL;
    }
    else if (status === 403){
      alert("권한이 없습니다.")
    }
    return Promise.reject(err);
  }

  document.getElementById("todoUpdate").addEventListener("click", async () => {
    try {
      const formData = new FormData();
      formData.append("name", document.getElementById("name").value);
      formData.append("description", document.getElementById("description").value);
      formData.append("complete", document.getElementById("complete").checked ? "true" : "false");
      formData.append("exp", document.getElementById("exp").value || 0);

      const fileInput = document.getElementById("image");
      if (fileInput.files.length > 0) {
        formData.append("image", fileInput.files[0]);
      }

      const res = await window.api.patch(`/todo/viewsets/view/${todoId}/`, formData);
      console.log("수정 성공:", res.data);
      window.location.href = `/todo/detail/${todoId}/`;

    } catch (err) {
      // 인증 문제면 로그인으로 보내기
      handleAuthError(err).catch(() => {});
      console.error("수정 실패:", err.response?.data || err.message);
      alert("수정 실패: 콘솔/네트워크 확인");
    }
  });

});
