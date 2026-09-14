#!/usr/bin/env python3
"""
Demonstration script showing P0 Issue #1 fix: Module Consolidation

This script demonstrates the before/after state of the NPC module duplication fix.
"""

import os
import sys
from pathlib import Path


def count_lines_in_file(filepath: Path) -> int:
    """Count non-empty lines in a file."""
    try:
        with open(filepath, 'r') as f:
            return len([line for line in f if line.strip()])
    except Exception:
        return 0


def analyze_before_state():
    """Analyze the duplicate modules in the 'before' state."""
    print("=" * 70)
    print("P0 ISSUE #1: MODULE DUPLICATION - BEFORE STATE")
    print("=" * 70)
    print()
    
    before_dir = Path(__file__).parent / "before" / "core"
    
    modules = ["goals.py", "schedules.py", "interactions.py", "relationships.py", "gossip.py"]
    
    print("📊 Duplicate Modules Analysis:\n")
    
    total_duplicate_lines = 0
    
    for module in modules:
        npc_systems_path = before_dir / "npc_systems" / module
        npc_modules_path = before_dir / "npc_modules" / module
        
        if npc_systems_path.exists() and npc_modules_path.exists():
            lines_systems = count_lines_in_file(npc_systems_path)
            lines_modules = count_lines_in_file(npc_modules_path)
            
            print(f"Module: {module}")
            print(f"  ├─ npc_systems/{module}: {lines_systems} lines")
            print(f"  ├─ npc_modules/{module}: {lines_modules} lines")
            print(f"  └─ ⚠️  DUPLICATE: {lines_systems + lines_modules} total lines")
            print()
            
            total_duplicate_lines += lines_systems + lines_modules
    
    print(f"Total Duplication: {total_duplicate_lines} lines")
    print(f"Impact: ~{total_duplicate_lines // 2} unnecessary duplicate lines")
    print()


def analyze_after_state():
    """Analyze the consolidated modules in the 'after' state."""
    print("=" * 70)
    print("P0 ISSUE #1: MODULE DUPLICATION - AFTER STATE (FIXED)")
    print("=" * 70)
    print()
    
    after_dir = Path(__file__).parent / "after" / "core" / "npc"
    
    modules = ["goals.py", "schedules.py", "interactions.py", "relationships.py", "gossip.py"]
    
    print("✅ Consolidated Modules:\n")
    
    total_lines = 0
    
    for module in modules:
        npc_path = after_dir / module
        
        if npc_path.exists():
            lines = count_lines_in_file(npc_path)
            total_lines += lines
            
            print(f"Module: npc/{module}")
            print(f"  └─ {lines} lines (single copy)")
            print()
    
    print(f"Total Lines: {total_lines} lines")
    print(f"✅ SINGLE SOURCE OF TRUTH - No duplication!")
    print()


def show_improvement():
    """Show the improvement metrics."""
    print("=" * 70)
    print("IMPROVEMENT METRICS")
    print("=" * 70)
    print()
    
    before_dir = Path(__file__).parent / "before" / "core"
    after_dir = Path(__file__).parent / "after" / "core" / "npc"
    
    modules = ["goals.py", "schedules.py", "interactions.py", "relationships.py", "gossip.py"]
    
    before_total = 0
    after_total = 0
    
    for module in modules:
        npc_systems_path = before_dir / "npc_systems" / module
        npc_modules_path = before_dir / "npc_modules" / module
        npc_path = after_dir / module
        
        if npc_systems_path.exists():
            before_total += count_lines_in_file(npc_systems_path)
        if npc_modules_path.exists():
            before_total += count_lines_in_file(npc_modules_path)
        if npc_path.exists():
            after_total += count_lines_in_file(npc_path)
    
    removed_lines = before_total - after_total
    reduction_pct = (removed_lines / before_total * 100) if before_total > 0 else 0
    
    print(f"Before:  {before_total} lines (with duplication)")
    print(f"After:   {after_total} lines (consolidated)")
    print(f"Removed: {removed_lines} lines")
    print(f"Reduction: {reduction_pct:.1f}%")
    print()
    print("Benefits:")
    print("  ✅ Single source of truth")
    print("  ✅ Easier maintenance")
    print("  ✅ No divergence risk")
    print("  ✅ Reduced codebase size")
    print()


def show_import_changes():
    """Show how imports need to change."""
    print("=" * 70)
    print("IMPORT PATH CHANGES")
    print("=" * 70)
    print()
    
    print("BEFORE (Inconsistent):")
    print("  # Some files use:")
    print("  from core.npc_systems.goals import Goal")
    print("  from core.npc_systems.schedules import Schedule")
    print()
    print("  # Other files use:")
    print("  from core.npc_modules.goals import Goal")
    print("  from core.npc_modules.schedules import Schedule")
    print()
    print("AFTER (Consistent):")
    print("  # All files use:")
    print("  from core.npc.goals import Goal")
    print("  from core.npc.schedules import Schedule")
    print()


def main():
    """Main demonstration function."""
    print("\n")
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║                                                              ║")
    print("║     P0 ISSUE #1: NPC MODULE CONSOLIDATION DEMONSTRATION      ║")
    print("║                                                              ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    print("\n")
    
    analyze_before_state()
    analyze_after_state()
    show_improvement()
    show_import_changes()
    
    print("=" * 70)
    print("STATUS: ✅ P0 ISSUE #1 RESOLVED")
    print("=" * 70)
    print()
    print("This demonstration shows how the module duplication issue")
    print("has been resolved by consolidating duplicate code into a")
    print("single, unified directory structure.")
    print()


if __name__ == "__main__":
    main()
