---
name: 릴스-만들기
description: 짧은 원본 영상(아기 영상 등)을 인스타 릴스용 세로 영상으로 만든다. 세로 크롭 + 귀여운 자막 + 오리지널 합성 BGM을 ffmpeg로 입힌다. "릴스 만들어줘", "쇼츠로 만들어줘" 같은 요청 시 사용.
---

# 릴스-만들기

짧은(10~20초 내외) 원본 영상을 인스타 릴스/쇼츠용 세로 영상으로 가공하는 파이프라인.
2026-07-06 "유하_주먹고기.mp4" 작업에서 확립됨.

## 전제 조건

- Node.js, FFmpeg, Python(+ numpy/scipy는 video-use venv에 있음)이 설치돼 있어야 함.
- HyperFrames + Video Use가 `C:\Users\eastp\.claude\skills\`에 전역 설치돼 있으면 좋지만, 이 파이프라인 자체는 **순수 ffmpeg만으로 동작**하고 HyperFrames/Video Use 없이도 완결된다. (컷 편집이 필요 없는 짧은 클립엔 이 방식이 더 빠르고 간단함)
- 이 파이프라인은 Windows에서 **PowerShell로 실행해야 한다.** Git Bash에서 ffmpeg drawtext를 실행하면 fontconfig 관련 세그폴트가 난다 (원인 불명, PowerShell에서는 정상 동작).

## 1단계: 판단이 필요한 것 (사용자에게 물어볼 것)

- **화면 비율**: 릴스는 보통 세로 9:16. 원본이 가로면 크롭 방향(어디를 중심으로 자를지) 확인.
- **원본 오디오**: 살릴지(예: 아기 웅얼거림·촵촵 소리처럼 그 자체가 콘텐츠인 경우) vs 뮤트하고 BGM만 쓸지.
- **자막 문구·톤**: 감성적/유머러스/짧고 굵게 등. 여러 버전 뽑아서 고르게 하는 게 좋음.
- **BGM**: 기본값은 **없음** (2026-07-06 결정: 인스타 업로드 후 자체 오디오 기능으로 입히는 게 정석이라, 파일엔 안 넣는 쪽으로 확정). 명시적으로 요청할 때만 3단계의 오리지널 합성 BGM을 입힌다.
- **썸네일**: 기본으로 1:1(1080×1080) 정사각형 썸네일을 별도 이미지로 같이 만든다 (4단계 참고). 어느 타임스탬프 프레임이 좋을지는 `timeline_view.py`로 필름스트립을 먼저 보고 고른다.

## 2단계: BGM 라이선스 원칙 (중요)

- **인스타/틱톡이 추천하는 유행곡을 다운받아 mp4 파일에 심으면 안 된다.** 그 음원들은 플랫폼 내부 재생 권한만 있는 라이선스라 파일로 내보내면 저작권 침해 소지가 있다.
- **정석 경로**: 자막만 있고 음악 없는(또는 볼륨 낮춘) 버전을 만들어 인스타에 업로드 → 인스타 자체 "오디오 추가"에서 유행곡 선택.
- **파일에 미리 입혀야 하면**: ① 아래 3-1단계의 BGM 라이브러리(Pixabay Content License로 확보한 로열티프리 곡) ② 직접 합성한 오리지널 멜로디(3-2단계) 중에서 고른다.

## 3-1단계: BGM 라이브러리 (Pixabay Content License, 2026-07-07 확보)

경로: `C:\Users\eastp\OneDrive\바탕 화면\Claude\video-editor\bgm-library\`

| 파일명 | 분위기 | 원곡 정보 |
|---|---|---|
| 귀여운_글로켄슈필우쿨렐레_zec53.mp3 | 귀엽고 발랄한 (우쿨렐레+글로켄슈필) | "Glockenspiel Ukulele" by zec53, pixabay.com/music/happy-childrens-tunes-glockenspiel-ukulele-287830 |
| 신나는_휘슬조이라이드_TopFlow.mp3 | 신나고 경쾌한 (휘슬) | "Whistle Joyride" by Top-Flow, pixabay.com/music/happy-childrens-tunes-whistle-joyride-193123 |
| 자장가_젠틀베이비슬립_alexmorgan.mp3 | 잔잔하고 포근한 (자장가) | "Gentle Baby Sleep Lullaby Dream" by alex-morgan, pixabay.com/music/lullabies-gentle-baby-sleep-lullaby-dream-530944 |
| 뮤직박스_매직더스트앤스타라이트_DJMYRIDA.mp3 | 뮤직박스/반짝이는 느낌 | "Magic Dust & Starlight" by DJMYRIDA, pixabay.com/music/modern-classical-magic-dust-amp-starlight-519510 |

- 전부 "Free for use under the Pixabay Content License" 배지 확인 후 다운로드함. 크레딧 표기 불필요, 상업적 이용 가능.
- 마지막 곡(DJMYRIDA)은 팔로워 수가 적고 "Content ID Registered" 배지가 없는 업로더지만, 라이선스 문구 자체는 동일하게 표시돼 있어 사용엔 문제없음. 더 안전한 대체곡을 원하면 Content ID Registered 배지가 있는 트랙으로 교체 검토.
- 원본 mp3 길이가 영상보다 길면 `ffmpeg -i in.mp3 -t <영상길이> -af "afade=t=out:st=<길이-1>:d=1" out.wav`로 트림 + 페이드아웃.
- **새 곡을 더 받을 때**: Pixabay 페이지에서 쿠키 배너는 "모두 거부"로 닫고, 우측 상단 초록색 "Download" 버튼 클릭 → 다운로드 폴더에 자동 저장됨(포맷 선택 없이 바로 mp3). 페이지 상단에 "Free for use under the Pixabay Content License" 문구가 있는지 반드시 확인 후 진행.

## 3-2단계: 오리지널 BGM 합성 (ffmpeg만으로, 라이브러리에 맞는 곡이 없을 때)

## 3단계: 오리지널 BGM 합성 (ffmpeg만으로, 저작권 완전 자유)

사인파 + 배음(2배 주파수, 낮은 볼륨) 조합으로 벨/글로켄슈필 톤을 만들고, 음표별로 붙여서 멜로디를 구성한다.

```bash
gen_note() {
  local freq=$1 dur=$2 outfile=$3 overtone_vol=$4 decay_start=$5
  local overtone=$(python3 -c "print(${freq}*2)")
  ffmpeg -y -f lavfi -i "sine=frequency=${freq}:duration=${dur}:sample_rate=44100" \
    -f lavfi -i "sine=frequency=${overtone}:duration=${dur}:sample_rate=44100" \
    -filter_complex "[1:a]volume=${overtone_vol}[ov];[0:a][ov]amix=inputs=2:duration=first[mx];[mx]afade=t=out:st=${decay_start}:d=$(python3 -c "print(${dur}-${decay_start})"),afade=t=in:d=0.01,volume=0.7[out]" \
    -map "[out]" -ac 2 "${outfile}" -loglevel error
}
# 음표들을 gen_note로 만든 뒤 concat demuxer로 이어붙이고,
# 전체에 afade in/out으로 시작/끝을 부드럽게.
```

톤 변화 아이디어: 음표 길이(짧으면 발랄, 길면 차분), 음역대(높으면 뮤직박스, 낮으면 자장가), `aecho` 필터(반짝이는 느낌), 스타카토 vs 레가토(decay_start 타이밍).

이미 만들어둔 4종 참고용 샘플: `C:\Users\eastp\OneDrive\바탕 화면\Claude\video-editor\footage\edit\bgm\options\` (little_bell, playful_pluck, soft_lullaby, music_box)

## 4단계: 최종 렌더링 (PowerShell)

```powershell
$fontPath = "C\:\\Windows\\Fonts\\malgunbd.ttf"   # 한글 지원 폰트, 콜론 이스케이프 필수
$textPath = "C\:\\...\\caption.txt"                # 자막은 -vf 문자열에 직접 넣지 말고 textfile로 (한글 인코딩 깨짐 방지)
$vf = "crop=W:H:X:Y,scale=1080:1920,setsar=1,drawtext=fontfile='$fontPath':textfile='$textPath':fontcolor=white:fontsize=95:borderw=8:bordercolor=black@0.55:box=1:boxcolor=0xFF8FB8@0.4:boxborderw=25:x=(w-text_w)/2:y=h-320:alpha='if(lt(t,0.4),t/0.4,if(gt(t,DUR-0.5),(DUR-t)/0.5,1))'"
$af = "[0:a]volume=1.0[a0];[1:a]volume=0.18[a1];[a0][a1]amix=inputs=2:duration=first:dropout_transition=0,volume=1.3[a]"
ffmpeg -y -i "원본.mp4" -i "bgm.wav" -filter_complex "[0:v]$vf[v];$af" -map "[v]" -map "[a]" `
  -c:v libx264 -crf 18 -preset medium -pix_fmt yuv420p -c:a aac -b:a 192k -movflags +faststart "edit\final.mp4"
```

