"""keiso の生成物を作り直し、色の決まりを確かめる。標準ライブラリだけで動く。

使い方: python3 tools/build.py

  tokens/palette.json      → tokens/themes.css（正本は palette.json。CSS は手で直さない）
  tokens/extra-colors.json → tokens/extra-colors.css
  tools/solid_icons.py     → icons/solid/*.svg
  tokens/icons.json        （ドットと線のアイコンの一覧。線のアイコンは icons/line/ にある分を並べる）

文字として使う色の組み合わせが、どれか 1 つでもコントラスト比 4.5 未満なら、何も書かずに exit 1 で止まる。
"""
from __future__ import annotations

import base64
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import solid_icons  # noqa: E402

DEFAULT_LIGHT = "shiro"
DEFAULT_DARK = "kuro"
MIN_RATIO = 4.5

# 文字として重ねる組み合わせ（文字の色, 背景の色）
TEXT_PAIRS = [("text", "base"), ("text", "surface"), ("text", "sunken"), ("muted", "base"), ("muted", "surface"),
              ("accent-strong", "base"), ("accent-strong", "surface"), ("on-accent-strong", "accent-strong"),
              ("on-alert", "alert"), ("selection-text", "selection-bg")]
for _role in ("success", "info", "warning", "alert"):
    TEXT_PAIRS += [(_role, "base"), (_role, "surface"), (_role, f"{_role}-bg")]


