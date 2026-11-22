# 이슈 부엉이 (owl-reporter) 캐릭터 규칙

`wwyd554/IP-skill`의 IP 팩 형식과 `talvanes/character-turnaround-sheets`의 정체성 고정 방식을 따랐다.
기준 이미지: `assets/turnaround.png` (앞·옆·뒤), `assets/owl_surprised.png` (대표 이미지)

## 캐릭터 역할
- "3분 이슈 정리"를 전하는 기자. 독자 대신 놀라고, 고민하고, 기뻐하는 반응 담당
- 카드 표지에서는 말풍선으로 독자의 속마음을 대신 말하고, 영상에서는 장면 분위기를 바꾸는 역할

## 고정 특징 (절대 유지)
- 통통하고 둥근 주황색 부엉이, 머리와 몸이 하나로 이어진 2등신
- **양쪽으로 길게 솟은 뾰족한 주황 귀깃 2개**, 그 사이에 작은 갈색 중절모
- 크고 둥근 검은 뿔테 안경, 눈동자는 짙은 갈색에 흰 하이라이트 2개
- 노란 부리
- 흰 셔츠 깃 + 빨간 넥타이
- 크림색 배, 갈색 비늘 모양 깃털 무늬
- 주황 발, 뒤에서 보면 부채꼴 꼬리깃
- 평면 2D 벡터 스티커 그림체, 굵은 짙은 갈색 외곽선

## 바뀌어도 되는 것
- 표정과 날개 동작 (놀람, 고민, 기쁨, 걱정, 설명)
- 들고 있는 소품: 노란 마이크, 신문, 없음
- 주변 효과: 반짝이, 물음표, 땀방울, 강조선

## 바뀌면 안 되는 것 (금지)
- 귀깃이나 중절모가 사라지는 것, 모자 종류가 바뀌는 것
- 안경 모양 변경(사각형 등), 넥타이 색 변경
- 사실적·3D 그림체, 몸 색이 주황에서 벗어나는 것
- 실존 인물 얼굴, 글자나 로고를 그려 넣는 것

## 이미지 생성 프롬프트 조각
> This exact same owl reporter mascot, identity locked: chubby round orange owl, two tall pointed orange ear tufts with a small brown fedora between them, big round black-rimmed glasses, yellow beak, white shirt collar with red necktie, cream belly with scalloped feather marks, orange feet. Flat 2D vector sticker style, clean thick dark outline. Plain pure white background, no glow, no text.

생성할 때는 항상 `assets/owl_surprised.png`의 원본 생성 작업(job a1336bba-727a-441f-a1f4-699cbca27f17)을 참고 이미지로 넣는다.

## 일관성 확인 목록
- [ ] 귀깃 2개와 중절모가 보인다
- [ ] 둥근 뿔테 안경, 빨간 넥타이, 크림색 배 무늬가 그대로다
- [ ] 그림체가 평면 스티커 스타일이다
- [ ] 표정과 동작만 바뀌고 정체성은 같다

## 표정 파일 (배경 투명 PNG)
| 파일 | 표정 | 쓰는 곳 |
|---|---|---|
| owl_surprised.png | 놀람, 마이크와 신문 | 충격 이슈, 기본 표지 |
| owl_thinking.png | 고민, 물음표 | 검증 중, 논란, 분석 |
| owl_happy.png | 기쁨, 만세 | 혜택, 좋은 소식 |
| owl_worried.png | 걱정, 땀방울 | 하락, 피해, 주의 |
| owl_explaining.png | 설명, 왼쪽 가리킴 | 본문 카드, 정리 |
