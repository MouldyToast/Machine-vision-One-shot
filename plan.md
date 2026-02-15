# LabelImg: PyQt5 to PyQt6 Migration Plan

## Overview

Migrate all 17 Python source files, build scripts, CI configs, and packaging from PyQt5 to PyQt6. The codebase has ~2,500 lines of Qt-dependent code across `labelImg.py` and the `libs/` package.

---

## Phase 1: Update Imports Across All Files

**Goal:** Replace every `PyQt5` import with `PyQt6` and handle relocated modules.

### Step 1.1 — Replace `PyQt5` → `PyQt6` in all import statements

Files to update (all files importing from PyQt5):
- `labelImg.py`
- `libs/canvas.py`
- `libs/shape.py`
- `libs/utils.py`
- `libs/labelDialog.py`
- `libs/colorDialog.py`
- `libs/lightWidget.py`
- `libs/zoomWidget.py`
- `libs/toolBar.py`
- `libs/combobox.py`
- `libs/default_label_combobox.py`
- `libs/hashableQListWidgetItem.py`
- `libs/stringBundle.py`
- `libs/labelFile.py`
- `libs/ustr.py`
- `tests/test_qt.py`
- `tests/test_utils.py`

### Step 1.2 — Move `QAction` from `QtWidgets` to `QtGui`

In Qt6, `QAction` was moved back to `QtGui`. Every file that does:
```python
from PyQt5.QtWidgets import QAction
```
must become:
```python
from PyQt6.QtGui import QAction
```

Primary file affected: `libs/utils.py` (creates actions used app-wide).

---

## Phase 2: Fix Deprecated / Removed APIs

### Step 2.1 — Replace `exec_()` with `exec()`

Qt6 drops the underscore workaround. Change all calls:

| File | Line(s) | Change |
|------|---------|--------|
| `labelImg.py` | ~1496, ~1719 | `app.exec_()` → `app.exec()`, `dlg.exec_()` → `dlg.exec()` |
| `libs/colorDialog.py` | ~33 | `self.exec_()` → `self.exec()` |
| `libs/labelDialog.py` | ~87 | `self.exec_()` → `self.exec()` |

### Step 2.2 — Remove all `sip.setapi()` calls

Qt6 no longer uses SIP API v1/v2 distinction. Remove entirely from:
- `labelImg.py`
- `libs/combobox.py`
- `libs/default_label_combobox.py`
- `libs/hashableQListWidgetItem.py`
- `libs/stringBundle.py`

### Step 2.3 — Replace `QDesktopWidget` with `QScreen`

`QDesktopWidget` is removed in Qt6. In `labelImg.py` (~line 489-490):

```python
# Before (Qt5):
nScreens = QApplication.desktop().screenCount()
availGeo = QApplication.desktop().availableGeometry(i)

# After (Qt6):
screens = QApplication.screens()
nScreens = len(screens)
availGeo = screens[i].availableGeometry()
```

### Step 2.4 — Replace `QRegExp` with `QRegularExpression`

In `libs/utils.py` (~line 64):

```python
# Before (Qt5):
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator
validator = QRegExpValidator(QRegExp(r'[^ \t]+'), None)

# After (Qt6):
from PyQt6.QtCore import QRegularExpression
from PyQt6.QtGui import QRegularExpressionValidator
validator = QRegularExpressionValidator(QRegularExpression(r'[^ \t]+'), None)
```

### Step 2.5 — Replace `QFontMetrics.width()` with `horizontalAdvance()`

In `libs/lightWidget.py` (~line 25) and `libs/zoomWidget.py` (~line 25):

```python
# Before:
fm.width(str(self.maximum()))
# After:
fm.horizontalAdvance(str(self.maximum()))
```

### Step 2.6 — Fix `QTextStream.setCodec()` removal

In `libs/stringBundle.py` (~line 69):

```python
# Before (Qt5):
text = QTextStream(f)
text.setCodec("UTF-8")

# After (Qt6): QTextStream defaults to UTF-8, remove setCodec call.
# Or switch to pure Python file reading with open(path, encoding='utf-8').
```

Recommended: Replace the entire `QFile`/`QTextStream` block with standard Python `open()` since the file is a simple `.properties` file and doesn't need Qt I/O.

---

## Phase 3: Fix Qt6 Enum Scoping Changes

### Step 3.1 — Update all unscoped enums to fully-scoped enums

Qt6 requires fully-qualified enum names. This is the most pervasive change.

