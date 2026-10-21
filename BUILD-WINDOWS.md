# Fontra Pak Windows Build

This file documents the **Windows** build of Fontra Pak. The full procedure,
including the version convention and the troubleshooting notes, lives in the
fork's skill doc:

```
../.skills-data-prompt/build-fontra-windows-skill.md
```

## One command

```bash
cd fontra-pak
python build-timestamped.py
```

The script:

1. installs `requirements.txt` and `requirements-dev.txt`;
2. installs the parent Fontra package in editable mode (`pip install -e ..`);
3. builds the client bundle (`npm install && npm run bundle` in the parent);
4. stamps the timestamped version into `../src/fontra/_version.py`;
5. verifies that the installed `fontra.__version__` reports that version;
6. runs PyInstaller on `FontraPak.spec`;
7. copies the executable to `dist/Fontra-Pak-v{VERSION}/Fontra Pak.exe`.

The version format is `YYYY.MM.DD.HH` in the GMT+1 (Europe/Paris) timezone.

## How the version reaches the executable

`FontraPak.spec` builds the Windows version resource from the installed
package:

```python
from fontra import __version__ as fontraVersion
...
version=buildWindowsVersionResource() if sys.platform == "win32" else None,
```

So there is exactly **one** version to set: `../src/fontra/_version.py`.
Step 4 of the build script writes it, and step 5 checks that the editable
install really reports it — that is what guarantees the `.exe` shows the
right version in Explorer's file properties.

> Do not re-introduce a separate `version-info.txt`: the upstream spec
> derives the version resource from `fontra.__version__`, and keeping a
> second source of truth is what used to drift out of sync.

## Icon

`icon/FontraIcon.ico` is the Windows icon. To regenerate it from the SVG
source:

```bash
python scripts/convert-icons-simple.py
```

`icon/fontra-icon-source.svg` is the source of truth for the icon.

## Verify the build

```bash
python test-export.py
```

Expected: `Passed: 7, Failed: 0`.

## Keeping this in sync with upstream

`fontra-pak` is a fork of `https://github.com/fontra/fontra-pak`. This
repository deliberately keeps a few **additive** files that upstream does not
have, because they serve the Windows build:

| File | Why it stays |
|---|---|
| `build-timestamped.py` | the one-command, timestamped Windows build |
| `test-export.py` | the export smoke test |
| `hook-fontra.backends.py`, `hook-fontra_compile.py` | PyInstaller hooks (auto-discovered) |
| `scripts/convert-icons*.py`, `icon/fontra-icon-source.svg` | the icon toolchain |
| `requirements-dev.txt` | `delocate` stays commented out: it is macOS-only |

Everything else is taken from upstream verbatim. When merging upstream, keep
these files and take upstream's version of the rest — in particular
`FontraPak.spec`, which upstream owns.
