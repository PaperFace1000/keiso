# ♿ アクセシビリティ

## 🔍 コントラスト

- 文字は背景との比 **4.5 以上**（4 テーマすべて）。`tools/build.py` が検査し、下回ると止まる（`docs/color.md`）
- 差し色を文字にするときは `--color-accent-strong` を使う。`--color-accent` はカーキと黒でベースとの比が 4.5 に届かない
- 枠・点・フォーカスの輪など文字でないものは、比 3 を目安にする
- 押せないもの（`opacity: .45`）は比が下がる。押せない理由が分かりにくいときは、近くに文で書く

## 🚦 色だけに頼らない

- 状態は、四角い点・アイコン・名前（`SUCCESS`・`INFO`・`WARNING`・`ALERT`）を必ず並べる
- 液晶のテーマは地が緑なので、SUCCESS の緑が見分けにくい。名前があれば色に頼らずに済む
- 切り替えは `ON` / `OFF` の文字を出す。目盛りは数字を出す
- 分類の色は、名前の文字と並べる（色だけで選ばせない）

## ⌨️ キーボード操作

- すべての操作を Tab と Enter / Space で行えること。メニューとタブは矢印キーで動き、Esc で閉じる
- ダイアログが開いたらフォーカスを中に移し、閉じたら開いたボタンに戻す。開いている間は後ろの画面を操作できない
- キーボードで動かす前提の画面（`docs/patterns.md` の「キーボードで動かす」）でも、マウスと指で同じことができること

## 🎯 フォーカスの見え方

```css
:focus-visible { outline: 2px solid var(--color-focus); outline-offset: 2px; }
```

- フォーカスの輪は差し色の 2px。入力欄では欄に重ねる（`outline-offset: 0`）
- プロンプトのように中の `input` を見せない部品は、外側の枠に輪を出す（`:focus-within`）
- 輪を消さない（`outline: none` だけを書かない）

## 🏷️ aria と読み上げ

- アイコンは飾りとして `aria-hidden="true"`。アイコンだけのボタンには `aria-label`
- 入力欄はラベル・説明・エラーを結び付ける（`<label for>`・`aria-describedby`）。プレースホルダーをラベルの代わりにしない
- エラーの欄は `aria-invalid="true"`
- 送信中のボタンに `aria-busy="true"`
- ALERT の知らせは `role="alert"`、それ以外の知らせは `role="status"`
- 選んでいる行は `aria-selected="true"`（選ぶ一覧）か `aria-current="true"`（今開いているもの）。区切りの選択は `aria-pressed`
- 今いるページのリンクは `aria-current="page"`。ナビには `aria-label` で名前を付ける
- 大文字のラベルは `text-transform` で大文字にし、元の文字は普通に書く（読み上げが 1 文字ずつ読まないように）
- `<html lang="ja">`

## 🎞️ 動き

- 点滅・順に灯る点・つまみの移動など、動きはすべて `prefers-reduced-motion: reduce` で止める

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation: none !important; transition: none !important; }
}
```

- 1 秒に 3 回より速く点滅させない
