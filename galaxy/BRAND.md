# Galaxy Brand Tokens

These values were chosen as a placeholder dark/space palette because
`ekosmos.com` was unreachable (HTTP 503) when this scaffold was generated.
Replace the tokens below with the canonical eKosmos brand values and the
Desk theme + logo will pick them up automatically.

## Colors

| Token              | Hex       | Use                             |
|--------------------|-----------|---------------------------------|
| `--galaxy-bg`      | `#0B1020` | App background (deep space)     |
| `--galaxy-surface` | `#141A2E` | Cards, navbar                   |
| `--galaxy-primary` | `#5B8CFF` | Primary actions, links          |
| `--galaxy-accent`  | `#9D7BFF` | Highlights, AI surfaces         |
| `--galaxy-success` | `#3FD9A4` | Positive status                 |
| `--galaxy-warn`    | `#F5B547` | SLA at-risk                     |
| `--galaxy-danger`  | `#FF6B6B` | SLA breach, critical            |
| `--galaxy-text`    | `#E6ECFF` | Primary text on dark            |
| `--galaxy-muted`   | `#8892B8` | Secondary text                  |

Edit `galaxy/public/scss/galaxy_variables.scss` to change them.

## Logo

- `galaxy/public/images/galaxy-logo.svg` — wordmark used in the navbar
- `galaxy/public/images/galaxy-favicon.svg` — browser favicon

Both are simple SVG placeholders ("eKosmos · Galaxy"). Drop in the real
logo at the same paths to replace.

## Typography

Placeholder: Inter for UI, JetBrains Mono for code. No webfont is bundled
yet — the Desk falls back to its default sans stack until the real
ekosmos.com font choice is provided.
