#!/usr/bin/env python3
"""
menu.py - Pentest assistido interativo (uso educacional).

Voce escolhe a ferramenta no menu; o script pede SO o que falta
(alvo, porta, URL, wordlist), mostra o comando, pede confirmacao
e executa, gravando tudo num relatorio Markdown.

USO LEGAL APENAS - Lei 12.737/2012 (Brasil):
  - laboratorios (TryHackMe, HackTheBox, suas VMs)
  - sistemas proprios
  - pentests com autorizacao por escrito

DEPENDENCIAS (instale o que faltar; ferramenta ausente e' avisada):
  sudo apt install nmap nikto whatweb gobuster hydra sqlmap dnsutils whois curl
"""

import argparse
import datetime
import pathlib
import re
import shlex
import socket
import subprocess
import sys

STATE = {"target": None, "target_raw": None, "report": None}

LEGAL_BANNER = """
==================================================================
PENTEST ASSISTIDO - USO LEGAL E AUTORIZADO APENAS
==================================================================
Pratique somente em:
  - laboratorios (TryHackMe, HackTheBox, suas VMs)
  - sistemas proprios
  - pentests com autorizacao por escrito
Lei 12.737/2012 (Brasil) criminaliza acesso/escaneamento nao
autorizado. Voce e' responsavel pelo uso desta ferramenta.
==================================================================
"""

MENU = """
==================================================================
PENTEST ASSISTIDO - menu interativo
==================================================================
Alvo: {target}
Relatorio: {report}

  [1]  Definir/trocar alvo

  Recon
  [2]  DNS (dig A + MX)
  [3]  WHOIS
  [4]  HTTP headers (curl) + analise de cabecalhos de seguranca
  [5]  whatweb (deteccao de tecnologias)

  Portas / vulnerabilidades de rede
  [6]  nmap rapido (top 100 portas + scripts default)
  [7]  nmap completo (-p- todos os portos)
  [8]  nmap vuln (--script vuln, identifica CVEs conhecidos)

  Web
  [9]  nikto (varredura de vulnerabilidades web)
  [10] gobuster dir (enumeracao de diretorios)
  [11] sqlmap (teste de SQLi em URL com parametro)

  Credenciais (USE APENAS EM LAB / SISTEMA PROPRIO)
  [12] hydra SSH (forca bruta)

  Combos
  [13] Pipeline recon completo (rodar 2 -> 6 em sequencia)

  [14] Ver relatorio acumulado
  [0]  Sair
==================================================================
"""


def ask(prompt, default=None):
    if default is not None:
        s = input(f"{prompt} [{default}]: ").strip()
        return s or default
    return input(f"{prompt}: ").strip()


def need_target():
    if not STATE["target"]:
        print("\n[!] Nenhum alvo definido. Use a opcao [1] primeiro.")
        return False
    return True


def set_target():
    t = ask("Alvo (IP, hostname ou URL)")
    if not t:
        print("Cancelado.")
        return
    host = re.sub(r"^https?://", "", t, flags=re.I).split("/")[0].split(":")[0]
    STATE["target"] = host
    STATE["target_raw"] = t
    try:
        ip = socket.gethostbyname(host)
        print(f"[+] {host} -> {ip}")
    except Exception:
        print(f"[!] Nao resolveu {host} via DNS.")


def confirm_cmd(cmd):
    rendered = " ".join(shlex.quote(c) for c in cmd)
    print(f"\nComando: $ {rendered}")
    a = input("Executar? (s/N): ").strip().lower()
    return a in ("s", "sim", "y", "yes")


def log_section(title, body):
    if not STATE["report"]:
        return
    ts = datetime.datetime.now().strftime("%H:%M:%S")
    body = (body or "").strip() or "(sem saida)"
    with open(STATE["report"], "a", encoding="utf-8") as f:
        f.write(f"\n## [{ts}] {title}\n\n```\n{body}\n```\n")


