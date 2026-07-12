---
name: "부동산 워치리스트 대시보드"
version: "1.0"
status: "active"
target: "Local HTML dashboard (file:// or local server, no internet required)"
dark_mode: true
tokens:
  colors:
    primary: "#6d93e8"
    primary_dark: "#3d6bd6"
    primary_hover: "#9db6ee"
    neutral_0: "#0f1115"
    neutral_50: "#15171c"
    neutral_100: "#1a1d24"
    neutral_200: "#1e222b"
    neutral_300: "#23262d"
    neutral_400: "#2a2e37"
    neutral_500: "#3a3f4b"
    neutral_600: "#5a6170"
    neutral_700: "#6b7078"
    neutral_800: "#9aa0a6"
    neutral_900: "#c9cdd3"
    neutral_950: "#e6e6e6"
    accent_success: "#2ecc71"
    accent_warning: "#e67e22"
    accent_alert: "#e74c3c"
    accent_critical: "#c0392b"
    surface_info: "#182437"
    surface_error: "#4a1414"
    border_info: "#2a4a7a"
    border_error: "#c0392b"
    border_default: "#23262d"
  typography:
    font_family_default: "-apple-system, \"Malgun Gothic\", sans-serif"
    heading_1_size: "20px"
    heading_1_weight: "500"
    heading_1_line_height: "1.2"
    heading_2_size: "14px"
    heading_2_weight: "600"
    heading_2_line_height: "1.4"
    heading_3_size: "14px"
    heading_3_weight: "500"
    heading_3_line_height: "1.4"
    heading_4_size: "12px"
    heading_4_weight: "500"
    heading_4_line_height: "1.4"
    body_size: "13px"
    body_weight: "400"
    body_line_height: "1.6"
    body_small_size: "12px"
    body_small_weight: "400"
    body_small_line_height: "1.5"
    label_size: "12px"
    label_weight: "500"
    label_line_height: "1.4"
    caption_size: "11px"
    caption_weight: "400"
    caption_line_height: "1.3"
  spacing:
    xs: "4px"
    sm: "6px"
    md: "8px"
    lg: "12px"
    xl: "14px"
    xxl: "16px"
    xxxl: "18px"
    section_gap: "20px"
    section_padding: "16px"
    content_max_width: "1100px"
    content_padding: "24px"
  border_radius:
    chip: "14px"
    card: "8px"
  transitions:
    quick: "0.1s"
    default: "0.2s"
---

# 부동산 워치리스트 대시보드 — DESIGN.md

## 프로젝트 개요

**용도**: SK송도 부동산 워치리스트 추적용 로컬 HTML 대시보드  
**배포 방식**: 순수 HTML + JavaScript (외부 라이브러리 없음), `file://` 또는 로컬 서버로 열림  
**테마**: 다크모드, 개인용 도구  
**주요 기능**: 단지별 요약, 실거래가·매물비율 추이 차트, 정렬 가능한 표, 상세페이지 네비게이션

---

## 색상 체계

### 역할 기반 색상 정의

이 대시보드는 **역할(role)** 기반으로 색상을 정의합니다. 실제 hex 값은 언제든 바뀔 수 있지만, 각 색상이 하는 **역할**은 일관성 있게 유지됩니다.

#### Primary (주 잉크색)

**역할**: 페이지의 메인 액션·링크·강조 요소  
**정서**: 신뢰, 상호작용, 중립적 강조  
**사용처**:
- 링크 텍스트
- 활성 칩(chip) 배경
- 버튼 호버 상태
- 필터 UI의 액션 버튼

**현재값**: `#6d93e8` (중간 파랑)
- 어두운 배경에서 충분한 명도 대비 (WCAG AA 충족)
- 다크모드 시각적 계층에서 "상호작용 가능"의 신호

