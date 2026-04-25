# Incruit Design Tokens

Figma Tokens (Tokens Studio) 호환 JSON.

## 사용법

### Figma에서 import

1. Figma 파일에 [Tokens Studio for Figma](https://tokens.studio/) 플러그인 설치
2. 플러그인 열기 → Settings → Sync Providers → JSON Bin / GitHub
3. `tokens.json`을 token sets로 import
4. Token sets order: `global` → `light` → `dark` (다크 모드 작업 시 토글)

### Tailwind / CSS로 export (Style Dictionary)

```bash
npm install -D style-dictionary
npx style-dictionary build --config sd.config.js
```

`sd.config.js` 예시:
```js
module.exports = {
  source: ['design-tokens/tokens.json'],
  platforms: {
    css: {
      transformGroup: 'css',
      buildPath: 'build/css/',
      files: [{ destination: 'tokens.css', format: 'css/variables' }]
    },
    tailwind: {
      transformGroup: 'js',
      buildPath: 'build/tailwind/',
      files: [{ destination: 'tokens.js', format: 'javascript/module' }]
    }
  }
}
```

## 구조

- **global**: 원시 토큰 (color palette, font, spacing, border-radius, shadow, typography)
- **light**: 라이트 테마 시맨틱 (background, text, border, interactive)
- **dark**: 다크 테마 시맨틱

`{global.color.primary.500}` 같은 reference 사용 → 테마 전환 시 시맨틱 토큰만 바꾸면 됨.

## 폰트

`fontFamily.sans` = `"Incruit Sans, ..."` 로 정의됨. Figma에서 사용하려면:
1. `build/IncruitSans-*.otf` 9개 weights를 Figma 데스크탑 앱에 설치
2. 또는 [Figma Custom Fonts](https://help.figma.com/hc/en-us/articles/4406439888919) 통해 팀 전체 공유

## 갱신 정책

- v0.x: 잦은 변경 (실험)
- v1.0+: 시맨틱 토큰 이름은 deprecation 사이클 거침 (3개월 noticed → remove)
- 색상 hex 값 변경은 토큰 이름 유지 (재해석)

## 검증

`tokens.json` validate:
```bash
python3 -c "import json; json.load(open('design-tokens/tokens.json')); print('OK')"
```
