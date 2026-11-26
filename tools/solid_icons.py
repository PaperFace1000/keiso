"""ソリッドのアイコンの定義。tools/build.py が icons/solid/*.svg と見本の埋め込みを作る。

決まり（docs/icons.md）:
  - 24×24 の格子。形は 2〜22 の範囲に収める
  - 円・角丸の四角・三角などの基本の図形を塗り、意味はくり抜き（白抜き）で表す
  - 角は小さく丸める。くり抜きの線の太さは 2〜2.4 にそろえる
  - 1 色（currentColor）。SVG のマスクで、塗り（white）からくり抜き（black）を引く

各アイコンは (塗る図形, くり抜く図形) の SVG 断片の組。
"""
import math

R = 'stroke-linejoin="round"'
CUT = 'fill="none" stroke="black" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"'
CUT_THIN = 'fill="none" stroke="black" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"'
STROKE = 'fill="none" stroke="white" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round"'
DISC = '<circle cx="12" cy="12" r="10" fill="white"/>'


def poly(points, fill="white", width=2.5):
    pts = " ".join(f"{x:.2f},{y:.2f}" for x, y in points)
    return f'<polygon points="{pts}" fill="{fill}" stroke="{fill}" stroke-width="{width}" {R}/>'


def hexagon(r, fill, width=2.5):
    return poly([(12 + r * math.cos(math.radians(-90 + 60 * k)), 12 + r * math.sin(math.radians(-90 + 60 * k))) for k in range(6)], fill, width)


def star():
    pts = []
    for k in range(10):
        r = 10 if k % 2 == 0 else 4.4  # 座標は poly() が小数 2 桁に丸める
        a = math.radians(-90 + 36 * k)
        pts.append((12 + r * math.cos(a), 12.6 + r * math.sin(a)))
    return poly(pts, "white", 2)


GEAR_TEETH = "".join(f'<rect x="10.4" y="1.6" width="3.2" height="5" rx="1" fill="white" transform="rotate({45 * k} 12 12)"/>' for k in range(8))
EXCLAIM_BAR = '<rect x="10.8" y="{y}" width="2.4" height="{h}" rx="1.2" fill="black"/><circle cx="12" cy="{dy}" r="1.3" fill="black"/>'

