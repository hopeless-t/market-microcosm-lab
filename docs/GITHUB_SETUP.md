# GitHub repository setup

The code and public documentation are already prepared. The following repository-level switches are not writable through the current connected GitHub tool and therefore require an owner click.

## Repository description and topics

On the repository home page, open the About settings with the gear icon.

Recommended description:

> Self-improving research lab for sustainable market microcosms: robust viability, allocation, governance, and long-run ecosystem survival.

Recommended topics:

- market-design
- mechanism-design
- agent-based-modeling
- viability-theory
- simulation
- complex-systems
- self-improving-systems
- subscription-economy
- computational-economics
- monte-carlo

After Pages is enabled, set Website to:

    https://hopeless-t.github.io/market-microcosm-lab/

## GitHub Pages

Go to Settings → Pages.

Under Build and deployment choose:

- Source: Deploy from a branch
- Branch: main
- Folder: /docs

Save.

The expected site URL is:

    https://hopeless-t.github.io/market-microcosm-lab/

The page source is version-controlled in docs; no separate website repository is required.

## Wiki

Go to Settings → General → Features and enable Wikis.

The canonical Wiki drafts live in the repository under wiki so the knowledge base remains version-controlled even if the GitHub Wiki is deleted or disabled.

Create these pages from the corresponding source files:

- Home ← wiki/Home.md
- Architecture ← wiki/Architecture.md
- Experiments ← wiki/Experiments.md

The repository files remain the source of truth; the GitHub Wiki is a convenience surface.

## Suggested branch protection later

Once the experiment suite becomes more expensive, consider protecting main and requiring the CI check before merge. Do this only after the workflow name/check has stabilized.

## Discussions

Optional. Discussions could be useful later for case-study proposals and mechanism hypotheses, but it is not required for the research loop.


## Social preview

A 1280×640 source artwork is version-controlled at:

    docs/assets/social-preview.svg

If you want the repository card on GitHub/social shares to use it, open:

**Settings → General → Social preview → Edit**

and upload a rasterized PNG/JPEG version of that artwork. This is optional; it does not affect the research system or Pages site.
