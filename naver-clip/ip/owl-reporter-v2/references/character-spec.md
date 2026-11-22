# 이슈 부엉이 v2 (owl-reporter-v2) 캐릭터 규칙

이전 버전(`owl-reporter`)이 너무 튄다는 의견을 반영해 더 귀엽고 차분하게 다시 디자인했다. 이전 팩은 지우지 않고 그대로 두었다.
기준 이미지: `assets/turnaround.png` (앞·옆·뒤), `assets/owl_hero.png` (대표 이미지)

## 캐릭터 역할
- "3분 이슈 정리"를 전하는 귀여운 기자. 내용을 가리지 않고 옆에서 반응하는 보조 역할
- 영상에서는 화면 구석에 작게(약 300px) 나오고, 카드 표지에서는 말풍선과 함께 나온다

## 고정 특징 (절대 유지)
- 2등신 귀요미 비율: 크고 둥근 머리와 작은 몸이 하나로 이어진 모양
- 파스텔 살구색 몸, 크림색 얼굴과 배, 배에 물결 모양 깃털 무늬
- 작고 뾰족한 귀깃 2개, 그 사이에 작은 갈색 중절모
- 가느다란 둥근 안경, 별 모양 하이라이트가 있는 크고 반짝이는 갈색 눈
- 작은 노란 부리, 분홍 볼터치
- 작은 빨간 나비넥타이
- 짧은 날개, 노란 발
- 얇고 부드러운 갈색 외곽선, 평면 스티커 그림체

## 바뀌어도 되는 것
- 표정과 날개 동작 (놀람, 고민, 기쁨, 걱정, 설명)
- 소품: 노란 마이크, 신문, 없음
- 주변 효과: 반짝이, 물음표, 느낌표, 땀방울

## 바뀌면 안 되는 것 (금지)
- 진한 주황이나 굵은 검은 외곽선 (이전 버전처럼 튀는 색감)
- 긴 넥타이, 귀깃이나 중절모가 사라지는 것
- 사실적·3D 그림체, 실존 인물, 글자나 로고

## 이미지 생성 프롬프트 조각
> This exact same cute pastel owl mascot (identity locked: chibi round peach-apricot body, cream face, two small ear tufts, tiny brown fedora, thin round glasses, sparkly eyes, rosy cheeks, small red bow tie, thin soft brown outline, kawaii flat sticker style). Plain pure white background, no glow, no text.

생성할 때는 항상 대표 이미지의 원본 작업(job 28c586ac-9ea5-47d4-966b-19bdbb1547f1)을 참고 이미지로 넣는다.
모델이 배경을 투명하게 만들어 주는 경우가 있으니, 결과 이미지의 알파 채널을 먼저 확인한다.

## 일관성 확인 목록
- [ ] 파스텔 살구색, 얇은 갈색 외곽선
- [ ] 귀깃 2개 + 작은 중절모 + 둥근 안경 + 빨간 나비넥타이
- [ ] 2등신 비율, 볼터치
- [ ] 표정과 동작만 바뀌고 정체성은 같다