Examples of required changes throughout the codebase:

```python
# Cursors
Qt.ArrowCursor         → Qt.CursorShape.ArrowCursor
Qt.PointingHandCursor  → Qt.CursorShape.PointingHandCursor
Qt.CrossCursor         → Qt.CursorShape.CrossCursor
Qt.WaitCursor          → Qt.CursorShape.WaitCursor

# Alignment
Qt.AlignLeft           → Qt.AlignmentFlag.AlignLeft
Qt.AlignRight          → Qt.AlignmentFlag.AlignRight
Qt.AlignCenter         → Qt.AlignmentFlag.AlignCenter

# Toolbar areas
Qt.LeftToolBarArea     → Qt.ToolBarArea.LeftToolBarArea
Qt.RightToolBarArea    → Qt.ToolBarArea.RightToolBarArea
Qt.TopToolBarArea      → Qt.ToolBarArea.TopToolBarArea

# Dock widget areas
Qt.RightDockWidgetArea → Qt.DockWidgetArea.RightDockWidgetArea
Qt.NoDockWidgetArea    → Qt.DockWidgetArea.NoDockWidgetArea

# Window flags
Qt.Window              → Qt.WindowType.Window
Qt.WindowStaysOnTopHint → Qt.WindowType.WindowStaysOnTopHint

# Key codes
Qt.Key_Return          → Qt.Key.Key_Return
Qt.Key_Escape          → Qt.Key.Key_Escape
Qt.Key_Space           → Qt.Key.Key_Space
# (and all other Qt.Key_* constants)

# Mouse buttons
Qt.LeftButton          → Qt.MouseButton.LeftButton
Qt.RightButton         → Qt.MouseButton.RightButton

# Keyboard modifiers
Qt.ShiftModifier       → Qt.KeyboardModifier.ShiftModifier
Qt.ControlModifier     → Qt.KeyboardModifier.ControlModifier

# Item flags
Qt.ItemIsEnabled       → Qt.ItemFlag.ItemIsEnabled
Qt.ItemIsSelectable    → Qt.ItemFlag.ItemIsSelectable
Qt.ItemIsUserCheckable → Qt.ItemFlag.ItemIsUserCheckable

# Check state
Qt.Checked             → Qt.CheckState.Checked
Qt.Unchecked           → Qt.CheckState.Unchecked

# Scroll bar policy
Qt.ScrollBarAlwaysOff  → Qt.ScrollBarPolicy.ScrollBarAlwaysOff
Qt.ScrollBarAsNeeded   → Qt.ScrollBarPolicy.ScrollBarAsNeeded

# Focus policy
Qt.NoFocus             → Qt.FocusPolicy.NoFocus

# Pen styles
Qt.NoPen               → Qt.PenStyle.NoPen

# Orientation
Qt.Horizontal          → Qt.Orientation.Horizontal
Qt.Vertical            → Qt.Orientation.Vertical

# QMessageBox buttons
QMessageBox.Yes        → QMessageBox.StandardButton.Yes
QMessageBox.No         → QMessageBox.StandardButton.No
QMessageBox.Cancel     → QMessageBox.StandardButton.Cancel
QMessageBox.Save       → QMessageBox.StandardButton.Save
QMessageBox.Discard    → QMessageBox.StandardButton.Discard

# QMessageBox icons
QMessageBox.Warning    → QMessageBox.Icon.Warning
QMessageBox.Information → QMessageBox.Icon.Information

# QFileDialog options
QFileDialog.ShowDirsOnly → QFileDialog.Option.ShowDirsOnly

# QPainter render hints
QPainter.Antialiasing  → QPainter.RenderHint.Antialiasing
QPainter.HighQualityAntialiasing → QPainter.RenderHint.Antialiasing  # removed in Qt6

# QSizePolicy
QSizePolicy.Maximum    → QSizePolicy.Policy.Maximum
QSizePolicy.Minimum    → QSizePolicy.Policy.Minimum

# QPalette roles
QPalette.Base          → QPalette.ColorRole.Base
```

**Files affected:** Primarily `labelImg.py`, `libs/canvas.py`, `libs/shape.py`, `libs/labelDialog.py`, `libs/utils.py`.

### Step 3.2 — Fix enum flag combinations with bitwise OR

In Qt6, combining flags requires explicit use of the enum types. Check that bitwise OR operations between flags still work, e.g.:
```python
Qt.ItemIsEnabled | Qt.ItemIsSelectable
→ Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable
```

