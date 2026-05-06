# Tasks: refactor-console-app

## Review Workload Forecast

| Field | Value |
|-------|-------|
| Estimated changed lines | ~350-400 |
| 400-line budget risk | Medium |
| Chained PRs recommended | No |
| Suggested split | Single PR |
| Delivery strategy | ask-on-risk |
| Chain strategy | pending |

Decision needed before apply: No
Chained PRs recommended: No
Chain strategy: stacked-to-main
400-line budget risk: Medium

### Suggested Work Units

| Unit | Goal | Likely PR | Notes |
|------|------|----------|-------|
| 1 | Create all new modules + refactor app.py | PR 1 | Single PR - infrastructure + integration together for atomic refactor |

## Phase 1: Infrastructure

- [ ] 1.1 Create `console/ui/__init__.py` — empty module init
- [ ] 1.2 Create `console/validators/__init__.py` — empty module init
- [ ] 1.3 Create `console/formatters/__init__.py` — empty module init

## Phase 2: Core Modules

- [ ] 2.1 Extract `MenuConsola` class to `console/ui/menu.py`
  - Copy class from `app.py` lines 34-60
  - Dependencies: Phase 1.1
  - Verify: Import works `from console.ui.menu import MenuConsola`

- [ ] 2.2 Create `console/ui/handlers.py` with menu builders
  - Create `_build_main_menu()`, `_build_estudiantes_menu()`, `_build_cursos_menu()`, etc.
  - Dependencies: Phase 2.1
  - Verify: Handlers return configured MenuConsola instances

- [ ] 2.3 Create `console/validators/input_helpers.py`
  - Extract `validar_cedula_ecuador` wrapper or check functions
  - Extract required field validators for nombres, celular, correo
  - Dependencies: Phase 1.2
  - Verify: Validation functions work identically

- [ ] 2.4 Create `console/formatters/table_formatter.py`
  - Extract table printing for estudiantes, cursos lists
  - Dependencies: Phase 1.3
  - Verify: Output format matches original

- [ ] 2.5 Create `console/formatters/menu_formatter.py`
  - Extract menu header/footer formatting
  - Dependencies: Phase 1.3
  - Verify: Menu display matches original

- [ ] 2.6 Create `console/formatters/data_formatter.py`
  - Extract data display formatters (estudiante details, curso details, certificados)
  - Dependencies: Phase 1.3
  - Verify: Data output matches original

## Phase 3: Integration

- [ ] 3.1 Refactor `console/app.py` to import from modules
  - Import MenuConsola from `console.ui.menu`
  - Import handlers from `console.ui.handlers`
  - Import validators from `console.validators.input_helpers`
  - Import formatters from `console.formatters`
  - Keep only `AplicacionConsola` orchestration
  - Dependencies: Phases 2.1-2.6
  - Verify: `python app.py` runs without errors

## Phase 4: Cleanup & Verification

- [ ] 4.1 Remove dead code (`_generar_certulario` method)
  - Delete lines 346-369 from original app.py
  - Dependencies: Phase 3.1
  - Verify: Only `_generar_certificado` remains (duplicated logic removed)

- [ ] 4.2 Verify behavior matches original
  - Run app.py and test each menu option
  - Check output matches original format
  - Dependencies: Phase 4.1
  - Verify: All menus work, data displays correctly, no regressions