# scripts/recon.py

Script de **recon automatizado** que recebe um alvo e roda em sequência um pipeline de varreduras de rede/web, gerando um relatório em Markdown.

> Uso **estritamente educacional e defensivo**. Lei 12.737/2012 (Brasil) criminaliza acesso/escaneamento não autorizado. Use apenas em **laboratórios, sistemas próprios ou pentests com autorização por escrito**.

## O que ele faz

Modo padrão (rápido, ~1–3 min):

- `dig` (A e MX) — DNS
- `whois` — registro do domínio (resumo)
- `curl -sIL` — cabeçalhos HTTP + checagem dos cabeçalhos de segurança (HSTS, CSP, X-Frame-Options, etc.)
- `nmap -sV -sC --top-ports 100` — portas/serviços/scripts default
- `whatweb` — tecnologias detectadas

Modo `--full` (lento, vários minutos), além do acima:

- `nmap -p- -sV -sC` — todos os 65535 portos
- `nmap --script vuln` — scripts NSE de identificação de vulnerabilidades
- `nikto` — varredura de vulnerabilidades web

**Não inclui** exploração, força bruta, fuzzing de credenciais ou nada destrutivo — só identificação.

## Instalação das dependências

```bash
sudo apt install nmap nikto whatweb dnsutils whois curl
```

Ferramentas que não estiverem instaladas são puladas (o relatório indica).

## Como usar

```bash
chmod +x scripts/recon.py

# scan rápido
./scripts/recon.py scanme.nmap.org

# scan completo (vulnerabilidades)
./scripts/recon.py 192.168.1.10 --full

# diretório de saída customizado
./scripts/recon.py meusite.local --out /tmp/relatorios
```

Ao iniciar, o script mostra um banner e exige você digitar **`SIM`** para confirmar autorização. Sem isso, ele cancela.

O relatório fica em `reports/<alvo>-<timestamp>.md`.

## Flag `--yes`

Pula a confirmação interativa. **Use só** quando estiver scriptando em ambiente que você já validou como autorizado (ex: CI rodando contra um lab seu).

## Onde praticar legalmente

- [TryHackMe](https://tryhackme.com/) — labs guiados
- [HackTheBox](https://www.hackthebox.com/) — máquinas vulneráveis
- [scanme.nmap.org](http://scanme.nmap.org) — alvo oficial do projeto Nmap para testes
- Suas próprias VMs (Metasploitable, DVWA, VulnHub)
