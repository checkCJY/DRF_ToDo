
/* =========================================================
   DOM이 완전히 로드되면 실행
========================================================= */
document.addEventListener("DOMContentLoaded", () => {

    /* -------------------------------------------------------
      1) 기본 설정 값
    -------------------------------------------------------- */
    const LOGIN_PAGE_URL = "/login/";
    let currentPage = 1;
    let currentPageSize = 3;

    /* -------------------------------------------------------
      2) window.api 존재 확인
    -------------------------------------------------------- */
    if (!window.api) {
        console.error("window.api가 없습니다. base.html에서 static/js/api.js가 로드됐는지 확인하세요.");
        alert("설정 오류: api.js가 로드되지 않았습니다.");
        return;
    }

    /* -------------------------------------------------------
      3) access_token 체크
    -------------------------------------------------------- */
    const access = localStorage.getItem(ACCESS_KEY);
    if (!access) {
        console.log("access_token 없음 → 로그인 이동");
        window.location.href = LOGIN_PAGE_URL;
        return;
    }

    /* -------------------------------------------------------
      4) 인증 실패(401/403) 공통 처리 함수
    -------------------------------------------------------- */
    function handleAuthError(err) {
        const status = err.response?.status;
        if (status === 401 || status === 403) {
            console.log("인증 실패(401/403) → 토큰 삭제 후 로그인 이동");
            localStorage.removeItem("ACCESS_KEY");
            localStorage.removeItem("REFRESH_KEY");
            window.location.href = LOGIN_PAGE_URL;
        }
        return Promise.reject(err);
    }

    /* -------------------------------------------------------
      5) interaction API 엔드포인트 문자열 생성기
    -------------------------------------------------------- */
    const InteractionAPI = {
        like: (todoId) => `/interaction/like/${todoId}/`,
        bookmark: (todoId) => `/interaction/bookmark/${todoId}/`,
        comment: (todoId) => `/interaction/comment/${todoId}/`,
        commentList: (todoId) => `/interaction/comment/${todoId}/list/`, // Part 12 추가
    };

    /* =========================================================
      6) Todo 카드 하나를 생성해서 반환하는 함수
      - div 생성 + innerHTML 세팅 + 클릭 이벤트 등록
      - renderTodos()에서 호출됨
    ========================================================= */
    function createTodoCard(todo) {
        const div = document.createElement("div");
        div.className = "todo-item";
        div.dataset.id = todo.id;

        // 이미지 URL 처리
        const imageSrc = todo.image
            ? (todo.image.startsWith("http") ? todo.image : `${location.origin}${todo.image}`)
            : "";

        // 서버가 null/undefined를 주는 경우 기본값 처리
        const likeCount = Number(todo.like_count ?? 0);
        const bookmarkCount = Number(todo.bookmark_count ?? 0);
        const commentCount = Number(todo.comment_count ?? 0);
        const isLiked = Boolean(todo.is_liked ?? false);
        const isBookmarked = Boolean(todo.is_bookmarked ?? false);

        div.innerHTML = `
            <p><strong>제목:</strong> ${todo.name ?? ""}</p>
            <p><strong>설명:</strong> ${todo.description ?? ""}</p>
            <p><strong>완료 여부:</strong> ${todo.complete ? "완료" : "미완료"}</p>
            <p><strong>exp:</strong> ${todo.exp ?? 0}</p>
            <p><strong>작성자:</strong> ${todo.username ?? ""}</p>
            ${imageSrc ? `<img src="${imageSrc}" style="max-width:200px;">` : ""}

            <!-- 액션 버튼 영역 -->
            <div class="todo-actions" style="display:flex; gap:10px; align-items:center; margin-top:10px;">
                <button class="btn-like" type="button"
                    data-id="${todo.id}"
                    aria-pressed="${isLiked}"
                    style="display:flex; gap:6px; align-items:center; border-radius:999px; padding:6px 10px;">
                    <span class="icon">${isLiked ? "❤️" : "🤍"}</span>
                    <span class="count">${likeCount}</span>
                </button>

                <button class="btn-bookmark" type="button"
                    data-id="${todo.id}"
                    aria-pressed="${isBookmarked}"
                    style="display:flex; gap:6px; align-items:center; border-radius:999px; padding:6px 10px;">
                    <span class="icon">${isBookmarked ? "🔖" : "📑"}</span>
                    <span class="count">${bookmarkCount}</span>
                </button>

                <button class="btn-comment" type="button"
                    data-id="${todo.id}"
                    style="display:flex; gap:6px; align-items:center; border-radius:999px; padding:6px 10px;">
                    <span class="icon">💬</span>
                    <span class="count">${commentCount}</span>
                </button>
            </div>

            <!-- 댓글 입력 영역(토글로 보이게 함) -->
            <div class="comment-box" style="display:none; margin-top:10px;">
                <textarea class="comment-text" rows="3" style="width:100%;"></textarea>
                <button class="comment-submit" data-id="${todo.id}">등록</button>
            </div>

            <!-- 댓글이 화면에 쌓일 영역 -->
            <div class="comment-list" style="margin-top:8px;"></div>

            <hr>
        `;

        // 카드 클릭 → 상세 이동 (액션 버튼/댓글 영역 제외)
        div.addEventListener("click", (e) => {
            if (e.target.closest(".todo-actions") || e.target.closest(".comment-box")) return;
            window.location.href = `/todo/detail/${todo.id}/`;
        });

        return div;
    }

    /* =========================================================
      7) Todo 목록을 화면에 그리는 함수
      - createTodoCard()로 카드를 만들어서 컨테이너에 추가
    ========================================================= */
    function renderTodos(todos) {
        const container = document.querySelector(".todocontainer");
        container.innerHTML = "";

        if (!todos || todos.length === 0) {
            container.innerHTML = "<p>등록된 Todo 없음</p>";
            return;
        }

        todos.forEach(todo => {
            const div = createTodoCard(todo);
            container.appendChild(div);
            loadComments(todo.id, div);
        });
    }

    async function loadComments(todoId, card) {

        // Todo 카드 내부에 있는 댓글 표시 영역(.comment-list)을 찾음
        const listEl = card.querySelector(".comment-list");

        // 만약 댓글 표시 영역이 없다면 함수 종료
        // (DOM 구조가 바뀌거나 오류가 있을 때 방어 코드)
        if (!listEl) return;

        // 서버에 댓글 목록 요청
        // 예: /interaction/comment/{todoId}/list/
        const res = await window.api.get(InteractionAPI.commentList(todoId));

        // 서버 응답에서 댓글 데이터 가져오기
        const comments = res.data || [];

        // 기존 댓글 목록 초기화
        listEl.innerHTML = "";

        // 댓글 배열을 순회하면서 화면에 댓글 생성
        comments.forEach(c => {

            // 댓글 DOM 요소 생성
            const item = document.createElement("div");
            item.className = "comment-item";
            item.style.padding = "6px 0";

            // 댓글 내용 표시
            // username → 작성자
            // content → 댓글 내용
            item.innerHTML = `<div style="font-size:14px;">
            <strong>${c.username ?? ""}</strong> : ${c.content ?? ""}
            </div>`;

            // 댓글을 댓글 목록 영역에 추가
            listEl.appendChild(item);
        });
    }

    /* =========================================================
      8) 특정 페이지를 서버에서 불러오는 함수
    ========================================================= */
    function loadPage(page) {
        window.api.get(`/todo/viewsets/view/?page=${page}&page_size=${currentPageSize}`)
            .then(res => {
                const data = res.data;
                renderTodos(data.data || data.results || []);
                updatePaginationUI(data);
                currentPage = data.current_page || page;
            })
            .catch(err => {
                handleAuthError(err).catch(() => {});
                console.error("페이지 로드 실패", err.response?.data || err.message);
            });
    }

    /* =========================================================
      9) 페이지네이션 UI 업데이트
    ========================================================= */
    function updatePaginationUI(data) {
        const current = data.current_page ?? currentPage ?? 1;
        const total =
            data.page_count ??
            (typeof data.count === "number" && data.results
                ? Math.ceil(data.count / data.results.length)
                : "?");

        document.getElementById("pageInfo").innerText = `${current} / ${total}`;
        document.getElementById("prevBtn").disabled = !(data.previous);
        document.getElementById("nextBtn").disabled = !(data.next);
    }

    /* =========================================================
      10) 이벤트 위임 (document 한 곳에서 버튼 클릭 처리)
    ========================================================= */
    document.addEventListener("click", async (e) => {

        /* 좋아요 버튼 처리 */
        const likeBtn = e.target.closest(".btn-like");
        if (likeBtn) {
            e.stopPropagation();
            e.preventDefault();

            const todoId = likeBtn.dataset.id;
            try {
                const res = await window.api.post(InteractionAPI.like(todoId));
                const { liked, like_count } = res.data;

                likeBtn.setAttribute("aria-pressed", String(liked));
                likeBtn.querySelector(".icon").textContent = liked ? "❤️" : "🤍";
                likeBtn.querySelector(".count").textContent = Number(like_count ?? 0);
            } catch (err) {
                handleAuthError(err).catch(() => {});
                console.error("좋아요 실패:", err.response?.data || err.message);
                alert("좋아요 실패");
            }
            return;
        }

        /* 북마크 버튼 처리 */
        const bookmarkBtn = e.target.closest(".btn-bookmark");
        if (bookmarkBtn) {
            e.stopPropagation();
            e.preventDefault();

            const todoId = bookmarkBtn.dataset.id;
            try {
                const res = await window.api.post(InteractionAPI.bookmark(todoId));
                const { bookmarked, bookmark_count } = res.data;

                bookmarkBtn.setAttribute("aria-pressed", String(bookmarked));
                bookmarkBtn.querySelector(".icon").textContent = bookmarked ? "🔖" : "📑";
                bookmarkBtn.querySelector(".count").textContent = Number(bookmark_count ?? 0);
            } catch (err) {
                handleAuthError(err).catch(() => {});
                console.error("북마크 실패:", err.response?.data || err.message);
                alert("북마크 실패");
            }
            return;
        }

        /* 댓글 버튼 클릭 → 입력창 토글 */
        const commentBtn = e.target.closest(".btn-comment");
        if (commentBtn) {
            e.stopPropagation();
            e.preventDefault();

            const card = commentBtn.closest(".todo-item");
            const box = card.querySelector(".comment-box");
            box.style.display = (box.style.display === "none" || !box.style.display) ? "block" : "none";
            return;
        }

        /* 댓글 등록 처리 */
        const submitBtn = e.target.closest(".comment-submit");
        if (submitBtn) {
            e.stopPropagation();
            e.preventDefault();

            const todoId = submitBtn.dataset.id;
            const card = submitBtn.closest(".todo-item");
            const textarea = card.querySelector(".comment-text");
            const content = textarea.value.trim();

            if (!content) return;

            try {
                const res = await window.api.post(InteractionAPI.comment(todoId), { content });
                const saved = res.data;

                // 화면에 댓글 DOM 추가
                const listEl = card.querySelector(".comment-list");
                const item = document.createElement("div");
                item.className = "comment-item";
                item.style.padding = "6px 0";
                item.innerHTML = `
                    <div style="font-size:14px;">
                        <strong>${saved.username ?? "me"}</strong> : ${saved.content}
                    </div>
                `;
                listEl.prepend(item);

                // 댓글 수 +1
                const countEl = card.querySelector(".btn-comment .count");
                countEl.textContent = Number(countEl.textContent || 0) + 1;

                // 입력창 초기화 + 유지
                textarea.value = "";
                card.querySelector(".comment-box").style.display = "block";
            } catch (err) {
                handleAuthError(err).catch(() => {});
                console.error("댓글 등록 실패", err.response?.data || err.message);
                alert("댓글 등록 실패");
            }
            return;
        }
    });

    /* =========================================================
      11) 페이지네이션 버튼 이벤트
    ========================================================= */
    document.getElementById("prevBtn").addEventListener("click", () => {
        if (currentPage > 1) loadPage(currentPage - 1);
    });

    document.getElementById("nextBtn").addEventListener("click", () => {
        loadPage(currentPage + 1);
    });

    /* =========================================================
      12) 페이지 크기 변경 → 1페이지부터 다시 로드
    ========================================================= */
    document.getElementById("pageSizeBtn").addEventListener("click", () => {
        const val = parseInt(document.getElementById("pageSizeInput").value);
        if (val >= 1 && val <= 20) {
            currentPageSize = val;
            loadPage(1);
        } else {
            alert("1에서 20 사이의 숫자를 입력해주세요.");
        }
    });

    /* =========================================================
      13) Todo 생성 페이지 이동
    ========================================================= */
    document.getElementById("createBtn").addEventListener("click", () => {
        window.location.href = "/todo/create/";
    });

    /* =========================================================
      14) 최초 1페이지 로드
    ========================================================= */
    loadPage(1);

    document.getElementById("movieReviewsBtn").addEventListener("click", () => {
        window.location.href = "/reviews/page/";
    });
});
