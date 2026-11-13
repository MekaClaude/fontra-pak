"""PyInstaller hook for the top-level fontra package.

Ensures the fork's local plugins (src/fontra/localplugins/) are bundled as
data files. They are served at runtime through the ``fontra.webcontent``
entry point ``localplugins = "fontra.localplugins"``, so the directory must
be present in the frozen bundle; otherwise /localplugins/... 404s and the
plugins fail to load with "Module didn't load".
"""

from PyInstaller.utils.hooks import collect_data_files, collect_submodules

# Collect the plugin files (JS/JSON/CSS/...) and submodules.
datas = collect_data_files("fontra.localplugins")
hiddenimports = collect_submodules("fontra.localplugins")