def run_and_log(cmd, title, timeout=900):
    if not confirm_cmd(cmd):
        print("Pulado.")
        return
    print("\n--- saida ---")
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        if r.stdout:
            print(r.stdout)
        if r.stderr.strip():
            print("[stderr]", r.stderr[:800])
        body = r.stdout + (("\n[stderr]\n" + r.stderr) if r.stderr.strip() else "")
        log_section(title, body)
    except FileNotFoundError:
        msg = f"[!] '{cmd[0]}' nao instalado."
        print(msg)
        log_section(title, msg)
    except subprocess.TimeoutExpired:
        msg = f"[!] Timeout apos {timeout}s."
        print(msg)
        log_section(title, msg)
    except KeyboardInterrupt:
        msg = "[!] Interrompido (Ctrl+C)."
        print(msg)
        log_section(title, msg)


def need_wordlist(path):
    if pathlib.Path(path).exists():
        return True
    print(f"[!] Wordlist nao encontrada: {path}")
    print("    Tente: /usr/share/wordlists/dirb/common.txt")
    print("    Ou:    /usr/share/wordlists/rockyou.txt (pacote wordlists)")
    return False


# ---------- Ferramentas ----------

def tool_dns():
    if not need_target():
        return
    t = STATE["target"]
    run_and_log(["dig", "+short", t], f"dig A {t}", timeout=30)
    run_and_log(["dig", "+short", "-t", "MX", t], f"dig MX {t}", timeout=30)


def tool_whois():
    if not need_target():
        return
    run_and_log(["whois", STATE["target"]], f"whois {STATE['target']}", timeout=30)


def tool_http_headers():
    if not need_target():
        return
    scheme = ask("Esquema (http/https)", "https")
    url = f"{scheme}://{STATE['target']}"
    run_and_log(
        ["curl", "-sIL", "--max-time", "15", "-A",
         "Mozilla/5.0 menu.py/edu", url],
        f"curl headers {url}",
        timeout=30,
    )


def tool_whatweb():
    if not need_target():
        return
    run_and_log(
        ["whatweb", "--no-errors", "-a", "3", STATE["target"]],
        f"whatweb {STATE['target']}",
        timeout=120,
    )


def tool_nmap_quick():
    if not need_target():
        return
    run_and_log(
        ["nmap", "-Pn", "-sV", "-sC", "--top-ports", "100", "-T4", STATE["target"]],
        f"nmap quick {STATE['target']}",
        timeout=600,
    )


def tool_nmap_full():
    if not need_target():
        return
    run_and_log(
        ["nmap", "-Pn", "-sV", "-sC", "-p-", "-T4", STATE["target"]],
        f"nmap full {STATE['target']}",
        timeout=1800,
    )


def tool_nmap_vuln():
    if not need_target():
        return
    run_and_log(
        ["nmap", "-Pn", "--script", "vuln", "-T4", STATE["target"]],
        f"nmap vuln {STATE['target']}",
        timeout=1800,
    )


def tool_nikto():
    if not need_target():
        return
    scheme = ask("Esquema (http/https)", "https")
    url = f"{scheme}://{STATE['target']}"
    run_and_log(
        ["nikto", "-h", url, "-Tuning", "x", "-maxtime", "10m"],
        f"nikto {url}",
        timeout=900,
    )


def tool_gobuster():
    if not need_target():
        return
    scheme = ask("Esquema (http/https)", "https")
    url = f"{scheme}://{STATE['target']}"
    wordlist = ask("Wordlist", "/usr/share/wordlists/dirb/common.txt")
    if not need_wordlist(wordlist):
        return
    extensions = ask("Extensoes (vazio para nenhuma; ex: php,html,txt)", "")
    cmd = ["gobuster", "dir", "-u", url, "-w", wordlist, "-q"]
    if extensions:
        cmd += ["-x", extensions]
    run_and_log(cmd, f"gobuster {url}", timeout=1200)


