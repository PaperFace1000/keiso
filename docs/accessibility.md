# ♿ アクセシビリティ

## 🔍 コントラスト

- 文字は背景との比 **4.5 以上**（4 テーマすべて）。`tools/build.py` が検査し、下回ると止まる（`docs/color.md`）
- 差し色を文字にするときは `--color-accent-strong` を使う。`--color-accent` は黒のテーマでベースとの比が 4.5 に届かない（カーキもぎりぎりの 4.5）
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
- メニューは ↑↓・Home・End で動き、Enter で選び、Esc と Tab で閉じる。ポップオーバーは Esc で閉じてボタンにフォーカスを戻す（`docs/components.md`）
- 探す欄と一覧を組み合わせる部品（段階的に絞る選択など）は、フォーカスを欄に置いたまま `aria-activedescendant` で行を指す。日本語の変換中のキー（`isComposing`）は選ぶ操作にしない
- マスを並べる選び手（色・アイコン）は、矢印キーで上下左右に動ける
- 並べ替えの「上へ」「下へ」のように、押したあともフォーカスを残したいボタンは、端で `disabled` にせず `aria-disabled="true"` にする（`disabled` にするとフォーカスが外れる）

## 🎯 フォーカスの見え方

```css
:focus-visible {
  outline: 2px solid var(--color-focus);
  outline-offset: var(--k-focus-offset, 2px);
  animation: k-lock-on .18s steps(3, end), k-focus-blink 1.2s steps(1, end) .18s infinite;
}
```

- フォーカスの輪は差し色の 2px。入力欄では欄に重ねる（`outline-offset: 0`）
- プロンプトのように中の `input` を見せない部品は、外側の枠に輪を出す（`:focus-within`）
- フォーカスの輪の色は本文の色（`--color-focus`）。**赤（差し色・ALERT）にしない。** 入力の誤り（赤い枠と左の帯）と見分けられなくなるため
- 今フォーカスがある部品を見失わないよう、輪は動かす。当たった瞬間に外側から 3 段で吸い付き（0.18 秒）、その後は 1.2 秒おきに強い枠線の色と入れ替わって点滅する。キーボードで一覧を動かしている間は、選んでいる行の `▸` も同じ間隔で点滅させる
- 動きはどれも段階的（`steps()`）にし、なめらかに動かさない。`prefers-reduced-motion: reduce` の人には動かさず、輪だけを出す
- 輪を消さない（`outline: none` だけを書かない）

## 🏷️ aria と読み上げ

- アイコンは飾りとして `aria-hidden="true"`。アイコンだけのボタンには `aria-label`
- 入力欄はラベル・説明・エラーを結び付ける（`<label for>`・`aria-describedby`）。プレースホルダーをラベルの代わりにしない
- エラーの欄は `aria-invalid="true"`
- 送信中のボタンに `aria-busy="true"`
- ALERT の知らせは `role="alert"`、それ以外の知らせは `role="status"`
- 選んでいる行は `aria-selected="true"`（選ぶ一覧）か `aria-current="true"`（今開いているもの）。区切りの選択は `aria-pressed`
- 今いるページのリンクは `aria-current="page"`。ナビには `aria-label` で名前を付ける
- 開け閉めするボタン（メニュー・ポップオーバー・開け閉めする欄）は `aria-expanded` と `aria-controls`。メニューを開くボタンは `aria-haspopup="menu"`
- 入と切が変わるボタン（行のピン・除外の切り替え）は `aria-pressed`。`aria-label` は押すとどうなるかを書き、状態と一緒に替える
- カレンダーの今日のマスは `aria-current="date"`
- 件数・月・並び順など、操作の結果で変わる文は `aria-live="polite"` で読み上げる
- 見せずに読み上げだけさせる文は `.k-visually-hidden` で隠す（`display: none` にしない）
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