---

## Phase 4: Fix QFileDialog Return Value Changes

### Step 4.1 — Update `QFileDialog` static method return values

In Qt6, `QFileDialog.getOpenFileName()` and similar methods return a tuple `(filename, filter)` — same as Qt5, but verify all call sites unpack correctly. The codebase currently uses index `[0]` to get the filename, which should still work.

Review all usages in `labelImg.py` to confirm they handle the tuple return.

---

## Phase 5: Update Resource Compilation

### Step 5.1 — Update Makefile

Replace `pyrcc5` with PyQt6's resource approach. Note: PyQt6 removed the `pyrcc6` tool. Resources must be loaded differently.

**Option A (Recommended):** Use `importlib.resources` or load files directly from the filesystem instead of compiled `.qrc`.

**Option B:** Use the `PyQt6` resource system via `rcc` from the Qt6 SDK:
```makefile
# Replace pyrcc5 with rcc from Qt6 SDK
qt6:
	/path/to/qt6/rcc -g python -o libs/resources.py resources.qrc
```

### Step 5.2 — Regenerate `libs/resources.py`

After choosing the resource approach, regenerate the compiled resource file. If using Option A, refactor resource loading in `libs/stringBundle.py` and anywhere `:/` prefixed paths are used.

---

## Phase 6: Update Dependencies and Build Configuration

### Step 6.1 — Update `requirements/requirements-linux-python3.txt`

```
PyQt6>=6.5.0
lxml==4.9.1
```

### Step 6.2 — Update `setup.py`

```python
REQUIRED_DEP = ['PyQt6', 'lxml']
REQUIRES_PYTHON = '>=3.8.0'  # PyQt6 requires Python 3.8+
```

Also update classifiers to reflect supported Python versions (3.8+).

### Step 6.3 — Update `.github/workflows/package.yml`

Replace all `pyqt5==5.15.6` references with `PyQt6>=6.5.0`.

Update PyInstaller hidden imports:
```
--hidden-import=pyqt5 → --hidden-import=PyQt6
```

### Step 6.4 — Update build scripts in `build-tools/`

Review and update:
- `build-ubuntu-binary.sh`
- `build-windows-binary.sh`
- `build-for-macos.sh`
- `build-for-pypi.sh`

---

## Phase 7: Update Tests

### Step 7.1 — Update test imports

In `tests/test_qt.py` and `tests/test_utils.py`:
- Replace `PyQt5` imports with `PyQt6`
- Update any enum references
- Ensure `QApplication` instantiation works with Qt6

---

## Phase 8: Verification and Testing

### Step 8.1 — Run the test suite
```bash
python3 -m unittest discover tests
```

### Step 8.2 — Manual smoke test
- Launch the app: `python3 labelImg.py`
- Open an image, draw bounding boxes
- Save in Pascal VOC, YOLO, and CreateML formats
- Test zoom, light adjustment, label editing
- Test keyboard shortcuts
- Test file browser and recent files

### Step 8.3 — Platform testing
- Test on Linux, macOS, and Windows
- Verify PyInstaller packaging still works

---

## Execution Order Summary

| Step | Description | Complexity | Files |
|------|------------|------------|-------|
| 1.1 | Replace PyQt5 → PyQt6 imports | Low | 17 files |
| 1.2 | Move QAction to QtGui import | Low | ~3 files |
| 2.1 | exec_() → exec() | Low | 4 files |
| 2.2 | Remove sip.setapi() calls | Low | 5 files |
| 2.3 | QDesktopWidget → QScreen | Medium | 1 file |
| 2.4 | QRegExp → QRegularExpression | Low | 1 file |
| 2.5 | QFontMetrics.width() → horizontalAdvance() | Low | 2 files |
| 2.6 | QTextStream.setCodec() removal | Low | 1 file |
| 3.1 | Fully-scoped enum migration | **High** | ~8 files |
| 3.2 | Fix flag combinations | Medium | ~4 files |
| 4.1 | QFileDialog return values | Low | 1 file |
| 5.1-5.2 | Resource compilation | Medium | 2 files |
| 6.1-6.4 | Dependencies & build config | Low | ~6 files |
| 7.1 | Test updates | Low | 2 files |
| 8.1-8.3 | Verification | — | — |

**Highest risk item:** Phase 3 (enum scoping) — most pervasive change, touching nearly every file. Requires careful search-and-replace with manual review.
