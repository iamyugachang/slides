# Yuga Chang Career Portfolio Deck — Design Specification

## Goal

Create a public, English-language web presentation that positions Yuga Chang as an end-to-end **Data & AI Engineer**. The deck should show a coherent progression from computer vision research, through production recommendation systems and data engineering, to data and AI platform engineering.

The central thesis is:

> I build Data & AI systems that ship — from models and experiments to products and reliable platforms.

This is a public portfolio rather than an exhaustive résumé. It must be memorable in a short viewing session, readable without a presenter, and safe to publish on GitHub Pages.

## Audience and constraints

- Primary audience: recruiters, engineering leaders, peers, and public portfolio visitors.
- Language: English only.
- Density: low-density, speaker-led visual rhythm with enough context for asynchronous public viewing.
- Length: exactly 9 slides.
- Format: a self-contained Frontend Slides HTML deck with no build step.
- Repository: `iamyugachang/slides`.
- Deck path: `career-portfolio/index.html`.
- Expected public URL: `https://iamyugachang.github.io/slides/career-portfolio/`.
- Source material: facts and public outcomes visible in Yuga's supplied LinkedIn screenshots.
- Privacy boundary: do not expose confidential architecture, unpublished scale, customer data, internal project names, proprietary processes, or non-public business metrics.

## Narrative approach

Use the approved **End-to-End Builder** approach. The deck is not a chronological résumé recital. Each career stage demonstrates a broader engineering layer:

```text
Computer Vision → Data Engineering → Recommendation & Product → Data & AI Platform
```

The recurring visual capability rail is:

```text
VISION → DATA → ML → PRODUCT → PLATFORM
```

The deck should make clear that Yuga can work across the full lifecycle:

```text
Data → Models → Experiments → Products → Platforms
```

## Slide outline

### 1. Cover — I Build Data & AI Systems That Ship

- Name: Yuga Chang.
- Role: Data & AI Engineer.
- Supporting line: from computer vision research to recommendation at scale and the platforms that make AI reliable in production.
- Show the three-stage arc: Computer Vision → Recommendation → Data & AI Platform.
- Purpose: establish the end-to-end thesis immediately.

### 2. My Engineering Lens

- Present one simple lifecycle: Data → Models → Experiments → Products → Platforms.
- State that the work does not stop at model training; success means a reliable system that reaches real users.
- Avoid a generic skill list or logo wall.

### 3. Computer Vision Foundations

- Combine Ford Motor Company and Infortrend Technology into one foundation chapter.
- Public technologies may include YOLOv3/YOLOv4, LSTM, GANs, object tracking, TensorRT, and OpenVINO.
- Feature two visible outcomes from the supplied material:
  - misconduct-detection accuracy improved from 78.65% to 95.47%;
  - monitoring cost reduced by 70%.
- Frame this stage as the foundation in model design, evaluation, optimization, and edge deployment.

### 4. Building the Data Foundation

- Cover the KKBOX Analytics Engineer role.
- Explain the data foundation behind product and ML systems rather than listing tools without context.
- Public technologies may include ETL/CDC pipelines, Spark, Kafka, Airflow, AWS/GCP, OLTP/OLAP, data warehouse/marts, and data quality.
- Emphasize dependable data flow from operational sources to downstream analytics and ML consumers.

### 5. Recommendation at Scale

- Cover the KKBOX Data Scientist role.
- Use `100M+` as the dominant public outcome: more than 100 million daily personalized recommendations.
- Public approaches may include DSSM neural networks, collaborative filtering, model distillation, AWS SageMaker, and AWS Personalize.
- Explain the engineering problem as scaling personalization, not merely training a recommender.
- Do not invent the missing number before “million users” in the source screenshot.

### 6. From Metrics to Product Outcomes

- Connect technical evaluation to product behavior.
- Public technical metrics may include NDCG@k, MAP, and MRR@k.
- Public product outcomes may include CTR, favoriting, and sharing rates; do not invent percentage uplifts.
- Include AI Playlist as an example combining RAG, fine-tuned LLMs, music embeddings, metadata, and audio features.
- Frame A/B testing as the bridge between model performance and user value.

### 7. Building Data & AI Platforms

- Cover the TSMC Senior Software Engineer role using only public, user-supplied information.
- Public concepts may include private-cloud PaaS, lakehouse, streaming, Kubernetes, Trino, Iceberg, dbt, Airflow, Kafka, and Spark Structured Streaming.
- Describe the platform objective at a high level: accelerate trustworthy data-driven and AI applications.
- Do not include internal topology, cluster sizes, throughput, availability targets, organization names, incidents, or proprietary implementation details.