- `alpha=` 표현식은 자막이 갑자기 뿅 뜨지 않고 0.4초에 걸쳐 페이드인, 끝나기 0.5초 전부터 페이드아웃하게 함 (딱딱한 정적 자막보다 훨씬 자연스러움).
- 크롭 좌표(W:H:X:Y)는 원본 해상도와 피사체 위치에 따라 매번 계산: 세로 크롭 폭 = 원본높이 * 9/16, X = (원본너비-크롭폭)/2 (얼굴이 중앙에 없으면 조정).
- 원본 오디오를 살릴 땐 `volume=1.0`, BGM은 0.15~0.25 정도로 낮게 — 원본 소리(아기 웅얼거림 등)가 콘텐츠의 핵심이면 절대 깔지 말 것.

## 5단계: 자체 검증

`video-use`의 `timeline_view.py`로 결과물 필름스트립을 뽑아 자막 위치·크롭 프레이밍을 눈으로 확인.

```bash
cd ~/.claude/skills/video-use && uv run python helpers/timeline_view.py "<final.mp4 경로>" 0 <영상길이>
```

## 4단계-부록: 1:1 썸네일 만들기

```powershell
$vf = "crop=H:H:X:0,scale=1080:1080,setsar=1,drawtext=fontfile='$fontPath':textfile='$textPath':fontcolor=white:fontsize=70:borderw=6:bordercolor=black@0.55:box=1:boxcolor=0xFF8FB8@0.4:boxborderw=20:x=(w-text_w)/2:y=h-160"
ffmpeg -y -ss <타임스탬프> -i "원본.mp4" -vf $vf -frames:v 1 "edit\thumbnail.png"
```

