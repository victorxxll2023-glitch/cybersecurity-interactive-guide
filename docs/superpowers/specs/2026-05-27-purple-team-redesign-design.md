# Purple Team Redesign — Design Spec

**Data:** 2026-05-27
**Branch:** `feat/purple-team-redesign`
**Escopo:** Overhaul visual completo do `index.html`, mantendo todo o JS de lógica intacto.

## Conceito

Site é a interseção **Red Team × Blue Team = Purple Team**. Toda página fala duas
línguas: ataque (vermelho) e defesa (azul). Roxo é o ponto onde elas se
encontram — o operador (você). Apela pra recrutador de red E blue, sinaliza
maturidade de mercado (Purple Team é termo respeitado).

## Paleta

```
--bg #0a0a0f  --bg-2 #12121a  --bg-3 #1a1a25
--red #ef4444  --red-deep #b91c1c  --red-tint rgba(239,68,68,.08)
--blue #3b82f6  --blue-deep #1d4ed8  --blue-tint rgba(59,130,246,.08)
--purple #a855f7  --purple-deep #7e22ce  --purple-glow rgba(168,85,247,.35)
--ink #e8e6f0  --ink-2 #b4b1c4  --ink-mute #6e6b80  --hair #25232f
```

Fraunces sai do uso geral, fica só pros **números grandes dos stats** e pra
pontuação do hero. JetBrains Mono assume protagonismo. Inter pra corpo.

## Blocos do design

### 1. Hero — Split terminal (red × blue)
- Eyebrow badge "PURPLE TEAM · OPERATOR" no topo.
- Headline: `Conheço o ataque. / Defendo o sistema.` (mono grande, ponto em Fraunces).
- Subtitle: "Trilha de estudo PT-BR · 126 conceitos · 6 níveis".
- **Dois terminais lado a lado** digitando em sincronia:
  - Esquerda: `attacker@kali` rodando `nmap -sV`.
  - Direita: `soc@blue-team` recebendo alerta no SIEM.
- Loop ~12s. No mobile, empilham (red em cima, blue embaixo).
- CTAs: `[ Começar do nível 1 → ]` (roxo cheio) + `[ Ver roadmap ]` (outline).

### 2. Navegação — Tab bar sticky
- Brand mono à esquerda + tabs no centro + progresso global à direita.
- Cada tab tem dot colorido indicando team affinity:
  - N1, Roteiro, Dossiê, Quiz, Início → roxo
  - N2 → red-leaning · N3, N4, Gerador → red
  - N5, N6, Bases → blue
- Tab ativa = pílula cheia da cor do team.
- Mini progresso: `87/126 ▰▰▰▰▰▰▱▱▱` à direita, lê localStorage em tempo real.

### 3. Frame de seção — Preâmbulo terminal
Cada aba começa com:
```
$ cd ~/trilha/nivel-3 && cat README.md
────────────────────────────────────
NÍVEL 3 — EXPLORANDO VULNERABILIDADES
[ 12 tópicos · 8 estudados · 67% ] [ team: ● red dominant ]
```

### 4. Cards — Team markers + border beam + spotlight
- Top bar de cada card: `● TEAM · #id` à esquerda, study LED à direita.
- Team marker: RED / BLUE / PURPLE conforme natureza do tópico.
- Hover: border beam (conic-gradient animado 3s) + spotlight (radial roxo seguindo cursor).
- Study LED substitui o checkbox atual — `○` vazio, `●` colorido no team quando estudado.
- "Aprender a fundo" mantém details/summary, só restyle.
- Comandos clicáveis: janela mini terminal, prefix `$`, hover mostra `↗ copy`.
- Callouts: tip → blue · danger → red · (novo) warn → purple (uso ético).

### 5. Fundo animado — Grid + Aurora
- Layer 1: cor sólida `--bg`.
- Layer 2: grid 40x40px em perspectiva, animação translateY 60s infinita, mask top/bottom.
- Layer 3: aurora (radial-gradient blur), red top-left + blue top-right + purple bottom-center, drift 90s, mix-blend `screen`.
- Layer 4 (opcional): noise SVG 3% opacity.
- `position: fixed` em todas — sem repaint no scroll.
- `prefers-reduced-motion` desliga animações, mantém estático.

### 6. Stats + Marquee dual (na aba Início)
- 4 stats grandes: conceitos / níveis / comandos / ferramentas.
- Números em Fraunces italic 72px, count-up no viewport via Motion.
- Subline: contagem real-time de "● red X/126 estudados · ● blue Y/126".
- Marquee dual: linha RED → esquerda, linha BLUE → direita.
- Cada chip: nome da ferramenta + dot do team. Hover pausa.
- Bloco "Open to work" abaixo com placeholders editáveis.

### 7. Motion system
- Hero: stagger no eyebrow / headline / subtitle / terminals / CTAs.
- Cards: fade-in + slideY 12px, stagger 40ms.
- Section transitions: fade-out 80ms → fade-in 200ms + slideY 8px.
- Count-ups: 1.2s easeOut quando entram no viewport.
- Border beam: 3s loop conic-gradient.
- Aurora: 90s drift loop.
- Tudo respeita `prefers-reduced-motion: reduce`.

## O que NÃO muda (preservação)

- **localStorage keys:** `cyber_studied_v1`, `cyber_dossie_v1`.
- **IDs e classes JS-críticas:** `#toTop`, `#termType`, `#quizApp`, `#genTarget`, `#searchInput`, `#navTabs`, `.topic`, `code.cmd`, `#meta`, `#nivel1-6`, `#roteiro`, `#gerador`, `#bases`, `#dossie`, `#quiz`.
- **Função `showView()`** e toda navegação por abas.
- **Mapa `PH`** de placeholders dos comandos clicáveis.
- **Array `QUESTIONS`** do quiz, `dorks/cmds/discover` do gerador.
- **Conteúdo** dos cards (todos os 126 conceitos, callouts, links, comandos).

## Plano de execução

1. Substituir bloco `<style>` inteiro (paleta nova + componentes novos).
2. Substituir markup do `<header>` (hero novo split-terminal).
3. Injetar layers de fundo (grid + aurora) no body.
4. Substituir nav (`#navTabs`) por versão sticky com dots.
5. Inserir preâmbulo terminal em cada seção (`#meta`, `#nivel1-6`, etc.).
6. Adicionar team markers + study LED nos `.topic` cards (data-team attribute + CSS).
7. Adicionar stats + marquee + open-to-work na `#meta`.
8. Adicionar JS novo (em IIFE separado): typing sync dos dois terminais,
   count-up nos stats, team marker auto-classifier por keyword nos cards,
   atualização real-time da nav progress.
9. Validar: parser HTML, `node --check` no JS, testar manualmente cada aba.
10. Commit com mensagem descritiva.

## Critérios de sucesso

- Recrutador entende em 5s: "esse cara estuda red E blue".
- Toda funcionalidade existente continua funcionando.
- Build/parse: HTML balanceado, JS sem erro de sintaxe.
- Acessibilidade: contrastes OK, `prefers-reduced-motion` honrado, foco visível.
- Mobile: hero empilha, marquee continua, cards legíveis.
