#!/usr/bin/env python3
"""Generate original, offline-ready SVG learning diagrams for this repository.

Usage: python3 scripts/diagram_generator.py
       python3 scripts/diagram_generator.py --check

No third-party packages. Diagrams are teaching schematics, not Packet Tracer screenshots;
IP addresses and device names are matched to the corresponding Markdown examples.
Every SVG has an accessible title and description and uses no external resources.
"""

from __future__ import annotations

import argparse
import html
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "diagrams"

NAVY = "#142B46"
INK = "#1C344D"
MUTED = "#556B82"
TEAL = "#087F6C"
BLUE = "#2467B2"
VIOLET = "#7452AD"
AMBER = "#AF6B0A"
RED = "#BF4A52"
PALE = {TEAL: "#E5F5EF", BLUE: "#E7F0FA", VIOLET: "#F0EBFA", AMBER: "#FFF4DC", RED: "#FCECEE", NAVY: "#EAF0F6"}
COLORS = [TEAL, BLUE, VIOLET, AMBER, RED, NAVY]


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


class Art:
    """Small layered SVG drawing API. Link strokes sit below opaque device cards."""

    def __init__(self, title: str, subtitle: str, category: str, note: str, height: int = 690):
        self.title, self.subtitle, self.category, self.note, self.h = title, subtitle, category, note, height
        self.layers: dict[str, list[str]] = {key: [] for key in ("zones", "links", "nodes", "labels", "front")}
        self.devices: dict[str, tuple[float, float, float, float]] = {}

    def put(self, layer: str, value: str) -> None:
        self.layers[layer].append(value)

    def rect(self, x: float, y: float, w: float, h: float, fill: str = "white", stroke: str = "none",
             rx: float = 14, sw: float = 1.5, layer: str = "zones") -> None:
        self.put(layer, f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" '
                        f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')

    def line(self, x1: float, y1: float, x2: float, y2: float, color: str = TEAL, width: float = 3,
             dashed: str = "", arrow: bool = False, layer: str = "links") -> None:
        dash = f' stroke-dasharray="{dashed}"' if dashed else ""
        mark = f' marker-end="url(#{self._marker(color)})"' if arrow else ""
        self.put(layer, f'<path d="M{x1:.1f} {y1:.1f} L{x2:.1f} {y2:.1f}" fill="none" '
                        f'stroke="{color}" stroke-width="{width}" stroke-linecap="round"{dash}{mark}/>')

    @staticmethod
    def _marker(color: str) -> str:
        return {TEAL: "arrow-teal", BLUE: "arrow-blue", VIOLET: "arrow-violet",
                RED: "arrow-red", AMBER: "arrow-amber"}.get(color, "arrow-navy")

    def circle(self, x: float, y: float, r: float, fill: str, stroke: str = "none", sw: float = 1,
               layer: str = "nodes") -> None:
        self.put(layer, f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')

    def text(self, x: float, y: float, s: str, size: float = 18, color: str = INK, weight: int = 500,
             anchor: str = "start", layer: str = "labels", max_width: float = 0, mono: bool = False) -> None:
        # Intentionally favor native SVG text: crisp, searchable, accessible and GitHub compatible.
        if max_width and len(s) * size * 0.56 > max_width:
            size = max(12, round(max_width / (0.56 * max(len(s), 1)), 1))
        font = "Consolas, DejaVu Sans Mono, monospace" if mono else "DejaVu Sans, Arial, sans-serif"
        self.put(layer, f'<text x="{x}" y="{y}" text-anchor="{anchor}" '
                        f'font-family="{font}" font-size="{size}" fill="{color}" font-weight="{weight}">{esc(s)}</text>')

    def pill(self, x: float, y: float, s: str, color: str = BLUE, layer: str = "front", width: float = 0) -> None:
        w = width or min(310, max(68, 22 + 8.4 * len(s)))
        self.rect(x - w / 2, y - 17, w, 30, PALE.get(color, PALE[NAVY]), "none", 15, layer=layer)
        self.text(x, y + 4, s, 13.5, color, 700, "middle", layer, max_width=w - 14)

    def zone(self, x: float, y: float, w: float, h: float, title: str, color: str = BLUE) -> None:
        self.rect(x, y, w, h, PALE.get(color, PALE[BLUE]), color + "55", 22, layer="zones")
        self.text(x + 22, y + 32, title, 17, color, 750, layer="labels", max_width=w - 44)

    def _icon(self, kind: str, cx: float, cy: float, color: str) -> None:
        # Original, simplified pictograms. No Cisco trademarks or external icon fonts.
        self.circle(cx, cy, 24, color, layer="nodes")
        def path(d: str, width: float = 2.6, fill: str = "none") -> None:
            self.put("nodes", f'<path d="{d}" stroke="white" stroke-width="{width}" fill="{fill}" '
                              'stroke-linecap="round" stroke-linejoin="round"/>')
        x, y = cx, cy
        if kind in ("pc", "laptop"):
            path(f'M{x-13} {y-10} h26 v18 h-26 z')
            path(f'M{x-7} {y+13} h14 M{x} {y+8} v5')
            if kind == "laptop": path(f'M{x-18} {y+13} h36')
        elif kind in ("router", "cloud"):
            path(f'M{x-13} {y-4} h26 M{x-13} {y+5} h26 M{x+8} {y-8} l5 4 -5 4 M{x-8} {y+1} l-5 4 5 4')
        elif kind in ("switch", "wlc"):
            path(f'M{x-17} {y-8} h34 v17 h-34 z')
            for xx in (-11, -2, 7): path(f'M{x+xx} {y-1} h4 v4 h-4 z', 1.5)
            path(f'M{x+15} {y-1} v4', 2.2)
        elif kind == "server":
            path(f'M{x-12} {y-15} h24 v29 h-24 z M{x-7} {y-6} h12 M{x-7} {y+2} h12')
            self.circle(x + 7, y + 9, 1.6, "white")
        elif kind in ("wifi", "ap"):
            path(f'M{x-15} {y-2} Q{x} {y-17} {x+15} {y-2} M{x-10} {y+2} Q{x} {y-8} {x+10} {y+2} '
                 f'M{x-4} {y+7} Q{x} {y+3} {x+4} {y+7}')
            self.circle(x, y + 12, 2.3, "white")
        elif kind == "phone":  # handheld smartphone (used by the Wi-Fi lesson)
            path(f'M{x-8} {y-14} h16 v28 h-16 z M{x-3} {y+10} h6')
        elif kind == "ipphone":  # original outline of a desk IP phone with handset and keypad
            path(f'M{x-15} {y-9} h30 v24 h-30 z M{x-11} {y-4} h11 v11 h-11 z')
            path(f'M{x-15} {y-14} Q{x} {y-19} {x+15} {y-14} M{x-15} {y-14} v3 M{x+15} {y-14} v3')
            for xx in (5, 10):
                for yy in (-2, 3, 8):
                    self.circle(x+xx,y+yy,1.25,"white")
        elif kind == "printer":
            path(f'M{x-12} {y-14} h24 v9 h-24 z M{x-16} {y-4} h32 v15 h-32 z M{x-10} {y+4} h20 v11 h-20 z')
        elif kind == "shield":
            path(f'M{x} {y-16} l13 5 v10 q0 10 -13 17 q-13 -7 -13 -17 v-10 z M{x-6} {y} l4 4 8 -9')
        elif kind == "file":
            path(f'M{x-11} {y-15} h17 l6 6 v24 h-23 z M{x+6} {y-15} v7 h6 M{x-5} {y+1} h11 M{x-5} {y+7} h11')
        elif kind == "gear":
            self.circle(x, y, 10, "none", "white", 2.5)
            self.circle(x, y, 3, "white")
            for deg in range(0, 360, 45):
                r = math.radians(deg)
                path(f'M{x+11*math.cos(r):.1f} {y+11*math.sin(r):.1f} L{x+16*math.cos(r):.1f} {y+16*math.sin(r):.1f}', 2.5)
        else:  # simple checkmark / generic task
            path(f'M{x-12} {y+1} l8 8 17 -19')

    def node(self, key: str, x: float, y: float, kind: str, name: str, detail: str,
             color: str = BLUE, w: int = 166, h: int = 126) -> None:
        self.devices[key] = (x, y, w, h)
        self.rect(x-w/2, y-h/2, w, h, "#FFFFFF", "#C9D8E5", 17, layer="nodes")
        self.rect(x-w/2, y-h/2, w, 6, color, "none", 4, layer="nodes")
        self._icon(kind, x, y-27, color)
        self.text(x, y+15, name, 18, INK, 750, "middle", "nodes", w-18)
        self.text(x, y+41, detail, 14.5, MUTED, 550, "middle", "nodes", w-18)

    def edge(self, start: str, end: str, style: str = "wired", label: str = "", offset: int = -22,
             arrow: bool = False, status: str = "") -> None:
        a = self.devices[start]; b = self.devices[end]
        x1,y1,w1,h1 = a; x2,y2,w2,h2 = b
        dx,dy = x2-x1,y2-y1
        def border(w: float,h: float) -> float:
            return min(w/(2*abs(dx)) if dx else float("inf"), h/(2*abs(dy)) if dy else float("inf"))
        t1,t2 = border(w1,h1),border(w2,h2)
        sx,sy = x1+dx*t1,y1+dy*t1
        ex,ey = x2-dx*t2,y2-dy*t2
        color = {"wired": TEAL, "trunk": VIOLET, "wireless": BLUE, "fault": RED, "blocked": AMBER,
                 "wan": BLUE, "capwap": VIOLET}.get(style,TEAL)
        dash = {"trunk":"10 6", "wireless":"4 10", "fault":"7 7", "blocked":"8 7", "wan":"10 6", "capwap":"4 6"}.get(style, "")
        self.line(sx,sy,ex,ey,color,4 if style=="trunk" else 3,dash,arrow)
        self.circle(sx,sy,5.3,AMBER if status=="amber" else color,layer="front")
        self.circle(ex,ey,5.3,AMBER if status=="amber" else color,layer="front")
        if label:
            self.pill((sx+ex)/2, (sy+ey)/2 + offset, label, color)

    def callout(self, x: int, y: int, w: int, h: int, title: str, lines: list[str], color: str = BLUE) -> None:
        self.rect(x, y, w, h, PALE.get(color,PALE[BLUE]), color+"55", 15, layer="nodes")
        self.rect(x, y, 6, h, color, "none", 2, layer="nodes")
        self.text(x+20,y+30,title,18,color,750,layer="front",max_width=w-40)
        for i,line in enumerate(lines):
            self.text(x+20,y+58+i*23,line,15.5,INK,500,layer="front",max_width=w-40)

    def render(self) -> str:
        h=self.h
        defs = '''<defs><pattern id="dots" width="28" height="28" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1" fill="#DFE7EE"/></pattern>'''
        for name, color in (("teal",TEAL),("blue",BLUE),("violet",VIOLET),("amber",AMBER),("red",RED),("navy",NAVY)):
            defs += f'<marker id="arrow-{name}" markerWidth="10" markerHeight="10" refX="9" refY="5" orient="auto" markerUnits="strokeWidth"><path d="M0 1 L9 5 L0 9 Z" fill="{color}"/></marker>'
        defs += '</defs>'
        head = (f'<rect width="1120" height="{h}" fill="#F8FAFD"/><rect x="0" y="103" width="1120" height="{h-171}" fill="url(#dots)"/>'
                f'<rect x="0" y="0" width="1120" height="103" fill="{NAVY}"/>'
                f'<rect x="0" y="100" width="1120" height="4" fill="{TEAL}"/>')
        # Header and footer stay readable when images are embedded at narrow widths.
        self.text(40,46,self.title,29,"#FFFFFF",750,layer="front",max_width=840)
        self.text(41,76,self.subtitle,16,"#D4E3EF",450,layer="front",max_width=870)
        self.rect(904,29,175,42,"#214563","none",21,layer="front")
        self.text(991,56,self.category.upper(),13.3,"#FFFFFF",700,"middle","front",max_width=154)
        self.rect(0,h-68,1120,68,"#EAF0F6","none",0,layer="front")
        self.rect(40,h-51,4,32,TEAL,"none",2,layer="front")
        self.text(57,h-29,self.note,15,INK,540,layer="front",max_width=1010)
        return (f'<svg xmlns="http://www.w3.org/2000/svg" width="1120" height="{h}" viewBox="0 0 1120 {h}" '
                f'role="img" aria-label="{esc(self.title)}"><title>{esc(self.title)}</title>'
                f'<desc>{esc(self.subtitle)}. {esc(self.note)}</desc>{defs}{head}'
                + ''.join(''.join(self.layers[k]) for k in ("zones","links","nodes","labels","front")) + '</svg>\n')


DIAGRAMS: dict[str, Art] = {}


def save(name: str, art: Art) -> None:
    if name in DIAGRAMS:
        raise ValueError(f"duplicate diagram: {name}")
    DIAGRAMS[name] = art


def overview(name: str, title: str, subtitle: str, note: str,
             items: list[tuple[str,str,str,str,str,str]], category: str = "learning map") -> None:
    """Six/three/four/nine distinct concept cards, each with a meaningful takeaway."""
    n=len(items)
    if n==3: cols, card_h, height, ys = 3,245,635,[207]
    elif n==4: cols,card_h,height,ys=2,183,690,[151,358]
    elif n in (8,9): cols,card_h,height,ys=3,167,795,[145,328,511]
    else: cols,card_h,height,ys=3,176,690,[150,350]
    a=Art(title,subtitle,category,note,height)
    w={2:490,3:318}[cols]
    xs=([50,580] if cols==2 else [45,401,757])
    for i,(tag,heading,line1,line2,color,kind) in enumerate(items):
        x,y=(223+(i-6)*356,ys[2]) if n==8 and i>=6 else (xs[i%cols],ys[i//cols])
        a.rect(x,y,w,card_h,"#FFFFFF","#D6E2EC",17,layer="nodes")
        a.rect(x,y,7,card_h,color,"none",3,layer="nodes")
        a._icon(kind,x+45,y+42,color)
        a.text(x+84,y+34,tag,13,color,750,layer="front",max_width=w-100)
        a.text(x+84,y+61,heading,20,INK,750,layer="front",max_width=w-103)
        a.text(x+23,y+100,line1,16,MUTED,500,layer="front",max_width=w-46)
        a.text(x+23,y+127,line2,15,MUTED,500,layer="front",max_width=w-46)
    save(name,a)


def flow(name: str, title: str, subtitle: str, note: str,
         steps: list[tuple[str,str,str,str]], category: str = "workflow") -> None:
    a=Art(title,subtitle,category,note,620)
    count=len(steps)
    w=242 if count==4 else 190
    gap=24 if count==4 else 24
    total=w*count+gap*(count-1)
    left=(1120-total)/2
    y=200; h=239
    for i,(heading,line1,line2,color) in enumerate(steps):
        x=left+i*(w+gap)
        a.rect(x,y,w,h,"#FFFFFF","#D6E2EC",19,layer="nodes")
        a.rect(x,y,w,7,color,"none",3,layer="nodes")
        a.circle(x+37,y+42,21,color,layer="nodes")
        a.text(x+37,y+49,str(i+1),20,"white",750,"middle","front")
        a.text(x+21,y+105,heading,19,INK,750,layer="front",max_width=w-38)
        a.text(x+21,y+149,line1,15.5,MUTED,500,layer="front",max_width=w-38)
        a.text(x+21,y+180,line2,15.5,MUTED,500,layer="front",max_width=w-38)
        if i<count-1:
            a.line(x+w+3,y+121,x+w+gap-6,y+121,color,3,arrow=True)
    save(name,a)


def topo(name: str,title: str,subtitle: str,note: str,nodes: list[tuple],edges: list[tuple],
         zones: list[tuple] = (), callouts: list[tuple] = (), pills: list[tuple] = (),
         height: int = 690, category: str = "packet tracer topology") -> None:
    a=Art(title,subtitle,category,note,height)
    for z in zones:a.zone(*z)
    for n in nodes:a.node(*n)
    for e in edges:a.edge(*e)
    for c in callouts:a.callout(*c)
    for p in pills:a.pill(*p)
    save(name,a)

# ── Root navigation: each map has different learning content, not a stock banner. ──
overview("repo-overview", "Cisco Packet Tracer Lab | visual guide", "Choose a learning track, then build, test and explain the packet path.",
         "Start with a diagram; open its linked lesson for commands, IP tables and Packet Tracer files.", [
    ("START HERE", "Practical track", "18 guided labs: CLI to IPv6", "Build a topology in Packet Tracer", TEAL,"router"),
    ("UNDERSTAND WHY", "CCNA fundamentals", "9 theory chapters + quizzes", "OSI, IP, VLAN, ACL and NAT", BLUE,"file"),
    ("TRY MORE", "Extra labs", "8 service + security labs", "FTP, VoIP, DHCP and DAI", VIOLET,"server"),
    ("OPEN A LAB", "Packet Tracer files", "18 existing .pkt to inspect", "Later labs are build-alongs", AMBER,"switch"),
    ("LOOK IT UP", "Reference library", "CLI sheet + 2 illustrated books", "Search a command or packet flow", BLUE,"file"),
    ("CHECK YOUR WORK", "Python helper scripts", "Subnet, config, quiz and audit", "Rebuild diagrams without packages", TEAL,"gear")],"repository map")

overview("roadmap-30-day", "30-day learning path", "Six stages from your first network to a working capstone.",
         "The roadmap has daily tasks and a 7-day exam-week shortcut; the stages here are a visual summary.", [
    ("DAYS 01-05", "Network + first CLI", "LAN, OSI and Router modes", "Finish: first successful ping", TEAL,"pc"),
    ("DAYS 06-12", "IP + static routes", "IPv4, subnetting and /30 WAN", "Finish: two LANs communicate", BLUE,"router"),
    ("DAYS 13-18", "Network services", "DHCP, DNS, web, FTP, email", "Finish: test each server", VIOLET,"server"),
    ("DAYS 19-23", "VLAN + switching", "Trunk, ROAS, STP and LACP", "Finish: inter-VLAN access", AMBER,"switch"),
    ("DAYS 24-27", "Enterprise features", "OSPF, Wi-Fi, SSH, NTP, Syslog", "Finish: secure and observe", BLUE,"shield"),
    ("DAYS 28-30", "Capstone + review", "Build an office or campus LAN", "Finish: verify, explain, repair", TEAL,"gear")],"30-day plan")

flow("contributing-workflow", "How a contribution reaches the repository", "From a new lab idea to a verified, visual pull request.",
     "All new Markdown guides should include a relevant local image and work without external assets.", [
    ("Fork + branch", "Clone the repository", "Start a feat/ branch", BLUE),
    ("Write + illustrate", "Add a .md lab guide", "Embed SVG; .pkt if built", VIOLET),
    ("Audit", "Run repo_doctor.py", "Fix broken links/images", AMBER),
    ("Open a PR", "Explain the lab result", "Include verification", TEAL)])

overview("rename-map", "Where the old files went", "Use this map when an old bookmark or Packet Tracer filename stops working.",
         "The table below this diagram gives the exact old-to-new filename for every affected file.", [
    ("BEFORE", "Mixed lesson files", "'Basic Network Lab #1.2.md'", "Several duplicate root documents", AMBER,"file"),
    ("NOW", "lessons/01...18.md", "One merged guide per topic", "Concept → lab → verify", TEAL,"file"),
    ("BEFORE", "Space-heavy .pkt names", "'Mash_topology.pkt' typo", "Hard to link and navigate", RED,"switch"),
    ("NOW", "pkt-files/ folders", "labs/ · practice/ · topologies/", "'mesh-topology.pkt'", BLUE,"switch")],"migration map")

overview("practical-course-map", "18 practical lessons | build in order", "The visuals show the topology first; the Markdown explains every configuration step.",
         "Lessons 01–08 have downloadable .pkt examples; later lessons include build-along guides and practice.", [
    ("01-04", "First connections", "CLI → static routing → DHCP", "Then name-to-IP DNS and HTTP", TEAL,"router"),
    ("05-08", "Switch + integrate", "VLAN → trunk → STP/LACP", "Finish the office capstone", BLUE,"switch"),
    ("09", "See real hardware", "Router, switch, cables, SFP", "Photos beside PT equivalents", AMBER,"gear"),
    ("10-12", "Practice + repair", "10 guided, 20 self-test tasks", "9 real troubleshooting cases", VIOLET,"shield"),
    ("13-14", "Routing + wireless", "RIPv2/OSPF and home Wi-Fi", "WLC + LAP enterprise LAN", BLUE,"wifi"),
    ("15-18", "Enterprise + IPv6", "SSH, SVI, HSRP and SLAAC", "Static routes and OSPFv3", TEAL,"router")],"practical track")

# ── First fifteen practical lessons: roles and addresses follow lesson tables. ──
topo("lesson-01-first-ping","Lesson 01 | first LAN and ping","PC0 and PC1 share 192.168.1.0/24; their ICMP echo stays on the switch.",
     "PC0 → SW1 → PC1 is a local ping. R1 at .1 is their gateway for other networks.",[
    ("r",560,210,"router","R1 / 1941","G0/0: 192.168.1.1",BLUE),
    ("sw",560,358,"switch","SW1 / 2960","G0/1 to R1",TEAL),
    ("pc0",300,506,"pc","PC0","192.168.1.2/24",BLUE),
    ("pc1",820,506,"pc","PC1","192.168.1.3/24",BLUE)],
    [("r","sw"),("sw","pc0"),("sw","pc1")],
    [(78,146,964,446,"LAN 192.168.1.0/24",BLUE)],
    [(785,177,230,88,"Port map",["R1 G0/0 ↔ SW1 G0/1","PCs ↔ SW1 Fa0/1-2"],TEAL)])

topo("lesson-02-static-routing","Lesson 02 | two routers, two LANs","A /30 WAN connects the networks; both routers need a route back.",
     "R1 needs 192.168.2.0/24 via 10.0.0.2; R2 needs 192.168.1.0/24 via 10.0.0.1.",[
    ("pc0",114,324,"pc","PC0","192.168.1.10",BLUE,142),
    ("s1",280,324,"switch","SW1","LAN 1",TEAL,138),
    ("r1",445,324,"router","R1","WAN 10.0.0.1",BLUE,150),
    ("r2",677,324,"router","R2","WAN 10.0.0.2",BLUE,150),
    ("s2",843,324,"switch","SW2","LAN 2",TEAL,138),
    ("pc1",1008,324,"pc","PC1","192.168.2.10",BLUE,142)],
    [("pc0","s1"),("s1","r1"),("r1","r2","wan"),("r2","s2"),("s2","pc1")],
    [(38,157,476,396,"LAN 1  ·  192.168.1.0/24",BLUE),(608,157,474,396,"LAN 2  ·  192.168.2.0/24",TEAL)],
    [(65,454,465,101,"R1: forward route",["192.168.2.0/24 → 10.0.0.2"],BLUE),
     (588,454,465,101,"R2: return route",["192.168.1.0/24 → 10.0.0.1"],TEAL)],
    [(560,265,"10.0.0.0/30",AMBER)])

# DHCP DORA is a request/response sequence, not four devices.
a=Art("Lesson 03 | DHCP: DORA sequence","One client and one router negotiate an address in four messages.","packet flow",
      "Excluded .1–.10; DHCP begins leasing from 192.168.1.11 in this lab.")
a.node("client",167,332,"pc","PC0","IP: not assigned",BLUE,184)
a.node("server",952,332,"router","R1 / DHCP","Gateway: 192.168.1.1",TEAL,204)
a.zone(298,151,526,397,"192.168.1.0/24  ·  one broadcast domain",BLUE)
for y,name,direction,color in [(215,"1  DISCOVER  ·  who can offer an IP?",1,BLUE),
                               (303,"2  OFFER  ·  192.168.1.11 proposed",-1,TEAL),
                               (391,"3  REQUEST  ·  please reserve .11",1,BLUE),
                               (479,"4  ACK  ·  lease confirmed",-1,TEAL)]:
    if direction==1:a.line(315,y,809,y,color,3,arrow=True)
    else:a.line(809,y,315,y,color,3,arrow=True)
    a.pill(560,y-16,name,color,width=407)
save("lesson-03-dhcp-dora",a)

topo("lesson-04-dns-http","Lesson 04 | a website has two steps","The same Server0 provides DNS and HTTP; its address is static.",
     "DNS resolves www.office.local → 192.168.1.100; then HTTP fetches the page from that IP.",[
    ("r",560,195,"router","R1 gateway","192.168.1.1",BLUE),
    ("sw",560,350,"switch","Switch0","LAN 192.168.1.0/24",TEAL,188),
    ("pc",226,350,"pc","PC0","IP via DHCP",BLUE),
    ("srv",893,350,"server","Server0","192.168.1.100",VIOLET)],
    [("r","sw"),("sw","pc"),("sw","srv")],
    [(90,154,939,407,"DNS + HTTP on one local LAN",BLUE)],
    [(78,482,456,90,"1  Ask DNS",["www.office.local → 192.168.1.100"],BLUE),
     (584,482,456,90,"2  Request web page",["HTTP → Server0 on the same LAN"],VIOLET)])

topo("lesson-05-vlan-isolation","Lesson 05 | VLAN isolation on one switch","Access ports on one physical switch form two separate broadcast domains.",
     "PC0 ↔ PC1 and PC2 ↔ PC3 can ping; VLAN 10 ↔ VLAN 20 needs a router.",[
    ("sw",560,230,"switch","SW1 / 2960","4 access ports",TEAL,184),
    ("p0",211,445,"pc","PC0",".10.1  |  Fa0/1",BLUE,154),
    ("p1",407,445,"pc","PC1",".10.2  |  Fa0/2",BLUE,154),
    ("p2",714,445,"pc","PC2",".20.1  |  Fa0/3",VIOLET,154),
    ("p3",910,445,"pc","PC3",".20.2  |  Fa0/4",VIOLET,154)],
    [("sw","p0"),("sw","p1"),("sw","p2"),("sw","p3")],
    [(81,348,449,196,"VLAN 10  ·  CSE  ·  192.168.10.0/24",BLUE),
     (590,348,449,196,"VLAN 20  ·  EEE  ·  192.168.20.0/24",VIOLET)],
    pills=[(560,313,"NO ROUTER = NO CROSS-VLAN PING",RED)])

topo("lesson-06-switch-trunk","Lesson 06A | one trunk, two VLANs","Lab Part 2: SW1 G0/1 connects to SW2 G0/1 as an 802.1Q trunk.",
     "PC0 ↔ PC2 (VLAN 10) works; PC1 ↔ PC3 (VLAN 20) works; cross-VLAN ping needs a router.",[
    ("s1",344,316,"switch","SW1 / 2960","G0/1 ↔ SW2",TEAL,187),
    ("s2",776,316,"switch","SW2 / 2960","G0/1 ↔ SW1",TEAL,187),
    ("p0",167,508,"pc","PC0","VLAN 10 · .10.1",BLUE,160),
    ("p1",448,508,"pc","PC1","VLAN 20 · .20.1",VIOLET,160),
    ("p2",672,508,"pc","PC2","VLAN 10 · .10.2",BLUE,160),
    ("p3",952,508,"pc","PC3","VLAN 20 · .20.2",VIOLET,160)],
    [("s1","s2","trunk","802.1Q · VLAN 10 + 20",-28),
     ("s1","p0"),("s1","p1"),("s2","p2"),("s2","p3")],
    [],[(61,147,450,83,"VLAN 10 · 192.168.10.0/24",["PC0 ↔ PC2: ping works across the trunk"],BLUE),
        (609,147,450,83,"VLAN 20 · 192.168.20.0/24",["PC1 ↔ PC3: ping works across the trunk"],VIOLET)])

topo("lesson-06-router-on-a-stick","Lesson 06B | inter-VLAN with one router port","Lab Part 3: R1 G0/0 joins SW1 G0/1 via a trunk; each subinterface has a VLAN tag.",
     "PC0 .10.1 → GW .10.254 → R1 → GW .20.254 → PC1 .20.1: inter-VLAN ping succeeds.",[
    ("r",560,211,"router","R1 / 1941","G0/0 physical port",BLUE,199),
    ("sw",560,378,"switch","SW1 / 2960","G0/1 trunk to R1",TEAL,192),
    ("pc0",246,520,"pc","PC0 / VLAN 10","192.168.10.1",BLUE,191),
    ("pc1",874,520,"pc","PC1 / VLAN 20","192.168.20.1",VIOLET,191)],
    [("r","sw","trunk"),("sw","pc0"),("sw","pc1")],
    [],[(52,159,400,93,"VLAN 10 gateway",["G0/0.10 · dot1Q 10","192.168.10.254/24"],BLUE),
        (667,159,402,93,"VLAN 20 gateway",["G0/0.20 · dot1Q 20","192.168.20.254/24"],VIOLET)])

topo("lesson-07-stp-loop","Lesson 07 | switching without a loop","STP blocks one redundant path; the remaining links form a loop-free tree.",
     "A blocked/amber port is normal in STP. Its exact location depends on bridge priority and cost.",[
    ("sw1",272,260,"switch","SW1","Root Bridge",TEAL,174),
    ("sw2",848,260,"switch","SW2","Designated port",BLUE,174),
    ("sw3",560,429,"switch","SW3","Alternate port",AMBER,174)],
    [("sw1","sw2"),("sw1","sw3"),("sw2","sw3","blocked","STP BLOCKS",-9,False,"amber")],
    [],[(75,515,457,83,"Port security",["Sticky MAC → an unknown PC is rejected"],BLUE),
        (586,515,457,83,"EtherChannel / LACP",["Two physical links → one logical Po1"],VIOLET)])

topo("lesson-08-office-capstone","Lesson 08 | office network capstone","VLAN 10 and VLAN 20 share a switch but meet only through R1 subinterfaces.",
     "Server0 is static in VLAN 10; R1 provides both VLAN gateways and DHCP pools.",[
    ("r",560,202,"router","R1 / ROAS",".10 = .10.1  |  .20 = .20.1",BLUE,230),
    ("sw",560,347,"switch","SW1","G0/1 → R1 trunk",TEAL,184),
    ("p0",235,506,"pc","PC0 / CSE","VLAN 10 · DHCP",BLUE),
    ("p1",563,506,"pc","PC1 / EEE","VLAN 20 · DHCP",VIOLET),
    ("srv",884,506,"server","Server0",".10.100 · DNS+HTTP",BLUE,202)],
    [("r","sw","trunk"),("sw","p0"),("sw","p1"),("sw","srv")],
    [(92,395,308,190,"VLAN 10 · CSE",BLUE),(443,395,236,190,"VLAN 20 · EEE",VIOLET),
     (732,395,303,190,"VLAN 10 · Services",BLUE)],
    [(745,167,311,90,"Web lookup",["www.office.local → .10.100"],TEAL)])

overview("lesson-09-hardware-chain","Lesson 09 | from Packet Tracer to a real rack","Find the device in Packet Tracer, then recognize its physical ports and cables.",
         "The lesson below contains actual router, switch, cable, SFP and rack photos.", [
    ("LAYER 3", "Router", "Interfaces connect IP networks", "Console cable for initial CLI", BLUE,"router"),
    ("LAYER 2", "Switch", "Fa/Gi ports connect LAN devices", "Green LEDs indicate link state", TEAL,"switch"),
    ("PHYSICAL", "Cables + optics", "RJ-45, console, SFP and fiber", "Match each connector to its port", AMBER,"gear")],"hardware map")

flow("lesson-10-practice-cycle","Lesson 10 | ten guided practice tasks","Six simpler tasks, then four harder tasks; every answer can be checked.",
     "Keep the answer toggle closed until you have tested your own topology.",[
    ("Build", "Place devices and links", "Use the given IP table",BLUE),
    ("Configure", "Add VLANs, routes or", "DHCP as the task asks",VIOLET),
    ("Simulate", "Send a simple PDU", "Ping both directions",AMBER),
    ("Explain + check", "Compare show output", "Then open the solution",TEAL)])

overview("lesson-11-practice-levels","Lesson 11 | twenty self-practice challenges","The same network skills become progressively less guided.",
         "Problems 18–20 are timed exam simulations. Draw your topology before you configure it.",[
    ("TASKS 01-07", "Basic", "First LAN, router and VLAN", "Verify with ping and show",TEAL,"pc"),
    ("TASKS 08-13", "Intermediate", "Trunk, ROAS and services", "Explain which device forwards",BLUE,"switch"),
    ("TASKS 14-17", "Small hard", "Multi-router / DHCP relay", "Find the missing route or helper",AMBER,"router"),
    ("TASKS 18-20", "Exam simulation", "Build and extend a full LAN", "Use a timer; document results",VIOLET,"shield")],"challenge ladder")

flow("lesson-12-debug-path","Lesson 12 | find where a packet stops","Follow the path from a local link to an end-to-end service.",
     "The nine problem-bank cases illustrate VLAN, return route, DHCP, OSPF, SSH and Wi-Fi faults.",[
    ("Physical", "Cable + green LEDs", "show ip int brief",TEAL),
    ("Local address", "IP, mask and gateway", "ipconfig / ping gateway",BLUE),
    ("Forwarding", "VLAN, trunk and route", "show vlan / show ip route",VIOLET),
    ("Service", "DHCP, SSH or WLAN", "Test the exact protocol",AMBER)])

# OSPF alternate path: the R1–R2 direct link is failed, not the entire topology.
a=Art("Lesson 13 | OSPF finds another path","Three routers in area 0; a failed direct link can be bypassed via R3.","routing + failover",
      "OSPF neighbors exchange routes. After convergence: R1 → R3 → R2 when R1–R2 fails.")
for n in [("r1",244,413,"router","R1 / HQ","192.168.1.0/24",BLUE),
          ("r2",876,413,"router","R2 / Branch-1","192.168.2.0/24",BLUE),
          ("r3",560,217,"router","R3 / Branch-2","192.168.3.0/24",TEAL)]:a.node(*n)
a.edge("r1","r2","fault","10.0.12.0/30  ·  link down",-28)
a.edge("r1","r3","wired","10.0.13.0/30",-22)
a.edge("r3","r2","wired","10.0.23.0/30",-22)
a.callout(82,506,445,84,"Before the failure",["Direct R1 → R2 route is preferred"],AMBER)
a.callout(595,506,445,84,"After OSPF converges",["Backup: R1 → R3 → R2"],TEAL)
save("lesson-13-ospf-failover",a)

topo("lesson-14-home-wifi","Lesson 14A | home Wi-Fi on WRT300N","A home router combines DHCP, switching, routing and a wireless access point.",
     "SSID MaksDev-WiFi; WPA2-PSK; laptop needs WPC300N before it can join wirelessly.",[
    ("lap",237,228,"laptop","Laptop0","WPC300N module",BLUE,181),
    ("phone",237,440,"phone","Smartphone0","WPA2-PSK",BLUE,181),
    ("wrt",608,334,"wifi","WRT300N","LAN 192.168.0.1/24",TEAL,218),
    ("isp",958,334,"router","ISP router","WAN side (optional)",AMBER,183)],
    [("lap","wrt","wireless"),("phone","wrt","wireless"),("wrt","isp","wired","WAN",-27)],
    [(68,150,761,382,"",BLUE)],
    [(66,521,993,74,"Join sequence",["Power OFF laptop → insert WPC300N → Power ON → connect to SSID"],TEAL)],
    [(600,185,"DHCP begins at 192.168.0.100",BLUE)])

topo("lesson-14-enterprise-wlc","Lesson 14B | enterprise WLC + lightweight AP","The WLC configures the WLAN; LAP-PT carries it to wireless clients.",
     "CAPWAP runs over the wired LAN. In Packet Tracer, LAP-PT needs a power brick on a non-PoE 2960.",[
    ("admin",179,212,"pc","Admin PC0","192.168.10.10",BLUE,166),
    ("srv",470,212,"server","Server0 / DHCP","192.168.10.5",VIOLET,186),
    ("wlc",806,212,"wlc","WLC-2504","192.168.10.250",VIOLET,188),
    ("sw",518,369,"switch","SW1 / 2960","192.168.10.0/24",TEAL,196),
    ("lap",518,522,"ap","LAP-PT","CAPWAP joined",TEAL,174),
    ("client",903,522,"laptop","Laptop1","SSID: Campus-Corp",BLUE,198)],
    [("admin","sw"),("srv","sw"),("wlc","sw"),("sw","lap","capwap"),
     ("lap","client","wireless","Wi-Fi",-28)],
    [],[(64,455,311,91,"Packet Tracer reminder",["Power brick → LAP-PT Physical","WLAN status must be Enabled"],AMBER)],
    [(738,352,"CAPWAP via wired LAN",VIOLET)])

topo("lesson-15-ssh-ntp-syslog","Lesson 15 | secure and observe your router","The admin reaches R1 with SSH; R1 syncs time and exports logs to Server0.",
     "SSH: TCP/22 · NTP: UDP/123 · Syslog: usually UDP/514 in this lab.",[
    ("r",545,208,"router","R1 / SSHv2","192.168.1.1",BLUE,189),
    ("sw",545,369,"switch","SW1","SVI: 192.168.1.2",TEAL,187),
    ("pc",224,515,"pc","Admin PC0","192.168.1.10",BLUE,177),
    ("srv",891,515,"server","Server0","192.168.1.100",VIOLET,187)],
    [("r","sw"),("sw","pc"),("sw","srv")],
    [(76,150,969,421,"Management LAN · 192.168.1.0/24",BLUE)],
    [(741,171,294,115,"Server0 services",["NTP time → R1 clock","Syslog ← R1 event messages"],VIOLET)],
    [(244,432,"SSH TCP/22",BLUE),(906,432,"NTP + Syslog",VIOLET)])

# ── CCNA Fundamentals: conceptual diagrams, not recycled practical topologies. ──
overview("ccna-course-map", "CCNA fundamentals | theory to capstone", "Nine chapters build a mental model before the command-line practice.",
         "The accompanying hands-on labs demonstrate the theory; the final chapter integrates it all.", [
    ("01", "Network basics", "LAN vs WAN · switch vs router", "Recognize each forwarding role", TEAL,"switch"),
    ("02", "OSI + TCP/IP", "Seven layers · encapsulation", "Predict the PDU at each layer", BLUE,"file"),
    ("03", "Ethernet + ARP", "MAC address · switching table", "Resolve an IP to a local MAC", VIOLET,"switch"),
    ("04", "IPv4 addressing", "Network and host portions", "Identify gateway vs host IP", TEAL,"pc"),
    ("05", "Subnetting basics", "Block size · /24 into /26", "Find network and broadcast", BLUE,"gear"),
    ("06", "VLSM planning", "Different prefixes, zero overlap", "Allocate largest subnet first", AMBER,"file"),
    ("07", "ACL + NAT", "Permit/deny and private/public", "Watch an address be translated", RED,"shield"),
    ("08", "Troubleshooting", "Test the path layer by layer", "Locate the first failing hop", VIOLET,"gear"),
    ("09", "Campus capstone", "VLAN + DHCP + DNS + NAT", "Build, secure and verify", TEAL,"router")],"ccna study map")

topo("ccna-01-lan-wan","CCNA 01 | a LAN reaches a WAN","Switches connect local devices; routers connect different IP networks.",
     "Same subnet → switch forwarding. Other network → send the frame to the default gateway.",[
    ("pc",151,326,"pc","PC0","192.168.1.10",BLUE,154),
    ("sw",393,326,"switch","SW1","one LAN",TEAL,154),
    ("r",689,326,"router","R1 gateway","192.168.1.1",BLUE,166),
    ("wan",960,326,"cloud","Other network","WAN / internet",AMBER,177)],
    [("pc","sw"),("sw","r"),("r","wan","wan")],
    [(47,158,570,395,"LOCAL AREA NETWORK  ·  LAN",TEAL),
     (658,158,414,395,"ROUTED NETWORK  ·  WAN",AMBER)],
    [(72,446,516,82,"Layer 2: Switch",["Learns source MAC and forwards frames"],TEAL),
     (677,446,368,82,"Layer 3: Router",["Forwards packets by destination IP"],BLUE)])

# OSI stack: aligned rows on the left and explicit many-to-one TCP/IP mapping at right.
a=Art("CCNA 02 | OSI maps to TCP/IP","The seven-layer model describes how data is wrapped before transmission.","layer model",
      "Sending: application → transport → IP packet → Ethernet frame → bits; receiving reverses it.")
a.text(82,137,"OSI MODEL · 7 LAYERS",17,BLUE,750)
a.text(783,137,"TCP/IP MODEL · 4 LAYERS",17,VIOLET,750)
rows=[("7","Application","HTTP · DNS","Data",TEAL),
      ("6","Presentation","Encode · encrypt","Data",BLUE),
      ("5","Session","Conversation","Data",BLUE),
      ("4","Transport","TCP · UDP","Segment",VIOLET),
      ("3","Network","IPv4 · routing","Packet",AMBER),
      ("2","Data Link","Ethernet · MAC","Frame",TEAL),
      ("1","Physical","Cable · radio","Bits",BLUE)]
for i,(num,name,example,pdu,color) in enumerate(rows):
    y=151+53*i
    a.rect(74,y,605,48,"#FFFFFF",color+"66",11,layer="nodes")
    a.circle(107,y+24,17,color,layer="nodes")
    a.text(107,y+30,num,16,"white",750,"middle","front")
    a.text(138,y+31,name,17,INK,700,layer="front")
    a.text(351,y+31,example,14.5,MUTED,500,layer="front",max_width=175)
    a.pill(616,y+24,pdu,color,width=105)
for y,height,title,color in [(151,154,"Application (L7–L5)",TEAL),
                             (310,48,"Transport (L4)",VIOLET),
                             (363,48,"Internet (L3)",AMBER),
                             (416,101,"Network access (L2–L1)",BLUE)]:
    a.rect(760,y,297,height,PALE[color],color+"77",12,layer="nodes")
    a.text(908,y+height/2+6,title,17,color,750,"middle","front",max_width=270)
    a.line(681,y+height/2,749,y+height/2,color,2,arrow=True)
save("ccna-02-osi-tcpip",a)

# ARP request broadcast vs reply unicast, using the device MAC mapping in the lesson.
a=Art("CCNA 03 | ARP resolves a local IP to a MAC","To send a unicast IP packet on a LAN, first find the next-hop MAC.","arp sequence",
      "ARP request: broadcast. ARP reply: unicast. The switch also learns the source MAC on each port.")
a.zone(54,154,1010,401,"",BLUE)
a.pill(560,530,"LAN · 192.168.1.0/24",BLUE,width=287)
a.node("a",167,355,"pc","PC0","IP .10 · MAC AA:AA",BLUE,206)
a.node("sw",560,355,"switch","SW1","MAC learning",TEAL,176)
a.node("b",947,355,"pc","PC1","IP .20 · MAC BB:BB",VIOLET,206)
a.edge("a","sw");a.edge("sw","b")
a.callout(72,174,477,115,"1  ARP REQUEST · broadcast",["Who has 192.168.1.20?","Sent to FF:FF:FF:FF:FF:FF"],BLUE)
a.callout(569,174,477,115,"2  ARP REPLY · unicast",[".20 is at MAC BB:BB","PC0 caches IP → MAC mapping"],VIOLET)
a.line(276,471,835,471,TEAL,3,arrow=True)
a.pill(555,453,"NOW PC0 CAN SEND AN ETHERNET FRAME",TEAL,width=374)
save("ccna-03-arp",a)

# IPv4 fields are separated visually into network and host bits.
a=Art("CCNA 04 | read an IPv4 address","192.168.10.25/24 has 24 network bits and 8 host bits.","ipv4 anatomy",
      "For /24: network .0, usable hosts .1–.254, broadcast .255; the host .25 is usable.")
for i,(octet,color) in enumerate([("192",BLUE),("168",BLUE),("10",BLUE),("25",AMBER)]):
    x=82+i*248
    a.rect(x,184,218,166,PALE[color],color+"88",20,layer="nodes")
    a.text(x+109,268,octet,46,color,750,"middle","front")
    a.text(x+109,312,"NETWORK" if i<3 else "HOST",16,color,750,"middle","front")
    if i<3:a.text(x+233,270,".",32,MUTED,650,"middle","front")
a.rect(82,369,715,43,PALE[BLUE],"none",16,layer="nodes")
a.rect(825,369,218,43,PALE[AMBER],"none",16,layer="nodes")
a.text(440,398,"24 bits  ·  192.168.10",17,BLUE,750,"middle","front")
a.text(934,398,"8 bits  ·  .25",17,AMBER,750,"middle","front")
for x,head,value,color in [(85,"NETWORK","192.168.10.0",BLUE),(412,"GATEWAY","192.168.10.1",TEAL),
                           (742,"BROADCAST","192.168.10.255",AMBER)]:
    a.callout(x,452,295,94,head,[value],color)
save("ccna-04-ipv4-address",a)

# /26 begins at 0, 64, 128, 192. Network/broadcast values verified against ipaddress.
a=Art("CCNA 05 | /24 split into four /26 networks","Mask 255.255.255.192 gives blocks of 64 addresses each.","subnetting /26",
      "Block size: 256 − 192 = 64. A /26 has 62 usable host addresses (network and broadcast excluded).")
for i,(block,usable,bc,color) in enumerate([
    (".0–.63",".1–.62",".63",BLUE),
    (".64–.127",".65–.126",".127",TEAL),
    (".128–.191",".129–.190",".191",VIOLET),
    (".192–.255",".193–.254",".255",AMBER)]):
    x=54+i*268
    a.rect(x,173,244,333,"#FFFFFF",color+"88",19,layer="nodes")
    a.rect(x,173,244,9,color,"none",4,layer="nodes")
    a.text(x+20,213,f"SUBNET {chr(65+i)}",16,color,750,layer="front")
    a.text(x+20,257,block,27,INK,750,layer="front",max_width=208)
    a.text(x+20,293,f"192.168.1.{[0,64,128,192][i]}/26",14,MUTED,600,layer="front")
    a.line(x+20,313,x+221,313,"#D6E2EC",1.5)
    a.text(x+20,348,"USABLE HOSTS",14,color,750,layer="front")
    a.text(x+20,378,usable,20,INK,650,layer="front")
    a.text(x+20,422,"BROADCAST",14,color,750,layer="front")
    a.text(x+20,453,bc,20,INK,650,layer="front")
save("ccna-05-subnet-26",a)

# Exact VLSM allocation: 100→/25, 50→/26, 20→/27, 2→/30.
a=Art("CCNA 06 | VLSM: largest subnet first","Allocate different-sized blocks inside the same 192.168.1.0/24 network.","vlsm address plan",
      "Ranges do not overlap: .0–127, .128–191, .192–223, .224–227. Remaining .228–255 are free.",720)
for i,(dept,hosts,prefix,span,color) in enumerate([
    ("CSE Lab","100 hosts","192.168.1.0/25",".0 – .127",BLUE),
    ("EEE Lab","50 hosts","192.168.1.128/26",".128 – .191",TEAL),
    ("Office","20 hosts","192.168.1.192/27",".192 – .223",VIOLET),
    ("Router link","2 hosts","192.168.1.224/30",".224 – .227",AMBER)]):
    y=150+101*i
    a.rect(69,y,981,89,"#FFFFFF","#D6E2EC",14,layer="nodes")
    a.rect(69,y,10,89,color,"none",3,layer="nodes")
    a.text(102,y+36,dept,20,INK,750,layer="front")
    a.text(102,y+65,hosts,15,MUTED,500,layer="front")
    a.pill(625,y+45,prefix,color,width=285)
    a.text(1009,y+51,span,20,color,750,"end","front")
# Scaled address bar, including the small /30 allocation and the remaining free addresses.
x=69; y=579; scale=981/256
for length,color in [(128,BLUE),(64,TEAL),(32,VIOLET),(4,AMBER),(28,"#CDD8E3")]:
    a.rect(round(x,2),y,round(length*scale,2),25,color,"none",0,layer="nodes")
    x+=length*scale
a.text(70,565,"0",14,MUTED,650);a.text(1047,565,"255",14,MUTED,650,"end")
save("ccna-06-vlsm-plan",a)

topo("ccna-07-acl-nat","CCNA 07 | filter traffic, translate its source","ACL chooses permitted traffic; PAT shares one public IPv4 address.",
     "PAT rewrites the private source IP to 203.0.113.2 and distinguishes flows by port / ICMP ID.",[
    ("pc",130,340,"pc","PC0","192.168.1.10",BLUE,155),
    ("sw",325,340,"switch","SW1","Inside LAN",TEAL,149),
    ("r",559,340,"router","R1 / PAT","203.0.113.2",VIOLET,183),
    ("isp",783,340,"router","ISP","203.0.113.1",AMBER,150),
    ("srv",992,340,"server","Remote host","198.51.100.1",BLUE,169)],
    [("pc","sw"),("sw","r"),("r","isp","wan"),("isp","srv")],
    [(48,155,409,403,"PRIVATE · 192.168.1.0/24",BLUE),
     (625,155,451,403,"PUBLIC / TEST WAN",AMBER)],
    [(70,472,490,93,"ACL action",["Permit/deny based on matching rule"],BLUE),
     (595,472,455,93,"PAT action",["Inside .1.10 → public .113.2"],VIOLET)])

flow("ccna-08-troubleshoot-tests","CCNA 08 | test the path in four hops","Each successful test narrows the fault to the next section of the path.",
     "If gateway ping works but remote ping fails, inspect routes and the return path.",[
    ("This device", "ipconfig / all", "Correct IP, mask, DNS?",BLUE),
    ("Local gateway", "ping 192.168.1.1", "Layer 2 / VLAN OK?",TEAL),
    ("Remote hop", "tracert remote-IP", "Where does it stop?",VIOLET),
    ("Final service", "nslookup / browser", "DNS, TCP and ACL OK?",AMBER)])

topo("ccna-09-campus-capstone","CCNA 09 | a four-VLAN campus","The campus router has VLAN subinterfaces; an ISP router sits across the WAN.",
     "VLAN 40 servers: .40.10 DHCP+DNS and .40.20 HTTP. R1 routes; NAT/ACL apply per lab.",[
    ("r",544,195,"router","Campus R1","ROAS + NAT/ACL",BLUE,193),
    ("isp",887,195,"router","ISP R2","203.0.113.1",AMBER,180),
    ("sw",544,346,"switch","Core SW1","802.1Q trunk",TEAL,183),
    ("cse",160,527,"pc","CSE","192.168.10.0/24",BLUE,174),
    ("eee",417,527,"pc","EEE","192.168.20.0/24",VIOLET,174),
    ("admin",674,527,"pc","Admin","192.168.30.0/24",TEAL,174),
    ("servers",938,527,"server","Server room","192.168.40.0/24",AMBER,192)],
    [("r","isp","wan"),("r","sw","trunk"),("sw","cse"),("sw","eee"),
     ("sw","admin"),("sw","servers")],
    [],[(61,159,282,92,"R1 outside",["WAN: 203.0.113.2/30"],BLUE)],
    [(159,429,"VLAN 10",BLUE),(417,429,"VLAN 20",VIOLET),
     (674,429,"VLAN 30",TEAL),(938,429,"VLAN 40",AMBER)])

# ── Extra labs: service-specific packet flows and reproducible topologies. ──
overview("extra-labs-map","Eight extra labs | from servers to security","Open existing .pkt examples, or build the later labs from their illustrated guides.",
         "Extras 07 and 08 are new build-alongs, not downloadable Packet Tracer projects.",[
    ("01", "FTP server", "Two subnets + router", "Upload put, download get",BLUE,"server"),
    ("02", "Email server", "SMTP push + POP3 pull", "Mail crosses a routed LAN",VIOLET,"server"),
    ("03", "Shared printer", "DHCP PCs + static printer", "Exclude the printer IP",TEAL,"printer"),
    ("04", "IP subnet tester", "One switch, four hosts", "Prove the /26 boundary",AMBER,"pc"),
    ("05", "Six topologies", "Bus, star, ring, mesh...", "Compare actual .pkt layouts",BLUE,"switch"),
    ("06", "Broken lab detective", "Inject one fault at a time", "Observe → repair → verify",RED,"shield"),
    ("07", "VoIP IP telephony", "2811 CME + two 7960s", "Voice VLAN and option 150",VIOLET,"ipphone"),
    ("08", "DHCP Snooping + DAI", "Trust only server uplink", "DAI behavior may differ in PT",TEAL,"shield")],"extra lab index")

flow("extra-broken-detective","Extra 06 | broken network detective","Keep the fault hidden until you can identify the symptom and failing hop.",
     "Six scenarios: routing, DHCP, ROAS, EtherChannel, OSPF and SSH. The guide has hints and fixes.",[
    ("Pick a case", "Open its matching .pkt", "Read the case symptom",BLUE),
    ("Inject one fault", "Paste its .ios script", "On the stated device",RED),
    ("Collect clues", "ping, show, ipconfig", "Locate the first failure",AMBER),
    ("Repair + prove", "Change the root cause", "Retest both directions",TEAL)])

topo("extra-email-smtp-pop3","Extra 02 | SMTP sends; POP3 receives","SW1 and SW2 join two /24 LANs through Router2; each LAN has its own switch.",
     "SMTP TCP/25: PC0 → SW1 → Router2 → SW2 → Server. POP3 TCP/110: PC1 → SW2 → Server.",[
    ("sender",139,340,"pc","PC0 / sender","192.168.10.3",BLUE,157),
    ("sw1",338,340,"switch","SW1","LAN 1",TEAL,141),
    ("r",552,340,"router","Router2",".10.1  |  .20.1",BLUE,170),
    ("sw2",757,340,"switch","SW2","LAN 2",TEAL,141),
    ("srv",961,265,"server","Email Server","192.168.20.3",VIOLET,179),
    ("recv",961,426,"pc","PC1 / recipient","192.168.20.2",BLUE,179)],
    [("sender","sw1"),("sw1","r"),("r","sw2"),("sw2","srv"),("sw2","recv")],
    [(51,151,399,445,"LAN 1 · 192.168.10.0/24",BLUE),
     (671,151,405,445,"LAN 2 · 192.168.20.0/24",VIOLET)],
    [(71,505,359,82,"SEND / SMTP",["PC0 → Router2 → Server"],BLUE),
     (686,505,367,82,"RECEIVE / POP3",["PC1 → SW2 → Server"],VIOLET)])

topo("extra-ftp-transfer","Extra 01 | FTP across two networks","Office hosts reach an FTP server only through the router gateway.",
     "PC0 192.168.1.2 → R1 → FTP 10.10.10.2. Login on TCP/21; put uploads; get downloads.",[
    ("pc",141,322,"pc","PC0","192.168.1.2",BLUE,161),
    ("sw",363,322,"switch","SW1 / 2960","PC1–3 also connect",TEAL,182),
    ("r",633,322,"router","R1 / 1941",".1.1  |  10.10.10.1",BLUE,195),
    ("ftp",951,322,"server","FTP Server","10.10.10.2",VIOLET,192)],
    [("pc","sw"),("sw","r"),("r","ftp")],
    [(49,146,449,413,"OFFICE LAN · 192.168.1.0/24",BLUE),
     (777,146,301,413,"SERVER LAN · 10.10.10.0/24",VIOLET)],
    [(85,461,409,92,"FTP control",["Authenticate on TCP port 21"],BLUE),
     (598,461,418,92,"FTP data",["put uploads / get downloads"],VIOLET)])

topo("extra-subnet-tester","Extra 04 | same switch, different /26","Four PCs share the cable network but not the same IP subnet.",
     "PC0 .10 ↔ PC1 .50 works. PC0 .10 → PC2 .65 needs a router with valid /26 interfaces.",[
    ("sw",559,221,"switch","SW1","Layer 2 only",TEAL,180),
    ("a",174,449,"pc","PC0","192.168.1.10",BLUE,164),
    ("b",401,449,"pc","PC1","192.168.1.50",BLUE,164),
    ("c",718,449,"pc","PC2","192.168.1.65",VIOLET,164),
    ("d",946,449,"pc","PC3","192.168.1.120",VIOLET,164)],
    [("sw","a"),("sw","b"),("sw","c"),("sw","d")],
    [(61,342,468,205,"SUBNET A  ·  192.168.1.0/26",BLUE),
     (591,342,468,205,"SUBNET B  ·  192.168.1.64/26",VIOLET)],
    [],[(560,566,"CROSS-SUBNET PING NEEDS A ROUTER",RED)])

# Six independently drawn miniature graph structures with explicit connectivity.
a=Art("Extra 05 | six network topology shapes","Topology describes the physical or logical arrangement of the nodes.","topology gallery",
      "A switched Ethernet ring needs loop prevention (STP). The diagrams are schematic, not screenshots.")
shapes=[("BUS","One shared backbone",BLUE),("STAR","One central switch",TEAL),
        ("RING","Each node has 2 neighbors",VIOLET),("MESH","Every node interconnects",AMBER),
        ("TREE","Core → distribution → access",BLUE),("HYBRID","More than one design",TEAL)]
for idx,(title,subtitle,color) in enumerate(shapes):
    col,row=idx%3,idx//3
    x=47+col*356;y=147+row*208
    a.rect(x,y,312,185,"#FFFFFF","#D4E0EB",17,layer="nodes")
    a.text(x+19,y+31,title,17,color,750,layer="front")
    a.text(x+19,y+157,subtitle,14,MUTED,500,layer="front",max_width=275)
    cx,cy=x+156,y+91
    # Inside-panel edges must be painted AFTER the opaque panel cards.
    def mini_edge(p,q,c=color):a.line(p[0],p[1],q[0],q[1],c,2.5,layer="front")
    def mini_dot(p):a.circle(*p,8,color,layer="front")
    if idx==0:  # bus
        mini_edge((x+52,cy+20),(x+260,cy+20))
        for px in (x+66,x+129,x+192,x+255):
            mini_edge((px,cy-28),(px,cy+20));mini_dot((px,cy-28))
    elif idx==1:  # star
        center=(cx,cy+4)
        ps=[(cx-96,cy-31),(cx+96,cy-31),(cx-96,cy+42),(cx+96,cy+42)]
        for p in ps:mini_edge(center,p);mini_dot(p)
        mini_dot(center)
    elif idx==2:  # ring
        ps=[(cx-67,cy-32),(cx+67,cy-32),(cx+67,cy+48),(cx-67,cy+48)]
        for i in range(4):mini_edge(ps[i],ps[(i+1)%4])
        for p in ps:mini_dot(p)
    elif idx==3:  # full mesh of four
        ps=[(cx-70,cy-33),(cx+70,cy-33),(cx-70,cy+47),(cx+70,cy+47)]
        for i in range(4):
            for j in range(i+1,4):mini_edge(ps[i],ps[j])
        for p in ps:mini_dot(p)
    elif idx==4:  # tree
        root=(cx,cy-43);mid=[(cx-61,cy+5),(cx+61,cy+5)]
        leaves=[(cx-102,cy+49),(cx-31,cy+49),(cx+31,cy+49),(cx+102,cy+49)]
        for p in mid:mini_edge(root,p)
        for i,p in enumerate(leaves):mini_edge(mid[i//2],p)
        for p in [root]+mid+leaves:mini_dot(p)
    else:  # two stars tied through a backbone
        centers=[(cx-61,cy+6),(cx+61,cy+6)];mini_edge(*centers)
        for j,c in enumerate(centers):
            for p in [(c[0]-31,cy-36),(c[0]+31,cy-36),(c[0]+(-31 if j==0 else 31),cy+47)]:
                mini_edge(c,p);mini_dot(p)
            mini_dot(c)
save("extra-six-topologies",a)

topo("extra-office-printer","Extra 03 | shared network printer","Three DHCP clients print to one statically addressed printer on the same LAN.",
     "Reserve 192.168.1.10 for Printer-PT by excluding .1–.10 from the DHCP pool.",[
    ("r",557,191,"router","R1 / DHCP","192.168.1.1",BLUE,177),
    ("sw",557,341,"switch","SW1 / 2960","Fa0/1–3 + Fa0/10",TEAL,199),
    ("hr",158,510,"pc","HR PC0","DHCP: .11",BLUE,162),
    ("ac",412,510,"pc","Accounts PC1","DHCP: .12",BLUE,171),
    ("mg",673,510,"pc","Manager PC2","DHCP: .13",BLUE,173),
    ("pr",955,510,"printer","Printer-PT","STATIC: .10",AMBER,181)],
    [("r","sw"),("sw","hr"),("sw","ac"),("sw","mg"),("sw","pr")],
    [(64,151,990,432,"ONE LAN  ·  192.168.1.0/24",BLUE)],
    [],[(954,417,"EXCLUDED FROM DHCP",AMBER)])

# ── File catalog, references and helper scripts. ──
overview("pkt-lab-catalog","Packet Tracer file catalog","Open a .pkt file in Packet Tracer; use the matching .md for the IP plan and commands.",
         "Six .ios files are command fault scripts, NOT native .pkt projects; paste them on the stated device.",[
    ("8 FILES", "Serial lesson labs", "pkt-files/labs/lesson-*.pkt", "First ping → office capstone",BLUE,"router"),
    ("4 FILES", "Extra practice", "pkt-files/practice/*.pkt", "FTP, email, printer, subnet",TEAL,"server"),
    ("6 FILES", "Topology examples", "pkt-files/topologies/*.pkt", "Bus, star, ring, mesh...",VIOLET,"switch"),
    ("6 SCRIPTS", "Broken lab faults", "troubleshooting/*.ios", "Apply to an existing project",RED,"shield")],"file catalog")

flow("pkt-fault-script-workflow","Fault scripts | use with an existing .pkt","A .ios file contains IOS commands to paste, not a Packet Tracer project file.",
     "Always open the matching .pkt first. Paste only into the device named in the case instructions.",[
    ("Open .pkt", "Choose the matching lab", "Start from a known state",BLUE),
    ("Paste .ios", "Target R1, R2 or SW", "One case at a time",RED),
    ("Investigate", "Read CLI and ping output", "Keep the fix hidden",AMBER),
    ("Restore service", "Remove the wrong config", "Verify both directions",TEAL)])

overview("reference-library-map","Three references for three different questions","Select the resource that answers your immediate lab question.",
         "The OSI book already embeds six vector diagrams; all reference material is available offline.",[
    ("LOOK UP A COMMAND", "Cisco CLI sheet", "Router, switch, OSPF, SSH", "Syntax and verification commands",BLUE,"file"),
    ("DEBUG A REAL PC", "30 useful commands", "ping, dig, ssh, tcpdump...", "Linux / Windows / macOS",TEAL,"pc"),
    ("FOLLOW A REQUEST", "OSI illustrated book", "Search → DNS → TCP → HTTP", "Six embedded vector diagrams",VIOLET,"server")],"reference shelf")

flow("reference-cli-modes","Cisco IOS | which prompt accepts this command?","CLI modes change what commands you can run on a router or switch.",
     "Use end to return to R1#, then copy running-config startup-config to save changes.",[
    ("R1>", "User EXEC", "Type: enable",BLUE),
    ("R1#", "Privileged EXEC", "Type: conf t",TEAL),
    ("R1(config)#", "Global config", "Type: interface g0/0",VIOLET),
    ("R1(config-if)#", "Interface config", "IP + no shutdown",AMBER)],"cli mode map")

overview("reference-30-command-toolbox","30 practical commands | what are you testing?","Group commands by the evidence you need, not by the operating system you use.",
         "The book provides five real examples and platform notes per command; these are quick category cues.",[
    ("01", "Reachability", "ping · traceroute · mtr", "Is the host reachable?",TEAL,"pc"),
    ("02", "Address + interface", "ip · ifconfig · ipconfig", "Which IP and mask are set?",BLUE,"gear"),
    ("03", "Routes + neighbors", "ip route · arp · ip neigh", "Where is the next hop?",VIOLET,"router"),
    ("04", "Name resolution", "dig · nslookup · host", "What address does DNS return?",AMBER,"server"),
    ("05", "Sockets + ports", "ss · netstat · nmap", "Which service is listening?",BLUE,"shield"),
    ("06", "Remote access", "ssh · scp · curl", "Can you connect / transfer?",TEAL,"file"),
    ("07", "Packets on wire", "tcpdump · Wireshark", "What did the network send?",VIOLET,"switch"),
    ("08", "Firewall + policy", "iptables · ufw · netsh", "What blocks this connection?",RED,"shield"),
    ("09", "Performance", "iperf3 · speedtest", "Is it latency or throughput?",AMBER,"gear")],"command toolkit")

overview("scripts-automation-pipeline","Six Python tools | repeatable lab work","Zero third-party packages: generate, practice, illustrate and verify.",
         "Run python3 scripts/diagram_generator.py --check to confirm the SVGs are up to date.",[
    ("BUILD GUIDES", "lab_writer.py", "Lesson and Extra Lab templates", "New content needs a local image",TEAL,"file"),
    ("GENERATE IOS", "ios_config_generator.py", "19 presets incl. HSRP/IPv6", "Paste one role per device",BLUE,"router"),
    ("PLAN IP", "subnet_calculator.py", "CIDR, VLSM and exam drills", "Avoid overlapping subnets",VIOLET,"gear"),
    ("PRACTICE", "quiz_trainer.py", "86 questions + flashcards", "Check before opening answers",AMBER,"pc"),
    ("DRAW VISUALS", "diagram_generator.py", "Original, local SVG diagrams", "Regenerate after IP edits",BLUE,"switch"),
    ("AUDIT ALL", "repo_doctor.py", "Links, images, Markdown, .pkt", "--strict before a PR",TEAL,"shield")],"tool workflow")


flow("reference-osi-search-journey","OSI book | from search to screen","The browser request is packaged, routed and unpacked before results appear.",
     "DNS finds an address; transport, IP and Ethernet carry the request; the server replies in reverse.",[
    ("Browser", "Search text becomes", "an application request",BLUE),
    ("DNS lookup", "Name → server IP", "Resolver returns an IP",TEAL),
    ("Send packets", "TCP/TLS + IP + frame", "Bits cross each local link",VIOLET),
    ("Web server", "Processes HTTP request", "Returns a response",AMBER),
    ("Render page", "Decode the response", "Browser shows results",TEAL)],"seven-layer journey")


# ── Phase 3 (v3.0): ten additional topic-specific, offline-ready illustrations. ──
# Each scene follows the exact ports/IPs of its build-along Markdown; not screenshots.
a=Art("Lesson 16 | one switch, two routed VLANs",
      "A 3560 provides both gateways: .10.1 for VLAN 10 and .20.1 for VLAN 20.",
      "SVI topology", "All four host links are access ports; inter-VLAN forwarding needs ip routing.",780)
a.zone(49,392,494,236,"VLAN 10  |  CSE",BLUE)
a.rect(577,392,494,236,PALE[TEAL],TEAL+"55",22,layer="zones")
a.text(1051,424,"VLAN 20  |  EEE",17,TEAL,750,"end",layer="labels")
a.node("sw",560,239,"switch","SW1 / 3560","SVI10: .10.1  |  SVI20: .20.1",VIOLET,300)
for key,x,name,addr,col in (("p0",169,"PC0","192.168.10.10",BLUE),
                             ("p1",405,"PC1","192.168.10.11",BLUE),
                             ("p2",715,"PC2","192.168.20.10",TEAL),
                             ("p3",951,"PC3","192.168.20.11",TEAL)):
    a.node(key,x,531,"pc",name,addr,col,172)
    a.edge("sw",key)
a.pill(560,354,"ip routing ON   |   no separate router",VIOLET,width=386)
a.pill(296,622,"Fa0/1-2 access  |  192.168.10.0/24",BLUE,width=407)
a.pill(824,622,"Fa0/3-4 access  |  192.168.20.0/24",TEAL,width=407)
a.callout(248,648,624,57,"PC0 -> SVI 10 -> L3 route -> SVI 20 -> PC2",[],VIOLET)
save("lesson-16-svi-topology",a)

flow("lesson-16-svi-packet-path","Lesson 16 | why a VLAN can reach another VLAN",
     "A Layer-3 switch routes between two connected SVI networks.",
     "Without ip routing the two VLANs stay separate; no trunk or external router is used.",[
    ("PC0 / VLAN 10","192.168.10.10/24","target: 192.168.20.10",BLUE),
    ("Gateway / SVI10","192.168.10.1 receives","frame from Fa0/1",TEAL),
    ("Route on SW1","ip routing chooses","VLAN 20 connected route",VIOLET),
    ("SVI20 -> PC2","to 192.168.20.10","new L2 delivery",AMBER)],"packet path")

a=Art("Lesson 17 | HSRP virtual default gateway",
      "Two router uplinks reach a test loopback; PC0 never changes its gateway.",
      "HSRP topology", "198.51.100.10 is a documentation-only remote target, not the real Internet.",850)
a.zone(62,149,995,241,"Two independent upstream paths",BLUE)
a.zone(62,404,995,338,"Shared LAN: 192.168.50.0/24",TEAL)
a.node("r1",207,251,"router","R1 / ACTIVE","G0/0: 192.168.50.2",BLUE,197)
a.node("r3",560,232,"router","R3 / TEST","Lo0: 198.51.100.10",VIOLET,214)
a.node("r2",913,251,"router","R2 / STANDBY","G0/0: 192.168.50.3",TEAL,197)
a.node("sw",560,498,"switch","SW1 / 2960","Fa0/2 R1  |  Fa0/3 R2",TEAL,230)
a.node("pc",560,661,"pc","PC0","192.168.50.10/24",BLUE,207)
a.edge("r1","r3","wan","10.0.13.0/30",-29)
a.edge("r2","r3","wan","10.0.23.0/30",-29)
a.edge("r1","sw")
a.edge("r2","sw")
a.edge("sw","pc","wired","Fa0/1",-19)
a.pill(560,388,"VIP / default gateway: 192.168.50.1",AMBER,width=357)
a.pill(560,765,"Power R1 OFF -> R2 active; PC0 gateway stays .50.1",TEAL,width=500)
save("lesson-17-hsrp-topology",a)

flow("lesson-17-hsrp-failover","Lesson 17 | gateway failover in four steps",
     "The virtual IP stays constant even as the router that owns it changes.",
     "An R1 power outage also drops its WAN; R3 then retains the R2 return path.",[
    ("Normal", "R1 active, R2 standby", "VIP: 192.168.50.1",BLUE),
    ("R1 powered off", "Both R1 links go down", "wait for HSRP hold",RED),
    ("R2 becomes active", "same VIP on LAN", "R3 returns via R2",VIOLET),
    ("Test again", "PC0 pings VIP and", "198.51.100.10",TEAL)],"failover flow")

a=Art("Lesson 18 | three IPv6 subnets, two routers",
      "PC0 uses SLAAC; PC1 has a known static IPv6 test address.",
      "IPv6 topology", "Use global 2001:db8:20::10 for the cross-LAN ping; fe80:: is link-local.",730)
a.zone(36,149,466,364,"LAN A  |  2001:db8:10::/64",BLUE)
a.zone(618,149,466,364,"LAN B  |  2001:db8:20::/64",TEAL)
for key,x,kind,name,detail,col,w in (("pc0",113,"pc","PC0","SLAAC / RA",BLUE,145),
                                     ("s1",280,"switch","SW1","Layer 2",TEAL,140),
                                     ("r1",449,"router","R1","G0/0: 10::1",BLUE,155),
                                     ("r2",671,"router","R2","G0/0: 20::1",VIOLET,155),
                                     ("s2",840,"switch","SW2","Layer 2",TEAL,140),
                                     ("pc1",1007,"pc","PC1","20::10 static",BLUE,145)):
    a.node(key,x,340,kind,name,detail,col,w)
for first,second in (("pc0","s1"),("s1","r1"),("r2","s2"),("s2","pc1")):
    a.edge(first,second)
a.edge("r1","r2","wan")
a.pill(560,230,"G0/1 <-> G0/1 : 2001:db8:12::/64",VIOLET,width=360)
a.pill(264,472,"R1 LL gateway: fe80::1",BLUE,width=295)
a.pill(855,472,"R2 LL gateway: fe80::2",TEAL,width=295)
a.callout(53,540,490,101,"First: static routes",["R1 -> 20::/64 via 12::2", "R2 -> 10::/64 via 12::1"],BLUE)
a.callout(578,540,490,101,"Then: OSPFv3 (remove static)",["Transit neighbors FULL", "Remote LAN routes marked O"],VIOLET)
save("lesson-18-ipv6-topology",a)

flow("lesson-18-ipv6-how-it-works","Lesson 18 | SLAAC is not a routing protocol",
     "First give hosts an address; then give routers a path to the remote /64.",
     "The static and OSPFv3 stages are alternatives: remove static before checking O routes.",[
    ("R1 advertises", "RA: 2001:db8:10::/64", "gateway: fe80::1",BLUE),
    ("PC0 autoconfigs", "global IPv6 varies", "read its ipconfig",TEAL),
    ("Static stage", "route to remote /64", "both directions needed",AMBER),
    ("OSPFv3 stage", "remove static routes", "neighbor FULL -> O route",VIOLET)],"address + route")

a=Art("Extra 07 | two IP phones, one CME router",
      "2811 Fa0/0 carries two tagged VLANs to SW1; phones register on voice VLAN 20.",
      "VoIP topology", "Phone0 PC port carries data VLAN 10; phone-to-phone calls stay inside this lab.",900)
a.node("r",560,200,"router","R1 / 2811 CME","Fa0/0.20: 192.168.20.1",BLUE,254)
a.node("sw",560,370,"switch","SW1 / 2960","Gi0/1 trunk: VLAN 10,20",TEAL,266)
a.zone(90,450,942,219,"Voice VLAN 20",VIOLET)
a.node("p0",282,564,"ipphone","Phone0 / 7960","DHCP / ext 1001*",VIOLET,201)
a.node("p1",837,564,"ipphone","Phone1 / 7960","DHCP / ext 1002*",VIOLET,201)
a.node("pc",282,762,"pc","PC0 (optional)","192.168.10.10/24",BLUE,205)
a.edge("r","sw","trunk")
a.edge("sw","p0")
a.edge("sw","p1")
a.edge("p0","pc")
a.pill(560,448,"Phone ports: access 10 + voice 20",VIOLET,width=346)
a.pill(560,647,"Voice 192.168.20.0/24  |  DHCP option 150 -> .20.1",VIOLET,width=523)
a.pill(285,685,"Phone PC port -> data VLAN 10",BLUE,width=316)
a.callout(520,699,537,106,"Registration order may swap extensions",[
    "Check phone screens before dialing 1001 -> 1002", "Power adapters may be needed in Packet Tracer"],AMBER)
save("extra-07-voip-topology",a)

flow("extra-07-voip-call-flow","Extra 07 | from power-on to ringing",
     "A DHCP address alone does not mean the IP phone is registered.",
     "* Phone0/Phone1 extension order depends on registration; check displays.",[
    ("Power + VLAN", "7960 joins VLAN 20", "SW phone port",BLUE),
    ("DHCP lease", "192.168.20.x", "option 150 -> CME IP",TEAL),
    ("Phone config", "TFTP from R1 .20.1", "CME learns the phone",VIOLET),
    ("Extension", "DN1: 1001 / DN2: 1002", "auto-assign order varies",AMBER),
    ("Call", "dial the other DN", "ring -> answer",TEAL)],"call setup")

a=Art("Extra 08 | one trusted DHCP server port",
      "DHCP Snooping filters server replies on untrusted ports; DAI uses bindings.",
      "L2 security", "Diagram shows the intended policy; Packet Tracer DAI enforcement can be incomplete.",860)
a.zone(55,147,1010,606,"VLAN 1  |  192.168.1.0/24  |  access ports",BLUE)
a.node("r",555,241,"router","R1 / legit DHCP","G0/0: 192.168.1.1",TEAL,224)
a.node("sw",555,421,"switch","SW1 / 2960","Snooping + DAI policy",BLUE,247)
a.node("pc0",182,626,"pc","PC0","DHCP / Fa0/1",BLUE,169)
a.node("pc1",469,626,"pc","PC1","DHCP / Fa0/2",BLUE,169)
a.node("bad",890,626,"server","RogueServer",".254 / Fa0/3",RED,200)
a.edge("r","sw")
for key in ("pc0","pc1","bad"):
    a.edge("sw",key)
a.pill(757,330,"Gi0/1: DHCP + ARP trusted",TEAL,width=302)
a.pill(816,521,"Fa0/3: untrusted",RED,width=206)
a.pill(556,730,"Only DHCP clients have IP + MAC + VLAN + port bindings",VIOLET,width=524)
save("extra-08-dhcp-dai-topology",a)

flow("extra-08-dhcp-dai-decision","Extra 08 | two different security checks",
     "Snooping filters DHCP server replies; DAI checks ARP sender identity.",
     "DAI drop is real IOS behavior; Packet Tracer may accept CLI but not enforce it.",[
    ("Server reply", "Gi0/1 trusted: allow", "Fa0/3 rogue: deny",BLUE),
    ("Lease binding", "learn client IP + MAC", "VLAN + incoming port",TEAL),
    ("Host ARP", "untrusted Fa0/1-2", "lookup sender in table",VIOLET),
    ("DAI decision*", "match -> forward", "mismatch -> drop",RED)],"security logic")


def main() -> int:
    parser=argparse.ArgumentParser(description="Build original SVG diagrams used by the Markdown guides")
    parser.add_argument("--check",action="store_true",help="fail if generated SVGs are missing or not up to date")
    args=parser.parse_args()
    if not args.check: OUT.mkdir(parents=True,exist_ok=True)
    stale=[]
    for name,art in sorted(DIAGRAMS.items()):
        file=OUT/f"{name}.svg"
        svg=art.render()
        if args.check:
            if not file.exists() or file.read_text(encoding="utf-8") != svg:stale.append(file.relative_to(ROOT).as_posix())
        elif not file.exists() or file.read_text(encoding="utf-8") != svg:
            file.write_text(svg,encoding="utf-8")
    print(f"{'Checked' if args.check else 'Generated'} {len(DIAGRAMS)} original SVG learning diagrams in {OUT.relative_to(ROOT)}")
    if stale:
        for f in stale: print(f"  STALE / MISSING: {f}")
        return 1
    return 0


if __name__=="__main__":
    raise SystemExit(main())
