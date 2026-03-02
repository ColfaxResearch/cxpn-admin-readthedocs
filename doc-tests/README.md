# doc-tests

Documentation validation checks used before pushing changes.

## What it checks

- Strict Sphinx build: `sphinx-build -b html -W -n --keep-going`
- Mermaid blocks in `*.rst` files:
  - Mermaid directives are non-empty
  - Diagram declarations start with a known Mermaid diagram keyword
  - Delimiters are balanced (`()`, `[]`, `{}`)
  - If `mmdc` is installed, each Mermaid block is parsed by Mermaid CLI

## Run manually

```bash
./doc-tests/run-doc-tests.sh
```

## Enable automatic pre-push validation

```bash
git config core.hooksPath .githooks
```

After this, every `git push` runs `doc-tests/run-doc-tests.sh` first.
