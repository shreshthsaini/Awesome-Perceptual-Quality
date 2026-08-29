# Contributing

Thanks for helping keep this catalog current. Contributions are welcome from anyone, including authors adding their own work.

## The one rule that matters

**Do not edit `README.md`.** It is generated. Every table comes from the CSV files in `data/`, and a pull request that edits the README directly will be closed with a pointer back here.

## Adding a paper or dataset

1. Add one row to the right file:
   - `data/methods.csv` for metrics, models, and algorithms
   - `data/datasets.csv` for subjective studies and benchmarks
   - `data/toolboxes.csv`, `data/challenges.csv`, `data/surveys.csv` for the rest
2. Regenerate and check:

   ```bash
   python3 scripts/validate.py
   python3 scripts/generate_readme.py
   ```

   Both are standard library only. No dependencies to install.
3. Commit the CSV change **and** the regenerated `README.md` together.

## What belongs here

A method or dataset is in scope if it concerns **perceptual quality of images or video**: predicting, measuring, or collecting human judgements of visual quality.

In scope: full-reference and no-reference metrics, subjective studies, quality-focused benchmarks, MLLM-based quality reasoning, HDR quality, UGC quality, aesthetics when tied to a quality score, compression and streaming quality.

Out of scope: generic image restoration or generation papers that report quality metrics but do not study quality assessment itself; perceptual losses used only as a training signal; general-purpose vision benchmarks without subjective quality labels.

Borderline cases are fine to submit. Say why you think it fits and we will discuss it in the pull request.

## Field conventions

| Field | Convention |
| :--- | :--- |
| `name` | Short handle used in the field, for example `BRISQUE`, `KoNViD-1k`. Not the full title. |
| `title` | Full paper title, methods only. |
| `year` | Four digits. Use the year of the venue, or of first arXiv posting if unpublished. |
| `venue` | Short form: `TIP`, `CVPR`, `NeurIPS`, `arXiv`. |
| `paper_url` | Prefer the arXiv abstract page or the official proceedings page. HTTPS only. |
| `code_url` | Author-maintained repository. A GitHub link renders as a live star badge. Leave blank if none is public rather than linking a reimplementation. |
| `data_url` | Download or project page for a dataset. |
| `content` | Dataset scale, for example `10,073 images` or `39,000 videos`. |
| `annotations` | Rating count or protocol, for example `1.2M ratings`. Leave blank if you cannot confirm it. |
| `tags` | Space separated, from the vocabulary below. |
| `note` | One line, under about 110 characters. What it does, not how good it is. |
| `category` | Which table it lands in. See below. |

Leave a field blank rather than guessing. An empty cell is honest; an invented number is not, and it tends to get copied onward.

### Tag vocabulary

Primary, shown as coloured badges in the tables: `HDR` `UGC` `VQA` `IQA`

Modifiers: `FR` `NR` `RR` `PU` `CLASSICAL` `DEEP` `CLIP` `TRANSFORMER` `MLLM` `RL` `REASONING` `BENCHMARK` `SYNTHETIC` `AUTHENTIC` `AIGC` `AESTHETIC` `STREAMING` `GAMING` `COMPRESSION`

`validate.py` rejects tags outside this list. To propose a new one, open an issue first so the vocabulary does not fragment.

### Categories

`data/methods.csv`: `mllm`, `hdr`, `vqa`, `nr-iqa`, `fr-iqa` (tables render in that order)

`data/datasets.csv`: `aigc`, `hdr`, `video`, `image` (tables render in that order)

Use `aigc` for subjective data on generated output, whatever the modality. Otherwise pick by content type.

A paper sits in exactly one category, the table where a reader would look for it first. Cross-cutting membership is what tags are for: an HDR video quality model belongs in `hdr` with tags `HDR VQA`.

## Fixing things

Corrections are as valuable as additions. Wrong years, dead links, misattributed venues, and inflated dataset sizes are all worth a pull request. If you find an entry that misrepresents your own work, please say so and it will be fixed quickly.

## Adding your own work

Encouraged, with two requests: put it in the section where it actually belongs rather than the most visible one, and mention in the pull request that you are an author. Self-submissions are normal in this field and disclosure just makes review faster.