- 정사각형 크롭 폭 = 원본 높이(H), X = (원본너비-H)/2 (얼굴 위치에 따라 조정).
- `-ss`로 표정 좋은 프레임 타임스탬프를 지정. `timeline_view.py`로 미리 훑어보고 고르면 빠름.

## HDR 원본(아이폰 등) 처리

- 아이폰 촬영본은 종종 HEVC 10bit + Dolby Vision/HLG(HDR)로 인코딩돼 있다. `ffprobe`로 `color_transfer: arib-std-b67` 또는 `side_data_type: DOVI configuration record`가 보이면 HDR 원본.
- **기본값은 톤매핑(SDR 변환) 없이 그대로 스케일만 적용.** (2026-07-07 결정: 톤매핑판을 보여줬더니 사용자가 "별로야, SDR로 변환하지 말아줘"라고 함 — 원본 색감을 더 선호함.)
- `zscale=t=linear:npl=100,...,tonemap=hable,...` 체인은 **명시적으로 요청받았을 때만** 적용. 괜히 먼저 톤매핑해서 보여주지 말 것.
- 이미 세로로 촬영된 아이폰 영상은 회전 메타데이터(`rotation: -90` 등)가 있어도 ffmpeg가 자동으로 반영해서 디코딩하므로 별도 회전 처리 불필요 — `ffprobe`로 실제 표시 해상도(회전 적용 후) 확인 후 크롭 필요 여부만 판단.

## 6단계: 게시글 문구 + 해시태그 (항상 같이 제안)

렌더링 결과물을 줄 때 **항상** 인스타 게시글용 문구 2~3개 + 해시태그도 같이 제안한다 (2026-07-07 확정 요청).

- **톤**: 아빠(도요) 시점, 귀엽고 짧게. 아기를 관찰하는 애정 어린 유머 — "나(아기) 목소리 흉내"가 아니라 "아빠가 보면서 느끼는 마음"으로 쓴다.
- **해시태그**: 4개 정도만. 기본 세트: `#딸바보 #육아스타그램 #newbornbaby #유하` — 영상 컨셉에 맞으면 하나 정도 교체.
- 영상 컨셉(이번엔 "사장님 포스" 같은 상황극)에 맞춰 톤을 맞추되, 과하게 길게 늘어놓지 않는다.

## 알아둘 것

- Video Use(컷 편집)는 대사 있는 긴 영상에서 필러워드 제거할 때만 필요. 이런 짧고 컷 편집 불필요한 클립엔 안 써도 됨.
- 강이(유튜브 학습노트 에이전트)에게 위임한 경험상, 위임형 에이전트가 실제 작업 없이 "완료 보고"만 하고 끝내는 경우가 있었음 — 결과물(파일 존재 여부) 항상 직접 확인할 것.
