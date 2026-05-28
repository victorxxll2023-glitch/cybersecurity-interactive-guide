# findings.md — Auditoria FASE 1

> Estado auditado: `index.html` (7.563 linhas, 136 cards, single-file, sem build).
> Contexto: nas últimas sessões o site recebeu identidade "Purple Team" (accent roxo + terminal + emojis). O novo brief pede o OPOSTO em vários pontos (sem roxo/IA, sem emoji, menos terminal, glassmorphism corporativo SOC). Esta auditoria reconcilia os dois.

## ETAPA 0 — Skills / ferramentas disponíveis (nada a instalar)

Tudo já disponível no ambiente (Claude Code + plugins). Não há "instalação" — são capacidades já presentes:

| Skill do brief | Recurso real disponível | Uso |
|---|---|---|
| Planning With Files | `planning-with-files:plan` ✅ | organizar auditoria/plano/progresso (estes arquivos) |
| Frontend Design | `frontend-design:frontend-design` ✅ | execução do redesign (FASE 3) |
| Code Review | `code-review:code-review`, `pr-review-toolkit:code-reviewer` ✅ | revisão final |
| UI/UX, Design System, Responsive, A11y, Visual Hierarchy, Component Arch | competências cobertas por frontend-design + expertise (não são plugins separados) | aplicadas direto |
| Performance Analysis | inline (validação HTML/JS + budget de animação GPU) | medir jank |

Nenhuma reinstalação. Nenhuma dependência nova de runtime (segue single-file, sem build).

## FASE 1 — Auditoria (Problema · Impacto · Solução · Prioridade)

### A. Identidade visual / risco "estética de IA"
| # | Problema | Impacto | Solução | Prio |
|---|---|---|---|---|
| A1 | Roxo (#a855f7) é o accent dominante do sistema (~142 usos) | Lê como "SaaS de IA"; o brief pede explicitamente para evitar roxo/rosa | Remover roxo como accent do sistema; accent neutro = grafite/aço; manter dualidade Blue/Red | **ALTA** |
| A2 | Emojis em 136 títulos de card + nav + headers + botões | Lê informal/amador; brief pede zero emoji | Substituir por ícones SVG stroke (estilo Lucide/Tabler), monocromáticos e temáveis | **ALTA** |
| A3 | Aurora (blobs radiais à deriva) no fundo | "Bolhas abstratas" que o brief quer evitar | Trocar por malha/data-flow técnico SVG (nós + linhas), discreto e funcional | MÉDIA |
| A4 | Terminal por toda parte (hero split + preâmbulo `$ cd` por seção) | "Terminal falso em tudo" que o brief alerta | Manter UM console refinado no hero (estilo SOC, não hacker); trocar preâmbulos por headers de painel/dashboard | MÉDIA |

### B. Experiência desktop / uso do espaço
| # | Problema | Impacto | Solução | Prio |
|---|---|---|---|---|
| B1 | Tipografia e componentes dimensionados mobile-first; muita coisa pequena no desktop | Subaproveita telas grandes; parece "esticado" | Escala tipográfica desktop-first; densidade e padding maiores em ≥1200px | **ALTA** |
| B2 | Hero não entrega o pitch de 5s (stats/diferenciais/features estão na aba Início, não no hero) | Recrutador não entende valor em 5s | Hero-plataforma: headline + subheadline + tiles de stats + features + fundo técnico animado | **ALTA** |
| B3 | Shell = topbar + 13 chips horizontais planos | Falta cara de "plataforma"; navegação plana | Considerar rail/agrupamento (Aprender · Praticar · Ferramentas · Sobre); header de seção tipo dashboard | MÉDIA |
| B4 | Áreas vazias no desktop (ex: pager só "Próximo" à direita) | Espaço morto | Grids melhores; preencher com meta/contexto útil | MÉDIA |

### C. Hierarquia visual / cards
| # | Problema | Impacto | Solução | Prio |
|---|---|---|---|---|
| C1 | Cards planos (transparente + hairline + linhas de grid) | Falta profundidade/sofisticação que o brief quer (glass) | Glass premium nos painéis-chave; cards com elevação sutil e hierarquia clara | **ALTA** |
| C2 | Título com emoji + "o que/por que" + LED + marker → apertado | Leitura cansativa; ícone não-profissional | Reorganizar: ícone SVG + título + tag de team + corpo legível + ação | MÉDIA |

### D. Cor / saturação / botões
| # | Problema | Impacto | Solução | Prio |
|---|---|---|---|---|
| D1 | Red #ef4444 / Blue #3b82f6 saturados ("quase neon") | Brief pede azul-petróleo/ciano/grafite e vinho/âmbar/laranja-queimado, sem neon | Repaletizar para tons dessaturados corporativos | **ALTA** |
| D2 | Botões com preenchimento sólido saturado (primary roxo) | Brief pede botões glass/transparentes refinados | Botões vidro: borda + blur sutil + hover elegante + microanimação | MÉDIA |

### E. Imagens / visuais técnicos
| # | Problema | Impacto | Solução | Prio |
|---|---|---|---|---|
| E1 | Só 5 imagens raster (screenshots), enterradas em "aprofundar" | Falta visual técnico que o brief pede | Adicionar SVGs funcionais: topologia de rede, threat map, data-flow, mini-dashboard SOC | MÉDIA |
| E2 | Matriz MITRE ATT&CK já é boa | — | Manter e refinar na nova paleta/glass | BAIXA |

### F. Acessibilidade
| # | Problema | Impacto | Solução | Prio |
|---|---|---|---|---|
| F1 | Modo Attack/Defense esconde via `opacity:.13` mas mantém no DOM/foco | Conteúdo "invisível" ainda navegável por teclado/leitor | Usar `hidden`/`inert` ou aria + remover do tab order quando esmaecido | MÉDIA |
| F2 | Emoji como ícone é lido literalmente pelo leitor de tela | Ruído para AT | SVG com `aria-hidden` + texto real resolve | MÉDIA |
| F3 | Texto `--ink-3`/muted pode ter contraste baixo no novo fundo | WCAG AA em risco | Validar contraste ≥ 4.5:1 no corpo | MÉDIA |

### G. Performance (já melhorada — proteger)
| # | Problema | Impacto | Solução | Prio |
|---|---|---|---|---|
| G1 | Jank de scroll já corrigido (blur/blend/backdrop removidos) | — | Novas animações só em `transform`/`opacity`; **não** aplicar backdrop-blur nos 136 cards | **ALTA (guardrail)** |

## Conflitos com o trabalho recente (decisões que precisam do dono)
1. **Roxo** é hoje o accent do sistema — o brief manda remover. → precisa confirmar accent neutro substituto.
2. **Emojis** estão em 136 cards — o brief manda remover. → esforço grande; precisa confirmar escopo.
3. **Terminal** está no hero + todas as seções — o brief pede reduzir. → precisa confirmar quanto manter.
4. **Glassmorphism** em 136 cards com backdrop-blur destruiria a performance (G1). → precisa confirmar onde aplicar glass de verdade vs glass-lite.
