# lukas-nilsson.com

Portfolio site for Lukas Nilsson: developer (AI & integration) at Atlantic Packaging, into the tech side of finance. Scroll through a 3D Manhattan trading floor at sunset to land at a terminal that shows his day job and side projects.

- Single `index.html` built on [Three.js](https://threejs.org) (loaded from jsDelivr), no build step.
- `assets/people/`: seated business avatars from [Microsoft Rocketbox](https://github.com/microsoft/Microsoft-Rocketbox) (MIT, see `ROCKETBOX-LICENSE.md`), textures resized for the web.
- `assets/anim/`: Rocketbox "sit at table" animations, stripped down to JSON clips.
- `assets/env/`: `venice_sunset_1k.hdr` from [Poly Haven](https://polyhaven.com/a/venice_sunset) (CC0) for lighting and reflections.

Run locally with any static server (e.g. `python3 -m http.server`); opening the file directly won't load the assets.

## Blog (`/blog`)

[lukas-nilsson.com/blog](https://lukas-nilsson.com/blog/) is built by GitHub Pages' Jekyll with the Minima theme. The portfolio files above have no front matter, so Jekyll copies them through unchanged.

- `_posts/`: one Markdown file per post (`YYYY-MM-DD-title.md`)
- `assets/images/<post>/`: figures for each post
- `scripts/`: Python that regenerates those figures (`pip install -r scripts/requirements.txt`, then e.g. `python scripts/bachelier_figures.py`)
- Local preview: `bundle install && bundle exec jekyll serve`
