# Proposal: refactor-console-app

## Intent

Refactor console/app.py (452 lines) from a monolithic file mixing UI, input handling, business logic, and output formatting into a modular structure with clean separation of concerns. Remove dead code (`_generar_certulario`) and extract repeated validation/formatting logic into reusable modules.

## Scope

### In Scope
- Create `console/ui/` module with MenuConsola class
- Create `console/validators/` module with input validation helpers
- Create `console/formatters/` module with table and message formatters
- Refactor app.py into thin entry point (~60 lines)
- Remove dead code: `_generar_certulario()` (line 346)
- Verify I/O behavior matches original

### Out of Scope
- Changes to business logic in services/servicios.py
- GUI or web applications
- Database schema changes

## Capabilities

> This is a pure refactor — no new capabilities, no spec-level behavior changes.

### New Capabilities
None (pure refactoring)

### Modified Capabilities
None (existing console functionality preserved)

## Approach

1. Create module directories with `__init__.py`: `ui/`, `validators/`, `formatters/`
2. Move `MenuConsola` class to `ui/menu.py`
3. Extract validation helpers to `validators/input_helpers.py`: cedula validation, required field checks
4. Extract output formatters to `formatters/table_formatter.py`: table display, messages
5. Refactor `app.py` to import from new modules, keep only orchestration logic
6. Verify by running app and comparing output

## Affected Areas

| Area | Impact | Description |
|------|--------|-------------|
| `console/app.py` | Modified | Thin entry point, ~60 lines |
| `console/ui/__init__.py` | New | UI module |
| `console/ui/menu.py` | New | MenuConsola class |
| `console/ui/handlers.py` | New | Menu building and navigation |
| `console/validators/__init__.py` | New | Validators module |
| `console/validators/input_helpers.py` | New | Validation helpers |
| `console/formatters/__init__.py` | New | Formatters module |
| `console/formatters/table_formatter.py` | New | Table display, messages |

## Risks

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Import cycles between modules | Low | Clear dependency direction: app → ui → validators/formatters |
| Behavior regression | Low | Compare output before/after, test edge cases |

## Rollback Plan

1. Revert all new files in `ui/`, `validators/`, `formatters/`
2. Restore original `app.py` from git
3. Verify: `git checkout console/app.py`

## Dependencies

- Python 3.14+ (per sdd-init)
- No external dependencies required

## Success Criteria

- [ ] app.py reduced to ~60 lines
- [ ] All menu operations work identically
- [ ] Dead code removed
- [ ] No import cycles
- [ ] Tests pass (if exist)