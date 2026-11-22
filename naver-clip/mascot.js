// 오리지널 마스코트 '이슈 부엉이' SVG. expr: surprised | thinking | happy
module.exports = function mascot(expr = 'surprised') {
  const body = '#FF9F1C', belly = '#FFE8C2', dark = '#2B2118';
  let eyes, beak, extra = '', brows = '';
  if (expr === 'happy') {
    eyes = `<path d="M118 178 q32 -34 64 0" stroke="${dark}" stroke-width="14" fill="none" stroke-linecap="round"/>
            <path d="M218 178 q32 -34 64 0" stroke="${dark}" stroke-width="14" fill="none" stroke-linecap="round"/>`;
    beak = `<path d="M182 222 L218 222 L200 252 Z" fill="#FF6B35"/>`;
    extra = `<ellipse cx="110" cy="225" rx="22" ry="12" fill="#FF7A90" opacity=".55"/><ellipse cx="290" cy="225" rx="22" ry="12" fill="#FF7A90" opacity=".55"/>
             <text x="330" y="70" font-size="70" font-weight="900" fill="#FFE14D" font-family="P">♪</text>`;
  } else if (expr === 'thinking') {
    eyes = `<circle cx="150" cy="180" r="44" fill="#fff"/><circle cx="250" cy="180" r="44" fill="#fff"/>
            <circle cx="166" cy="166" r="17" fill="${dark}"/><circle cx="266" cy="166" r="17" fill="${dark}"/>
            <path d="M106 180 a44 44 0 0 1 88 0 Z" fill="${belly}"/><path d="M206 180 a44 44 0 0 1 88 0 Z" fill="${belly}"/>`;
    beak = `<path d="M184 226 L216 226 L200 250 Z" fill="#FF6B35"/>`;
    extra = `<text x="312" y="90" font-size="96" font-weight="900" fill="#fff" stroke="${dark}" stroke-width="5" font-family="P">?</text>
             <path d="M70 120 q-14 26 0 36 q14 -10 0 -36 Z" fill="#7FD3FF"/>`;
  } else { // surprised
    eyes = `<circle cx="150" cy="180" r="48" fill="#fff"/><circle cx="250" cy="180" r="48" fill="#fff"/>
            <circle cx="150" cy="182" r="13" fill="${dark}"/><circle cx="250" cy="182" r="13" fill="${dark}"/>`;
    beak = `<ellipse cx="200" cy="240" rx="18" ry="22" fill="${dark}"/><path d="M184 222 L216 222 L200 234 Z" fill="#FF6B35"/>`;
    brows = `<path d="M112 112 q38 -22 76 0" stroke="${dark}" stroke-width="10" fill="none" stroke-linecap="round"/>
             <path d="M212 112 q38 -22 76 0" stroke="${dark}" stroke-width="10" fill="none" stroke-linecap="round"/>`;
    extra = `<path d="M340 40 l-8 52" stroke="#FFE14D" stroke-width="14" stroke-linecap="round"/><circle cx="328" cy="114" r="8" fill="#FFE14D"/>
             <path d="M372 70 l-26 40" stroke="#FFE14D" stroke-width="10" stroke-linecap="round"/><path d="M300 30 l2 44" stroke="#FFE14D" stroke-width="10" stroke-linecap="round"/>`;
  }
  return `<svg viewBox="0 0 400 420" xmlns="http://www.w3.org/2000/svg">
    <path d="M92 92 L120 30 L150 86 Z" fill="${body}"/><path d="M308 92 L280 30 L250 86 Z" fill="${body}"/>
    <ellipse cx="200" cy="250" rx="150" ry="160" fill="${body}"/>
    <ellipse cx="200" cy="300" rx="100" ry="105" fill="${belly}"/>
    <path d="M60 250 q-30 60 20 110 q20 -50 10 -110 Z" fill="#E8890F"/><path d="M340 250 q30 60 -20 110 q-20 -50 -10 -110 Z" fill="#E8890F"/>
    <path d="M150 300 q10 8 20 0 M190 330 q10 8 20 0 M230 300 q10 8 20 0" stroke="#E8C79A" stroke-width="6" fill="none" stroke-linecap="round"/>
    <circle cx="150" cy="180" r="56" fill="none" stroke="${dark}" stroke-width="10"/><circle cx="250" cy="180" r="56" fill="none" stroke="${dark}" stroke-width="10"/>
    <path d="M194 176 h12" stroke="${dark}" stroke-width="10"/>
    ${eyes}${brows}${beak}
    <path d="M150 404 l-14 14 M150 404 l0 16 M150 404 l14 14 M250 404 l-14 14 M250 404 l0 16 M250 404 l14 14" stroke="#FF6B35" stroke-width="9" stroke-linecap="round"/>
    ${extra}
  </svg>`;
};
