"""ドットのアイコンの定義と、32×32 格子の丸ドットへの置き換え。

アイコンは 0〜1 の座標の図形で書く（左上が 0,0）。描くときは各マスの中心が線から
STROKE / 2 以内にあればドットを打つ。図形の種類:
  ("seg", x1, y1, x2, y2)            線分
  ("poly", [(x, y), ...], closed)     折れ線（closed=True で閉じる）
  ("ring", cx, cy, r)                 円周
  ("arc", cx, cy, r, deg0, deg1)      円弧（0 度が右、時計回り）
  ("disc", cx, cy, r)                 塗りつぶした円
  ("box", x1, y1, x2, y2)             塗りつぶした四角
"""
import math

GRID = 32
STROKE = 2.4  # 線の太さ（ドットの数）。32 格子で 2〜3 ドットになる
DOT_R = 0.42  # ドットの半径（マスの幅 = 1）

C = 0.5  # 中心

ICONS = {
    # 状態の印
    "alert": [("poly", [(0.5, 0.12), (0.92, 0.86), (0.08, 0.86)], True), ("seg", 0.5, 0.40, 0.5, 0.62), ("disc", 0.5, 0.74, 0.03)],
    "warning": [("poly", [(0.5, 0.08), (0.92, 0.5), (0.5, 0.92), (0.08, 0.5)], True), ("seg", 0.5, 0.30, 0.5, 0.56), ("disc", 0.5, 0.68, 0.03)],
    "info": [("ring", C, C, 0.40), ("disc", 0.5, 0.31, 0.03), ("seg", 0.5, 0.45, 0.5, 0.72)],
    "success": [("ring", C, C, 0.40), ("poly", [(0.30, 0.52), (0.45, 0.66), (0.72, 0.38)], False)],
    "error": [("ring", C, C, 0.40), ("seg", 0.35, 0.35, 0.65, 0.65), ("seg", 0.65, 0.35, 0.35, 0.65)],
    "question": [("ring", C, C, 0.40), ("arc", 0.5, 0.40, 0.12, 180, 410), ("seg", 0.5, 0.52, 0.5, 0.58), ("disc", 0.5, 0.70, 0.03)],
    # 操作
    "check": [("poly", [(0.16, 0.52), (0.40, 0.76), (0.84, 0.28)], False)],
    "close": [("seg", 0.2, 0.2, 0.8, 0.8), ("seg", 0.8, 0.2, 0.2, 0.8)],
    "plus": [("seg", 0.5, 0.16, 0.5, 0.84), ("seg", 0.16, 0.5, 0.84, 0.5)],
    "search": [("ring", 0.42, 0.42, 0.28), ("seg", 0.63, 0.63, 0.88, 0.88)],
    "refresh": [("arc", C, C, 0.34, 300, 590), ("poly", [(0.62, 0.12), (0.70, 0.22), (0.58, 0.30)], False)],
    "download": [("seg", 0.5, 0.12, 0.5, 0.64), ("poly", [(0.28, 0.44), (0.5, 0.66), (0.72, 0.44)], False), ("seg", 0.14, 0.86, 0.86, 0.86)],
    "upload": [("seg", 0.5, 0.66, 0.5, 0.14), ("poly", [(0.28, 0.36), (0.5, 0.14), (0.72, 0.36)], False), ("seg", 0.14, 0.86, 0.86, 0.86)],
    "power": [("arc", C, 0.54, 0.34, 300, 600), ("seg", 0.5, 0.10, 0.5, 0.48)],
    # もの
    "home": [("poly", [(0.12, 0.48), (0.5, 0.14), (0.88, 0.48)], False), ("poly", [(0.22, 0.40), (0.22, 0.86), (0.78, 0.86), (0.78, 0.40)], False),
             ("poly", [(0.42, 0.86), (0.42, 0.62), (0.58, 0.62), (0.58, 0.86)], False)],
    "file": [("poly", [(0.22, 0.10), (0.60, 0.10), (0.78, 0.28), (0.78, 0.90), (0.22, 0.90)], True), ("poly", [(0.60, 0.10), (0.60, 0.28), (0.78, 0.28)], False)],
    "folder": [("poly", [(0.10, 0.22), (0.40, 0.22), (0.48, 0.32), (0.90, 0.32), (0.90, 0.82), (0.10, 0.82)], True)],
    "inbox": [("poly", [(0.10, 0.54), (0.10, 0.84), (0.90, 0.84), (0.90, 0.54)], False), ("poly", [(0.10, 0.54), (0.34, 0.54), (0.40, 0.64), (0.60, 0.64), (0.66, 0.54), (0.90, 0.54)], False),
              ("poly", [(0.10, 0.54), (0.24, 0.18), (0.76, 0.18), (0.90, 0.54)], False)],
    "image": [("poly", [(0.10, 0.16), (0.90, 0.16), (0.90, 0.84), (0.10, 0.84)], True), ("ring", 0.34, 0.38, 0.07),
              ("poly", [(0.12, 0.76), (0.40, 0.52), (0.58, 0.68), (0.70, 0.58), (0.88, 0.74)], False)],
    "mail": [("poly", [(0.10, 0.22), (0.90, 0.22), (0.90, 0.78), (0.10, 0.78)], True), ("poly", [(0.12, 0.26), (0.5, 0.54), (0.88, 0.26)], False)],
    "user": [("ring", 0.5, 0.34, 0.17), ("arc", 0.5, 0.92, 0.34, 180, 360)],
    "lock": [("poly", [(0.18, 0.44), (0.82, 0.44), (0.82, 0.88), (0.18, 0.88)], True), ("arc", 0.5, 0.40, 0.20, 180, 360),
             ("seg", 0.30, 0.40, 0.30, 0.44), ("seg", 0.70, 0.40, 0.70, 0.44), ("seg", 0.5, 0.60, 0.5, 0.72)],
    "bell": [("arc", 0.5, 0.42, 0.26, 180, 360), ("seg", 0.24, 0.42, 0.24, 0.66), ("seg", 0.76, 0.42, 0.76, 0.66),
             ("seg", 0.12, 0.72, 0.88, 0.72), ("seg", 0.42, 0.86, 0.58, 0.86), ("seg", 0.5, 0.08, 0.5, 0.14)],
    "clock": [("ring", C, C, 0.40), ("seg", 0.5, 0.5, 0.5, 0.24), ("seg", 0.5, 0.5, 0.68, 0.62)],
    "calendar": [("poly", [(0.12, 0.20), (0.88, 0.20), (0.88, 0.88), (0.12, 0.88)], True), ("seg", 0.12, 0.38, 0.88, 0.38),
                 ("seg", 0.32, 0.10, 0.32, 0.26), ("seg", 0.68, 0.10, 0.68, 0.26), ("box", 0.30, 0.54, 0.40, 0.64), ("box", 0.60, 0.54, 0.70, 0.64)],
    "gear": [("ring", C, C, 0.14)] + [("seg", 0.5 + 0.26 * math.cos(a), 0.5 + 0.26 * math.sin(a), 0.5 + 0.40 * math.cos(a), 0.5 + 0.40 * math.sin(a))
                                       for a in [i * math.pi / 4 for i in range(8)]] + [("ring", C, C, 0.27)],
    "star": [("poly", [(0.5 + (0.42 if i % 2 == 0 else 0.18) * math.cos(-math.pi / 2 + i * math.pi / 5),
                        0.53 + (0.42 if i % 2 == 0 else 0.18) * math.sin(-math.pi / 2 + i * math.pi / 5)) for i in range(10)], True)],
    "heart": [("arc", 0.32, 0.36, 0.18, 150, 360), ("arc", 0.68, 0.36, 0.18, 180, 390), ("seg", 0.15, 0.44, 0.5, 0.84), ("seg", 0.85, 0.44, 0.5, 0.84)],
    "wifi": [("arc", 0.5, 0.80, 0.62, 225, 315), ("arc", 0.5, 0.80, 0.40, 225, 315), ("arc", 0.5, 0.80, 0.18, 225, 315), ("disc", 0.5, 0.80, 0.03)],
    "wifi-off": [("arc", 0.5, 0.80, 0.62, 225, 315), ("arc", 0.5, 0.80, 0.40, 225, 315), ("arc", 0.5, 0.80, 0.18, 225, 315), ("disc", 0.5, 0.80, 0.03),
                 ("seg", 0.14, 0.14, 0.86, 0.86)],
    "battery": [("poly", [(0.08, 0.30), (0.82, 0.30), (0.82, 0.70), (0.08, 0.70)], True), ("seg", 0.92, 0.42, 0.92, 0.58),
                ("box", 0.18, 0.40, 0.58, 0.60)],
    "signal": [("seg", 0.20, 0.84, 0.20, 0.66), ("seg", 0.40, 0.84, 0.40, 0.50), ("seg", 0.60, 0.84, 0.60, 0.32), ("seg", 0.80, 0.84, 0.80, 0.14)],
    "terminal": [("poly", [(0.08, 0.16), (0.92, 0.16), (0.92, 0.84), (0.08, 0.84)], True), ("poly", [(0.22, 0.36), (0.38, 0.50), (0.22, 0.64)], False),
                 ("seg", 0.46, 0.66, 0.72, 0.66)],
    "empty": [("poly", [(0.10, 0.10), (0.90, 0.10), (0.90, 0.90), (0.10, 0.90)], True), ("seg", 0.10, 0.90, 0.90, 0.10)],
    # keiso の印（珪素の結晶の格子）
    "keiso": [("poly", [(0.5 + 0.40 * math.cos(math.pi / 6 + i * math.pi / 3), 0.5 + 0.40 * math.sin(math.pi / 6 + i * math.pi / 3)) for i in range(6)], True),
              ("disc", 0.5, 0.5, 0.06)],
}

