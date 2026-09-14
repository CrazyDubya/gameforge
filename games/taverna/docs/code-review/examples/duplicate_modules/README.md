# Module Duplication Issue Example

This directory demonstrates the critical P0 issue identified in the code review: **~6,100 lines of duplicate code** between `npc_systems/` and `npc_modules/`.

## Problem Statement

The Living Rusted Tankard codebase contains two nearly identical directory structures:
- `core/npc_systems/`
- `core/npc_modules/`

These directories contain 100% duplicate implementations of 5 major modules:

| Module | Lines | Status |
|--------|-------|--------|
| goals.py | 956 | 100% duplicate |
| schedules.py | 867 | 100% duplicate |
| interactions.py | 669 | 100% duplicate |
| relationships.py | 626 | 100% duplicate |
| gossip.py | 638 | 100% duplicate |

**Total Duplication**: 3,756 lines × 2 = **7,512 lines** (counting both copies)

## Impact

1. **Maintenance Burden**: Any bug fix or feature must be applied twice
2. **Risk of Divergence**: Changes applied to only one copy create inconsistencies
3. **Wasted Space**: ~20% of codebase is unnecessary duplication
4. **Confusion**: Developers don't know which directory to use
5. **Testing Overhead**: Need to test both paths even though they're identical

## Examples

### Before: Duplicate Structure

```
core/
├── npc_systems/
│   ├── __init__.py
│   ├── goals.py           # 956 lines
│   ├── schedules.py       # 867 lines
│   ├── interactions.py    # 669 lines
│   ├── relationships.py   # 626 lines
│   └── gossip.py          # 638 lines
│
└── npc_modules/
    ├── __init__.py
    ├── goals.py           # 956 lines (DUPLICATE!)
    ├── schedules.py       # 867 lines (DUPLICATE!)
    ├── interactions.py    # 669 lines (DUPLICATE!)
    ├── relationships.py   # 626 lines (DUPLICATE!)
    └── gossip.py          # 638 lines (DUPLICATE!)
```

### After: Consolidated Structure

```
core/
└── npc/
    ├── __init__.py
    ├── goals.py           # 956 lines (single copy)
    ├── schedules.py       # 867 lines (single copy)
    ├── interactions.py    # 669 lines (single copy)
    ├── relationships.py   # 626 lines (single copy)
    └── gossip.py          # 638 lines (single copy)
```

## Solution

### Step 1: Choose Canonical Directory
Pick one directory as the source of truth (e.g., `npc_systems`)

### Step 2: Create New Unified Directory
```bash
mkdir -p core/npc
```

### Step 3: Move Files
```bash
mv core/npc_systems/* core/npc/
```

### Step 4: Update Imports Across Codebase
```python
# Before
from core.npc_systems.goals import Goal
from core.npc_modules.goals import Goal

# After
from core.npc.goals import Goal
```

### Step 5: Remove Duplicate Directory
```bash
rm -rf core/npc_modules
rm -rf core/npc_systems
```

## Expected Results

- **Lines Removed**: 3,756 duplicate lines
- **Maintenance Effort**: Reduced by 50% for NPC-related code
- **Code Quality Score**: Improves from 81/100 to ~85/100
- **Duplication Metric**: Drops from 20% to <5%

## Implementation Timeline

- **Analysis**: 4 hours
- **Implementation**: 16 hours
- **Testing**: 8 hours
- **Total**: 28 hours (3.5 developer-days)

## Risk Mitigation

1. **Create feature branch** for testing
2. **Keep backups** until validation complete
3. **Update imports incrementally** with testing after each batch
4. **Comprehensive test run** before merging
5. **Deprecation warnings** for old import paths (if needed for external users)

## See Also

- `/examples/duplicate_modules/before/` - Example of duplicate structure
- `/examples/duplicate_modules/after/` - Example of consolidated structure
- `/REFACTORING_PLAN.md` - Full refactoring plan
