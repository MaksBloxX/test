#!/usr/bin/env python3
"""Generate 26 original 30-second illustrated GIF walkthroughs (not PT recordings).

Build (optional Pillow + CairoSVG):
    python3 scripts/gif_walkthrough_generator.py
Check committed media without CairoSVG:
    python3 scripts/gif_walkthrough_generator.py --check

Each 12-frame GIF has a 2.5-second delay per frame = exactly 30 seconds
per loop. Original repository SVGs are the backgrounds, while a conceptual
six-stage timeline explains topology, configuration and verification. Lesson
06 switches SVG backgrounds between its separate switch-trunk and ROAS labs.
No network packets or Packet Tracer sessions are simulated by this script.
"""

from __future__ import annotations

import argparse
import hashlib
import io
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent
DEST = ROOT / "assets" / "gifs"
FRAME_COUNT = 12
FRAME_DELAY = 2500
SIZE = (960, 776)

# Priority in GIF-CATALOG.md means study importance, not confidence of simulator support.
# Six distinct stages per lab. Two timeline frames per stage make one 30s loop.
LABS = [
    ("lessons/01-router-cli-basics.md", "Router CLI and your first ping", "packet tracer router CLI modes first LAN ping", "P1", [
        ("Meet the devices", "One router, one switch and two PCs share a first LAN."),
        ("Wire the LAN", "Check green link lights before entering commands."),
        ("Configure R1", "Assign an interface IP address and issue no shutdown."),
        ("Address the PCs", "Use two different host IPs in the same subnet."),
        ("Send a ping", "PC0 to PC1 stays on the switch in one LAN."),
        ("Prove the result", "Check show ip interface brief and two-way ping."),
    ]),
    ("lessons/02-static-routing.md", "Two routers and static routes", "packet tracer two routers static route return path ping", "P1", [
        ("Two separate LANs", "A router and a local gateway serve each LAN."),
        ("Connect R1 to R2", "Use the dedicated transit subnet between routers."),
        ("Add the forward route", "R1 points to R2 for the remote destination LAN."),
        ("Add the return route", "R2 must also know the route back to PC0."),
        ("Inspect the tables", "Look for static S routes with show ip route."),
        ("Prove end-to-end", "Ping from PC0 to PC1, then test in reverse."),
    ]),
    ("lessons/03-dhcp.md", "Router DHCP and DORA", "packet tracer DHCP DORA discover offer request acknowledge", "P1", [
        ("Client requests IP", "A host without an address broadcasts Discover."),
        ("Server offers IP", "The router replies from its configured DHCP pool."),
        ("Client accepts", "Request selects an offer; ACK confirms the lease."),
        ("Protect reserved IPs", "Exclude the router gateway and static servers."),
        ("Inspect the lease", "Use show ip dhcp binding and PC ipconfig."),
        ("Test connectivity", "Ping the default gateway from a DHCP client."),
    ]),
    ("lessons/04-dns-http-server.md", "DNS name to HTTP page", "packet tracer DNS A record HTTP web server name resolution", "P1", [
        ("Plan the server", "Give DNS and web services a stable server IP."),
        ("Add the DNS record", "Map the chosen host name to the server IP."),
        ("Turn on HTTP", "The page is served only after HTTP is enabled."),
        ("Configure the client", "Set a DNS server address on the PC or DHCP pool."),
        ("Try name resolution", "Ping the server IP, then the chosen name."),
        ("Open the page", "Browse to the host name and inspect the response."),
    ]),
    ("lessons/05-vlan.md", "VLAN isolation", "packet tracer switch VLAN 10 VLAN 20 access ports isolation", "P1", [
        ("Create two VLANs", "A VLAN separates switch broadcast domains."),
        ("Assign access ports", "Place each PC port in its planned VLAN."),
        ("Test same-VLAN hosts", "Matching VLAN and subnet can communicate."),
        ("Test different VLANs", "Without routing, cross-VLAN ping should fail."),
        ("Inspect membership", "Use show vlan brief on the switch."),
        ("Explain the boundary", "A trunk alone does not route between VLANs."),
    ]),
    ("lessons/06-trunk-inter-vlan.md", "802.1Q trunk and ROAS", "packet tracer VLAN trunk 802.1Q router on a stick ping", "P1", [
        ("Part 2: create VLANs", "PC0 / PC2 share VLAN 10; PC1 / PC3 share VLAN 20."),
        ("Part 2: switch trunk", "SW1 to SW2 carries both VLANs; this does NOT route."),
        ("Part 3: NEW topology", "Replace SW2 uplink with R1 G0/0 on SW1 Gi0/1."),
        ("Part 3: set gateways", "R1 .10.254 and .20.254 serve distinct VLANs."),
        ("Part 3: trace the path", "PC0 VLAN 10 to PC1 VLAN 20 passes through R1."),
        ("Verify separately", "Part 2 PC0 to PC2; Part 3 PC0 to PC1."),
    ]),
    ("lessons/07-switching.md", "STP, port security and EtherChannel", "packet tracer spanning tree blocked port security etherchannel", "P1", [
        ("Prevent L2 loops", "STP blocks one redundant forwarding path."),
        ("Check root bridge", "Read spanning-tree role and port state."),
        ("Secure a host port", "Restrict allowed MAC addresses on an access port."),
        ("Bundle links", "EtherChannel combines compatible member ports."),
        ("Simulate a change", "Disconnect one member and inspect the result."),
        ("Verify each feature", "Use show spanning-tree and show etherchannel."),
    ]),
    ("lessons/08-final-project.md", "Office network capstone", "packet tracer office VLAN trunk DHCP DNS HTTP router on a stick", "P1", [
        ("Sketch the topology", "Label the router, switch, servers and clients."),
        ("Assign addresses", "Keep gateway and server IPs stable and unique."),
        ("Bring up services", "Configure DHCP, DNS and the required application."),
        ("Check L2 and L3", "Verify VLAN ports, links and gateway reachability."),
        ("Run user tests", "Use ping, name lookup and the service client."),
        ("Record evidence", "Save a working .pkt only after real PT testing."),
    ]),
    ("lessons/09-real-hardware.md", "Physical network hardware", "router switch SFP patch panel fiber rack packet tracer equivalent", "P2", [
        ("Identify the rack", "Locate the patch panel, switch and router."),
        ("Follow a cable", "Trace from endpoint to panel to switch port."),
        ("Match media", "Copper and fiber need different ports and optics."),
        ("Find the uplink", "An SFP module connects supported fiber links."),
        ("Compare the simulator", "A Packet Tracer icon is not physical wiring."),
        ("Check interfaces", "Inspect port labels, link light and speed."),
    ]),
    ("lessons/10-practice-lab.md", "Ten independent practice tasks", "packet tracer networking practice ten tasks verify before solution", "P2", [
        ("Read the task", "Choose a simple or a harder network challenge."),
        ("Draw the topology", "Plan the IPs and ports before configuration."),
        ("Attempt it yourself", "Do not open the solution before testing."),
        ("Capture evidence", "Use ping or show commands named in the task."),
        ("Open a hint", "Only then compare the hidden answer."),
        ("Repeat cleanly", "Rebuild from memory and save your own .pkt."),
    ]),
    ("lessons/11-practice-list.md", "Practice ladder and checklist", "CCNA packet tracer practice list beginner intermediate advanced", "P2", [
        ("Pick a level", "Start with LAN basics, then routing and services."),
        ("Set a goal", "Write down what the network must prove."),
        ("Build the lab", "Address each device and configure one layer at a time."),
        ("Run the checks", "Capture ping and show output rather than guessing."),
        ("Fix one failure", "Change one thing and repeat the exact test."),
        ("Log progress", "Mark completed tasks; advance when repeatable."),
    ]),
    ("lessons/12-problem-solve.md", "Network detective: nine cases", "packet tracer nine troubleshooting problems ping show commands", "P1", [
        ("Observe the symptom", "Read the failed ping or service behavior."),
        ("Localize the fault", "Start at the endpoint, then links and gateway."),
        ("Inspect state", "Use the appropriate show commands on each device."),
        ("Change one cause", "Repair the actual configuration mismatch."),
        ("Repeat the failure test", "Pass the same test that originally failed."),
        ("Explain the fix", "Record what was wrong and why the repair works."),
    ]),
    ("lessons/13-dynamic-routing-ospf.md", "RIPv2 and OSPFv2 failover", "packet tracer OSPFv2 RIP routing triangle failover neighbor", "P1", [
        ("Build three routers", "Give each transit link its own subnet."),
        ("Advertise prefixes", "Configure RIPv2 or OSPFv2 for the correct links."),
        ("Check adjacency", "Look for OSPF neighbors and learned routes."),
        ("Run a baseline ping", "Confirm both forward and return paths."),
        ("Drop a link", "Disconnect a primary path and wait for convergence."),
        ("Check the alternate", "Observe new routes and restored ping."),
    ]),
    ("lessons/14-wireless-lan.md", "Home Wi-Fi and enterprise WLC", "packet tracer WRT300N WPA2 WLC LAP CAPWAP wireless", "P1", [
        ("Home Wi-Fi first", "Set an SSID and WPA2 passphrase on WRT300N."),
        ("Connect a client", "Give the laptop a compatible wireless adapter."),
        ("Verify DHCP", "Check its address and ping the wireless gateway."),
        ("Add enterprise gear", "Compare the WLC and LAP management path."),
        ("Inspect association", "Check join, SSID, security and client IP."),
        ("Compare the designs", "A home router and WLC solve different needs."),
    ]),
    ("lessons/15-ssh-syslog-ntp.md", "SSH, NTP and Syslog", "packet tracer ssh v2 ntp syslog device hardening", "P1", [
        ("Harden access", "Create a local login and protect the VTY lines."),
        ("Enable SSHv2", "Generate RSA keys after setting a domain name."),
        ("Test remote login", "Use SSH; avoid the unencrypted Telnet path."),
        ("Synchronize time", "Check the NTP server and device clock."),
        ("Send logs", "Set the Syslog host and produce a test event."),
        ("Verify evidence", "Inspect SSH, clock and captured Syslog entries."),
    ]),
    ("lessons/16-multilayer-switch-svi.md", "3560 SVI inter-VLAN routing", "packet tracer 3560 multilayer switch SVI ip routing VLAN", "P1", [
        ("Wire four PCs", "All access ports terminate on one 3560 switch."),
        ("Create two VLANs", "Assign hosts to VLAN 10 or VLAN 20."),
        ("Configure SVIs", "Vlan10 and Vlan20 each need a gateway address."),
        ("Turn on L3", "Enable ip routing on the multilayer switch."),
        ("Check each VLAN", "Inspect show ip interface brief and show vlan."),
        ("Ping across", "Reach a host in the other VLAN without a router."),
    ]),
    ("lessons/17-hsrp-gateway-redundancy.md", "HSRP gateway failover", "packet tracer HSRP virtual gateway active standby power off return", "P1", [
        ("Shared virtual IP", "PC0 uses 192.168.50.1, not a router's real IP."),
        ("Elect the active router", "R1 priority 120 beats R2 priority 100."),
        ("Add WAN and replies", "Both paths and the R3 return routes matter."),
        ("Prove baseline", "Read show standby before pinging R3 loopback."),
        ("Power off R1", "Test full failure, not LAN-only shutdown."),
        ("Verify recovery", "R2 becomes active; remote ping resumes."),
    ]),
    ("lessons/18-ipv6-slaac-routing.md", "IPv6 SLAAC and OSPFv3", "packet tracer IPv6 router advertisement SLAAC static OSPFv3", "P1", [
        ("Three distinct /64s", "LAN A, transit and LAN B use separate prefixes."),
        ("Learn an address", "R1 advertises LAN A; PC0 uses Auto Config."),
        ("Set the test target", "PC1 uses known static 2001:db8:20::10."),
        ("Test static routing", "Add BOTH forward and return IPv6 routes."),
        ("Switch to OSPFv3", "Remove the static routes and form adjacency."),
        ("Verify O routes", "Check show ipv6 route and ping both ways."),
    ]),
    ("Extras/ftp-server-lab.md", "FTP upload and download", "packet tracer FTP server put get user permissions remote subnet", "P2", [
        ("Give the server an IP", "Keep server address and gateway stable."),
        ("Enable FTP", "Create a user with appropriate permissions."),
        ("Check reachability", "Ping the server before testing the app."),
        ("Log in", "Use the PC's FTP client and server credentials."),
        ("Transfer a file", "Try put and get; inspect remote files."),
        ("Check failures", "Review route, service state and permission flags."),
    ]),
    ("Extras/email-server-lab.md", "SMTP send and POP3 receive", "packet tracer email server SMTP POP3 two subnet send receive", "P2", [
        ("Plan two LANs", "Route between the sender, server and receiver."),
        ("Enable mail services", "Configure SMTP and POP3 on the server."),
        ("Add domain and users", "Create distinct accounts for both PCs."),
        ("Configure clients", "Match username, domain and incoming server."),
        ("Send a message", "PC0 submits mail over SMTP."),
        ("Receive and verify", "PC1 fetches it via POP3; inspect Inbox."),
    ]),
    ("Extras/office-shared-printer-lab.md", "Office shared printer", "packet tracer office printer static IP DHCP excluded address print test", "P2", [
        ("Address the printer", "Use a static IP outside the DHCP client range."),
        ("Protect the lease pool", "Exclude the printer and gateway addresses."),
        ("Connect office PCs", "Give clients valid leases and default gateways."),
        ("Reach the printer", "Ping its static address from each PC."),
        ("Send a job", "Use the Packet Tracer print function if present."),
        ("Troubleshoot", "Check cabling, IP overlap and service status."),
    ]),
    ("Extras/ip-subnet-tester-lab.md", "Subnet boundary tester", "packet tracer subnet tester /24 /26 ping different subnets", "P1", [
        ("Start with /24", "Hosts in one subnet can exchange local frames."),
        ("Split into /26", "Compare the new network and broadcast bounds."),
        ("Test same subnet", "A switch can forward between matching hosts."),
        ("Test other subnets", "Different networks need a router/gateway."),
        ("Reject invalid hosts", "Network and broadcast addresses are not hosts."),
        ("Check your math", "Confirm with subnet_calculator.py and ping."),
    ]),
    ("Extras/network-topologies-lab.md", "Six network topologies", "packet tracer bus star ring mesh tree hybrid six topologies", "P2", [
        ("Compare six designs", "Bus, star, ring, mesh, tree and hybrid."),
        ("Open one .pkt", "Start with an included topology project."),
        ("Trace a packet", "Use Simulation Mode to follow a PDU."),
        ("Break one link", "Observe the effect of failure and alternate paths."),
        ("Count mesh links", "A full mesh of N nodes has N(N-1)/2 links."),
        ("Explain the tradeoff", "Compare resilience, cable count and cost."),
    ]),
    ("Extras/broken-labs-challenge.md", "Six broken network challenges", "packet tracer broken network detective six IOS fault scripts", "P1", [
        ("Pick a case", "Open the linked base .pkt before applying a fault."),
        ("Insert the fault", "Paste its .ios script on the named device."),
        ("Observe failure", "Record the ping or service error first."),
        ("Gather evidence", "Use interface, VLAN, routing and DHCP checks."),
        ("Repair one cause", "Make the smallest justified change."),
        ("Prove the fix", "Repeat the original failure test and log result."),
    ]),
    ("Extras/voip-ip-telephony-lab.md", "CME voice and data VLANs", "packet tracer Cisco 2811 7960 CME option 150 voice VLAN call", "P2", [
        ("Prepare the phones", "Power both phones and connect their Switch port."),
        ("Separate traffic", "Voice VLAN 20 and data VLAN 10 share a trunk."),
        ("Deliver DHCP", "Option 150 points phones at CME/TFTP on R1."),
        ("Assign extensions", "Check registrations before using 1001/1002."),
        ("Place a call", "Dial the other phone's displayed extension."),
        ("Verify honestly", "Call GUI state is a simulator observation, not audio."),
    ]),
    ("Extras/dhcp-snooping-dai-lab.md", "DHCP Snooping and DAI policy", "packet tracer DHCP snooping DAI rogue DHCP ARP inspection binding", "P1", [
        ("Trust one uplink", "Only the legitimate router-facing Gi0/1 is trusted."),
        ("Keep hosts untrusted", "Client and rogue-server ports remain untrusted."),
        ("Learn DHCP bindings", "Check client IP, MAC, VLAN and switch port."),
        ("Test rogue offers", "Compare leases before and after rogue DHCP."),
        ("Try optional DAI", "Never enable it before confirmed bindings."),
        ("Report limits", "PT may accept DAI CLI without filtering ARP."),
    ]),
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def entry_path(source: str) -> Path:
    family, filename = source.split("/", 1)
    if family == "lessons":
        return DEST / filename.replace(".md", ".gif")
    extra_order = [entry[0] for entry in LABS if entry[0].startswith("Extras/")]
    return DEST / f"extra-{extra_order.index(source)+1:02}-{filename.replace('.md', '.gif')}"


def first_svg(source: str) -> Path:
    doc = ROOT / source
    matches = re.findall(r"!\[[^\]]*\]\(([^)]+\.svg)\)", doc.read_text(encoding="utf-8"))
    if not matches:
        raise ValueError(f"No SVG available for {source}")
    return (doc.parent / matches[0]).resolve()


def followup_svg(source: str) -> Path | None:
    """The switch-trunk and ROAS builds in Lesson 06 have different topologies."""
    if source != "lessons/06-trunk-inter-vlan.md":
        return None
    doc = ROOT / source
    images = re.findall(r"!\[[^\]]*\]\(([^)]+\.svg)\)", doc.read_text(encoding="utf-8"))
    if len(images) < 2:
        raise ValueError("Lesson 06 needs both separate topology diagrams")
    return (doc.parent / images[1]).resolve()


def metadata() -> list[dict]:
    records = []
    for source, title, search, priority, _ in LABS:
        svg = first_svg(source)
        record = {
            "source": source,
            "source_svg": svg.relative_to(ROOT).as_posix(),
            "source_sha256": sha256(svg),
            "gif": entry_path(source).relative_to(ROOT).as_posix(),
            "topic": title,
            "gif_search_name": search,
            "importance": priority,
            "frames": FRAME_COUNT,
            "duration_ms": FRAME_COUNT * FRAME_DELAY,
        }
        if extra := followup_svg(source):
            record["followup_svg"] = extra.relative_to(ROOT).as_posix()
            record["followup_sha256"] = sha256(extra)
        records.append(record)
    return records


def build() -> None:
    try:
        import cairosvg
        from PIL import Image, ImageDraw, ImageFont
    except ImportError as exc:
        raise SystemExit("Install requirements-docs.txt for Pillow and CairoSVG to generate GIFs") from exc
    DEST.mkdir(parents=True, exist_ok=True)
    regular = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    bold = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    title_font = ImageFont.truetype(bold, 25)
    body_font = ImageFont.truetype(regular, 18)
    small_font = ImageFont.truetype(bold, 13)
    notice_height = 32
    import xml.etree.ElementTree as ET

    def background(svg: Path):
        svg_root = ET.parse(svg).getroot()
        source_width, source_height = float(svg_root.get("width")), float(svg_root.get("height"))
        caption_top, notice_height = SIZE[1] - 128, 32
        max_height = caption_top - notice_height - 16
        render_width = min(SIZE[0], int(max_height * source_width / source_height))
        png = cairosvg.svg2png(url=str(svg), output_width=render_width)
        base = Image.open(io.BytesIO(png)).convert("RGB")
        canvas = Image.new("RGB", SIZE, "#F8FAFD")
        canvas.paste(base, ((SIZE[0]-base.width)//2,
                            notice_height + (caption_top-notice_height-base.height)//2))
        return canvas

    for source, title, _search, _priority, stages in LABS:
        initial_bg = background(first_svg(source))
        extra_bg = background(extra) if (extra := followup_svg(source)) else initial_bg
        frames_rgb = []
        for frame_id in range(FRAME_COUNT):
            stage_id = frame_id // 2
            stage_title, stage_note = stages[stage_id]
            # Switch-to-switch trunk (parts 1-2) and ROAS (parts 3-6) are different builds.
            frame = (initial_bg if stage_id < 2 else extra_bg).copy()
            draw = ImageDraw.Draw(frame)
            top = SIZE[1]-128
            draw.rectangle((0, top, SIZE[0], SIZE[1]), fill="#142B46")
            draw.rectangle((0, top, SIZE[0], top+5), fill="#087F6C")
            draw.text((25, top+17), stage_title, font=title_font, fill="#FFFFFF")
            draw.text((25, top+59), stage_note, font=body_font, fill="#D4E3EF")
            draw.text((SIZE[0]-195, top+20), f"STEP {stage_id+1:02}/06", font=small_font, fill="#FFCF7A")
            # Graphic timeline is a conceptual progress indicator, NOT a packet trace.
            x0, x1, line_y = 28, SIZE[0]-28, SIZE[1]-15
            draw.line((x0, line_y, x1, line_y), fill="#3E6478", width=5)
            progress = frame_id/(FRAME_COUNT-1)
            x = int(x0+(x1-x0)*progress)
            draw.line((x0, line_y, x, line_y), fill="#49D3B1", width=5)
            draw.ellipse((x-8,line_y-8,x+8,line_y+8),fill="#FFBE51")
            draw.rectangle((0, 0, SIZE[0], notice_height), fill="#E7F0FA")
            draw.text((25, 8), "ILLUSTRATED WALKTHROUGH  |  NOT PACKET TRACER FOOTAGE",
                      font=small_font, fill="#142B46")
            frames_rgb.append(frame)
        # One shared palette avoids color flicker; optimization stores frame deltas.
        palette = frames_rgb[0].quantize(colors=128, method=Image.Quantize.MEDIANCUT)
        frames = [f.quantize(palette=palette, dither=Image.Dither.NONE) for f in frames_rgb]
        out = entry_path(source)
        frames[0].save(out, format="GIF", save_all=True, append_images=frames[1:], loop=0,
                       duration=FRAME_DELAY, optimize=True, disposal=1)
        print(f"{out.relative_to(ROOT)}   {out.stat().st_size/1024:.0f} KiB")
    payload = metadata()
    for item in payload:
        item["gif_sha256"] = sha256(ROOT / item["gif"])
    (DEST / "manifest.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    check()


def check() -> None:
    try:
        from PIL import Image
    except ImportError as exc:
        raise SystemExit("Install requirements-docs.txt for Pillow GIF structural validation") from exc
    saved = json.loads((DEST / "manifest.json").read_text(encoding="utf-8"))
    current = metadata()
    if len(saved) != 26 or len(current) != 26:
        raise SystemExit(f"Expected 26 lab GIFs, found {len(saved)} saved and {len(current)} source guides")
    for record, expected in zip(saved, current):
        for key, value in expected.items():
            if record[key] != value:
                raise SystemExit(f"Stale GIF manifest: {record['gif']} field {key}")
        gif_path = ROOT / record["gif"]
        if not gif_path.is_file() or record["gif_sha256"] != sha256(gif_path):
            raise SystemExit(f"Missing or changed GIF: {gif_path}")
        with Image.open(gif_path) as img:
            if img.size != SIZE or img.n_frames != FRAME_COUNT or not img.info.get("loop") == 0:
                raise SystemExit(f"GIF size/frame/loop mismatch: {gif_path}")
            duration = 0
            for frame in range(img.n_frames):
                img.seek(frame)
                duration += img.info.get("duration", 0)
            if duration != 30000:
                raise SystemExit(f"GIF duration {duration} ms (expected 30000): {gif_path}")
    print("Verified 26 illustrated 30-second looping GIFs (312 frames, source hashes and timestamps).")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Verify committed GIF metadata, frames, duration and source hashes")
    args = parser.parse_args()
    check() if args.check else build()


if __name__ == "__main__":
    main()
