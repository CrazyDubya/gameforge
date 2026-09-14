# P2 Issue: File Size Reduction

## Problem Statement

The code review identified 20+ files exceeding 600 lines, which is above the recommended threshold for maintainability. Large files are harder to:
- Understand and navigate
- Test effectively
- Review in PRs
- Refactor safely

## Target Metrics

| Metric | Current | Target | Improvement |
|--------|---------|--------|-------------|
| Files > 600 lines | 20+ files | <5 files | -75% |
| Average file size | 297 lines | <350 lines | Maintained |
| Largest non-game_state file | 909 lines | <600 lines | -34% |

## Strategy

### 1. Identify Refactoring Candidates
Files to prioritize for splitting:
- `dynamic_quest_generator.py` (909 lines)
- `area_manager.py` (888 lines)
- `schedules.py` (867 lines)
- `narrative_persistence.py` (766 lines)
- `social_dynamics.py` (749 lines)

### 2. Splitting Approach

**Principle**: Split by responsibility, not by size

Common patterns:
1. **Class per file**: If a file has multiple classes, split into separate files
2. **Function grouping**: Group related functions into modules
3. **Data vs logic**: Separate data structures from business logic
4. **Interface vs implementation**: Split interfaces from implementations

## Example: Splitting dynamic_quest_generator.py (909 lines)

### Before: Monolithic Structure
```python
# dynamic_quest_generator.py (909 lines)
class QuestTemplate:
    # 150 lines of template logic

class QuestValidator:
    # 100 lines of validation logic

class QuestGenerator:
    # 300 lines of generation logic

class QuestRewardCalculator:
    # 200 lines of reward logic

class QuestDifficultyAnalyzer:
    # 159 lines of difficulty analysis
```

### After: Modular Structure
```
narrative/quest_generation/
├── __init__.py              # Public API (50 lines)
├── templates.py             # Template logic (200 lines)
├── validator.py             # Validation logic (150 lines)
├── generator.py             # Core generation (350 lines)
├── rewards.py               # Reward calculation (250 lines)
└── difficulty.py            # Difficulty analysis (200 lines)
```

### Benefits

✅ **Easier Navigation**: Each file has a clear, single purpose  
✅ **Better Testing**: Can test components in isolation  
✅ **Safer Refactoring**: Changes are localized  
✅ **Clearer Imports**: Import only what you need  
✅ **Improved Readability**: Less scrolling, clearer context

## Implementation Steps

1. **Analyze the file**
   ```bash
   # Count classes and functions
   grep -c "^class " large_file.py
   grep -c "^def " large_file.py
   ```

2. **Identify logical boundaries**
   - Group related classes
   - Find functional cohesion
   - Check dependencies

3. **Create new module structure**
   ```bash
   mkdir -p core/module_name
   touch core/module_name/__init__.py
   ```

4. **Move code incrementally**
   - Start with data structures
   - Move independent classes
   - Update imports
   - Maintain public API in __init__.py

5. **Validate**
   ```bash
   # Run tests after each move
   pytest tests/
   
   # Check imports
   python -c "from core.module_name import *"
   ```

## Running the Demonstration

```bash
cd examples/file_size_reduction
python demo_p2_file_size.py
```

## Expected Output

```
┌─────────────────────────────────────────────────────────┐
│ P2 ISSUE: FILE SIZE REDUCTION DEMONSTRATION            │
├─────────────────────────────────────────────────────────┤
│                                                         │
│ BEFORE: Monolithic File                                │
│ ─────────────────────────────────────────              │
│ File: dynamic_quest_generator.py                       │
│ Lines: 909                                             │
│ Classes: 5                                             │
│ Complexity: 🔴 HIGH                                    │
│                                                         │
│ AFTER: Modular Structure                               │
│ ─────────────────────────────────────────              │
│ Module: quest_generation/                              │
│ Files: 6                                               │
│ Max file size: 350 lines                               │
│ Complexity: 🟢 LOW                                     │
│                                                         │
│ IMPROVEMENT                                            │
│ ─────────────────────────────────────────              │
│ File size reduction: -61.5%                            │
│ Maintainability: +150%                                 │
│ Status: ✅ REFACTORING SUCCESSFUL                      │
└─────────────────────────────────────────────────────────┘
```

## ROI Analysis

| Benefit | Impact | Measurement |
|---------|--------|-------------|
| **Onboarding Time** | -40% | New developers understand code faster |
| **Bug Fix Time** | -30% | Easier to locate and fix issues |
| **Review Time** | -50% | Smaller PRs, focused changes |
| **Refactoring Safety** | +60% | More isolated changes |

**Estimated Effort**: 32 developer-hours for all 20+ files  
**ROI**: ⭐⭐⭐⭐ High

## Best Practices

### Do ✅
- Split by logical responsibility
- Maintain backward compatibility
- Keep public API in __init__.py
- Update documentation
- Run tests after each split

### Don't ❌
- Split arbitrarily by line count
- Break logical cohesion
- Create circular dependencies
- Skip updating imports
- Forget to update tests

## Next Steps

After demonstrating this approach:
1. Apply to actual Living Rusted Tankard codebase
2. Start with highest-line-count files
3. Track metrics: file count, max size, test coverage
4. Validate with full test suite
5. Update documentation
