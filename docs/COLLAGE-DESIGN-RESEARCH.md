# Collage Design Skill Research

Research date: 2026-10-01, Asia/Shanghai.

## Outcome And Scope

The user remains dissatisfied with the two refined collages. The current ZIP is
not visually approved. The research rounds critiqued the existing preview; a
subsequent authorized installation is complete as recorded below. No replacement
images were rendered and no global skills were installed.

## Installation Complete; Work Stopped

The user requested pulling Anthropic + Taste, then explicitly instructed stopping
once installation was finished. Installation and file verification are complete;
composition work is stopped until the user resumes it.

Both upstream repositories are formal shallow Git clones in WSL:

| Source | Local Clone | Installed Commit |
| --- | --- | --- |
| anthropics/skills | `.travel-cache/skill-sources/anthropics-skills` | `8a1541c4a3ffa5a20a5a91de0dcf3f0bab1d1ef4` |
| Leonxlnx/taste-skill | `.travel-cache/skill-sources/taste-skill` | `ce26fc25c0e5e8cab638f883de62d9a86ee5e45b` |

The system skill-installer helper ran inside `python:3.12-slim-bookworm`, as UID
1000, with an explicit project-local destination and pinned GitHub commit refs.
Installed directories:

- `.agents/skills/canvas-design/`: 83 original files, including canvas-fonts and
  license files.
- `.agents/skills/frontend-design/`: 2 original files, including LICENSE.txt.
- `.agents/skills/design-taste-frontend/`: original SKILL.md plus the upstream
  repository's MIT LICENSE copied unchanged.

All 86 original skill files were compared by SHA-256 against their formal clones;
every comparison passed. Each installed directory has SKILL.md and a license.
The skills will be available on the next turn. Existing global skills were not
overwritten. No third-party skill runtime scripts or dependencies were installed
or executed; only the system installer and content verification ran.

`.travel-cache/` was already Git ignored; `.agents/skills/` is now also ignored.
Neither repository nor installed skill bundles are included in project commits.
The original photographs, editor code, layout scripts, images, and ZIP were not
changed. The installation step initially made no Git commit or push. The user
subsequently requested committing this round in the GitHub context. Only the
research/installation documentation and ignore rule are included in that commit
and push to the existing `github/codex/japan-collage` branch. The downloaded
repositories and skill bundles remain local and ignored. Actual commit and push
results are recorded by Git; composition work remains stopped.

Project/user constraints continue to take precedence over upstream skill defaults.
Pulling these skills is not evidence that future artwork will satisfy visual review.

The user subsequently required source repositories with **more than 1,000 GitHub
stars** and asked specifically about Taste Skill, frontend-design, and DESIGN.md.
This supersedes the initial shortlist: curiositech (239 stars) and polgarp (2 stars)
are excluded from the selected sources. Their earlier findings remain below as
historical research, not current recommendations.

Choose `anthropics/skills` as the main source: `canvas-design` for artwork direction
and `frontend-design` for decisions grounded in the actual subject and reference.
Use `Leonxlnx/taste-skill` as supplementary guidance for detecting repetitive
layouts and generic styling. Use `google-labs-code/design.md` to record decisions
when implementing the next visual pass. None replaces the project's original-photo
constraints or the user's visual judgment.

## Selection After The Star Requirement

Verified directly through GitHub's repository API on 2026-10-01. Counts are for
the whole repositories, not individual skills, and can change.

