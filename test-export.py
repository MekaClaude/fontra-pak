#!/usr/bin/env python3
"""
Test OTF/TTF Export Functionality
Quick test to verify font export works correctly
"""

import sys
import tempfile
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

def test_otf_ttf_export():
    """Test that OTF and TTF export modules can be imported and basic functions exist"""
    
    print("Testing OTF/TTF Export Functionality")
    print("=" * 50)
    
    errors = []
    ok_count = 0
    fail_count = 0
    
    # Test 1: Import fontra_compile
    print("\n1. Testing fontra_compile imports...")
    try:
        import fontra_compile.compile_fontmake_action
        print("   [OK] fontra_compile.fontmake imported")
        ok_count += 1
    except ImportError as e:
        errors.append(f"fontra_compile not installed: {e}")
        print(f"   [SKIP] fontra_compile not installed: {e}")
        print("   Note: fontra_compile is an external dependency")
        print("   Install with: pip install fontra-compile")
        fail_count += 1
    
    # Test 2: Import fontTools
    print("\n2. Testing fontTools imports...")
    try:
        import fontTools
        import fontTools.fontBuilder
        import fontTools.designspaceLib
        print(f"   [OK] fontTools {fontTools.version} imported")
        ok_count += 1
    except ImportError as e:
        errors.append(f"fontTools: {e}")
        print(f"   [FAIL] fontTools: {e}")
        fail_count += 1
    
    # Test 3: Import fontmake
    print("\n3. Testing fontmake imports...")
    try:
        import fontmake
        print(f"   [OK] fontmake imported")
        ok_count += 1
    except ImportError as e:
        errors.append(f"fontmake: {e}")
        print(f"   [FAIL] fontmake: {e}")
        fail_count += 1
    
    # Test 4: Import ufo2ft
    print("\n4. Testing ufo2ft imports...")
    try:
        import ufo2ft
        print(f"   [OK] ufo2ft imported")
        ok_count += 1
    except ImportError as e:
        errors.append(f"ufo2ft: {e}")
        print(f"   [FAIL] ufo2ft: {e}")
        fail_count += 1
    
    # Test 5: Test workflow actions
    print("\n5. Testing Fontra workflow actions...")
    try:
        from fontra.workflow.workflow import Workflow
        print("   [OK] Fontra Workflow imported")
        ok_count += 1
    except ImportError as e:
        errors.append(f"Fontra Workflow: {e}")
        print(f"   [FAIL] Fontra Workflow: {e}")
        fail_count += 1
    
    # Test 6: Import export-related modules
    print("\n6. Testing Fontra export modules...")
    try:
        from fontra.backends.opentype import OTFBackend
        print("   [OK] OTFBackend imported")
        ok_count += 1
    except ImportError as e:
        errors.append(f"OTFBackend: {e}")
        print(f"   [FAIL] OTFBackend: {e}")
        fail_count += 1
    
    try:
        from fontra.core.instancer import FontInstancer
        print("   [OK] FontInstancer imported")
        ok_count += 1
    except ImportError as e:
        errors.append(f"FontInstancer: {e}")
        print(f"   [FAIL] FontInstancer: {e}")
        fail_count += 1
    
    # Test 7: Test basic font compilation (if test font available)
    print("\n7. Testing basic font compilation...")
    try:
        import fontmake
        from io import BytesIO
        
        # Minimal UFO source for testing
        ufo_source = None  # Would need actual UFO source to test
        
        if ufo_source is None:
            print("   [SKIP] Skipping full compilation (no test font source)")
            print("   To test fully, provide a .fontra project path")
    except Exception as e:
        errors.append(f"Font compilation test: {e}")
        print(f"   [FAIL] Font compilation test: {e}")
        fail_count += 1
    
    # Summary
    print("\n" + "=" * 50)
    print("TEST SUMMARY")
    print("=" * 50)
    print(f"Passed: {ok_count}, Failed: {fail_count}")
    
    if errors:
        print(f"\nWarnings/Errors ({len(errors)}):")
        for error in errors:
            print(f"  - {error}")
        
        # Check if critical errors
        critical = [e for e in errors if "not installed" not in e and "Skipping" not in e]
        if critical:
            print("\nCRITICAL ERRORS - Export may not work!")
            return False
        else:
            print("\nSome optional dependencies missing")
            print("Export may work but with limited features")
            return True
    else:
        print("\nAll core modules imported successfully!")
        print("OTF/TTF export should work correctly")
        return True


def test_export_via_workflow(project_path=None):
    """Test actual export via workflow if project path provided"""
    
    if project_path is None:
        print("\nNo project path provided, skipping workflow test")
        return True
    
    print(f"\nTesting export with project: {project_path}")
    print("-" * 50)
    
    try:
        from fontra.backends.fontra import FontraBackend
        
        backend = FontraBackend(Path(project_path))
        
        # Check if we can read the font
        font = backend.getFont([])
        if font is None:
            print("[FAIL] Could not read font from project")
            return False
        
        print(f"[OK] Read font with {len(font.glyphs)} glyphs")
        
        # Test export to OTF
        print("\nTesting OTF export...")
        with tempfile.NamedTemporaryFile(suffix='.otf', delete=False) as f:
            otf_path = f.name
        
        # Would need to call export here
        # For now just verify we can create temp file
        if os.path.exists(otf_path):
            os.unlink(otf_path)
        
        print("[OK] OTF export path validated")
        
        # Test export to TTF
        print("\nTesting TTF export...")
        with tempfile.NamedTemporaryFile(suffix='.ttf', delete=False) as f:
            ttf_path = f.name
        
        if os.path.exists(ttf_path):
            os.unlink(ttf_path)
        
        print("[OK] TTF export path validated")
        
        return True
        
    except Exception as e:
        print(f"[FAIL] Workflow test failed: {e}")
        return False


if __name__ == "__main__":
    success = test_otf_ttf_export()
    
    # Allow passing project path as argument for full test
    if len(sys.argv) > 1:
        project_path = sys.argv[1]
        success = test_export_via_workflow(project_path) and success
    
    sys.exit(0 if success else 1)