### 8. What I Bring End to End

- Present three connected capability pillars:
  - ML & AI;
  - Data Engineering;
  - Platform Engineering.
- Show how they connect across one system lifecycle rather than as a grid of disconnected technologies.
- Reinforce the differentiator: the ability to move between model, data, product, and platform concerns.

### 9. Closing — Models Are Only the Beginning

- Closing statement: `I turn data and models into systems people can trust and use.`
- Include public GitHub and LinkedIn links if a public LinkedIn URL is available in the existing profile context; otherwise include GitHub only rather than guessing a URL.
- Keep the ending minimal and suitable as a public contact/portfolio page.

## Visual system

Use the approved custom dark engineering aesthetic from Style A.

### Canvas

- Author every slide on a fixed 1920×1080 stage.
- Scale the stage uniformly to fit the browser viewport.
- Preserve 16:9 on phones; letterbox or pillarbox rather than reflowing slide content.
- No scrolling inside a slide.

### Palette

- Deep navy/charcoal base.
- Warm orange-red as the main active accent.
- Warm off-white primary text.
- Muted blue-gray secondary text and rules.
- Use the accent sparingly for active stages, outcomes, and directional marks.

### Typography

- Heavy, distinctive display face for major claims.
- Monospace face for technical labels, metadata, stage names, and metrics.
- Avoid Inter, Roboto, Arial, and default system-font presentation styling.
- Maintain comfortable public-reading sizes; split or shorten content instead of shrinking type.

### Graphic vocabulary

- Fine engineering grid lines.
- Large partial rings and precise geometric markers.
- A persistent capability rail with the current stage highlighted.
- Oversized numeric outcomes (`95.47%`, `−70%`, `100M+`) on evidence slides.
- Do not use company-logo walls, technology-logo walls, LinkedIn screenshots, stock illustrations, glassmorphism, or generic purple gradients.

### Motion

- Use one orchestrated entrance per slide: short upward reveals, line/path drawing, or stage-marker activation.
- Motion should clarify progression rather than decorate every element.
- Respect `prefers-reduced-motion` and provide a motion-free final state.

## Interaction

- Keyboard navigation: ArrowLeft, ArrowRight, PageUp, PageDown, Space, Home, and End.
- Mobile navigation: swipe left/right and tap zones.
- Track the active slide in the URL hash for refresh and direct links.
- Display a compact slide counter and unobtrusive control hint.
- Provide inline text editing using the standard Frontend Slides editing affordance unless it conflicts with the fixed-stage implementation.
- Print CSS must render one 1920×1080 slide per page and remove controls.

## Repository integration and publishing

- Add the deck at `career-portfolio/index.html`.
- Add the career portfolio to the existing root presentation index without disturbing the existing LLM capability deck.
- Keep source and runtime assets self-contained. External web fonts are allowed; no local absolute paths may appear in the published HTML.
- Publish through the repository's existing GitHub Pages workflow/configuration on `main`.
- Temporary style previews under `.frontend-slides/slide-previews/` are design artifacts and must be deleted before the implementation commit.

## Verification

Before claiming completion:

1. Confirm exactly 9 `.slide` elements and the required slide titles/content stages.
2. Validate HTML/CSS/JavaScript syntax and run `git diff --check`.
3. Serve locally over HTTP rather than relying only on `file://`.
4. Test keyboard, tap, swipe, Home/End, URL hash, reduced motion, and print mode.
5. Render every slide at a desktop viewport and at least one phone viewport.
6. Inspect screenshots for clipping, overlap, unreadably small text, low contrast, and unintended off-canvas content.
7. Perform at least one visual fix-and-reverify cycle.
8. Scan the final deck for confidential/internal terms, local absolute paths, placeholder text, and invented metrics.
9. Push to `main` and verify the public GitHub Pages URL returns HTTP 200 and contains the expected deck title.
10. Verify the existing slides collection index and existing deck still load.

## Non-goals

- No PPTX export in this version.
- No custom backend, analytics, authentication, contact form, or downloadable résumé generation.
- No employer logos or copyrighted assets unless explicitly supplied and approved.
- No exhaustive chronology, education detail slide, or every LinkedIn bullet.
- No invented metrics, inferred user counts, or confidential TSMC implementation details.
