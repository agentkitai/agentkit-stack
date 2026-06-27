# AgentKitAI — suite overview site

A self-contained static site documenting the whole AgentKitAI control plane:
`index.html` (the big picture + architecture diagram) plus one page per product
(AgentLens, AgentGate, Lore, FormBridge, AgentEval, agentkit-guardrails,
agentkit-cli, agentkit-stack). No build step, no dependencies — open
`index.html` in a browser and the inter-page links work straight off the
filesystem.

## Regenerate

The HTML + CSS are **generated** from a single data + template script. Edit the
product data (versions, features, interfaces) in `gen_site.py`, then:

```bash
python gen_site.py        # rewrites index.html, <product>.html, styles.css in place
```

Everything (including the inline SVG architecture diagram) is defined in
`gen_site.py` — don't hand-edit the generated `.html` files; they'll be
overwritten on the next run.

## Layout

- `gen_site.py` — source of truth: per-product data, the page template, the SVG diagram, and the CSS
- `index.html` — overview, architecture diagram, product cards
- `<product>.html` — purpose · architecture · key features · interfaces · how it fits · notable engineering · stack
- `styles.css` — shared dark theme
