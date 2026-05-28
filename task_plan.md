# task_plan.md — Redesign "SOC Platform" (Blue/Red profissional)

## Objetivo
Elevar o guia a uma plataforma de CyberSecurity de aparência profissional/corporativa
(referências: CrowdStrike, Splunk, Elastic Security, Defender XDR, SentinelOne, Palo Alto),
com dualidade Blue/Red elegante, glassmorphism premium, ícones SVG (sem emoji), paleta
dessaturada (sem neon, sem roxo de IA) e animações cinematográficas porém performáticas.

Restrições rígidas: não remover funcionalidades, não quebrar integrações/JS, manter
single-file, sem build, sem dependência de runtime nova. Animações só GPU (transform/opacity).

## Decisões TRAVADAS (2026-05-28)
- [x] **D-1 Accent neutro = GRAFITE/AÇO** (remove roxo de vez).
- [x] **D-2 Ícones SVG = TUDO, em fases** (136 cards + chrome).
- [x] **D-3 Terminal = só console refinado no hero + headers dashboard** (retira preâmbulo `$ cd`).
- [x] **D-4 Glass = real nos painéis-chave + glass-lite (sem blur) nos cards** (perf-safe).

## Fases de execução (FASE 3) — só após aprovar D-1..D-4
- [ ] **3A Design tokens**: nova paleta (Blue petróleo/ciano/grafite · Red vinho/âmbar/laranja-queimado · neutro), tokens de glass, sombras suaves, escala tipográfica desktop-first, espaçamento.
- [ ] **3B Sistema de ícones**: set SVG stroke inline (estilo Lucide/Tabler), via `data-icon` + injeção JS; substituir emojis (escopo conforme D-2).
- [ ] **3C Shell & navegação**: topbar/nav refinada, headers de seção estilo dashboard (substituem preâmbulo terminal conforme D-3), agrupamento opcional.
- [ ] **3D Hero-plataforma**: headline + subheadline + tiles de stats + features + fundo técnico animado (malha/data-flow SVG, GPU). Console refinado opcional.
- [ ] **3E Cards**: glass/elevação, hierarquia, ícone SVG, legibilidade, tags de team dessaturadas.
- [ ] **3F Botões/controles**: vidro/transparência refinada + hover/microanimação.
- [ ] **3G Visuais técnicos**: SVGs funcionais (topologia de rede, threat map, data-flow, mini-dashboard SOC) onde agregam.
- [ ] **3H Animações/microinterações**: entrada de cards, hover, contadores, radar/scanner discreto, linhas conectando nós, status pulsando — tudo GPU.
- [ ] **3I A11y & performance**: contraste AA, foco visível, `inert` no modo esmaecido, budget de animação, sem backdrop-blur em massa.
- [ ] **3J Revisão final** (olhar de recrutador técnico): real? profissional? desktop excelente? algo genérico/IA/amador? corrigir.

## Notas de sequência
- Cada fase: validar (HTML balanceado + `node --check`), commit atômico, push (Pages atualiza ~1-2min).
- Entregar em fases com checkpoints (não um big-bang) por causa do tamanho e do risco.
