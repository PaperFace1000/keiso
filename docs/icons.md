# 🔣 アイコン

アイコンは 2 種類を使い分ける。**画面に絵文字は使わない。** 一覧は `tokens/icons.json`、見本は `samples/icons.html`。

| 種類 | 置き場所 | 大きさ | 使いどころ |
|---|---|---|---|
| 線 | `icons/line/` | 基本 20px、詰めるところは 16px | 普段の操作（ボタン・メニュー・入力欄の中・知らせの欄の印・一覧の行） |
| ソリッド | `icons/solid/` | 基本 24px。16〜64px で使える | 目立たせたいところ（状態の印・知らせの欄・空の表示・ページの見出しの印・ロゴ） |

- 普段の操作は線、意味を目立たせたい印はソリッド、と役割で分ける。同じ画面に両方あってよいが、**1 つの欄の中では 2 種類を混ぜない**（知らせの欄の中ではソリッドだけ、ボタンの中では線だけ）
- 同じものを指すときは、線とソリッドで形の考え方をそろえる（`search` と `magnifying-glass` のように、一目で対応すること）
- どちらも `fill="currentColor"` で、色は親の文字の色を継ぐ。状態の印は親に `.k-role-*` を付けて役割の色にする
- アイコンは飾りとして `aria-hidden="true"` にする。アイコンだけのボタンには `aria-label` を付ける

## 〰️ 線のアイコン（Phosphor Icons の Light）

- Phosphor Icons の **Light**（線の細い太さ）から、よく使う 99 個を選んで `icons/line/` に置いている。名前は Phosphor の名前から `-light` を外したもの（`magnifying-glass.svg`）
- ライセンスは MIT（`docs/licenses.md`）
- 太さは Light にそろえる。Thin・Regular・Bold などを混ぜない

### 足す手順

1. 公式の npm のパッケージ `@phosphor-icons/core` を取得する（`npm pack @phosphor-icons/core`）。まとめサイトやミラーから取らない
2. `npm view @phosphor-icons/core dist.shasum` の値と、取得した `.tgz` の `sha1sum` が一致することを確かめる
3. 展開した `package/assets/light/<名前>-light.svg` を `icons/line/<名前>.svg` として写す（中身は変えない）
4. 版が上がっていたら、`package/LICENSE` と `THIRD_PARTY_LICENSES.md` の写しが同じかを確かめる
5. `python3 tools/build.py` を実行し、`tokens/icons.json` と見本に反映する

## ◆ ソリッドのアイコン（自作）

- 24×24 の格子に描き、形は 2〜22 の範囲に収める
- 円・角丸の四角・三角・ひし形・六角形などの**基本の図形を塗り、意味はくり抜き（白抜き）で表す**。細い線だけで描かない（縮めると線のアイコンと見分けがつかなくなるため）
- 角は UI と同じく小さく丸める（図形の角に 2〜2.5 の丸み）。くり抜きの線の太さは 2〜2.4 にそろえる
- 塗りの形なので 16px まで縮めても潰れない。基本は 24px、知らせの欄の中は 20〜22px、空の表示は 48px、ページの見出しの大きな印は 64〜96px
- 状態の 4 つは、色に頼らず形でも分かるようにする: SUCCESS は円に ✓、INFO は円に i、WARNING はひし形に !、ALERT は三角に !
- 図形の定義は `tools/solid_icons.py`。`tools/build.py` が `icons/solid/<名前>.svg` を作る（生成物なので手で直さない）。SVG はマスクで、塗り（白）からくり抜き（黒）を引いた 1 色の形にしている
- 今あるのは 35 個。分類は `GROUPS` にある（状態 6・操作 8・もの 20・印 1）

### 足す手順

1. `tools/solid_icons.py` の `ICONS` に、`(塗る図形, くり抜く図形)` の組で SVG の断片を書き足す
   - 塗る図形は `fill="white"`、くり抜く図形は `fill="black"` か `stroke="black"` で書く。くり抜きの線は定数 `CUT`（2.4）か `CUT_THIN`（2）を使う
   - 多角形は `poly()` を使うと角が丸まる。円の地は `DISC`
   - くり抜きどうし、くり抜きと外側の間は 1.6 以上空ける（16px で潰れないように）
2. `GROUPS` のどれかに名前を足す（足し忘れると `build.py` が止まる）
3. `python3 tools/build.py` を実行し、`samples/icons.html` を 16px・24px・48px で見て潰れていないかを確かめる
4. 線のアイコンと同じものを描くときは、名前と形の意味を線の側に合わせる
