<div align="center">

# Awesome Perceptual Quality

**Metrics, models, and subjective datasets for how images and video actually look to people.**

[![Awesome](https://awesome.re/badge-flat2.svg)](https://awesome.re)
![Methods](https://img.shields.io/badge/methods-{{stat:methods}}-1f6feb?style=flat-square)
![Datasets](https://img.shields.io/badge/datasets-{{stat:datasets}}-8250df?style=flat-square)
![UGC](https://img.shields.io/badge/UGC%20tagged-{{stat:ugc}}-1a7f37?style=flat-square)
![HDR](https://img.shields.io/badge/HDR%20tagged-{{stat:hdr}}-bf3989?style=flat-square)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen?style=flat-square)](CONTRIBUTING.md)
[![CI](https://github.com/shreshthsaini/Awesome-Perceptual-Quality/actions/workflows/ci.yml/badge.svg)](https://github.com/shreshthsaini/Awesome-Perceptual-Quality/actions/workflows/ci.yml)
[![Links](https://github.com/shreshthsaini/Awesome-Perceptual-Quality/actions/workflows/links.yml/badge.svg)](https://github.com/shreshthsaini/Awesome-Perceptual-Quality/actions/workflows/links.yml)

<img src="assets/landscape.svg" alt="Timeline of perceptual quality research across image quality, video quality, UGC, and HDR, showing that UGC and HDR subjective data arrived late and remains sparse" width="100%">

</div>

Image quality, video quality, user-generated content, and HDR, kept in one place instead of four. Datasets sit in their own tables so you can find data by what it holds rather than by which paper introduced it. Every entry is tagged along all four axes, so an HDR video model shows up whether you came looking for HDR or for video.

## Contact

Maintained by [Shreshth Saini](https://shreshthsaini.github.io). Corrections and additions are welcome through [issues](https://github.com/shreshthsaini/Awesome-Perceptual-Quality/issues) or a pull request.

If the catalog is useful in your work, a star helps others find it, and you can cite it as:

```bibtex
@misc{saini2026awesomeperceptualquality,
  title  = {Awesome Perceptual Quality: A Tagged Catalog of Image, Video, UGC and HDR Quality Assessment},
  author = {Saini, Shreshth},
  year   = {2026},
  url    = {https://github.com/shreshthsaini/Awesome-Perceptual-Quality}
}
```

## Tags

| Tag | Meaning |
| :--- | :--- |
| ![HDR](https://img.shields.io/badge/HDR-bf3989?style=flat-square&labelColor=bf3989) | High dynamic range, wide gamut, high bit depth |
| ![UGC](https://img.shields.io/badge/UGC-1a7f37?style=flat-square&labelColor=1a7f37) | User-generated content, authentic rather than simulated distortion |
| ![VQA](https://img.shields.io/badge/VQA-8250df?style=flat-square&labelColor=8250df) | Video quality |
| ![IQA](https://img.shields.io/badge/IQA-1f6feb?style=flat-square&labelColor=1f6feb) | Still image quality |

Modifiers narrow it further: `FR` and `NR` for reference availability, `MLLM` for language-model scorers, `AIGC` for generated content, `SYNTHETIC` and `AUTHENTIC` for how the distortion arose, plus `GAMING`, `STREAMING`, and `COMPRESSION`.

## Adding a paper

**Easiest way, no git at all:** [open an issue](https://github.com/shreshthsaini/Awesome-Perceptual-Quality/issues/new/choose), fill in the form, done. A bot builds the row, validates it, checks your links, regenerates the tables and opens the pull request for you. If something is off it says so in a comment rather than failing silently.

**Editing directly:** `README.md` is generated, so change the CSVs in `data/` instead, then run:

```bash
python3 scripts/validate.py
python3 scripts/generate_readme.py
```

Commit the CSV row and the regenerated README together. Standard library only, nothing to install.

Either way it is welcome, including your own papers. Saying you are an author just makes review faster. Conventions live in [CONTRIBUTING.md](CONTRIBUTING.md).

## Contents

- **[Datasets](#datasets)** ({{stat:datasets}})
  - [Generated content](#generated-content) ({{count:datasets:aigc}}) &nbsp;·&nbsp; diffusion and text-to-vision output
  - [HDR](#hdr) ({{count:datasets:hdr}}) &nbsp;·&nbsp; high dynamic range, wide gamut, UGC HDR
  - [Video](#video) ({{count:datasets:video}}) &nbsp;·&nbsp; UGC, streaming, gaming, compression
  - [Image](#image) ({{count:datasets:image}}) &nbsp;·&nbsp; synthetic distortion, in-the-wild, aesthetics
- **[Methods](#methods)** ({{stat:methods}})
  - [Multimodal and reasoning](#multimodal-and-reasoning) ({{count:methods:mllm}}) &nbsp;·&nbsp; MLLM scorers, RL-trained reasoning, benchmarks
  - [HDR](#hdr-1) ({{count:methods:hdr}}) &nbsp;·&nbsp; PU encodings, VDP family, HDR UGC models
  - [Video](#video-1) ({{count:methods:vqa}}) &nbsp;·&nbsp; full-reference, blind UGC, efficient samplers
  - [No-reference image](#no-reference-image) ({{count:methods:nr-iqa}}) &nbsp;·&nbsp; NSS, CNN, transformer, CLIP
  - [Full-reference image](#full-reference-image) ({{count:methods:fr-iqa}}) &nbsp;·&nbsp; classical indices, learned perceptual distances
- **[Challenges](#challenges)** ({{count:challenges}}) &nbsp;·&nbsp; NTIRE, AIM, AIS, CLIC, ICME, VQEG
- **[Surveys](#surveys)** ({{count:surveys}})
- **[Toolboxes](#toolboxes)** ({{count:toolboxes}}) &nbsp;·&nbsp; pyiqa, VMAF, PIQ, ColorVideoVDP
- **[Elsewhere](#elsewhere)** &nbsp;·&nbsp; related lists

---

## Datasets

Newest first. A blank cell means the number is not reliably documented, not that it is zero.

### Generated content

Subjective data for diffusion and text-to-vision output, where the failure modes differ from camera distortion.

<!-- AUTOGEN:datasets:aigc -->
<!-- /AUTOGEN -->

### HDR

<!-- AUTOGEN:datasets:hdr -->
<!-- /AUTOGEN -->

### Video

<!-- AUTOGEN:datasets:video -->
<!-- /AUTOGEN -->

### Image

<!-- AUTOGEN:datasets:image -->
<!-- /AUTOGEN -->

---

## Methods

### Multimodal and reasoning

Language models scoring quality, usually with an explanation attached, and the benchmarks built to test them.

<!-- AUTOGEN:methods:mllm -->
<!-- /AUTOGEN -->

### HDR

Luminance range and bit depth change what the distortions look like, so SDR metrics transfer badly.

<!-- AUTOGEN:methods:hdr -->
<!-- /AUTOGEN -->

### Video

Temporal quality, including the UGC case where authentic distortions stack on top of each other.

<!-- AUTOGEN:methods:vqa -->
<!-- /AUTOGEN -->

### No-reference image

Blind scoring, which is what most deployments need since the reference is rarely there.

<!-- AUTOGEN:methods:nr-iqa -->
<!-- /AUTOGEN -->

### Full-reference image

<!-- AUTOGEN:methods:fr-iqa -->
<!-- /AUTOGEN -->

---

## Challenges

<!-- AUTOGEN:challenges -->
<!-- /AUTOGEN -->

## Surveys

<!-- AUTOGEN:surveys -->
<!-- /AUTOGEN -->

## Toolboxes

Working implementations. Worth preferring over a fresh reimplementation, since small preprocessing differences move scores more than people expect.

<!-- AUTOGEN:toolboxes -->
<!-- /AUTOGEN -->

## Elsewhere

- [Awesome-Image-Quality-Assessment](https://github.com/chaofengc/Awesome-Image-Quality-Assessment), the reference IQA list, paired with the [IQA-PyTorch](https://github.com/chaofengc/IQA-PyTorch) toolbox
- [Awesome-High-Dynamic-Range-Imaging](https://github.com/rebeccaeexu/Awesome-High-Dynamic-Range-Imaging), HDR reconstruction and imaging
- [Awesome-Aesthetic-Evaluation-and-Cropping](https://github.com/bcmi/Awesome-Aesthetic-Evaluation-and-Cropping), aesthetics rather than fidelity

## License

[CC0](LICENSE). The catalog metadata is public domain. Linked papers, datasets, and code stay under their own licenses.
