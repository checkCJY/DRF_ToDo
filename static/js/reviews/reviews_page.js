/**
 * 리뷰 목록 + 감정분석 UI 스크립트
 *
 * DRF API(리뷰 목록 / 상세 / 감정분석)를 호출해 화면에 표시합니다.
 * base.html에서 window.api (axios 인스턴스)가 사전에 로드되어 있어야 합니다.
 */
document.addEventListener("DOMContentLoaded", () => {

  // --- 사전 체크 ---
  // window.api는 api.js에서 생성한 axios 인스턴스 (baseURL, 인증 헤더 등 포함)
  if (!window.api) {
    alert("설정 오류: api.js가 로드되지 않았습니다.");
    return;
  }

  // --- 페이지 이동 ---
  document.getElementById("backToTodo").onclick = () => location.href = "/todo/list/";

  // --- 상태 변수 ---
  let currentPage = 1;
  let selected = { id: null, title: "", review: "" }; // 현재 선택된 리뷰

  // --- API 엔드포인트 ---
  const LIST_URL        = (page) => `/api/reviews/collected-reviews/?page=${page}`;
  const SENTIMENT_BY_ID = (id)   => `/api/reviews/collected-reviews/${id}/sentiment/`;
  const SENTIMENT_TEXT  = `/api/reviews/collected-reviews/sentiment/`;

  // --- DOM 캐싱 ---
  const $list            = document.getElementById("reviewsList");
  const $pageInfo        = document.getElementById("pageInfo");
  const $prev            = document.getElementById("prevBtn");
  const $next            = document.getElementById("nextBtn");
  const $selectedId      = document.getElementById("selectedId");
  const $selectedTitle   = document.getElementById("selectedTitle");
  const $inputText       = document.getElementById("inputText");
  const $analyzeSelected = document.getElementById("analyzeSelected");
  const $result          = document.getElementById("resultArea");

  // ----------------------------------------------------------------

  /**
   * 감정분석 결과를 $result 영역에 배지 형태로 렌더링합니다.
   *
   * - id 기반 분석 응답: { sentiment: { label, score, ... } }
   * - 텍스트 직접 분석 응답: { label, score, ... }
   * 두 형태 모두 대응하기 위해 payload.sentiment를 우선 사용합니다.
   */
  function renderResult(payload) {
    const s = payload?.sentiment ?? payload;

    if (!s) {
      $result.textContent = "결과 없음";
      return;
    }

    const label = s.label || s.label_raw || "unknown";
    const score = (typeof s.score === "number") ? s.score.toFixed(4) : "-";

    // NSMC 관례: LABEL_1 = 긍정, LABEL_0 = 부정
    const isPos = (s.label === "positive" || s.label_raw === "LABEL_1");
    const badgeClass = isPos ? "pos" : "neg";
    const badgeText  = isPos ? "긍정" : "부정";

    $result.innerHTML = `
      <div class="badge ${badgeClass}">
        <strong>${badgeText}</strong>
        <span class="muted">score: ${score}</span>
      </div>
      <div style="margin-top:10px;" class="muted">
        <div>model: <code>${s.model ?? "-"}</code></div>
        <div>label_raw: <code>${s.label_raw ?? "-"}</code></div>
      </div>
    `;
  }

  /**
   * 리뷰 클릭 시 호출됩니다.
   * 선택 상태를 갱신하고, 우측 패널에 내용을 채운 뒤 분석 버튼을 활성화합니다.
   */
  function selectReview(itemEl, data) {
    // 기존 active 제거 후 클릭된 항목에만 active 추가
    [...document.querySelectorAll(".review-item")].forEach(el => el.classList.remove("active"));
    itemEl.classList.add("active");

    selected = { id: data.id, title: data.title, review: data.review };

    $selectedId.textContent    = String(selected.id);
    $selectedTitle.textContent = selected.title || "(제목 없음)";
    $inputText.value           = selected.review || "";
    $analyzeSelected.disabled  = false;
    $result.textContent        = "선택 리뷰를 분석할 준비가 됐어요.";
  }

  /**
   * 리뷰 배열을 받아 목록 영역($list)에 카드 형태로 렌더링합니다.
   * 본문은 최대 120자로 잘라 스니펫으로 표시합니다.
   */
  function renderList(items) {
    $list.innerHTML = "";

    if (!items || items.length === 0) {
      $list.innerHTML = "<p class='muted'>리뷰가 없습니다.</p>";
      return;
    }

    items.forEach(r => {
      const el = document.createElement("div");
      el.className = "review-item";

      const snippet = (r.review || "").slice(0, 120);
      el.innerHTML = `
        <div style="display:flex; justify-content:space-between; gap:10px;">
          <strong>${r.title ?? "(제목 없음)"}</strong>
          <span class="muted"> 글번호 ${r.id}</span>
        </div>
        <div class="review-snippet">
          ${snippet}${(r.review || "").length > 120 ? "..." : ""}
        </div>
      `;

      el.addEventListener("click", () => selectReview(el, r));
      $list.appendChild(el);
    });
  }

  /**
   * 페이지네이션 UI를 갱신합니다.
   * 서버 응답에서 current_page / page_count / previous / next 를 사용합니다.
   */
  function updatePagination(data) {
    const current = data.current_page ?? currentPage ?? 1;
    const total   = data.page_count ?? "?";

    $pageInfo.textContent = `${current} / ${total}`;

    // previous / next 가 null이면 버튼 비활성화
    $prev.disabled = !data.previous;
    $next.disabled = !data.next;
  }

  /**
   * 지정한 페이지의 리뷰 목록을 서버에서 가져와 렌더링합니다.
   * 서버 응답은 { data: [...] } 또는 { results: [...] } 두 형태를 허용합니다.
   */
  async function loadPage(page) {
    try {
      const res  = await window.api.get(LIST_URL(page));
      const data = res.data;

      renderList(data.data || data.results || []);
      updatePagination(data);
      currentPage = data.current_page || page;

    } catch (err) {
      console.error("리뷰 목록 로드 실패", err.response?.data || err.message);
      alert("리뷰 목록 로드 실패");
    }
  }

  // ----------------------------------------------------------------

  // --- 페이지 이동 버튼 ---
  $prev.onclick = () => { if (currentPage > 1) loadPage(currentPage - 1); };
  $next.onclick = () => loadPage(currentPage + 1); // disabled 처리는 updatePagination에서 담당

  // --- 선택 리뷰 감정 분석 ---
  document.getElementById("analyzeSelected").onclick = async () => {
    if (!selected.id) return;
    try {
      $result.textContent = "분석 중...";
      const res = await window.api.get(SENTIMENT_BY_ID(selected.id));
      renderResult(res.data);
    } catch (err) {
      console.error("선택 리뷰 분석 실패", err.response?.data || err.message);
      alert("선택 리뷰 분석 실패");
    }
  };

  // --- 텍스트 직접 감정 분석 ---
  document.getElementById("analyzeText").onclick = async () => {
    const text = $inputText.value.trim();
    if (!text) return alert("텍스트를 입력하세요.");
    try {
      $result.textContent = "분석 중...";
      const res = await window.api.post(SENTIMENT_TEXT, { text });
      renderResult(res.data);
    } catch (err) {
      console.error("텍스트 분석 실패", err.response?.data || err.message);
      alert("텍스트 분석 실패");
    }
  };

  // --- 초기화: 선택 상태 / 입력 / 결과 UI 리셋 ---
  document.getElementById("clearBtn").onclick = () => {
    selected = { id: null, title: "", review: "" };

    $selectedId.textContent    = "없음";
    $selectedTitle.textContent = "리뷰를 선택하세요";
    $inputText.value           = "";
    $analyzeSelected.disabled  = true;
    $result.textContent        = "결과가 여기에 표시됩니다.";

    [...document.querySelectorAll(".review-item")].forEach(el => el.classList.remove("active"));
  };

  // --- 초기 로드 ---
  loadPage(1);
});
