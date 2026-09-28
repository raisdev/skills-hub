# document-skills

Document processing skills for common office and PDF file formats:

- `xlsx` - create, edit, inspect, and analyze Excel spreadsheets
- `docx` - create, edit, and inspect Word documents
- `pptx` - create, edit, and inspect PowerPoint presentations
- `pdf` - inspect and extract content from PDF files

**Owner:** Cornell RAIS
**Status:** published

## Provenance

The `skills/` tree is vendored from the `anthropics-skills` submodule
(`submodules/anthropics-skills/skills/`), published by Anthropic. See each
skill's `LICENSE.txt` (c) 2025 Anthropic, PBC. All rights reserved.

It is generated content. Do not edit it by hand - refresh it with:

```bash
python3 plugins/document-skills/sync.py
```

The script copies each skill directory wholesale (including LICENSE files)
from the submodule, so upstream deletions propagate. `dist/` is the plugin
root that Claude Desktop installs; `sync.py` sits beside it, outside the
plugin root, so it never ships.