def tool_sqlmap():
    if not need_target():
        return
    print("\nAVISO: sqlmap executa testes ativos de SQL Injection.")
    print("       Use APENAS em alvo com autorizacao por escrito.")
    url = ask(
        "URL completa com parametro (ex: http://site/page.php?id=1)",
        STATE.get("target_raw") or "",
    )
    if not url or "?" not in url:
        print("[!] URL precisa conter parametro (ex: ?id=1).")
        return
    extras = ask("Opcoes extras", "--batch --level=2 --risk=1")
    cmd = ["sqlmap", "-u", url] + shlex.split(extras)
    run_and_log(cmd, f"sqlmap {url}", timeout=1800)


def tool_hydra_ssh():
    if not need_target():
        return
    print("\nAVISO: hydra faz forca bruta de credenciais.")
    print("       Use APENAS em laboratorios / sistemas seus.")
    user = ask("Usuario unico OU caminho para lista de usuarios")
    if not user:
        return
    wordlist = ask("Wordlist de senhas", "/usr/share/wordlists/rockyou.txt")
    if not need_wordlist(wordlist):
        return
    user_flag = ["-L", user] if pathlib.Path(user).exists() else ["-l", user]
    port = ask("Porta SSH", "22")
    cmd = ["hydra", "-t", "4"] + user_flag + ["-P", wordlist, "-s", port,
                                              f"ssh://{STATE['target']}"]
    run_and_log(cmd, f"hydra ssh {STATE['target']}", timeout=1800)


def tool_pipeline():
    if not need_target():
        return
    print("\nPipeline recon: DNS -> WHOIS -> headers -> whatweb -> nmap rapido.")
    for fn in (tool_dns, tool_whois, tool_http_headers, tool_whatweb, tool_nmap_quick):
        fn()


def view_report():
    rp = STATE.get("report")
    if rp and pathlib.Path(rp).exists():
        print("\n" + pathlib.Path(rp).read_text(encoding="utf-8"))
    else:
        print("(relatorio vazio)")


ACTIONS = {
    "1": set_target,
    "2": tool_dns,
    "3": tool_whois,
    "4": tool_http_headers,
    "5": tool_whatweb,
    "6": tool_nmap_quick,
    "7": tool_nmap_full,
    "8": tool_nmap_vuln,
    "9": tool_nikto,
    "10": tool_gobuster,
    "11": tool_sqlmap,
    "12": tool_hydra_ssh,
    "13": tool_pipeline,
    "14": view_report,
}


def main():
    ap = argparse.ArgumentParser(description="Pentest assistido interativo.")
    ap.add_argument("--out", default="reports", help="diretorio dos relatorios")
    ap.add_argument("--target", help="ja define o alvo (pula opcao [1])")
    args = ap.parse_args()

    print(LEGAL_BANNER)
    if not sys.stdin.isatty():
        print("[!] stdin nao-interativo. Use 'python3 -i menu.py' ou execute num terminal.")
        sys.exit(1)
    ok = input("Confirmo autorizacao para os testes que farei. Digite SIM: ").strip()
    if ok != "SIM":
        print("Cancelado.")
        sys.exit(1)

    pathlib.Path(args.out).mkdir(parents=True, exist_ok=True)
    ts = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    STATE["report"] = str(pathlib.Path(args.out) / f"sessao-{ts}.md")
    with open(STATE["report"], "w", encoding="utf-8") as f:
        f.write(f"# Sessao - {ts}\n\n")

    if args.target:
        STATE["target_raw"] = args.target
        STATE["target"] = re.sub(r"^https?://", "", args.target, flags=re.I).split("/")[0].split(":")[0]

    while True:
        print(MENU.format(
            target=STATE["target"] or "(nao definido)",
            report=STATE["report"],
        ))
        choice = input("Escolha: ").strip()
        if choice == "0":
            print(f"\nRelatorio: {STATE['report']}")
            break
        action = ACTIONS.get(choice)
        if not action:
            print("Opcao invalida.")
            continue
        try:
            action()
        except KeyboardInterrupt:
            print("\n[!] Acao interrompida (Ctrl+C).")
        except Exception as e:
            print(f"[!] Erro: {e}")


if __name__ == "__main__":
    main()