GROUPS = {
    "状態": ["alert", "warning", "info", "success", "error", "question"],
    "操作": ["check", "close", "plus", "search", "refresh", "download", "upload", "power"],
    "もの": ["home", "file", "folder", "inbox", "image", "mail", "user", "lock", "bell", "clock", "calendar", "gear",
             "star", "heart", "wifi", "wifi-off", "battery", "signal", "terminal", "empty"],
    "印": ["keiso"],
}


def _dist_seg(px, py, x1, y1, x2, y2):
    dx, dy = x2 - x1, y2 - y1
    t = max(0.0, min(1.0, ((px - x1) * dx + (py - y1) * dy) / (dx * dx + dy * dy)))
    return math.hypot(px - (x1 + t * dx), py - (y1 + t * dy))


def _hit(shape, px, py, half):
    kind = shape[0]
    if kind == "seg":
        return _dist_seg(px, py, *shape[1:]) <= half
    if kind == "poly":
        _, pts, closed = shape
        pairs = list(zip(pts, pts[1:])) + ([(pts[-1], pts[0])] if closed else [])
        return any(_dist_seg(px, py, a[0], a[1], b[0], b[1]) <= half for a, b in pairs)
    if kind == "ring":
        _, cx, cy, r = shape
        return abs(math.hypot(px - cx, py - cy) - r) <= half
    if kind == "arc":
        _, cx, cy, r, d0, d1 = shape
        steps = max(8, int(abs(d1 - d0) / 4))
        pts = [(cx + r * math.cos(math.radians(d0 + (d1 - d0) * i / steps)), cy + r * math.sin(math.radians(d0 + (d1 - d0) * i / steps)))
               for i in range(steps + 1)]
        return any(_dist_seg(px, py, a[0], a[1], b[0], b[1]) <= half for a, b in zip(pts, pts[1:]))
    if kind == "disc":
        _, cx, cy, r = shape
        return math.hypot(px - cx, py - cy) <= r + half
    if kind == "box":
        _, x1, y1, x2, y2 = shape
        return x1 - half / 2 <= px <= x2 + half / 2 and y1 - half / 2 <= py <= y2 + half / 2
    raise ValueError(f"知らない図形: {kind}")


def dots(name):
    """アイコンのドットの位置（マスの番号）を返す"""
    half = STROKE / GRID / 2
    shapes = ICONS[name]
    return [(i, j) for j in range(GRID) for i in range(GRID)
            if any(_hit(s, (i + 0.5) / GRID, (j + 0.5) / GRID, half) for s in shapes)]


def svg(name):
    circles = "".join(f'<circle cx="{i + 0.5}" cy="{j + 0.5}" r="{DOT_R}"/>' for i, j in dots(name))
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 {GRID} {GRID}" '
            f'fill="currentColor" aria-hidden="true">{circles}</svg>\n')
