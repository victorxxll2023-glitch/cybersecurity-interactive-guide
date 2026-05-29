#!/usr/bin/env python3
"""
recon.py - Recon e identificacao de vulnerabilidades (uso EDUCACIONAL).

USO:
  ./recon.py <alvo>             # scan rapido (recon: portas, servicos, headers)
  ./recon.py <alvo> --full      # scan completo (+ nmap vuln scripts + nikto)
  ./recon.py <alvo> --out DIR   # diretorio de saida (padrao: reports/)

EXEMPLOS:
  ./recon.py scanme.nmap.org
  ./recon.py 192.168.1.10 --full

AVISO - USO LEGAL APENAS (Lei 12.737/2012 - Brasil):
  - laboratorios (TryHackMe, HackTheBox, suas VMs)
  - sistemas proprios
  - pentests com autorizacao por escrito

DEPENDENCIAS (instale o que faltar; o script pula o que nao estiver presente):
  sudo apt install nmap nikto whatweb dnsutils whois curl
"""

import argparse
import datetime
import pathlib
import re
import shutil
import socket
import subprocess
import sys

NMAP_QUICK = ["nmap", "-Pn", "-sV", "-sC", "--top-ports", "100", "-T4"]
NMAP_FULL_PORTS = ["nmap", "-Pn", "-sV", "-sC", "-p-", "-T4"]
NMAP_VULN = ["nmap", "-Pn", "--script", "vuln", "-T4"]

SECURITY_HEADERS = [
    "strict-transport-security",
    "content-security-policy",
    "x-frame-options",
    "x-content-type-options",
    "referrer-policy",
    "permissions-policy",
]

BANNER = """\
============================================================
RECON ASSISTIDO - uso legal e autorizado APENAS
Alvo: {target}
Modo: {mode}
============================================================
Esta ferramenta executa varreduras de rede e web (nmap,
curl, nikto, whatweb). Pratique somente em:
  - laboratorios (TryHackMe, HTB) ou suas VMs
  - sistemas proprios
  - pentests com autorizacao por escrito
Lei 12.737/2012 (Brasil) criminaliza acesso/escaneamento
nao autorizado.
============================================================
"""


def run(cmd, timeout=600):
    print(f"\n$ {' '.join(cmd)}")
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return r.returncode, r.stdout, r.stderr
    except FileNotFoundError:
        return 127, "", f"comando nao encontrado: {cmd[0]}"
    except subprocess.TimeoutExpired:
        return 124, "", f"timeout apos {timeout}s"


def section(title, body, lang=""):
    body = (body or "").strip()
    if not body:
        return ""
    fence = f"```{lang}" if lang else "```"
    return f"\n## {title}\n\n{fence}\n{body}\n```\n"


def resolve(host):
    try:
        return socket.gethostbyname(host)
    except Exception:
        return None


def confirm(target, mode):
    print(BANNER.format(target=target, mode=mode))
    if not sys.stdin.isatty():
        print("stdin nao-interativo: use --yes apenas em ambiente autorizado.")
        sys.exit(1)
    ans = input(
        "Tenho autorizacao para escanear este alvo. Digite SIM para continuar: "
    ).strip()
    if ans != "SIM":
        print("Cancelado.")
        sys.exit(1)


def dns_block(host):
    out_parts = []
    if shutil.which("dig"):
        rc, out, _ = run(["dig", "+short", host])
        out_parts.append(section("DNS A (dig +short)", out))
        rc, out, _ = run(["dig", "+short", "-t", "MX", host])
        out_parts.append(section("DNS MX", out))
    elif shutil.which("host"):
        rc, out, _ = run(["host", host])
        out_parts.append(section("DNS (host)", out))
    return out_parts


def whois_block(host):
    if not shutil.which("whois"):
        return []
    rc, out, _ = run(["whois", host], timeout=30)
    if not out:
        return []
    keywords = (
        "domain", "registr", "creat", "updat", "expir",
        "name server", "org", "country", "status",
    )
    short = "\n".join(
        line for line in out.splitlines()
        if any(k in line.lower() for k in keywords)
    )
    return [section("whois (resumo)", short[:1500])]


