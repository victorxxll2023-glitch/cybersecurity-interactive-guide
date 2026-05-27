# CLAUDE.md — Memória do projeto

Guia para qualquer sessão futura do Claude continuar de onde paramos.
O dono do projeto fala **português**; responda em português.

## O que é
Trilha de estudo de cibersegurança (PT-BR), 100% front-end, **um único `index.html`**
servido no GitHub Pages. Educacional/defensivo: hacking ético, Blue Team, SOC, pentest.

- **URL no ar:** https://victorxxll2023-glitch.github.io/cybersecurity-interactive-guide/
- **Branch de trabalho:** `claude/detailed-learning-explanations-WRCdR`
- Sem build, sem framework, sem backend. Dependência externa: só Google Fonts (Inter + JetBrains Mono), com fallback para fontes do sistema.

## Estrutura de arquivos
- `index.html` — TUDO (HTML + CSS no `<style>` + JS em IIFEs no `<script>` final).
- `img/` — imagens reais (Wireshark, Zenmap, Metasploit, Kali, mapa WannaCry), licença livre (Wikimedia, GPL/CC BY-SA), otimizadas (~760px). Créditos nas legendas.
- `hero.png` / `attack.png` / `defense.png` — artes (hero.png é a og:image; o hero virou terminal, mas o arquivo é mantido).
- `netlify.toml`, `.gitignore`.

## Arquitetura do index.html
- **Seções (abas):** `#meta` (Início), `#roteiro`, `#nivel1..6`, `#gerador`, `#bases`, `#dossie`, `#quiz`. O `<header>` é o hero (terminal). Níveis 1–6 têm cards `.topic`.
- **JS (IIFEs independentes, no fim do `<script>`):**
  1. Voltar ao topo (`#toTop`).
  2. Efeito de digitação do hero terminal (`#termType`) — decorativo.
  3. Quiz dinâmico (`#quizApp`, array `QUESTIONS`, sorteia 10 de 15).
  4. Gerador (`#genTarget` + abas dorks/cmds/discover; arrays `dorks`, `cmds`, `discover`; campos de parâmetro `genUser/genPass/...`; integra com Dossiê).
  5. Navegação por abas + busca (`views[]`, `showView()`, chips `#navTabs`, paginação Anterior/Próximo, busca `#searchInput`).
  6. Progresso "marcar estudado" (localStorage `cyber_studied_v1`, barra por nível).
  7. Dossiê (localStorage `cyber_dossie_v1`, copiar/baixar/limpar).
  8. Comandos clicáveis (`code.cmd`): clicar copia com marcadores tipo `<IP_DO_ALVO>` e mostra dica do que editar; mapa `PH`.

## Preferências de design (atual)
Tema **"hacker discreto"**: base escura neutra + **verde terminal** controlado + roxo deepai suave.
- Variáveis em `:root` (NÃO renomear; mudar valores remapeia tudo): `--bg #0a0e14`, `--green #4ade80` (accent terminal), `--cyan #38bdf8`, `--purple #818cf8`, `--pink #f43f5e`, `--yellow #fbbf24`, `--border` (white-alpha neutro), `--border-strong` (verde), `--card`/`--panel` (glass), `--shadow`, `--radius`, `--mono`.
- **Botões em pílula** (border-radius 999px) estilo deepai; aba ativa = pílula verde; `.btn.primary` verde cheio.
- **Hero = janela de terminal** com digitação. Evitar: neon exagerado, matrix clichê, gamer.
- Fontes: Inter (texto) + JetBrains Mono (código/terminal).

## Regras de ÉTICA (críticas — sempre seguir)
- Ferramentas ofensivas (Hydra, Metasploit, SET, Responder, NetExec, Sliver, BadUSB, Meterpreter...) são OK como conteúdo educacional, SEMPRE com aviso de "uso só em lab/sistema próprio/pentest autorizado" e referência à Lei 12.737/2012.
- **NUNCA** fornecer/indicar bases de dados vazados, combolists (email:senha de pessoas reais) ou consulta de dados de terceiros (CPF etc.) — viola LGPD. Já foi recusado e deve continuar.
- Exposição pessoal: só HIBP, e só para o PRÓPRIO e-mail.
- Wordlists: linkar fontes oficiais (SecLists, rockyou via Kali), nunca re-hospedar; são dicionários de senhas comuns, não dados pessoais.

## Convenções de trabalho
- Desenvolver na branch acima; **PR + squash merge** (use as ferramentas `mcp__github__*`, não há `gh`).
- Antes do merge, se a branch divergiu do main (squash anterior), rebasear: `git rebase --onto origin/main <base> <branch>` e `git push --force-with-lease`.
- **Validar sempre antes de commitar:**
  - HTML bem-formado (parser Python que confere tags abertas/fechadas).
  - JS: extrair o conteúdo do `<script>` e rodar `node --check`.
  - Conferir contagem de tags `<details>`/`<svg>` e links (curl -I) quando adicionar URLs.
- O dono testa no celular (eu não tenho navegador aqui) — sempre avisar isso e pedir feedback de bugs visuais.
- Ao adicionar URLs externas, verificar com `curl` (200 = ok; 403 = bloqueia bot mas existe).

## Como adicionar um conceito novo (padrão do card)
Dentro do `<div class="cards">` do nível certo:
```html
<div class="topic">
  <h3>EMOJI Nome <span class="badge new">🆕</span></h3>
  <div class="line"><b>O que é:</b> ...</div>
  <div class="line"><b>Por que aprender:</b> ...</div>
  <a href="URL" target="_blank">Fonte ↗</a>
  <details class="deep"><summary>📖 Aprender a fundo</summary><div class="deep-body">
    <h4>Explicação completa</h4><p>...</p>
    <h4>Como instalar</h4><div class="cmd-list"><code class="cmd">comando</code></div>
    <h4>Como usar</h4><div class="cmd-list"><code class="cmd">tool <IP_DO_ALVO></code></div>
    <div class="callout tip|danger">defesa / aviso de uso autorizado</div>
  </div></details>
</div>
```
- Comandos clicáveis: usar marcadores `<IP_DO_ALVO>`, `<ALVO>`, `<USUARIO>`, `<wordlist>`, `<arquivo_hash>`, etc. (já no mapa `PH`); adicionar novos marcadores ao `PH` quando precisar.
- Atualizar a contagem do nível nas `.total-pill` do `#meta`.
- A barra de progresso e o "marcar estudado" são injetados via JS automaticamente em todo `.topic`.

## Estado atual (resumo)
6 níveis, ~126 blocos "Aprender a fundo" (todos os conceitos), gerador (Dorks/Comandos/Como descobrir) parametrizável, Dossiê do alvo, Progresso, Quiz (15 perguntas), Roteiro + labs, aba Bases (bases de segurança + wordlists), busca + navegação por abas + paginação, redesign "hacker discreto".
Conteúdo base: materiais da TI Academy (Prof. Robson Costa) — quando o dono manda print de uma aula nova, adicionar só o que falta (pular o que já existe).
