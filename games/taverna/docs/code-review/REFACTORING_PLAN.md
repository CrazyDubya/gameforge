# Refactoring Plan: Living Rusted Tankard

This document outlines the step-by-step refactoring plan to address critical code review findings.

## Overview

**Goal**: Reduce technical debt from 52% to <20% of codebase  
**Timeline**: 4-6 months  
**Estimated Effort**: 480-720 developer-hours

## Phase 1: NPC Module Consolidation (Priority P0)

### Objective
Eliminate 6,100 lines of duplicate code between `npc_systems/` and `npc_modules/`

### Steps

1. **Analysis Phase** (4 hours)
   - Compare both directory structures
   - Identify any divergence between duplicates
   - Document which is the "source of truth"
   - Check all import statements across codebase

2. **Decision Point** (1 hour)
   - Choose canonical directory (`core/npc/`)
   - Plan import path updates
   - Create migration checklist

3. **Implementation** (16 hours)
   - Create new `core/npc/` directory
   - Move files from chosen source directory
   - Update all import statements:
     ```python
     # Before
     from core.npc_systems.goals import Goal
     from core.npc_modules.goals import Goal
     
     # After
     from core.npc.goals import Goal
     ```
   - Remove duplicate directory
   - Update __init__.py files

4. **Validation** (8 hours)
   - Run full test suite
   - Fix any broken imports
   - Verify no functionality regression
   - Update documentation

### Files Affected
```
core/npc_systems/goals.py          → core/npc/goals.py
core/npc_systems/schedules.py      → core/npc/schedules.py
core/npc_systems/interactions.py   → core/npc/interactions.py
core/npc_systems/relationships.py  → core/npc/relationships.py
core/npc_systems/gossip.py         → core/npc/gossip.py
```

### Success Criteria
- [ ] Zero duplicate code between directories
- [ ] All tests passing
- [ ] All imports updated
- [ ] Documentation updated
- [ ] ~6,100 lines removed

### Risk Mitigation
- Create feature branch for testing
- Keep backup of both directories until validation complete
- Update imports in small batches
- Run tests after each batch

---

## Phase 2: Split game_state.py (Priority P0)

### Objective
Split monolithic 3,017-line file into 5 focused modules

### Current Structure Analysis
```
core/game_state.py (3,017 lines)
├── Classes: 3
├── Functions: 88
└── Complexity: CRITICAL
```

### Target Structure
```
core/game_state/
├── __init__.py           # Public API exports
├── player_state.py       # Player management (~600 lines)
├── world_state.py        # World/environment (~600 lines)
├── npc_state.py          # NPC tracking (~600 lines)
├── event_state.py        # Events/history (~600 lines)
└── core_state.py         # Shared utilities (~400 lines)
```

### Steps

1. **Analysis Phase** (8 hours)
   - Map all classes and their responsibilities
   - Identify dependencies between components
   - Document public API surface
   - List all external imports

2. **Design Phase** (4 hours)
   - Define module boundaries
   - Design __init__.py public API
   - Plan backward compatibility strategy
   - Create migration guide

3. **Implementation Phase** (40 hours)
   
   **Step 3a**: Create directory structure (1 hour)
   ```bash
   mkdir -p core/game_state
   touch core/game_state/__init__.py
   ```

   **Step 3b**: Extract player_state.py (8 hours)
   - Move player-related classes
   - Move player-related methods
   - Update internal imports
   - Test independently

   **Step 3c**: Extract world_state.py (8 hours)
   - Move world/area classes
   - Move environment methods
   - Update internal imports
   - Test independently

   **Step 3d**: Extract npc_state.py (8 hours)
   - Move NPC tracking classes
   - Move NPC-related methods
   - Update internal imports
   - Test independently

   **Step 3e**: Extract event_state.py (8 hours)
   - Move event queue classes
   - Move history methods
   - Update internal imports
   - Test independently

   **Step 3f**: Create core_state.py (4 hours)
   - Move shared utilities
   - Move common base classes
   - Ensure no circular dependencies

   **Step 3g**: Create public API (4 hours)
   - Design __init__.py exports
   - Maintain backward compatibility:
     ```python
     # core/game_state/__init__.py
     from .player_state import PlayerState
     from .world_state import WorldState
     from .npc_state import NPCState
     from .event_state import EventState
     
     # Maintain old imports
     __all__ = ['PlayerState', 'WorldState', 'NPCState', 'EventState']
     ```

4. **Migration Phase** (16 hours)
   - Update all external imports
   - Add deprecation warnings
   - Update tests
   - Update documentation

5. **Validation Phase** (8 hours)
   - Run full test suite
   - Performance testing
   - Integration testing
   - Documentation review

