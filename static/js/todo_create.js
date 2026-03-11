document.addEventListener("DOMContentLoaded", () => {
  // 로그인 페이지 주소, Todo 생성 API 주소
  const LOGIN_PAGE_URL = "/login/";
  const CREATE_API_URL = "/todo/viewsets/view/";

  if (!window.api) { // window.api 로드 여부 확인
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


  // [추가됨] 401/403 처리 로직을 함수로 분리 (기존 interceptor 대체)
  function handleAuthError(err) {
    const status = err.response?.status;
    if (status === 401 ) {
      console.log("인증 실패(401/403) → 토큰 삭제 후 로그인 이동");
      // 오타 수정
      localStorage.removeItem(ACCESS_KEY);
      localStorage.removeItem(REFRESH_KEY);
      window.location.href = LOGIN_PAGE_URL;
    }
    else if (status === 403){
      alert("권한이 없습니다.")
    }
    return Promise.reject(err);
  }

  const homeBtn = document.querySelector(".todoHome");

  homeBtn.addEventListener("click", () => {
      window.location.href = "/todo/list/";
    });


  /* Todo 생성 버튼 클릭 이벤트 */
  document.getElementById("todoCreate").addEventListener("click", async () => {
    try {
      // 파일 업로드를 포함한 데이터를 서버로 전송할 때 사용
      const formData = new FormData();

      // 입력된 Todo 데이터를 FormData에 추가
      formData.append("name", document.getElementById("name").value);
      formData.append("description", document.getElementById("description").value);
      formData.append("complete", document.getElementById("complete").checked);
      formData.append("exp", Number(document.getElementById("exp").value || 0));

      // 이미지 파일 input 요소 가져오기
      const fileInput = document.getElementById("image");

      // 파일이 선택되어 있으면 FormData에 이미지 추가
      if (fileInput.files.length > 0) {
        formData.append("image", fileInput.files[0]);
      }

      // Todo 생성 API 호출
      // JSON 대신 FormData 형태로 서버에 전송
      const res = await window.api.post("todo/viewsets/view/", formData);
      console.log(res.data);
      window.location.href = "/todo/list/";

    } catch (err) {
        // 인증 문제면 로그인으로 보내기
        handleAuthError(err).catch(() => {});

        console.error("생성 실패:", err.response?.data || err.message);
        alert("생성 실패: 콘솔/네트워크 확인");
    }
  });
})