def http_block(host):
    if not shutil.which("curl"):
        return []
    parts = []
    for scheme in ("https", "http"):
        url = f"{scheme}://{host}"
        rc, out, _ = run([
            "curl", "-sIL", "--max-time", "15",
            "-A", "Mozilla/5.0 recon.py/edu", url,
        ])
        if rc != 0 or not out:
            continue
        parts.append(section(f"HTTP headers - {url}", out))
        low = out.lower()
        checks = []
        for h in SECURITY_HEADERS:
            tag = "[+] presente" if h in low else "[!] AUSENTE "
            checks.append(f"{tag} - {h}")
        m = re.search(r"^server:\s*(.+)$", out, re.I | re.M)
        if m:
            checks.append(f"[i] Server header: {m.group(1).strip()}")
        parts.append(section(f"Cabecalhos de seguranca - {scheme}", "\n".join(checks)))
        break
    return parts


def nmap_block(host, full):
    if not shutil.which("nmap"):
        return ["\n## nmap\n\n> nmap nao instalado. `sudo apt install nmap`\n"]
    parts = []
    cmd = (NMAP_FULL_PORTS if full else NMAP_QUICK) + [host]
    rc, out, _ = run(cmd, timeout=1800 if full else 300)
    label = "todos os portos + scripts default" if full else "top 100 portos + scripts default"
    parts.append(section(f"nmap - {label}", out))
    if full:
        rc, out, _ = run(NMAP_VULN + [host], timeout=1800)
        parts.append(section("nmap - scripts vuln (NSE)", out))
    return parts


def whatweb_block(host):
    if not shutil.which("whatweb"):
        return []
    rc, out, _ = run(["whatweb", "--no-errors", "-a", "3", host])
    return [section("whatweb (tecnologias detectadas)", out)]


def nikto_block(host):
    if not shutil.which("nikto"):
        return ["\n## nikto\n\n> nikto nao instalado. `sudo apt install nikto`\n"]
    rc, out, _ = run(
        ["nikto", "-h", host, "-Tuning", "x", "-maxtime", "10m"],
        timeout=900,
    )
    return [section("nikto (varredura web)", out)]


def main():
    ap = argparse.ArgumentParser(
        description="Recon assistido educacional (Blue Team).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    ap.add_argument("target", help="IP, hostname ou URL")
    ap.add_argument("--full", action="store_true",
                    help="scan completo: todos os portos + nmap vuln scripts + nikto")
    ap.add_argument("--out", default="reports",
                    help="diretorio do relatorio (padrao: reports/)")
    ap.add_argument("--yes", action="store_true",
                    help="pula a confirmacao interativa (use so em ambiente autorizado)")
    args = ap.parse_args()

    raw = args.target.strip()
    host = re.sub(r"^https?://", "", raw, flags=re.I).split("/")[0].split(":")[0]
    if not host:
        print("Alvo invalido.")
        sys.exit(2)

    mode = "completo (+vuln scripts +nikto)" if args.full else "rapido (recon)"
    if not args.yes:
        confirm(host, mode)

    ts = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    out_dir = pathlib.Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    report_path = out_dir / f"{host}-{ts}.md"

    ip = resolve(host)
    parts = [
        f"# Recon - {host}\n",
        f"- Data: {ts}",
        f"- Modo: {mode}",
        f"- IP resolvido: `{ip or 'nao resolvido'}`",
        "",
        "> Relatorio gerado por recon.py. Use apenas em alvos autorizados.",
    ]

    parts.extend(dns_block(host))
    parts.extend(whois_block(host))
    parts.extend(http_block(host))
    parts.extend(nmap_block(host, args.full))
    parts.extend(whatweb_block(host))
    if args.full:
        parts.extend(nikto_block(host))

    parts.append("\n---\n\n_Revise o relatorio antes de compartilhar - pode conter dados sensiveis._\n")
    report_path.write_text("\n".join(parts), encoding="utf-8")
    print(f"\nRelatorio salvo em: {report_path}")


if __name__ == "__main__":
    main()
