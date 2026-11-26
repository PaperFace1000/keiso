# 🛠️ 実装の決まり

## 🎨 CSS

- 色は `var(--color-*)`・`var(--extra-*)` だけを使う。色の値（`#fff` や `rgb()`）を直接書かない。例外は影と幕の黒の透明度だけ
- テーマの色は `tokens/themes.css` を写した `styles/themes.css` に置き、入口で最初に読み込む。その次に全体の土台（`styles/base.css`）
- 大きさ・余白の値は `docs/layout.md` の段階から選ぶ
- 角は `--radius`（6px、箱）と `--radius-sm`（4px、小さな部品と箱の中で塗る行）の 2 段だけを使う。ほかの値を部品ごとに作らない（例外: チェックボックス・キー・件数など 16px 前後の小さな四角は 2〜3px）
- CSS のフレームワーク（Bootstrap・Tailwind など）は使わない。独自の配色と部品の見本があるため
- 外部の CDN・Web フォントを読み込まない。Doto を使うアプリは `fonts/doto-latin.woff2` を同梱する
- リンクの既定の下線は土台で外し、下線はなぞったときだけ（`text-underline-offset: 0.2em`）

### 🧱 base.css

```css
*, *::before, *::after { box-sizing: border-box; }
html { -webkit-text-size-adjust: 100%; }
body {
  margin: 0;
  background: var(--color-base);
  color: var(--color-text);
  font-family: "Hiragino Sans", "Noto Sans JP", "Yu Gothic UI", sans-serif;
  font-size: 15px;
  line-height: 1.7;
}
a { color: inherit; text-decoration: none; }
a:hover { text-decoration: underline; text-underline-offset: 0.2em; }
::selection { background: var(--color-selection-bg); color: var(--color-selection-text); }
:focus-visible { outline: 2px solid var(--color-focus); outline-offset: 2px; }
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation: none !important; transition: none !important; }
}
```

## 🌓 テーマの適用

- テーマは `<html>` の `data-theme` で切り替える（`shiro`・`kaki`・`ekisho`・`kuro`）。付けなければ OS のライト・ダークに従う
- 利用者が「OS に合わせる」を選んだら `data-theme` を外す（`auto` のような値を付けない）
- 選んだテーマは `localStorage` に残してよい。読むのも書くのも `try` / `catch` で囲み、使えない環境（プライベートな窓・保存の拒否）でも画面が動くようにする

```js
const read_theme = () => {
  try { return localStorage.getItem('app.theme'); } catch { return null; }
};
const save_theme = (key) => {
  try { localStorage.setItem('app.theme', key); } catch { /* 保存できなくても切り替えは効く */ }
};
```

- 画面がちらつかないよう、テーマを付ける処理は `<head>` の中で、CSS より前に走らせる
- テーマの一覧はアプリに直書きせず、`tokens/palette.json` の `key`・`label` から作る

## 🔧 生成スクリプト（tools/build.py）

```sh
python3 tools/build.py
```

| 正本（手で直す） | 生成物（手で直さない） |
|---|---|
| `tokens/palette.json` | `tokens/themes.css` |
| `tokens/extra-colors.json` | `tokens/extra-colors.css` |
| `tools/dot_icons.py` | `icons/dot/*.svg` |
| `icons/line/*.svg`（Phosphor から写したもの） | `tokens/icons.json` |
| `fonts/doto-latin.woff2` | `samples/assets/fonts.css`・`samples/assets/icons.js` |

- Python 3.9 以上の標準ライブラリだけで動く。パッケージを入れない
- 文字として使う色の組み合わせが 1 つでも比 4.5 未満だと、何も書かずに exit 1 で止まる。止まったら表示された組み合わせの値を `palette.json` で直す
- 生成物を手で直すと、次の実行で消える。必ず正本を直して作り直す
- 正本と生成物は同じコミットに入れる

## 🧪 見本（samples/）

- サーバー無しでファイルを直接開いて動くこと。`fetch()` でファイルを読まない（ファイルを直接開くと止められる）。フォントとアイコンは `tools/build.py` が JS / CSS に埋め込む
- 見本の共通の CSS・JS は `samples/assets/` に置く（`kit.css`・`sample.js`）。これは見本のためのもので、アプリへは配らない
- 見本で使う ID は `js-` で始める（`id="js-theme-switch"`）
- 見本のダミーの文言は、実在のアプリ・サービス・人を指さない身近な言葉にする

## 📜 JavaScript

- `var` を使わず `const` / `let`
- 比べるときは `===`
- 新しく書くコードの変数名はスネークケース（`const theme_key`）
