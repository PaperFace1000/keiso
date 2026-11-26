# 🛠️ 実装の決まり

## 🎨 CSS

- 色は `var(--color-*)`・`var(--extra-*)` だけを使う。色の値（`#fff` や `rgb()`）を直接書かない。例外は影と幕の黒の透明度だけ
- テーマの色は `tokens/themes.css` を写した `styles/themes.css` に置き、入口で最初に読み込む。その次に全体の土台（`styles/base.css`）
- 大きさ・余白の値は `docs/layout.md` の段階から選ぶ
- 角は `--radius`（6px、箱）と `--radius-sm`（4px、小さな部品と箱の中で塗る行）の 2 段だけを使う。ほかの値を部品ごとに作らない（例外: チェックボックス・キー・件数など 16px 前後の小さな四角は 2〜3px）
- CSS のフレームワーク（Bootstrap・Tailwind など）は使わない。独自の配色と部品の見本があるため
- 外部の CDN・Web フォントを読み込まない。Doto を使うアプリは `fonts/doto-latin.woff2` を同梱する
- リンクの既定の下線は土台で外し、下線はなぞったときだけ（`text-underline-offset: 0.2em`）
- 影は浮かぶもの（トースト・画面の上の知らせ・メニュー・ポップオーバー）にだけ、1 つの値（`--shadow-float`）で付ける。欄・カード・ダイアログには付けない
- スクロールバーは土台（`base.css`）でテーマの色にそろえ、部品ごとに上書きしない

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
/* hidden を付けたものは、display を持つ部品でも必ず隠す */
[hidden] { display: none !important; }
/* スクロールバー: 細く、つまみは四角。色は強い線の色、なぞると補足の文字の色 */
* { scrollbar-width: thin; scrollbar-color: var(--color-border-strong) transparent; }
::-webkit-scrollbar { width: 10px; height: 10px; }
::-webkit-scrollbar-track, ::-webkit-scrollbar-corner { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--color-border-strong); border: 3px solid transparent; border-radius: 1px; background-clip: padding-box; }
::-webkit-scrollbar-thumb:hover { background: var(--color-muted); background-clip: padding-box; }
::selection { background: var(--color-selection-bg); color: var(--color-selection-text); }
:focus-visible {
  outline: 2px solid var(--color-focus);
  outline-offset: var(--k-focus-offset, 2px);
  animation: k-lock-on .18s steps(3, end), k-focus-blink 1.2s steps(1, end) .18s infinite;
}
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
| `tools/solid_icons.py` | `icons/solid/*.svg` |
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
