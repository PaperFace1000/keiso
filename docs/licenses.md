# ⚖️ フォント・アイコンのライセンス

keiso とアプリで使うフォント・アイコンは、どれも配布元のライセンスに従って使う。一覧と許諾文の控えは、リポジトリ直下の `THIRD_PARTY_LICENSES.md`。

> **ライセンスは配布元が変えることがある。最新の条件は、必ず配布元の公式のページで確かめること。**
> keiso の文書や `THIRD_PARTY_LICENSES.md` に書いた内容は、書いた時点の控え。食い違うときは公式のページが正。

## 📌 使っている素材

| 素材 | 用途 | ライセンス | 入手元 | 置き場所 |
|---|---|---|---|---|
| Phosphor Icons（Light） | 線のアイコン | MIT | npm の `@phosphor-icons/core`（2.1.1） | `icons/line/` |
| Doto | ドットの数字 | SIL Open Font License 1.1 | GitHub の `google/fonts` の `ofl/doto` | `fonts/doto-latin.woff2` |
| OS のゴシック体・等幅フォント | 本文・ラベル・コード | OS の使用許諾 | — | 配らない（名前で指すだけ） |

ソリッドのアイコン（`icons/solid/`）は keiso の自作で、第三者の素材を含まない。

## 🧷 Phosphor Icons（MIT）

- 著作権表示: `Copyright (c) 2023 Phosphor Icons`
- 使ってよい・変えてよい・配ってよい（商用も可）。**配るときは著作権表示と許諾文を添える**
- アプリでは、使っている版のパッケージに入っている `LICENSE` から写して、第三者のライセンスの一覧に入れる
- SVG を HTML に直接書き写すときも、同じ版の許諾文を一覧に入れる
- 形を変えて使うときも、MIT の条件はそのまま残る
- 取得は公式の npm からだけ行い、`npm view @phosphor-icons/core dist.shasum` と取得した `.tgz` の `sha1sum` を照合する
- アイコンを足すたびに、取得した版の `package/LICENSE` と `THIRD_PARTY_LICENSES.md` の写しを比べる。最後に確かめた日と版は `THIRD_PARTY_LICENSES.md` に書く

## 🖋️ Doto（OFL 1.1）

- 著作権表示: `Copyright 2024 The Doto Project Authors`（全文は `fonts/Doto-OFL.txt`）
- フォントのファイルを単体で販売しない（アプリに同梱して配るのはよい）
- 改変したフォント（文字を絞ったものも含む）も OFL のまま配る。`fonts/doto-latin.woff2` は文字を英数字と記号だけに絞った改変版
- 同梱するときは著作権表示と OFL の全文を添える（`fonts/Doto-OFL.txt` を一緒に置く）
- 作者の名前を許可なく宣伝に使わない
- 輪郭に変えたロゴの SVG や画像には、これらの義務はかからない

### Doto を更新する

1. GitHub の `google/fonts` の `ofl/doto/` から `Doto[ROND,wght].ttf` と `OFL.txt` を取得する
2. `gh api repos/google/fonts/contents/ofl/doto` で出る `sha` と、取得したファイルの `git hash-object` が一致することを確かめる
3. fonttools の `pyftsubset` で文字を絞り、woff2 にする（作業用の仮想環境で行い、リポジトリには入れない）

```sh
pyftsubset 'Doto[ROND,wght].ttf' \
  --unicodes='U+0020-007E,U+00A0-00FF,U+2013-2014,U+2018-201D,U+2022,U+2026,U+2190-2193,U+00D7,U+00B0' \
  --layout-features='*' --flavor=woff2 --output-file=doto-latin.woff2
```

4. `fonts/doto-latin.woff2` と `fonts/Doto-OFL.txt` を置き換え、`python3 tools/build.py` を実行する
5. `OFL.txt` が変わっていたら `THIRD_PARTY_LICENSES.md` も直す

## 🖥️ OS のフォント

- OS に付属のフォント（ヒラギノ・游ゴシック・SF など）のファイルを、アプリやリポジトリに入れて配らない
- ロゴの画像を作るときに、OS のフォントを輪郭に変えて使わない（`docs/logo.md`）