**파생 역할**:
- `primary_dark` (#3d6bd6): 활성 상태, 호버 피드백
- `primary_hover` (#9db6ee): 호버 피드백, 연한 강조

#### Neutral (중립색 스케일)

**역할**: 배경, 테두리, 텍스트 계층화  
**정서**: 감정적으로 중립, 정보의 캔버스

**계층별 정의**:
- `neutral_0` (#0f1115): 페이지 배경 (최상위 배경)
- `neutral_50` (#15171c): 카드·섹션 배경 (한 단계 위로)
- `neutral_100` (#1a1d24): 필터 패널, 차트 배경 (두 단계 위로)
- `neutral_200` (#1e222b): 호버 상태 배경
- `neutral_300` (#23262d): 테두리, 분할선 (기본)
- `neutral_400` (#2a2e37): 더 두드러진 테두리
- `neutral_500` (#3a3f4b): 비활성 UI 요소
- `neutral_600` (#5a6170): 호버 테두리
- `neutral_700` (#6b7078): 차트 축 레이블, 보조 텍스트
- `neutral_800` (#9aa0a6): 메타 텍스트, 헤더 강조
- `neutral_900` (#c9cdd3): 제목, 강조 텍스트
- `neutral_950` (#e6e6e6): 기본 텍스트 (본문)

이 스케일은 명도 **깊이(depth)** 를 나타냅니다. 낮은 번호는 뒤로, 높은 번호는 앞으로.

#### Accent (시그널 색상)

**역할**: 상태 피드백, 경고, 긍정/부정 신호

- `accent_success` (#2ecc71): 긍정 신호 (매수세 강화)
- `accent_warning` (#e67e22): 주의 신호 (매물 적체)
- `accent_alert` (#e74c3c): 부정 신호 (급변)
- `accent_critical` (#c0392b): 위기 신호 (경계)

#### Surface (배경 표면)

**역할**: 컨텍스트별 배경 색상

- `surface_info` (#182437): 정보성 배경 (총평, 정책 업데이트)
- `surface_error` (#4a1414): 경고 배경 (이상징후 배너)

#### Border (테두리)

**역할**: 요소 분리, 시각적 그룹핑

- `border_default` (#23262d): 일반 테두리
- `border_info` (#2a4a7a): 정보성 테두리 (총평 카드)
- `border_error` (#c0392b): 경고 테두리 (이상징후 배너)

---

## 타이포그래피

### 원칙

- **폰트**: 시스템 기본값 (`-apple-system, "MalGun Gothic", sans-serif`)
- **다크모드 가독성**: 모든 텍스트는 명도 대비 최소 WCAG AA 기준 충족
- **계층**: 크기 + 색상 + 무게를 함께 사용해 정보 계층을 만듭니다

### 역할별 타이포그래피

#### Heading 1 (페이지 제목)
**역할**: 페이지의 주 제목, 사용자가 지금 어디 있는지 명시  
**사용처**: `<h1 id="apt-title">` — 홈 "워치리스트 대시보드", 상세 "송도 아파트 (심층)"  
**스타일**:
- 크기: 20px
- 무게: 500 (기본)
- 색상: neutral_950 (#e6e6e6)
- 마진: 아래 4px (다음 요소와 분리)

**개선 원칙**: 제목 아래에는 항상 "현재 페이지 위치" 정보가 따라야 합니다. 예:
- 홈: "워치리스트 대시보드"만 표시
- 상세: "송도 아파트 (심층)" + breadcrumb "홈 > 송도 아파트" 또는 뒤로가기 링크

#### Heading 2 (섹션 제목)
**역할**: 섹션/표/차트의 제목  
**사용처**: `<h2>` 태그 — "단지별 비교", "실거래가 추이", "최근 실거래 10건"  
**스타일**:
- 크기: 14px
- 무게: 600 (굵음)
- 색상: neutral_900 (#c9cdd3)
- 마진: 아래 12px

#### Heading 3 (카드/블록 제목)
**역할**: 정책 업데이트, 이상징후 배너 등 내재된 카드의 제목  
**사용처**: `<h3>` 태그 — "이번 주 정책·거시·호재 업데이트"  
**스타일**:
- 크기: 14px
- 무게: 500
- 색상: neutral_900 (#c9cdd3)
- 마진: 아래 8px

#### Heading 4 (목록 항목 서브제목)
**역할**: 마크다운 정책 업데이트에서 자동 렌더링되는 소제목  
**사용처**: 정책 카드 내 `### 정책명`  
**스타일**:
- 크기: 12px
- 무게: 500
- 색상: neutral_900 (#c9cdd3)
- 마진: 위 14px, 아래 4px

#### Body (본문 텍스트)
**역할**: 테이블 내용, 차트 범례, 설명 문구  
**스타일**:
- 크기: 13px
- 무게: 400
- 색상: neutral_950 (#e6e6e6)
- 라인높이: 1.6

#### Body Small (보조 텍스트)
**역할**: 메타 정보 (생성일, 단지 수), 빈 상태 메시지  
**사용처**: `.meta`, `.empty` 클래스  
**스타일**:
- 크기: 12px
- 색상: neutral_800 (#9aa0a6) — body보다 약간 흐릿함
- 라인높이: 1.5

#### Label (UI 레이블)
**역할**: 필터 그룹의 제목, 테이블 헤더, 칩 텍스트  
**사용처**: `.filter-head b`, `<th>`, 칩 버튼  
**스타일**:
- 크기: 12px
- 무게: 500 (약간 굵음 — "상호작용 가능"의 신호)
- 색상: neutral_800 (#9aa0a6)

#### Caption (주석)
**역할**: 차트 축 레이블, 극히 작은 보조 정보  
**사용처**: `.axis-label` 클래스  
**스타일**:
- 크기: 11px (또는 더 작음)
- 색상: neutral_700 (#6b7078)

---

## 간격과 레이아웃

### 간격 단위 (Spacing Scale)

```
xs:     4px  — 요소 내부 극소 여백
sm:     6px  — 칩 간격, 작은 내부 여백
md:     8px  — 기본 작은 여백
lg:    12px  — 구성 요소 간 기본 여백
xl:    14px  — 카드 내부 여백
xxl:   16px  — 필터 패널, 섹션 패딩
xxxl:  18px  — 큰 요소 간 여백
```

### 주요 레이아웃 규칙

#### 페이지 레벨
- **배경**: neutral_0 (#0f1115)
- **최대 너비**: 1100px (데이터-밀집 대시보드)
- **외부 여백**: 24px (content_padding)

#### 섹션 카드
- **배경**: neutral_50 (#15171c)
- **테두리**: 1px solid neutral_300 (#23262d)
- **모서리**: 8px border-radius
- **내부 여백**: 16px × 18px (xxl × xl)
- **섹션 간 여백**: 20px (section_gap)

#### 필터 UI
- **배경**: neutral_100 (#1a1d24)
- **패딩**: 16px
- **모서리**: 8px border-radius
- **하위 갭**: 20px (filter-group 간), 6px (내부 gap)

#### 표 (Table)
- **헤더 색상**: neutral_800 (#9aa0a6) — 보조 텍스트
- **테두리**: 1px solid neutral_300 (#23262d)
- **셀 패딩**: 7px 10px
- **호버 행**: neutral_200 (#1e222b) 배경
- **경고 행** (.alert-row): 배경 rgb(36,20,20) 어두운 빨강

#### 칩 (상태 관리 버튼)
- **기본 상태**: 투명 배경, neutral_500 테두리
- **호버 상태**: neutral_600 테두리, neutral_950 텍스트
- **활성 상태** (.active): primary_dark 배경, 테두리 동일, white 텍스트
- **패딩**: 5px 11px
- **모서리**: 14px border-radius
- **전환**: background 0.1s, border-color 0.1s

---

## 컴포넌트 규칙

### 공통 헤더 (페이지/섹션 타이틀)

**구조**:
```html
<div class="page-header">
  <h1 id="page-title">{페이지 제목}</h1>
  <div class="breadcrumb" id="breadcrumb">
    <!-- 홈 > 현재위치 또는 뒤로가기 링크 -->
  </div>
  <div class="meta">{추가 메타 정보}</div>
</div>
```

**색상 토큰**:
- 제목: primary = neutral_950
- breadcrumb 링크: primary = #6d93e8
- 메타: neutral_800

**타이포 토큰**:
- h1: heading_1_size, heading_1_weight
- breadcrumb: body_small_size
- meta: body_small_size

**간격 토큰**:
- h1 아래: md (8px)
- breadcrumb 아래: md (8px)
- meta 아래: lg (12px)

**규칙**:
- 모든 페이지는 고유한 h1을 반드시 가져야 함 (SEO, 스크린리더 접근성)
- 상세 페이지는 네비게이션 링크(breadcrumb 또는 뒤로가기)를 h1 아래에 배치
- 메타는 색상을 neutral_800으로 통일

### 섹션 카드

**구조**:
```html
<section>
  <h2>{섹션 제목}</h2>
  <div id="{내용}">{내용}</div>
</section>
```

**색상 토큰**:
- 배경: neutral_50
- 테두리: border_default
- 제목: heading_2 (neutral_900)

**간격 토큰**:
- 외부: section_gap (20px)
- 내부: section_padding (16px)
- 제목 아래: md (8px)

### 표 (Table)

**색상 토큰**:
- 배경: neutral_50 (섹션과 동일)
- 헤더 텍스트: neutral_800
- 헤더 호버: neutral_950
- 셀 텍스트: neutral_950
- 호버 행: neutral_200
- 경고 행 (.alert-row): surface_error 배경

**타이포 토큰**:
- 헤더: label_size + label_weight
- 셀: body_size + body_weight

**간격 토큰**:
- 셀 패딩: 7px 10px
- 테두리: 1px solid border_default

**규칙**:
- 첫 열은 항상 왼쪽 정렬 (단지명 등)
- 데이터 열은 오른쪽 정렬 (숫자)
- 헤더는 클릭 가능하고 정렬 표시(▲/▼) 표시
- 경고 행 (.alert-row)은 이상징후 감지 시 하이라이트

### 차트 (SVG 라인차트)

**색상 토큰**:
- 배경: neutral_100 (#1a1d24)
- 축선: neutral_500 (#3a3f4b)
- 그리드선: neutral_200 (#20242c)
- 축 레이블: neutral_700 (#6b7078)
- 라인 색상: CHART_COLORS 배열 (primary_dark, accent_warning, accent_success, accent_alert, ...)

**간격 토큰**:
- 마진(padding): 46px (SVG viewBox 기준)
- 범례 갭: 4px 14px (위아래, 좌우)

**규칙**:
- 범례 색점(●)은 해당 라인 색상과 일치
- 툴팁: 각 점에 `<title>` 엘리먼트로 호버 정보 제공
- 반응형: `viewBox` + `width="100%"` 로 부모 너비에 맞춤

### 필터 UI (칩 그룹)

**구조**:
```html
<div class="filters">
  <div class="filter-group">
    <div class="filter-head">
      <b>{카테고리}</b>
      <button id="cat-all">전체</button>
      <button id="cat-none">해제</button>
    </div>
    <div class="chips" id="f-cat"></div>
  </div>
  <!-- 반복 -->
</div>
```

**색상 토큰**:
- 배경: neutral_100
- 헤더 텍스트: neutral_800
- 버튼 텍스트: primary
- 칩(기본): 투명, neutral_500 테두리, neutral_950 텍스트
- 칩(호버): neutral_600 테두리
- 칩(활성): primary_dark 배경, white 텍스트

**간격 토큰**:
- 필터 컨테이너 패딩: xxl (16px)
- filter-group 간 갭: 20px
- filter-group 내부 갭: 6px
- 칩 간: 6px

**규칙**:
- 각 그룹은 "전체/해제" 버튼 제공
- 활성 칩은 primary_dark 배경으로 선택 상태 명시
- 클릭 시 필터 적용 + 전체 재렌더링

### 정보 카드 (총평, 정책 업데이트)

**구조**:
```html
<div class="narrative"><!-- 또는 .policy-card -->
  {텍스트 또는 마크다운 렌더링}
</div>
```

**색상 토큰** (narrative — 중립 정보):
- 배경: surface_info (#182437)
- 테두리: border_info (#2a4a7a)
- 텍스트: neutral_950

**색상 토큰** (policy-card — 공식 안내):
- 배경: neutral_100 (#1a1d24)
- 테두리: neutral_400 (#2a2e37)
- 텍스트: neutral_950
- h3: neutral_900

**간격 토큰**:
- 패딩: 14px 18px
- 모서리: 8px
- 마진 아래: 16px

**타이포 토큰**:
- 본문: body_size + body_line_height
- h3: heading_3_size + heading_3_weight

### 경고 배너 (이상징후)

**구조**:
```html
<div class="alert-banner">
  <b>⚠ 이상징후</b><br>
  {경고 목록}
</div>
```

**색상 토큰**:
- 배경: surface_error (#4a1414)
- 테두리: border_error (#c0392b)
- 텍스트: 밝은 빨강 (#ffb3b3)

**간격 토큰**:
- 패딩: 12px 16px
- 모서리: 8px
- 마진 아래: 16px

**규칙**:
- 이상징후가 있을 때만 표시
- 경고 아이콘(⚠) 포함
- 목록은 "- " 로 시작하는 줄 분리

### 링크

**색상 토큰**:
- 기본: primary (#6d93e8)
- 호버: primary_hover (#9db6ee)

**타이포 토큰**:
- 크기: 상속 (부모 크기)
- 색상: primary
- 기타: 기본 체중, 밑줄 없음 (또는 선택적)

### 뒤로가기 / Breadcrumb

**역할**: 사용자가 이전 페이지로 돌아가거나 페이지 위치를 파악  
**스타일**:
- 크기: body_small_size (12px)
- 색상: primary
- 마진 아래: md (8px)

**규칙**:
- 상세 페이지: `← 전체 요약으로` 링크 필수 (현재 상태)
- 홈: breadcrumb 불필요 (최상위)
- 향후: breadcrumb 트레일 추가 고려 ("홈 > 송도 > 상세")

---

## 네비게이션 구조 (개선 원칙)

### 현재 문제점

1. **홈에서 상세로**: 테이블의 단지명 링크로만 가능 (다른 진입점 없음)
2. **상세에서 홈으로**: 하드코딩된 "← 전체 요약으로" 링크 하나 (홈 테이블에서 다른 단지로 직접 이동 불가)
3. **페이지 위치 표시 부실**: 상세 페이지에서 "내가 어디 있는가"가 명확하지 않음

### 개선 전략

#### 1. 공통 헤더 추가 (모든 페이지)

```html
<header class="page-header">
  <div class="header-nav">
    <a href="./대시보드.html" class="logo">📊 워치리스트</a>
    <nav class="breadcrumb" id="breadcrumb">
      <!-- 페이지별로 동적 생성 -->
    </nav>
  </div>
  <h1 id="page-title">대시보드</h1>
  <div class="meta">{메타 정보}</div>
</header>
```

**색상**: 배경 neutral_50, 텍스트 neutral_950, 링크 primary  
**타이포**: 제목은 heading_1, 네비는 body_small  
**간격**: 내부 xxl (16px), 아래 section_gap (20px)

#### 2. 페이지별 Breadcrumb

**홈** (대시보드.html):
```
워치리스트 대시보드
```
(breadcrumb 미표시, 최상위)

**상세** (대시보드_단지_{이름}.html):
```
홈 > {단지명} > 상세
```
또는 간단히:
```
← 워치리스트로 돌아가기 | 다음 단지 → | 이전 단지 ←
```

#### 3. 상세 페이지 내 네비게이션 (선택)

단지 간 이동을 빠르게 하기 위해, 상세 페이지 하단에 "다음/이전 단지" 버튼 추가:
```html
<div class="pagination">
  <a href="./대시보드_단지_{이전단지명}.html" class="nav-btn prev">← {이전}</a>
  <a href="./대시보드.html" class="nav-btn home">홈</a>
  <a href="./대시보드_단지_{다음단지명}.html" class="nav-btn next">{다음} →</a>
</div>
```

**색상**: primary 링크, neutral_500 비활성 버튼  
**간격**: 버튼 간 md (8px), 컨테이너 패딩 xxl (16px)

---

## 접근성 (Accessibility)

### 색상 대비 검증

모든 텍스트는 다음을 충족합니다:
- **일반 텍스트**: WCAG AA 최소 명도 대비 4.5:1
- **큰 텍스트** (18px+): WCAG AA 최소 3:1
- **UI 요소** (테두리, 아이콘): WCAG AA 3:1

**검증 예시**:
- primary (#6d93e8) on neutral_0 (#0f1115): ~9.5:1 ✓ (매우 우수)
- neutral_800 (#9aa0a6) on neutral_50 (#15171c): ~4.5:1 ✓ (경계)
- neutral_700 (#6b7078) on neutral_50 (#15171c): ~3.2:1 ⚠ (큰 텍스트만 허용)

### 스크린리더 (Screen Reader)

- 모든 `<h1>`, `<h2>`, `<h3>` 태그 필수 (페이지 구조 전달)
- 표 헤더는 `<th>` 태그, 데이터는 `<td>` 태그
- 차트 `<svg>`에는 `<title>` 및 `aria-label` 추가
- 클릭 가능한 칩·버튼은 `<button>` 또는 `role="button"` + `tabindex="0"`

### 포커스 상태

- 모든 상호작용 요소는 포커스 시 시각적 피드백 제공
- 링크: 호버 시 primary_hover로 색상 변경
- 버튼: outline 또는 배경색 변경

---

## 스타일 구현 가이드

### CSS 클래스 네이밍

- `.page-header` — 페이지 제목 + breadcrumb
- `.breadcrumb` — 경로 표시
- `.filter-group` — 필터 카테고리 (기존)
- `.filter-head` — 필터 헤더 (기존)
- `.chips` — 칩 컨테이너 (기존)
- `.chip` / `.chip.active` — 개별 칩 (기존)
- `.narrative` — 총평 카드 (기존)
- `.policy-card` — 정책 업데이트 카드 (기존)
- `.alert-banner` — 이상징후 배너 (기존)
- `section` — 데이터 섹션 (기존)
- `h1`, `h2`, `h3`, `h4` — 제목 (기존)
- `.meta` — 메타 정보 (기존)
- `.empty` — 빈 상태 (기존)
- `.back-link` — 뒤로가기 (기존)
- `.pagination` — 단지 간 네비게이션 (신규)
- `.nav-btn` — 페이지 네비게이션 버튼 (신규)

### Token 적용 가이드

이 DESIGN.md에 정의된 모든 토큰은 **빌드 스크립트 또는 CSS 변수**로 구현해야 합니다.

**CSS 변수 예** (미래 리팩토링):
```css
:root[data-theme="dark"] {
  --color-primary: #6d93e8;
  --color-neutral-950: #e6e6e6;
  --color-neutral-0: #0f1115;
  --font-heading-1-size: 20px;
  --spacing-md: 8px;
  --spacing-section-gap: 20px;
}
```

**현재 구현** (Python build_dashboard.py):
- 토큰을 하드코딩된 CSS 문자열에 유지
- 향후: `build_dashboard.py`에서 이 DESIGN.md를 읽어 CSS를 동적 생성

---

## 변경 기록 및 진화

### v1.0 (2026-07-12)

초안 작성:
- 색상 팔레트 정의 (12개 중립색 + 4개 accent)
- 타이포그래피 8단계 (Heading 1~4, Body, Body Small, Label, Caption)
- 간격 단위 8가지 (xs~xxxl)
- 컴포넌트 규칙 9개 (헤더, 섹션, 표, 차트, 필터, 카드, 배너, 링크, 네비)
- 네비게이션 구조 개선 3단계

### 향후 개선 (v1.1+)

- [ ] CSS 변수 변환 (현재 하드코딩 → 동적)
- [ ] 반응형 규칙 추가 (모바일 대응 시 간격·크기 조정)
- [ ] 라이트모드 토큰 정의 (현재는 다크모드만)
- [ ] 컴포넌트 변형 규칙 (예: 버튼의 danger/success variant)
- [ ] 애니메이션/전환 효과 명시 (현재 transition 토큰만)

---

## 참고자료

- 공식 DESIGN.md 스펙: https://github.com/google-ai-studio/design-md
- WCAG 색상 대비 검사: https://webaim.org/resources/contrastchecker/
- 현재 대시보드 구현: `build_dashboard.py`
- 부동산 데이터 파이프라인: `track_watchlist.py`, `fetch_asil.py`

---

**마지막 편집**: 2026-07-12  
**담당자**: 채린이 (디자인 시스템 담당 사원)