### Success Criteria
- [ ] No single file > 700 lines
- [ ] All tests passing
- [ ] No circular dependencies
- [ ] Backward compatible imports
- [ ] Documentation complete

### Risk Mitigation
- Maintain backward compatibility in __init__.py
- Keep original file as backup
- Migrate in phases with validation
- Use feature flags if needed

---

## Phase 3: Test Organization (Priority P1)

### Objective
Consolidate all test files into `tests/` directory

### Current State
- 40 test files in `tests/` directory
- 32 test files in root directory
- Inconsistent naming conventions

### Target Structure
```
tests/
├── unit/
│   ├── test_core/
│   ├── test_npc/
│   └── test_narrative/
├── integration/
│   ├── test_api/
│   └── test_game_flow/
├── fixtures/
│   └── common_fixtures.py
└── conftest.py
```

### Steps

1. **Audit Phase** (4 hours)
   - List all test files in root
   - Categorize by type (unit/integration)
   - Check for test duplicates
   - Document dependencies

2. **Migration Phase** (8 hours)
   - Move files to appropriate directories
   - Update import paths
   - Update pytest configuration
   - Update CI/CD scripts

3. **Organization Phase** (4 hours)
   - Rename for consistency
   - Add category directories
   - Create shared fixtures
   - Update documentation

4. **Validation Phase** (4 hours)
   - Run all tests
   - Verify CI/CD pipeline
   - Update coverage reports

### Success Criteria
- [ ] All tests in `tests/` directory
- [ ] Clear categorization
- [ ] Consistent naming
- [ ] CI/CD updated
- [ ] All tests passing

---

## Phase 4: Quality Improvements (Priority P1-P2)

### Test Coverage Enhancement
- **Target**: Increase from 68% to 80%
- **Effort**: 40 hours
- **Approach**: Add tests for uncovered modules

### Documentation
- **Target**: Document all public APIs
- **Effort**: 24 hours
- **Approach**: Add docstrings and README files

### File Size Reduction
- **Target**: Average file size < 400 lines
- **Effort**: 32 hours
- **Approach**: Split remaining large files (20+ files > 600 lines)

---

## Timeline and Milestones

### Sprint 1-2 (Weeks 1-4)
- ✓ Phase 1: NPC Module Consolidation
- ✓ Phase 2: Split game_state.py (partial)

### Sprint 3-4 (Weeks 5-8)
- ✓ Phase 2: Split game_state.py (complete)
- ✓ Phase 3: Test Organization

### Sprint 5-6 (Weeks 9-12)
- ✓ Phase 4: Quality Improvements
- ✓ Documentation updates
- ✓ Performance optimization

### Sprint 7-8 (Weeks 13-16)
- ✓ Final validation
- ✓ Performance benchmarks
- ✓ Code review
- ✓ Release preparation

---

## Success Metrics

### Code Quality Goals
| Metric | Current | Target | Status |
|--------|---------|--------|--------|
| Code Duplication | 20% | <5% | 🔴 |
| Average File Size | 297 lines | <350 lines | 🟢 |
| Largest File | 3,017 lines | <700 lines | 🔴 |
| Test Coverage | 68% | 80% | 🟡 |
| Overall Score | 81/100 | 90/100 | 🟡 |

### Technical Debt Reduction
| Category | Current | Target | Reduction |
|----------|---------|--------|-----------|
| Architecture | 16,000 lines | 3,000 lines | -81% |
| Testing | 13,500 lines | 5,000 lines | -63% |
| Documentation | 9,000 lines | 2,000 lines | -78% |
| Performance | 5,000 lines | 2,000 lines | -60% |
| **Total** | **43,500** | **12,000** | **-72%** |

---

## Risk Assessment

### High Risk Items
1. **Breaking Changes**: Refactoring may break existing integrations
   - **Mitigation**: Maintain backward compatibility, feature flags
   
2. **Test Coverage Gaps**: May not catch all regressions
   - **Mitigation**: Increase test coverage before refactoring

3. **Time Estimation**: May take longer than planned
   - **Mitigation**: Phase approach, regular checkpoints

### Medium Risk Items
1. **Team Availability**: Resource constraints
2. **Merge Conflicts**: Parallel development
3. **Performance Regression**: New structure may impact performance

---

## Communication Plan

### Weekly Updates
- Progress on refactoring tasks
- Issues encountered
- Metrics dashboard
- Next steps

### Milestone Reviews
- End of each phase
- Demo of improvements
- Stakeholder feedback
- Go/no-go decisions

---

## Conclusion

This refactoring plan addresses the critical architectural issues identified in the code review. By following this phased approach, we can reduce technical debt by 72% while maintaining system stability and backward compatibility.

**Next Steps**:
1. Review and approve this plan
2. Allocate resources
3. Begin Phase 1: NPC Module Consolidation
4. Set up monitoring and metrics