def luminance(hex_color: str) -> float:
    h = hex_color.lstrip("#")
    def channel(v: float) -> float:
        return v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = (channel(int(h[i:i + 2], 16) / 255) for i in (0, 2, 4))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a: str, b: str) -> float:
    la, lb = sorted((luminance(a), luminance(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def check(palette: list[dict], extra: list[dict]) -> list[str]:
    errors = []
    for theme in palette:
        c = theme["colors"]
        for fg, bg in TEXT_PAIRS:
            r = contrast(c[fg], c[bg])
            if r < MIN_RATIO:
                errors.append(f"{theme['key']}: {fg} / {bg} = {r:.2f}")
        code = theme["code"]
        for k, v in code.items():
            if k.startswith("token-") and contrast(v, code["background"]) < MIN_RATIO:
                errors.append(f"{theme['key']}: code.{k} / background = {contrast(v, code['background']):.2f}")
    bases = {t["key"]: t["colors"] for t in palette}
    for group in extra:
        c = bases[group["theme"]]
        for item in group["colors"]:
            for bg_name, bg in (("surface", c["surface"]), ("bg", item["bg"])):
                r = contrast(item["text"], bg)
                if r < MIN_RATIO:
                    errors.append(f"{group['theme']}: extra.{item['key']} / {bg_name} = {r:.2f}")
    return errors


def theme_block(theme: dict) -> str:
    lines = [f"  color-scheme: {theme['colorScheme']};"]
    lines += [f"  --color-{k}: {v};" for k, v in theme["colors"].items()]
    lines.append("  /* コードの色分け（Shiki の CSS 変数テーマ）。文字の色はすべて背景の上で 4.5 以上 */")
    lines += [f"  --shiki-{k}: {v};" for k, v in theme["code"].items()]
    return "\n".join(lines)


def themes_css(palette: list[dict]) -> str:
    by_key = {t["key"]: t for t in palette}
    out = ["/* keiso のテーマ。tools/build.py が tokens/palette.json から作る。手で直さず palette.json を直して作り直すこと。",
           "   画面では必ずこの変数を使い、色を直接書かないこと。data-theme は <html> にも、見本のカードのような要素にも付けられる */", ""]
    out += [f"/* {by_key[DEFAULT_LIGHT]['label']}（既定）。data-theme が無ければ OS のライト・ダークに従う */",
            f':root,\n[data-theme="{DEFAULT_LIGHT}"] {{\n{theme_block(by_key[DEFAULT_LIGHT])}\n}}', ""]
    out += [f"/* data-theme が無く、OS がダークなら{by_key[DEFAULT_DARK]['label']} */",
            f"@media (prefers-color-scheme: dark) {{\n  :root:not([data-theme]) {{\n"
            + "\n".join("  " + line for line in theme_block(by_key[DEFAULT_DARK]).splitlines()) + "\n  }\n}", ""]
    for t in palette:
        if t["key"] == DEFAULT_LIGHT:
            continue
        out += [f"/* {t['label']}: {t['note']} */", f'[data-theme="{t["key"]}"] {{\n{theme_block(t)}\n}}', ""]
    return "\n".join(out)


def extra_css(extra: list[dict]) -> str:
    """テーマの要素に色ごとの値（--extra-<色>-text など）を置き、data-extra-color の要素がそれを読む。
    値は継承で一番近いテーマの要素から来るので、data-theme を入れ子にしても内側のテーマの色になる"""
    out = ["/* 分類やタグを見分ける色。tools/build.py が tokens/extra-colors.json から作る。",
           '   要素に data-extra-color="blue" を付け、var(--extra-text) / var(--extra-bg) / var(--extra-border) で塗る。',
           "   値はテーマの要素に色ごとに置いてあり、一番近い data-theme の値になる（テーマを入れ子にしてもよい） */", ""]
    for group in extra:
        theme = group["theme"]
        scopes = [f'[data-theme="{theme}"]']
        if theme == DEFAULT_LIGHT:
            scopes = [":root:not([data-theme])", *scopes]
        body = "\n".join(f"  --extra-{item['key']}-{part}: {item[part]};" for item in group["colors"] for part in ("text", "bg", "border"))
        out.append(f"{', '.join(scopes)} {{\n{body}\n}}")
        if theme == DEFAULT_DARK:
            out.append("@media (prefers-color-scheme: dark) {\n  :root:not([data-theme]) {\n"
                       + "\n".join("  " + line for line in body.splitlines()) + "\n  }\n}")
        out.append("")
    keys = [item["key"] for item in extra[0]["colors"]]
    for key in keys:
        out.append(f'[data-extra-color="{key}"] {{ --extra-text: var(--extra-{key}-text); --extra-bg: var(--extra-{key}-bg); --extra-border: var(--extra-{key}-border); }}')
    out.append("")
    return "\n".join(out)


def build_icons() -> dict:
    solid_dir = ROOT / "icons" / "solid"
    solid_dir.mkdir(parents=True, exist_ok=True)
    for old in solid_dir.glob("*.svg"):
        old.unlink()
    for name in solid_icons.ICONS:
        (solid_dir / f"{name}.svg").write_text(solid_icons.svg(name), encoding="utf-8")
    line_dir = ROOT / "icons" / "line"
    line_names = sorted(p.stem for p in line_dir.glob("*.svg")) if line_dir.exists() else []
    return {
        "solid": {"grid": 24, "baseSize": 24, "sizes": [16, 20, 24, 32, 48, 64], "groups": solid_icons.GROUPS},
        "line": {"source": "Phosphor Icons (Light)", "license": "MIT", "baseSize": 20, "names": line_names},
    }


def build_sample_assets() -> None:
    """見本はファイルを直接開いても動くよう、フォントとアイコンを JS / CSS に埋め込んで置く"""
    assets = ROOT / "samples" / "assets"
    assets.mkdir(parents=True, exist_ok=True)
    font = base64.b64encode((ROOT / "fonts" / "doto-latin.woff2").read_bytes()).decode()
    (assets / "fonts.css").write_text(
        "/* tools/build.py が fonts/doto-latin.woff2 を埋め込んで作る。Doto は SIL Open Font License 1.1（fonts/Doto-OFL.txt） */\n"
        "@font-face {\n  font-family: \"Doto\";\n  font-style: normal;\n  font-weight: 100 900;\n  font-display: swap;\n"
        f"  src: url(data:font/woff2;base64,{font}) format(\"woff2\");\n}}\n", encoding="utf-8")
    icons = {"solid": {n: solid_icons.svg(n).strip() for n in solid_icons.ICONS},
             "line": {p.stem: re.sub(r"\s+", " ", p.read_text(encoding="utf-8")).strip()
                      for p in sorted((ROOT / "icons" / "line").glob("*.svg"))}}
    (assets / "icons.js").write_text(
        "// tools/build.py が icons/ から作る。線は Phosphor Icons（MIT）、ソリッドは keiso の自作\n"
        f"window.KEISO_ICONS = {json.dumps(icons, ensure_ascii=False)};\n", encoding="utf-8")


def main() -> int:
    tokens = ROOT / "tokens"
    palette = json.loads((tokens / "palette.json").read_text(encoding="utf-8"))
    extra = json.loads((tokens / "extra-colors.json").read_text(encoding="utf-8"))
    missing = [n for names in solid_icons.GROUPS.values() for n in names if n not in solid_icons.ICONS]
    errors = check(palette, extra) + [f"solid_icons.GROUPS に定義の無いアイコン: {n}" for n in missing]
    if errors:
        sys.stderr.write("決まりに合わないものがあるため、何も書かずに止めた:\n  " + "\n  ".join(errors) + "\n")
        return 1
    (tokens / "themes.css").write_text(themes_css(palette), encoding="utf-8")
    (tokens / "extra-colors.css").write_text(extra_css(extra), encoding="utf-8")
    (tokens / "icons.json").write_text(json.dumps(build_icons(), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    build_sample_assets()
    print(f"ok: テーマ {len(palette)}、分類の色 {len(extra[0]['colors'])}、ソリッドのアイコン {len(solid_icons.ICONS)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
