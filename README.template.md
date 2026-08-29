<div align="center">

# Awesome Perceptual Quality

**Metrics, models, and subjective datasets for how images and video actually look to people.**

[![Awesome](https://awesome.re/badge-flat2.svg)](https://awesome.re)
![Methods](https://img.shields.io/badge/methods-{{stat:methods}}-1f6feb?style=flat-square)
![Datasets](https://img.shields.io/badge/datasets-{{stat:datasets}}-8250df?style=flat-square)
![UGC](https://img.shields.io/badge/UGC%20tagged-{{stat:ugc}}-1a7f37?style=flat-square)
![HDR](https://img.shields.io/badge/HDR%20tagged-{{stat:hdr}}-bf3989?style=flat-square)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen?style=flat-square)](CONTRIBUTING.md)

<img src="assets/landscape.svg" alt="Timeline of perceptual quality research across image quality, video quality, UGC, and HDR, showing that UGC and HDR subjective data arrived late and remains sparse" width="100%">

</div>

## What this is

A single catalog of perceptual quality assessment work: the metrics that predict human judgements of visual quality, the models that learn them, and the subjective studies that make either possible.

Four tags run through everything, and most entries carry more than one:

| Tag | Meaning |
| :--- | :--- |
| ![IQA](https://img.shields.io/badge/IQA-1f6feb?style=flat-square&labelColor=1f6feb) | Still image quality |
| ![VQA](https://img.shields.io/badge/VQA-8250df?style=flat-square&labelColor=8250df) | Video quality |
| ![UGC](https://img.shields.io/badge/UGC-1a7f37?style=flat-square&labelColor=1a7f37) | User-generated content, authentic rather than simulated distortion |
| ![HDR](https://img.shields.io/badge/HDR-bf3989?style=flat-square&labelColor=bf3989) | High dynamic range, wide gamut, high bit depth |

Modifier tags narrow things further: `FR` and `NR` for reference availability, `MLLM` for language-model-based scorers, `AIGC` for generated-content quality, `SYNTHETIC` and `AUTHENTIC` for how distortions arose, plus `GAMING`, `STREAMING`, and `COMPRESSION`.

## Why it exists

Quality assessment has no home list. Image quality is covered reasonably well by [Awesome-Image-Quality-Assessment](https://github.com/chaofengc/Awesome-Image-Quality-Assessment), but video quality has nothing dedicated at all, so video papers get absorbed into image lists or scattered across generation lists that were built for a different purpose. HDR quality is worse off again: it sits between [Awesome-High-Dynamic-Range-Imaging](https://github.com/rebeccaeexu/Awesome-High-Dynamic-Range-Imaging), which is organised around reconstruction, and general IQA lists that predate HDR content entirely.

The practical result is that finding the right dataset takes longer than it should. A researcher looking for authentic-distortion HDR video with subjective scores currently has to know which three unrelated lists to check.

This catalog puts image, video, UGC, and HDR in one place, tags each entry along all four axes, and keeps datasets in their own tables so you can find data by what it contains rather than by which paper introduced it.

## Contents

- [Datasets](#datasets)
  - [Image quality datasets](#image-quality-datasets)
  - [Video quality datasets](#video-quality-datasets)
  - [HDR quality datasets](#hdr-quality-datasets)
- [Methods](#methods)
  - [Full-reference image quality](#full-reference-image-quality)
  - [No-reference image quality](#no-reference-image-quality)
  - [Video quality](#video-quality)
  - [HDR quality](#hdr-quality)
  - [MLLM and reasoning-based quality](#mllm-and-reasoning-based-quality)
- [Toolboxes](#toolboxes)
- [Challenges](#challenges)
- [Surveys](#surveys)
- [Contributing](#contributing)

---

## Datasets

Subjective studies and benchmarks. Blank cells mean the number is not reliably documented, not that it is zero.

### Image quality datasets

<!-- AUTOGEN:datasets:image -->
<!-- /AUTOGEN -->

### Video quality datasets

<!-- AUTOGEN:datasets:video -->
<!-- /AUTOGEN -->

### HDR quality datasets

<!-- AUTOGEN:datasets:hdr -->
<!-- /AUTOGEN -->

---

## Methods

### Full-reference image quality

Metrics with access to a pristine reference.

<!-- AUTOGEN:methods:fr-iqa -->
<!-- /AUTOGEN -->

### No-reference image quality

Blind metrics that score an image on its own. This is what most real deployments need, since the reference is rarely available.

<!-- AUTOGEN:methods:nr-iqa -->
<!-- /AUTOGEN -->

### Video quality

Temporal quality, including the UGC setting where distortions are authentic and stack on top of each other.

<!-- AUTOGEN:methods:vqa -->
<!-- /AUTOGEN -->

### HDR quality

Metrics and models for high dynamic range content, where luminance range and bit depth change what distortions look like.

<!-- AUTOGEN:methods:hdr -->
<!-- /AUTOGEN -->

### MLLM and reasoning-based quality

Multimodal language models used as quality evaluators, producing a score with an explanation attached.

<!-- AUTOGEN:methods:mllm -->
<!-- /AUTOGEN -->

---

## Toolboxes

Working implementations. Prefer these over reimplementing a metric from its paper, since small preprocessing differences move scores more than most people expect.

<!-- AUTOGEN:toolboxes -->
<!-- /AUTOGEN -->

## Challenges

<!-- AUTOGEN:challenges -->
<!-- /AUTOGEN -->

## Surveys

<!-- AUTOGEN:surveys -->
<!-- /AUTOGEN -->

---

## Contributing

Pull requests are welcome, including for your own papers. See [CONTRIBUTING.md](CONTRIBUTING.md).

One thing to know before you start: **`README.md` is generated, so do not edit it.** Every table is rendered from the CSV files in `data/`. Add a row there, run the two scripts, and commit both changes:

```bash
python3 scripts/validate.py          # checks columns, tags, years, duplicate entries
python3 scripts/generate_readme.py   # rewrites README.md from data/ + README.template.md
```

Both use only the Python standard library.

The catalog is data rather than prose so that it stays maintainable. Lists like this usually die because updating them means hand-editing a large markdown file, and that gets tedious around the two hundredth entry. Here a contribution is one CSV row.

## Related lists

- [Awesome-Image-Quality-Assessment](https://github.com/chaofengc/Awesome-Image-Quality-Assessment), the reference IQA list, paired with the [IQA-PyTorch](https://github.com/chaofengc/IQA-PyTorch) toolbox
- [Awesome-High-Dynamic-Range-Imaging](https://github.com/rebeccaeexu/Awesome-High-Dynamic-Range-Imaging), HDR reconstruction and imaging
- [Awesome-Aesthetic-Evaluation-and-Cropping](https://github.com/bcmi/Awesome-Aesthetic-Evaluation-and-Cropping), aesthetics rather than fidelity

## License

[CC0](LICENSE). The catalog metadata is public domain. Linked papers, datasets, and code stay under their own licenses.
