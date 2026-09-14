# Import Path Comparison

This document shows how import paths change before and after consolidation.

## Before Consolidation

Different parts of the codebase import from different locations:

```python
# Some files import from npc_systems
from core.npc_systems.goals import Goal, GoalManager, GoalPriority
from core.npc_systems.schedules import Schedule, ScheduleManager
from core.npc_systems.interactions import Interaction, InteractionManager
from core.npc_systems.relationships import Relationship, RelationshipManager
from core.npc_systems.gossip import Gossip, GossipSystem

# Other files import from npc_modules (DUPLICATE!)
from core.npc_modules.goals import Goal, GoalManager, GoalPriority
from core.npc_modules.schedules import Schedule, ScheduleManager
from core.npc_modules.interactions import Interaction, InteractionManager
from core.npc_modules.relationships import Relationship, RelationshipManager
from core.npc_modules.gossip import Gossip, GossipSystem
```

### Problems

1. **Confusion**: Which import path should be used?
2. **Inconsistency**: Different files use different paths
3. **Bugs**: If a bug is fixed in one, it remains in the other
4. **Maintenance**: Changes must be made in two places

## After Consolidation

Single, consistent import path:

```python
# All files import from the unified location
from core.npc.goals import Goal, GoalManager, GoalPriority
from core.npc.schedules import Schedule, ScheduleManager
from core.npc.interactions import Interaction, InteractionManager
from core.npc.relationships import Relationship, RelationshipManager
from core.npc.gossip import Gossip, GossipSystem
```

### Benefits

1. **Clarity**: Single source of truth
2. **Consistency**: All code uses same path
3. **Maintainability**: Bug fixes only needed once
4. **Simplicity**: Easier for new developers

## Migration Script

To update all imports across the codebase:

```python
#!/usr/bin/env python3
"""
Script to migrate import statements from duplicate paths to unified path.
"""

import os
import re
from pathlib import Path


def migrate_imports(file_path: Path) -> bool:
    """Migrate imports in a single file."""
    try:
        content = file_path.read_text()
        original = content
        
        # Replace npc_systems imports
        content = re.sub(
            r'from core\.npc_systems\.(\w+)',
            r'from core.npc.\1',
            content
        )
        
        # Replace npc_modules imports
        content = re.sub(
            r'from core\.npc_modules\.(\w+)',
            r'from core.npc.\1',
            content
        )
        
        # Also handle direct imports
        content = re.sub(
            r'import core\.npc_systems\.(\w+)',
            r'import core.npc.\1',
            content
        )
        
        content = re.sub(
            r'import core\.npc_modules\.(\w+)',
            r'import core.npc.\1',
            content
        )
        
        if content != original:
            file_path.write_text(content)
            return True
        return False
        
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False


def main():
    """Migrate all Python files in the project."""
    project_root = Path(__file__).parent.parent
    python_files = project_root.rglob("*.py")
    
    updated_count = 0
    for file_path in python_files:
        # Skip the npc directories themselves
        if "npc_systems" in str(file_path) or "npc_modules" in str(file_path):
            continue
            
        if migrate_imports(file_path):
            print(f"Updated: {file_path}")
            updated_count += 1
    
    print(f"\nMigration complete! Updated {updated_count} files.")


if __name__ == "__main__":
    main()
```

## Testing Strategy

After running the migration:

```bash
# 1. Run all tests
pytest

# 2. Check for any remaining old imports
grep -r "npc_systems" --include="*.py" .
grep -r "npc_modules" --include="*.py" .

# 3. Verify no broken imports
python -m py_compile **/*.py

# 4. Run type checker
mypy core/
```

## Rollback Plan

If issues are discovered:

```bash
# Restore from backup
git checkout -- .

# Or revert the migration commit
git revert <commit-hash>
```

## Success Criteria

- [ ] All imports updated to use `core.npc.*`
- [ ] No references to `npc_systems` or `npc_modules` remain
- [ ] All tests passing
- [ ] Type checking passes
- [ ] No runtime import errors
