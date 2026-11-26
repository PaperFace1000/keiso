# 🔩 keiso（珪素）

無機質で静かな、少しだけ機械らしい配色と、同じ作りの部品を、複数のアプリでそろえるための**デザインシステム**です。

ここには、デザインの原則、色などの値（デザイントークン）、アイコン、部品と画面の組み立ての決まり、ブラウザで開ける見本を置きます。部品のコードはパッケージとして配らず、各アプリがこの決まりと見本に合わせて作ります。

名前は「珪素（けいそ）」から。半導体の素材であり、生き物の気配のない鉱物でもあります。画面も同じように、感情を足さず、情報だけが静かに並ぶものを目指します。

**見本**: 公開した見本はまだありません。手元で `samples/index.html` を開いてください。

## 🗂️ 構成

```
README.md                このファイル
CLAUDE.md                AI コーディングツール向けの決まり
THIRD_PARTY_LICENSES.md  第三者の素材（フォント・アイコン）とライセンスの一覧
docs/
  principles.md          デザインの原則
  color.md               配色（4 テーマ、役割の色、反転、点の格子、分類の色 12 色、コントラスト）
  typography.md          フォント、文字の大きさ、ラベル、ドットの数字
  icons.md               線のアイコンとソリッドのアイコンの使い分け・足し方
  components.md          部品の決まり（ボタン、入力欄、選択、タグ、状態の印、知らせ、一覧、表、数字の欄、メニュー、欄、期日の印など）
  patterns.md            画面の組み立て（ヘッダー、タブ、ダイアログ、空の表示、読み込み中、二重送信の防止、フィルタ、カレンダー、タイムラインなど）
  layout.md              本文の幅、列の組み方、スマホ幅、余白の段階
  logo.md                ロゴの作り
  accessibility.md       コントラスト、色だけに頼らない、キーボード、aria、動き
  coding.md              実装の決まり（テーマの適用、生成スクリプト、localStorage）
  licenses.md            フォント・アイコンのライセンスで守ること
tokens/
  palette.json           4 テーマの色の値（正本）
  themes.css             そのまま読み込める CSS 変数（palette.json から生成）
  extra-colors.json      分類の色 12 色 × 4 テーマ（正本）
  extra-colors.css       data-extra-color 属性で色を出す CSS（生成）
  icons.json             ソリッドと線のアイコンの一覧（生成）
icons/
  solid/                 自作のソリッドのアイコン（24 格子、生成）
  line/                  線のアイコン（Phosphor Icons の Light から選んだもの）
fonts/
  doto-latin.woff2       英数字だけに絞った Doto（ドットの数字用）
  Doto-OFL.txt           Doto のライセンス
tools/
  build.py               生成物を作り直し、色の決まりを確かめる
  solid_icons.py         ソリッドのアイコンの図形の定義
samples/                 ブラウザで直接開ける見本（サーバー不要、外部の読み込みなし）
  index.html             目次
  palette.html           4 テーマの色とコントラスト比
  extra-colors.html      分類の色の見本
  icons.html             アイコンの一覧
  ui-kit.html            部品の見本
  patterns.html          画面の組み立ての見本（カード・ログイン・表・本文・コード・差分・ログ）
  navigation.html        行き来の仕組み（ヘッダー、サイドバーと幅のつまみ・引き出し、ツリー、タブ、目次、検索のダイアログ）
  inputs.html            選ぶ・入れる部品（選択肢のボタン、日付・時刻、色とアイコンの選び手、セレクト、探して選ぶ欄、タグ、段階的に絞る選択、開け閉めする欄）
  overlays.html          浮かぶ部品とダイアログ（メニュー、状態の小ボタン、フィルタ、項目を選ぶダイアログ、詳細・入力のダイアログ、トースト、画面の上の知らせ、版の履歴）
  records.html           欄と一覧（欄の状態、分類の色のマスの行と行の変種、列をそろえる一覧、並べ替えるカード、ドラッグの並べ替え、目標に対する横棒、コピー、早見表）
  time.html              日付と時刻（期日の印、日付の送り、月のカレンダー、時刻つきのタイムライン）
  layout.html            2 列の画面、ドーナツの場合分け、横幅いっぱいの画面、枠の幅で形を変える部品、360px の見え方
  assets/                見本だけで使う CSS・JS（kit.css は部品、shell.css は画面の骨組み。アプリへは配らない）
```

## 🚀 使い方

### 🎨 色を取り込む

1. `tokens/themes.css` をアプリの `styles/themes.css` に写し、入口で最初に読み込む
2. 画面の CSS では `var(--color-text)` のように変数だけを使い、色を直接書かない
3. テーマは `<html data-theme="kaki">` のように `data-theme` で切り替える。付けなければ OS のライトなら白、ダークなら黒になる（詳しくは `docs/color.md`）
4. 分類やタグに色を付けるアプリは `tokens/extra-colors.css` も読み込み、要素に `data-extra-color="blue"` を付けて `var(--extra-text)` などで塗る

### 🔧 値を変える

色やアイコンを変えるときは、正本（`tokens/palette.json`・`tokens/extra-colors.json`・`tools/solid_icons.py`）を直してから、生成スクリプトを実行する。

```sh
python3 tools/build.py
```

- Python 3.9 以上の標準ライブラリだけで動く（追加のパッケージは要らない）
- 文字として使う色の組み合わせが 1 つでもコントラスト比 4.5 未満だと、何も書かずに止まる。値を直してからやり直すこと
- `themes.css`・`extra-colors.css`・`icons.json`・`icons/solid/`・`samples/assets/fonts.css`・`samples/assets/icons.js` は生成物。手で直さない

### 🧩 部品と決まりを取り込む

- 新しいアプリを作るときは `docs/components.md` と `docs/coding.md` を読み、同じ見た目の部品を作る
- 見た目に迷ったら `samples/ui-kit.html` を開いて合わせる
- アプリで良い作りを見つけたら、ここの文書と見本に書き戻す

### 👀 見本を見る

`samples/index.html` をブラウザで開く（サーバーは要らない）。ページの上のボタンで 4 テーマを切り替えられる。URL に `?theme=ekisho` のように付けると、そのテーマで開く。

## 🙅 プルリクエストと Issue

このリポジトリは個人で使うためのものです。プルリクエストと Issue は受け付けていません。

## ⚖️ ライセンス

- keiso 自身のライセンスは未定
- フォント・アイコンなど第三者の素材は、それぞれのライセンスに従う。一覧と許諾文は `THIRD_PARTY_LICENSES.md`、守ることは `docs/licenses.md`
- **ライセンスは配布元が変えることがある。最新の条件は、必ず配布元の公式のページで確かめること**（Phosphor Icons: npm の `@phosphor-icons/core` に入っている `LICENSE`、<https://github.com/phosphor-icons>。Doto: <https://github.com/google/fonts/blob/main/ofl/doto/OFL.txt>）
