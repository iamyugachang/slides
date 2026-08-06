# LLM Capability Evolution Deck — Design

## Goal

Create a short, speaker-led web presentation explaining that an LLM remains a next-token predictor while successive engineering layers solve the limitations of the previous layer.

The deck must make one causal chain easy to remember:

> next-token prediction → better examples/instructions → better context → retrieved knowledge → standardized tools → collaborating agents → reliable runtime → reusable procedures → verified loops

## Audience and density

- Audience: technically curious people who know AI terminology at a high level.
- Mode: speaker-led, low density.
- Language: Traditional Chinese, with standard English terms retained.
- Each slide communicates one idea using large type and at most two short explanatory statements.
- The sequence is a conceptual capability progression, not a claim that every term emerged in this exact historical order.

## Slide outline

1. **Title / thesis** — LLM 的本質始終是文字接龍；能力增長來自外層系統。
2. **Next-token prediction** — Bottleneck: predicts plausible text but has no task-specific state or reliable adaptation. Breakthrough needed: teach behavior inside the current input.
3. **In-context learning** — Solution: examples and instructions temporarily shape behavior. Bottleneck: results depend heavily on how the input is written.
4. **Prompt engineering** — Solution: systematically design instructions, examples, and output constraints. Bottleneck: wording alone cannot manage all relevant context.
5. **Context engineering** — Solution: curate the complete model-visible state: instructions, history, memory, tools, and documents. Bottleneck: the required knowledge may be stale or too large to preload.
6. **RAG** — Solution: retrieve only relevant external knowledge before generation. Bottleneck: the model can read external data but still lacks a standard way to act on systems.
7. **MCP** — Solution: standardize how models discover and call tools/resources. Bottleneck: one agent still has limited context, specialization, and parallelism.
8. **A2A / Agent-to-Agent** — Solution: agents delegate and collaborate through explicit interfaces. Bottleneck: collaboration alone does not guarantee safe, observable, repeatable execution.
9. **Harness** — Solution: wrap the model with runtime controls for tools, state, permissions, budgets, tracing, and recovery. Bottleneck: a generic runtime does not contain reusable domain procedures.
10. **Skill** — Solution: package instructions, examples, scripts, resources, and verification into reusable capabilities. Bottleneck: a single pass remains brittle when reality disagrees with the plan.
11. **Loop engineering** — Solution: engineer plan → act → observe → evaluate → retry loops with stop conditions and verification.
12. **Conclusion** — The model is still predicting tokens; engineering moved from prompting the model to constructing a system that can repeatedly reach verified outcomes.

## Visual direction

Use the approved **Evolution Rail** direction:

- Fixed 16:9 stage scaled uniformly to the viewport.
- Dark charcoal/navy background with warm amber as the active-stage accent.
- Persistent bottom rail showing all ten stages; the current stage expands and lights up.
- Stage number and term at upper left.
- One large bottleneck statement followed by a compact “突破” statement.
- Vary composition slightly for title and conclusion while keeping the same visual grammar.
- Avoid generic purple gradients, dashboard cards, dense bullets, and decorative title underlines.

## Interaction and implementation

- Self-contained static HTML deck with inline CSS and JavaScript; no framework or build step.
- Keyboard: ArrowLeft/ArrowRight, PageUp/PageDown, Space, Home, End.
- Mobile: swipe left/right and tap navigation zones.
- Visible slide counter and compact control hint.
- URL hash tracks the active slide for refresh and direct linking.
- Respect `prefers-reduced-motion`.
- Provide print CSS so browser print-to-PDF produces one slide per page.

## Repository and publishing

- Repository: `iamyugachang/slides`.
- Deck path: `llm-capability-evolution/index.html`.
- Root `index.html` acts as a minimal presentation index linking to this deck and future decks.
- Publish from the `main` branch root using GitHub Pages.
- Expected URL: `https://iamyugachang.github.io/slides/llm-capability-evolution/`.

## Verification

Before publishing:

1. Validate that exactly 12 slides exist and all ten named stages appear in order.
2. Open locally through an HTTP server and test keyboard, hash navigation, taps, and swipe logic.
3. Render screenshots at 1280×720 and a phone viewport; inspect for clipping, overlap, low contrast, and unreadably small text.
4. Perform at least one fix-and-reverify cycle after visual inspection.
5. Enable GitHub Pages and verify the deployed URL returns HTTP 200 and loads the expected title.

## Scope boundaries

- No PPTX export in this first version.
- No external fonts, image dependencies, analytics, comments, authentication, or backend.
- No claim that this is a strict chronological history; it is a pedagogical progression of system capabilities.