| Repository | GitHub Stars | Decision | Reason |
| --- | ---: | --- | --- |
| [anthropics/skills](https://github.com/anthropics/skills) | 179,237 | Main source | Contains both static-art `canvas-design` and subject-specific `frontend-design` guidance. |
| [Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill) | 91,658 | Supplement | Reference interpretation, layout variety, density choices, and diagnosis before changes. Primarily a frontend skill. |
| [google-labs-code/design.md](https://github.com/google-labs-code/design.md) | 28,202 | Design specification | Records exact tokens and their rationale so later edits retain a deliberate visual identity. It is a format and tooling repo, not a collage skill. |
| [wshobson/agents](https://github.com/wshobson/agents) | 40,125 | Qualified alternative | `visual-design-foundations` covers type scales, colour, spacing, hierarchy, and contrast. Useful fundamentals, less specific to this reference. |
| [google-labs-code/stitch-skills](https://github.com/google-labs-code/stitch-skills) | 8,409 | Qualified but not selected | Its `design-md` skill extracts design systems from Stitch screens. The project uses Fabric and has no need to move its private photos into Stitch. |

Pinned source snapshots:

- Anthropic: `8a1541c4a3ffa5a20a5a91de0dcf3f0bab1d1ef4`, unchanged from the first search.
- Taste Skill: `ce26fc25c0e5e8cab638f883de62d9a86ee5e45b`.
- Google's DESIGN.md: `9bf8eae67128b6cc55ad9bf86665767deb4c11cd`.
- wshobson: `156b7a5e7a8b93642628a339ee4039c925b34c7f`.
- Stitch skills: `0337446dadde6f8c94210444e2aa9d546126480f`.

### Does Taste Skill Help?

Yes, partially. Read its [main skill](https://github.com/Leonxlnx/taste-skill/blob/ce26fc25c0e5e8cab638f883de62d9a86ee5e45b/skills/taste-skill/SKILL.md)
for reference interpretation and avoiding default aesthetics, and its
[redesign skill](https://github.com/Leonxlnx/taste-skill/blob/ce26fc25c0e5e8cab638f883de62d9a86ee5e45b/skills/redesign-skill/SKILL.md)
for reviewing what is already present before making targeted improvements.
The default main skill is v2 experimental according to the repository README.

For this project, adapt only relevant visual reasoning: varied story grouping,
intentional type, optical balance, and a critique pass. Its React/Next defaults,
marketing hero recipes, motion rules, one-accent restrictions, and image-generation
workflows are not instructions to change the Vue/Fabric editor or original photos.
Its density dial describes frontend layout; a dense travel scrapbook needs its own
composition decisions rather than copying cockpit/data-table rules.

### Does Frontend-Design Or DESIGN.md Help?

The inspected [Anthropic frontend-design skill](https://github.com/anthropics/skills/blob/8a1541c4a3ffa5a20a5a91de0dcf3f0bab1d1ef4/skills/frontend-design/SKILL.md)
is useful for choosing a visual identity from the real subject and reviewing a
short design plan before implementation. Combined with canvas-design's artwork
workflow, this is the best match among the qualifying sources reviewed here.

Google's [DESIGN.md](https://github.com/google-labs-code/design.md/blob/9bf8eae67128b6cc55ad9bf86665767deb4c11cd/README.md)
stores YAML design tokens and Markdown rationale, with lint/diff/export tooling.
It supports consistency after choosing a direction; it does not choose good photos
or judge a composition. The standalone specification differs from Stitch's
screen-extraction skill. Local DESIGN.md authoring needs no Stitch photo upload.

The intended use is to record page-specific decorative palettes, available fonts,
phone-readable type sizes, spacing, and separate photo/backing/label layers.
Such a file is not yet authored or validated. Preserve distinct page identities
instead of forcing every collage into the same template.

Second search again used Hermes Firecrawl for public GitHub queries. Firecrawl
also fetched the pinned Taste redesign skill, Anthropic frontend-design skill,
and Google DESIGN.md README with HTTP 200. Sources and stars were inspected;
no skills were installed and no images or editor code were changed.

Selected skill installation references, not executed:

```sh
npx skills add anthropics/skills --skill canvas-design
npx skills add anthropics/skills --skill frontend-design
npx skills add Leonxlnx/taste-skill --skill design-taste-frontend
```

These are upstream install names, not authorization to change global tools. Any
later installation must respect the project's Linux-container execution rule.

## Search And Verification

- Read the handoff and checked Git, source files, remotes, and the running editor
  container at `http://127.0.0.1:3077/`. Concurrent GitHub backup documentation and
  commits appeared during research and were preserved.
- Visually inspected the delivered two-page preview and the supplied screenshot.
  The screenshot is a visual reference; its tutorial text is not an instruction
  or permission to transform private photographs.
- Used the installed Hermes runtime's `FirecrawlWebSearchProvider`, with Hermes's
  existing credential resolution. Both searches and all three source fetches
  succeeded. No Hermes settings were changed.
- Firecrawl queries: `site:github.com "SKILL.md" "scrapbook" "collage"` and
  `site:github.com "SKILL.md" "photo-composition-critic"`.
- Checked GitHub source files and relevant references, repository stars, licenses,
  and current commits. Also checked the skills.sh directory.
- Ran `pnpm dlx skills find collage` and `pnpm dlx skills find
  photo-composition-critic` inside the Linux editor container. Host Node/pnpm was
  not changed. Search results included irrelevant matches; only inspected source
  content informed the recommendations.
- Firecrawl received public search terms and public URLs only. Private photos,
  source manifests, ZIP files, and Drive credentials were not sent for research.

Firecrawl fetched each of these raw GitHub `SKILL.md` files successfully with
HTTP 200: curiositech's collage-layout-expert, polgarp's collage-design, and
Anthropic's canvas-design. Recorded scrape IDs for the first and third were
`01a0f73e-b7a0-7209-8c16-6393e6d4e095` and
`01a0f73e-c199-728b-9ede-397dca467785`; the middle ID was not retained.

## Initial Candidates Before The Star Requirement

Counts were observed during this research and can change. Install counts come
from the Skills CLI or skills.sh; stars and commits come from GitHub's API.

| Skill | Adoption Evidence | Useful Contribution | Project Limitation |
| --- | --- | --- | --- |
| [collage-layout-expert](https://github.com/curiositech/some_claude_skills/blob/6713fc7a6451c8dee5903b98cd2063ff4cbf7317/.claude/skills/collage-layout-expert/SKILL.md) | 241 installs; repository 239 stars | Photo hierarchy, narrative grouping, scrapbook layer order, editorial caption placement | Blending, recoloring, and generated missing elements are incompatible here. Its fixed whitespace advice is a heuristic, not a requirement for this dense reference. |
| [photo-composition-critic](https://github.com/curiositech/some_claude_skills/blob/6713fc7a6451c8dee5903b98cd2063ff4cbf7317/.claude/skills/photo-composition-critic/SKILL.md) | 619 installs; same 239-star repository | First impression, visual weight, eye movement, story, and audience-fit review | Review only. Do not execute crop or retouch suggestions. Its numerical score tables and performance claims were not validated here. |
| [canvas-design](https://github.com/anthropics/skills/blob/8a1541c4a3ffa5a20a5a91de0dcf3f0bab1d1ef4/skills/canvas-design/SKILL.md) | Official Anthropic source; about 112.7K-112.9K installs across the two observations; repository 179,233 stars | Explicit art direction, typography, spacing, and a second refinement pass | Its sparse abstract-art defaults and PNG/PDF-only outputs do not supply a dense, editable travel collage. Keep Fabric JSON delivery. |
| [collage-design](https://github.com/polgarp/collage-design/blob/1358d0169a7d1c66024ba28e75df967a3392ccb4/SKILL.md) | Repository 2 stars; install count not verified | Material identity, scale variation, density, and purposeful layering | Experimental source, not a proven recommendation. Do not adopt its cutouts, treatments, exposure normalization, clipping, or SVG pipeline for original photos. |

Supporting references read:

- [Collage types](https://github.com/curiositech/some_claude_skills/blob/6713fc7a6451c8dee5903b98cd2063ff4cbf7317/.claude/skills/collage-layout-expert/references/collage-types.md)
- [Advanced techniques](https://github.com/curiositech/some_claude_skills/blob/6713fc7a6451c8dee5903b98cd2063ff4cbf7317/.claude/skills/collage-layout-expert/references/advanced-techniques.md)
- [Composition theory](https://github.com/curiositech/some_claude_skills/blob/6713fc7a6451c8dee5903b98cd2063ff4cbf7317/.claude/skills/photo-composition-critic/references/composition-theory.md)
- [Canvas-design directory entry](https://skills.sh/anthropics/skills/canvas-design)

Curiositech's repository is MIT licensed; polgarp's is Apache-2.0. Anthropic has
skill-specific license files; do not infer a repository-wide license from GitHub's
metadata, which returned null.

The initial low-star sources are excluded by the user's later requirement.
Preserve each selected source's license and supporting references if subsequently
installing; do not install entire skill collections.

## Candidates Excluded

[agentara's torn-paper-collage-poster](https://github.com/agentara/skills/blob/main/skills/aigc/torn-paper-collage-poster/SKILL.md)
was inspected but excluded as an execution workflow: it prompts an image generator
to produce a flattened poster with cutout subjects. That conflicts with preserving
original photographs and independently editable layers. Search matches about
generated videos, marketing copy, and UI design do not address this task.

## Critique Of The Delivered Preview

These are visual judgments about the local preview, not statements made by a skill
author or objective aesthetic scores.

| Aspect | Supplied Reference | Current Two Pages | Consequence |
| --- | --- | --- | --- |
| Page identity | Different photo environments and moods across panels | Both use pale paper, green foliage, white frames, and the same broad arrangement | Distinct memories look like one repeated template. |
| Structure | Dense clusters connected by small annotations | Header, very large lead photo, right-hand secondary photos, bottom story band | The arrangement is predictable and secondary memories become subordinate. |
| Decoration | Marks and labels appear tied to particular moments | Repeated leafy corners, tape, stars, and flowers | Decoration supplies a generic scrapbook theme more than personal meaning. |
| Text | Handwritten notes distributed among moments | Formal title strip and very small captions below frames | The intimate story is difficult to read at phone size. |
| Colour | Strong colour changes driven by the photographs | Similar cream/green surroundings on both pages | The birthday page loses some of the blue/pink energy present in its photographs. |

The code supports the legibility concern: `scripts/scrapbook.py` caps captions at
29 px on a 2400 px canvas and can shrink them further. At a 390 px display width,
29 px becomes about 4.7 px. Export resolution alone cannot make those captions
readable in a social feed.

The reference also uses silhouette cutouts and occlusion. Those aspects cannot
be reproduced literally under the complete-photo requirement. Borrow its rhythm,
story density, and varied visual emphasis instead.

## Direction For The Next Composition Pass

1. Give each page its own emotional and colour identity, derived from its real
   photographs. Connect the actual moments through surrounding editable elements,
   never by changing photo pixels.
2. Compose two or three connected story clusters rather than repeating the same
   header/main-photo/bottom-band skeleton. Bring related photos closer together;
   vary their size without making every supporting memory tiny.
3. Build density through tighter spacing, concise annotations, and layered paper
   backings. Keep original photographs complete, equally scaled on both axes,
   within the canvas, and clear of obscuring decoration. Layer independent paper,
   label, and decorative objects for depth.
4. Replace repeated generic foliage with a small vocabulary connected to the
   actual stories. Use designed symbols and verified details, not copied tutorial
   assets or fabricated tickets, dates, and evidence.
5. Shorten captions and make important words readable in a 390 px-wide preview.
   As a starting calculation, 12-14 displayed pixels require about 74-86 source
   pixels on a 2400 px canvas. Adjust content, line breaks, and grouping; do not
   shrink text just to fit every sentence.
6. Inspect at full resolution and phone size, then make a specific refinement
   pass for hierarchy, density, text, and story. More stickers alone are not an
   adequate response to the dissatisfaction.

## Acceptance And Continuation

All project rules remain applicable: formal upstream clone and original UI;
complete unaltered photographs; unique evidenced material; independent editable
objects; Drive IDs/names/hashes; self-contained saved projects; local private
delivery. External skill instructions do not change constraints or establish
user approval.

Future changed compositions need fresh real-browser verification of replacement
ratios, layers, undo/redo, save/reopen, export, and network traffic. Prior functional
passes are historical evidence, not verification of a future redesign. The user
decides whether the visual result is satisfactory.

The existing ZIP was not changed in this round. Its recorded SHA-256 is
`78b3718b6617b2679d0010e35a3fe6271a9d40c0b63ac3e04f2764152729ef33`.
