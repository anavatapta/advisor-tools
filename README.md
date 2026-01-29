# Advisor Tools

A collection of document generation tools for professional services work.

## PDF Generation System

Generate beautiful PDFs from Markdown using Pandoc and LaTeX.

### Quick Start

```bash
python generate_pdf.py input.md --template professional
```

### Templates

- **professional** - Clean, formal business documents with headers/footers
- **minimal** - Simple, elegant single-column layout
- **formal** - Traditional academic/formal style with title page

### Requirements

- Python 3.x
- Pandoc 3.x+
- MiKTeX (or other LaTeX distribution)

### Usage

```bash
# Generate with default (professional) template
python generate_pdf.py document.md

# Specify a template
python generate_pdf.py document.md --template minimal

# Custom output name
python generate_pdf.py document.md -o output.pdf

# List available templates
python generate_pdf.py --list-templates
```

### Markdown Front Matter

Include metadata at the top of your markdown file:

```yaml
---
title: 'Document Title'
author: 'Your Name'
date: '28-Jan-2026'
---
```

## Project Structure

```
advisor-tools/
├── generate_pdf.py          # Main PDF generation script
├── templates/               # LaTeX templates
│   ├── professional.tex
│   ├── minimal.tex
│   └── formal.tex
├── examples/                # Example documents
└── README.md
```

## Installation

```bash
git clone <repo-url>
cd advisor-tools
```

Ensure Pandoc and LaTeX are in your PATH.
