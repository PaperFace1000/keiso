# 🔣 アイコン

アイコンは 2 種類を使い分ける。**画面に絵文字は使わない。** 一覧は `tokens/icons.json`、見本は `samples/icons.html`。

| 種類 | 置き場所 | 大きさ | 使いどころ |
|---|---|---|---|
| 線 | `icons/line/` | 基本 20px、詰めるところは 16px | 普段の操作（ボタン・メニュー・入力欄の中・知らせの欄の印・一覧の行） |
| ドット | `icons/dot/` | 基本 64px、最小 48px（96px も可） | 目立つところ（空の表示・状態を大きく見せる欄・ページの見出しの印・ロゴ） |

- 線のアイコンが入る場面にドットのアイコンを小さくして置かない。**48px より小さく出すときは線のアイコンを使う**（ドットが潰れて線に見えるため）
- 1 つの欄の中で 2 種類を混ぜない（空の表示の中ではドットだけ、ボタンの中では線だけ）
- どちらも `fill="currentColor"` で、色は親の文字の色を継ぐ。状態の印は親に `.k-role-*` を付けて役割の色にする
- アイコンは飾りとして `aria-hidden="true"` にする。アイコンだけのボタンには `aria-label` を付ける

## 〰️ 線のアイコン（Phosphor Icons の Light）

- Phosphor Icons の **Light**（線の細い太さ）から、よく使う 97 個を選んで `icons/line/` に置いている。名前は Phosphor の名前から `-light` を外したもの（`magnifying-glass.svg`）
- ライセンスは MIT（`docs/licenses.md`）
- 太さは Light にそろえる。Thin・Regular・Bold などを混ぜない

### 足す手順

1. 公式の npm のパッケージ `@phosphor-icons/core` を取得する（`npm pack @phosphor-icons/core`）。まとめサイトやミラーから取らない
2. `npm view @phosphor-icons/core dist.shasum` の値と、取得した `.tgz` の `sha1sum` が一致することを確かめる
3. 展開した `package/assets/light/<名前>-light.svg` を `icons/line/<名前>.svg` として写す（中身は変えない）
4. 版が上がっていたら、`package/LICENSE` と `THIRD_PARTY_LICENSES.md` の写しが同じかを確かめる
5. `python3 tools/build.py` を実行し、`tokens/icons.json` と見本に反映する

## ⠿ ドットのアイコン（自作）

- 32×32 の格子に、丸いドットで描く。線の太さは 2.4 ドット（2〜3 粒）、ドットの半径はマスの幅の 0.42
- 64px で出すと 1 ドットが 2px になり、粒が 1 つずつ見える。これが基本の大きさ
- 図形の定義は `tools/dot_icons.py`。`tools/build.py` が `icons/dot/<名前>.svg` を作る（生成物なので手で直さない）
- 今あるのは 35 個。分類は `GROUPS` にある（状態 6・操作 8・もの 20・印 1）

### 足す手順

1. `tools/dot_icons.py` の `ICONS` に、0〜1 の座標の図形で書き足す（左上が 0,0、右下が 1,1）
   - 使える図形: `seg`（線分）・`poly`（折れ線。閉じるかを指定）・`ring`（円周）・`arc`（円弧。0 度が右、時計回り）・`disc`（塗った円）・`box`（塗った四角）
   - 外側は 0.08〜0.92 の内に収める（端の粒が欠けないように）
   - 線どうしの間は 0.12 以上空ける（32 格子では 4 マス。詰めると潰れて 1 本に見える）
2. `GROUPS` のどれかに名前を足す（足し忘れると `build.py` が止まる）
3. `python3 tools/build.py` を実行し、`samples/icons.html` を 48px・64px・96px で見て潰れていないかを確かめる
4. 線のアイコンと同じものを描くときは、名前と形の意味を線の側に合わせる（`search` と `magnifying-glass` のように、意味が一目で対応すること）