ICONS = {
    # 状態の印
    "alert": (poly([(12, 3.2), (21.4, 19.8), (2.6, 19.8)]), EXCLAIM_BAR.format(y=8.6, h=6.2, dy=17.1)),
    "warning": (poly([(12, 2.6), (21.4, 12), (12, 21.4), (2.6, 12)]), EXCLAIM_BAR.format(y=6.8, h=6.4, dy=16.1)),
    "info": (DISC, '<circle cx="12" cy="7.4" r="1.4" fill="black"/><rect x="10.8" y="10.2" width="2.4" height="7.4" rx="1.2" fill="black"/>'),
    "success": (DISC, f'<polyline points="7.2,12.4 10.6,15.8 16.9,8.6" {CUT}/>'),
    "error": (DISC, f'<path d="M8.4 8.4 15.6 15.6 M15.6 8.4 8.4 15.6" {CUT}/>'),
    "question": (DISC, f'<path d="M9.3 9.4 A2.8 2.8 0 1 1 13.2 12 C12.4 12.4 12 12.9 12 13.7 V14" {CUT}/><circle cx="12" cy="17.2" r="1.3" fill="black"/>'),
    # 操作
    "check": (f'<polyline points="4.4,12.6 9.6,17.6 19.6,6.6" {STROKE}/>', ""),
    "close": (f'<path d="M5.6 5.6 18.4 18.4 M18.4 5.6 5.6 18.4" {STROKE}/>', ""),
    "plus": (f'<path d="M12 4 V20 M4 12 H20" {STROKE}/>', ""),
    "search": ('<circle cx="10.2" cy="10.2" r="7.8" fill="white"/><path d="M15.6 15.6 20.6 20.6" stroke="white" stroke-width="3.6" stroke-linecap="round"/>',
               '<circle cx="10.2" cy="10.2" r="4" fill="black"/>'),
    "refresh": (DISC, f'<path d="M16.6 13.4 A4.8 4.8 0 1 1 15.4 8.6" {CUT_THIN}/><polygon points="17.6,5.6 17.6,10.4 12.8,10.4" fill="black"/>'),
    "download": (DISC, f'<path d="M12 6.4 V15.2 M8.4 11.8 12 15.4 15.6 11.8" {CUT}/>'),
    "upload": (DISC, f'<path d="M12 17.6 V8.8 M8.4 12.2 12 8.6 15.6 12.2" {CUT}/>'),
    "power": (DISC, f'<path d="M8.6 8.8 A4.9 4.9 0 1 0 15.4 8.8 M12 6.2 V11.6" {CUT_THIN}/>'),
    # もの
    "home": ('<path d="M12 2.8 L21.6 11 V20 A1.8 1.8 0 0 1 19.8 21.8 H4.2 A1.8 1.8 0 0 1 2.4 20 V11 Z" fill="white" stroke="white" stroke-width="1.2" stroke-linejoin="round"/>',
             '<rect x="9.4" y="14" width="5.2" height="9" rx="1.2" fill="black"/>'),
    "file": ('<path d="M6 2 H14.2 L20 7.8 V20 A2 2 0 0 1 18 22 H6 A2 2 0 0 1 4 20 V4 A2 2 0 0 1 6 2 Z" fill="white"/>',
             '<path d="M14.2 2 V7.8 H20" fill="none" stroke="black" stroke-width="1.8"/><rect x="7.4" y="12" width="9.2" height="1.8" rx=".9" fill="black"/><rect x="7.4" y="15.6" width="6" height="1.8" rx=".9" fill="black"/>'),
    "folder": ('<rect x="2" y="3.6" width="9" height="5" rx="1.6" fill="white"/><rect x="2" y="6.6" width="20" height="13.8" rx="2.4" fill="white"/>',
               '<rect x="2" y="8.2" width="20" height="1.8" fill="black"/>'),
    "inbox": ('<rect x="2" y="4" width="20" height="16" rx="2.5" fill="white"/>',
              '<path d="M2 12.6 H7.6 L9.2 15.4 H14.8 L16.4 12.6 H22" fill="none" stroke="black" stroke-width="2" stroke-linejoin="round"/>'),
    "image": ('<rect x="2" y="4" width="20" height="16" rx="2.4" fill="white"/>',
              '<polygon points="5,17.2 9.8,11 13.2,14.6 15.4,12.4 19,17.2" fill="black" stroke="black" stroke-width="1" stroke-linejoin="round"/><circle cx="16" cy="8.6" r="1.8" fill="black"/>'),
    "mail": ('<rect x="2" y="4.6" width="20" height="14.8" rx="2.4" fill="white"/>', f'<polyline points="5,8.4 12,13.4 19,8.4" {CUT_THIN}/>'),
    "user": ('<circle cx="12" cy="7.4" r="4.6" fill="white"/><path d="M3 21.2 A9 8.4 0 0 1 21 21.2 Z" fill="white" stroke="white" stroke-width="1.2" stroke-linejoin="round"/>', ""),
    "lock": ('<path d="M7.4 10.6 V7.6 A4.6 4.6 0 0 1 16.6 7.6 V10.6" fill="none" stroke="white" stroke-width="2.6"/><rect x="3.6" y="10" width="16.8" height="12" rx="2.4" fill="white"/>',
             '<circle cx="12" cy="15" r="1.7" fill="black"/><rect x="11.1" y="15" width="1.8" height="3.6" rx=".9" fill="black"/>'),
    "bell": ('<path d="M12 2.6 C7.9 2.6 5.4 5.7 5.4 9.6 V14.6 L3.4 17.8 H20.6 L18.6 14.6 V9.6 C18.6 5.7 16.1 2.6 12 2.6 Z" fill="white" stroke="white" stroke-width="1" stroke-linejoin="round"/><circle cx="12" cy="20.6" r="2" fill="white"/>', ""),
    "clock": (DISC, f'<polyline points="12,6.6 12,12 15.6,14.2" {CUT}/>'),
    "calendar": ('<rect x="2.4" y="4.2" width="19.2" height="17.4" rx="2.4" fill="white"/><rect x="6.4" y="1.8" width="2.4" height="4.6" rx="1.2" fill="white"/><rect x="15.2" y="1.8" width="2.4" height="4.6" rx="1.2" fill="white"/>',
                 '<rect x="2.4" y="8.6" width="19.2" height="1.8" fill="black"/>' + "".join(
                     f'<rect x="{x}" y="{y}" width="2.8" height="2.8" rx=".6" fill="black"/>' for x, y in ((6, 12.6), (10.6, 12.6), (15.2, 12.6), (6, 16.6), (10.6, 16.6)))),
    "gear": ('<circle cx="12" cy="12" r="7.6" fill="white"/>' + GEAR_TEETH, '<circle cx="12" cy="12" r="3.2" fill="black"/>'),
    "star": (star(), ""),
    "heart": ('<path d="M12 20.6 C6.4 16.6 2.6 13.2 2.6 8.8 A4.8 4.8 0 0 1 12 6.6 A4.8 4.8 0 0 1 21.4 8.8 C21.4 13.2 17.6 16.6 12 20.6 Z" fill="white" stroke="white" stroke-width="1" stroke-linejoin="round"/>', ""),
    "wifi": ('<path d="M12 20.4 L2.2 9.2 A14 14 0 0 1 21.8 9.2 Z" fill="white" stroke="white" stroke-width="1.4" stroke-linejoin="round"/>',
             '<path d="M5.2 12.6 A9.6 9.6 0 0 1 18.8 12.6 M8.2 16 A5.2 5.2 0 0 1 15.8 16" fill="none" stroke="black" stroke-width="1.6"/>'),
    "wifi-off": ('<path d="M12 20.4 L2.2 9.2 A14 14 0 0 1 21.8 9.2 Z" fill="white" stroke="white" stroke-width="1.4" stroke-linejoin="round"/>',
                 '<path d="M5.2 12.6 A9.6 9.6 0 0 1 18.8 12.6 M8.2 16 A5.2 5.2 0 0 1 15.8 16" fill="none" stroke="black" stroke-width="1.6"/>'
                 '<path d="M3.4 3 21 20.6" stroke="black" stroke-width="4.4" stroke-linecap="round"/><path d="M3.4 3 21 20.6" stroke="white" stroke-width="2" stroke-linecap="round"/>'),
    "battery": ('<rect x="2" y="6.6" width="18" height="10.8" rx="2.2" fill="white"/><rect x="20.6" y="9.8" width="1.8" height="4.4" rx=".7" fill="white"/>',
                '<rect x="3.8" y="8.4" width="14.4" height="7.2" rx="1.2" fill="black"/><rect x="5.2" y="9.8" width="8" height="4.4" rx=".6" fill="white"/>'),
    "signal": ("".join(f'<rect x="{x}" y="{y}" width="3.4" height="{round(20.6 - y, 2):g}" rx="1" fill="white"/>' for x, y in ((3, 15.4), (8, 11.4), (13, 7.4), (18, 3.4))), ""),
    "terminal": ('<rect x="2" y="4" width="20" height="16" rx="2.4" fill="white"/>', f'<polyline points="6.2,8.8 9.6,12 6.2,15.2" {CUT_THIN}/><rect x="11.4" y="14.2" width="6.4" height="2" rx="1" fill="black"/>'),
    "empty": (DISC, '<path d="M6.6 17.4 17.4 6.6" stroke="black" stroke-width="2.4" stroke-linecap="round"/>'),
    # keiso の印（珪素の結晶の六角形）
    "keiso": (hexagon(9.4, "white"), hexagon(4.2, "black") + '<circle cx="12" cy="12" r="1.6" fill="white"/>'),
}

GROUPS = {
    "状態": ["alert", "warning", "info", "success", "error", "question"],
    "操作": ["check", "close", "plus", "search", "refresh", "download", "upload", "power"],
    "もの": ["home", "file", "folder", "inbox", "image", "mail", "user", "lock", "bell", "clock", "calendar", "gear",
             "star", "heart", "wifi", "wifi-off", "battery", "signal", "terminal", "empty"],
    "印": ["keiso"],
}


def svg(name: str) -> str:
    fill, cut = ICONS[name]
    mask_id = f"k-solid-{name}"
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" aria-hidden="true">'
            f'<mask id="{mask_id}" maskUnits="userSpaceOnUse" x="0" y="0" width="24" height="24">'
            f'<rect width="24" height="24" fill="black"/>{fill}{cut}</mask>'
            f'<rect width="24" height="24" fill="currentColor" mask="url(#{mask_id})"/></svg>\n')
