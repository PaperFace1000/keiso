# 📐 レイアウト

見本は `samples/layout.html`。

## 📏 余白の段階

余白・間はこの 7 段から選ぶ。CSS 変数は `--space-1`〜`--space-7`。

| 段 | 値 | 使いどころ |
|---|---|---|
| 1 | 4px | ラベルと欄、アイコンと小さな文字 |
| 2 | 8px | ボタンの中のアイコンと文字、ボタンどうし |
| 3 | 12px | 行の中の左右、表のセルの左右 |
| 4 | 16px | 欄の中の余白、欄どうし、画面の左右の最小の余白 |
| 5 | 24px | 値の一覧の列の間、節の中のまとまりの間 |
| 6 | 32px | ページの上の余白 |
| 7 | 48px | 節と節の間、ページの下の余白、空の表示の上下 |

- 兄弟の要素は flex か grid の `gap` で並べ、要素ごとの `margin` で間を作らない

## 🧱 本文の枠（`.k-page`）

- 本文は中央に置き、左右の余白は `max(16px, env(safe-area-inset-left, 0px))`（右も同じ）、上 32px、下 48px
- 節と節の間は 48px

### 画面の種類で本文の幅を変える

| 画面 | 本文の幅 | クラス |
|---|---|---|
| 一覧・図（既定） | 76rem | `.k-page` |
| 読み物（長い説明と数字が続く） | 64rem | `.k-page--reading` |
| 入力が主役（設定・作成） | 48rem | `.k-page--narrow` |
| 一覧をたくさん並べる | 上限なし | 画面ごとに `max-width: none` |

- 狭くするのは本文の枠で、欄ごとに `max-width` を付けて回らない
- ヘッダーの中身の幅は、本文の既定の幅（76rem）にそろえる

## 🗂️ 列の組み方

- 欄を並べる画面は grid で組み、狭くなったら 1 列に落とす

```css
.columns {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 320px), 1fr));
  gap: var(--space-4);
}
```

- 左に一覧、右に詳しい中身を出す画面は、左を 320px 前後に固定し、右を残りに。899px 以下では 1 列にして、一覧を選ぶと詳しい画面へ移る
- grid と flex の子で、本文・表・コードを持つものには `min-width: 0` を付ける（長い中身で列が押し広げられないように）
- 縦に積むだけの grid（欄・節）も、列を `grid-template-columns: minmax(0, 1fr)` にしておく。列を決めない grid は、1 行で省略する題名や横にスクロールするコードの中身の幅まで広がり、360px で画面が横に動く
- 数字の欄（`.k-stat`）は `repeat(auto-fit, minmax(180px, 1fr))` で並べる

## ↔️ 横幅いっぱいの画面

一覧をたくさん並べる画面だけ、本文の幅の上限を外す（`max-width: none`）。読む画面・入力の画面には使わない。見本は `samples/layout.html`。

| 項目 | 値 |
|---|---|
| 余白 | 上下 24px・32px、左右 24px。899px 以下は 16px |
| 列の比 | 項目の多い側を広く、3 : 2（`minmax(0, 3fr) minmax(0, 2fr)`）、間 16px、`align-items: start` |

**1 列のときに右の列の要約を先頭に出す**

```css
@media (max-width: 899px) {
  .columns--wide { display: flex; flex-direction: column; align-items: stretch; }
  .columns--wide > .column { display: contents; }
  .columns--wide > .column > * { min-width: 0; }
  .columns--wide .column__lead { order: -1; }
}
```

- `align-items: stretch` を忘れない（2 列のときの `start` が残ると、縦の flex で部品が中身の幅に縮む）
- 列の枠が無くなるので、間は flex の `gap` で取る。部品には `min-width: 0` を付け、1 行で省略する題名で横に広がらないようにする
- 先頭に出すのは 1 つだけ。読み上げとキーボードの順は HTML のままなので、先に読まれても困らないもの（要約）に限る

## 📦 置かれた枠の幅で形を変える部品

同じ部品を広い列にも狭い列にも置くときは、画面の幅ではなく部品の枠の幅で形を変える（`@container`）。

```css
.fit-card { container-type: inline-size; container-name: fit-card; }
.fit-card__body { display: grid; grid-template-columns: minmax(0, 1fr) minmax(9rem, 14rem) auto; gap: 8px 16px; }
@container fit-card (max-width: 479px) {
  .fit-card__body { grid-template-columns: minmax(0, 1fr) auto; }
  .fit-card__main { grid-column: 1 / -1; }
}
```

- 部品の外側の要素を入れ物にし、中身を `@container` で崩す（入れ物と中身を同じ要素にはできない）
- 入れ物は幅を外から決めてもらう要素にする。中身の幅で広がる場所（横並びの flex の子で `flex: none` など）に置くと幅が 0 になる
- 名前（`container-name`）を部品ごとに付け、ほかの入れ物の幅で崩れないようにする
- 小さいタブ（`.k-tabs--sm`）も帯を入れ物にして、480px 以下でアイコンを外している

## 📱 スマホの幅

- 360px の幅で崩れないこと。本文を横にスクロールさせない
- 横に長いもの（表・コード・図）は、それぞれの箱の中だけ横にスクロールさせる（`overflow-x: auto`）
- ボタンの並びは折り返す。ボタンの文言は折り返さない
- 押せるものは高さ 36px 以上（一覧の行は 44px 以上）
- 画面の端に固定するもの（ヘッダー・下のバー）は、端末の切り欠きの分（`env(safe-area-inset-*)`）を余白に足す
