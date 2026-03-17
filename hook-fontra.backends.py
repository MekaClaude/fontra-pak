"""PyInstaller hook for fontra.backends package.

This hook ensures all backend submodules and data files are included
in the PyInstaller bundle. The fontra.backends package uses dynamic
imports and entry points that PyInstaller's static analysis cannot
detect automatically.

This hook is used in addition to the collect_submodules() call in
FontraPak.spec to ensure backend modules are properly discovered.
"""

from PyInstaller.utils.hooks import collect_data_files, collect_submodules

# Collect all submodules within fontra.backends
hiddenimports = collect_submodules("fontra.backends")

# Collect all data files within fontra.backends
datas = collect_data_files("fontra.backends")
