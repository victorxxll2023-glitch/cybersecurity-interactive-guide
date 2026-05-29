# scripts/

Dois scripts complementares para uso **educacional e defensivo**.

> **Uso legal apenas** — Lei 12.737/2012 (Brasil) criminaliza acesso/escaneamento não autorizado. Pratique somente em **laboratórios, sistemas próprios ou pentests com autorização por escrito**.

| Script | Quando usar |
|---|---|
| **`menu.py`** | Modo **interativo**: você roda, aparece o menu, escolhe a ferramenta (nmap, nikto, gobuster, sqlmap, hydra…) e o script pergunta só o que falta (alvo, porta, URL, wordlist). Mostra o comando antes de cada execução pra você confirmar. |
| **`recon.py`** | Modo **automático em pipeline**: passa o alvo e ele roda DNS + headers + nmap + whatweb (e nmap vuln + nikto em `--full`) de uma vez, gerando relatório. |

Ambos exigem digitar **`SIM`** no início para confirmar autorização, e gravam tudo em `reports/<alvo>-<timestamp>.md` (ou `sessao-<timestamp>.md` no caso do menu).

---

## menu.py — pentest assistido interativo

```bash
chmod +x scripts/menu.py
./scripts/menu.py
# (ou já apontando o alvo)
./scripts/menu.py --target scanme.nmap.org
```

### Opções do menu

```
  [1]  Definir/trocar alvo

  Recon
  [2]  DNS (dig A + MX)
  [3]  WHOIS
  [4]  HTTP headers (curl) + análise de cabeçalhos de segurança
  [5]  whatweb (detecção de tecnologias)

  Portas / vulnerabilidades de rede
  [6]  nmap rápido (top 100 portas + scripts default)
  [7]  nmap completo (-p- todos os portos)
  [8]  nmap vuln (--script vuln, identifica CVEs conhecidos)

  Web
  [9]  nikto (varredura de vulnerabilidades web)
  [10] gobuster dir (enumeração de diretórios)
  [11] sqlmap (teste de SQLi em URL com parâmetro)

  Credenciais (LAB / SISTEMA PRÓPRIO APENAS)
  [12] hydra SSH (força bruta)

  Combos
  [13] Pipeline recon completo (2 → 6)

  [14] Ver relatório acumulado
  [0]  Sair
```

Para cada opção, o script pede só o que falta. Exemplo do gobuster:

```
Esquema (http/https) [https]: http
Wordlist [/usr/share/wordlists/dirb/common.txt]:
Extensões (vazio para nenhuma; ex: php,html,txt): php,html

Comando: $ gobuster dir -u http://alvo -w /usr/share/wordlists/dirb/common.txt -q -x php,html
Executar? (s/N): s
```

Cada saída é anexada ao relatório da sessão. Use **[14]** a qualquer momento para ver o que já foi coletado.

---

## recon.py — recon automatizado em pipeline

```bash
chmod +x scripts/recon.py

# scan rápido (~1–3 min)
./scripts/recon.py scanme.nmap.org

# scan completo (+ nmap vuln + nikto)
./scripts/recon.py 192.168.1.10 --full

# diretório de saída customizado
./scripts/recon.py meusite.local --out /tmp/relatorios
```

### Modos

- **Padrão (rápido):** `dig` (A/MX) + `whois` resumo + `curl -sIL` + análise dos cabeçalhos de segurança + `nmap -sV -sC --top-ports 100` + `whatweb`.
- **`--full` (lento):** acima + `nmap -p-` + `nmap --script vuln` + `nikto`.

**Não inclui** exploração, força bruta nem fuzzing de credenciais — só identificação.

### Flag `--yes`

Pula a confirmação interativa. **Use só** em pipelines já validados como autorizados (ex: CI rodando contra um lab seu).

---

## Instalação das dependências

```bash
sudo apt install nmap nikto whatweb gobuster hydra sqlmap dnsutils whois curl
# opcional, para wordlists:
sudo apt install wordlists seclists
```

Ferramentas que não estiverem instaladas são puladas (o relatório indica).

## Onde praticar legalmente

- [TryHackMe](https://tryhackme.com/) — labs guiados
- [HackTheBox](https://www.hackthebox.com/) — máquinas vulneráveis
- [scanme.nmap.org](http://scanme.nmap.org) — alvo oficial do projeto Nmap para testes
- Suas próprias VMs (Metasploitable, DVWA, VulnHub)
