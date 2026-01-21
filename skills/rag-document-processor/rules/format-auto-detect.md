# format-auto-detect

**Priority**: 1 (CRITICAL)
**Category**: Format Detection & Validation
**Impact**: Prevents processing failures due to incorrect format assumptions

## Why It Matters

Relying solely on file extensions is unreliable - files can be renamed or have incorrect extensions. Auto-detecting format from magic bytes ensures you process the file correctly.

**Incorrect approach** leads to:
- Processing failures (treating a DOCX as PDF)
- Data corruption (wrong parser for format)
- Poor user experience (cryptic error messages)

**Performance impact**: Negligible (<1ms) for massive reliability gain

## ❌ Incorrect Implementation

```python
# BAD: Only checking file extension
def process_document(file_path: str):
    if file_path.endswith('.pdf'):
        return process_pdf(file_path)
    elif file_path.endswith('.docx'):
        return process_docx(file_path)
    else:
        raise ValueError("Unsupported format")
```

**Problems:**
- File renamed from `report.docx` to `report.pdf` will fail
- User uploads `image.jpg` but file is actually PNG
- No validation of actual file content

## ✅ Correct Implementation

```python
import magic
from pathlib import Path
from typing import Literal, Tuple

DocumentFormat = Literal['pdf', 'docx', 'pptx', 'xlsx', 'jpg', 'png', 'txt']

# Magic byte signatures
MAGIC_SIGNATURES = {
    b'%PDF': 'pdf',
    b'PK\x03\x04': 'office',  # ZIP-based (DOCX, PPTX, XLSX)
    b'\xff\xd8\xff': 'jpg',
    b'\x89PNG': 'png',
}

def detect_format(file_path: str) -> Tuple[DocumentFormat, dict]:
    """
    Auto-detect document format from magic bytes and extension.

    Returns:
        (format, metadata) where metadata contains confidence and warnings
    """
    path = Path(file_path)

    # Read magic bytes
    with open(file_path, 'rb') as f:
        magic_bytes = f.read(8)

    # Detect from magic bytes (primary)
    detected_format = None
    for signature, fmt in MAGIC_SIGNATURES.items():
        if magic_bytes.startswith(signature):
            detected_format = fmt
            break

    # For Office formats, check specific type
    if detected_format == 'office':
        detected_format = detect_office_type(file_path)

    # Get extension (secondary validation)
    extension = path.suffix.lower().lstrip('.')

    # Validate consistency
    metadata = {
        'detected_format': detected_format,
        'extension': extension,
        'confidence': 'high',
        'warnings': []
    }

    if extension != detected_format:
        metadata['warnings'].append(
            f"Extension mismatch: file is {detected_format} but named .{extension}"
        )
        metadata['confidence'] = 'medium'

    return detected_format, metadata

def detect_office_type(file_path: str) -> DocumentFormat:
    """Detect specific Office format from ZIP structure."""
    import zipfile

    try:
        with zipfile.ZipFile(file_path) as zf:
            files = zf.namelist()

            if 'word/document.xml' in files:
                return 'docx'
            elif 'ppt/presentation.xml' in files:
                return 'pptx'
            elif 'xl/workbook.xml' in files:
                return 'xlsx'
    except zipfile.BadZipFile:
        raise ValueError("Corrupted Office document (invalid ZIP)")

    raise ValueError("Unknown Office format")

# Usage
def process_document(file_path: str):
    # Auto-detect format
    format_type, metadata = detect_format(file_path)

    # Log warnings if any
    if metadata['warnings']:
        logger.warning(f"Format detection warnings: {metadata['warnings']}")

    # Process based on actual format (not extension)
    if format_type == 'pdf':
        return process_pdf(file_path)
    elif format_type == 'docx':
        return process_docx(file_path)
    elif format_type in ['jpg', 'png']:
        return process_image(file_path)
    else:
        raise ValueError(f"Unsupported format: {format_type}")
```

**Benefits:**
- ✅ Detects actual file format regardless of extension
- ✅ Warns users about extension mismatches
- ✅ Prevents processing with wrong parser
- ✅ Provides confidence score for validation

## Integration Points

Apply this rule in:

- `backend/app/api/upload.py` - Validate uploaded files immediately
- `backend/app/services/document_service.py` - Before processing
- `scripts/validate_format.py` - Standalone validation tool

## Performance Notes

- Magic byte detection: <1ms per file
- Office type detection: 5-10ms (requires ZIP reading)
- Recommended: Cache results for repeated validation

## Related Rules

- `format-validate-structure` - Deeper validation after format detection
- `format-handle-corrupted` - Handle detection failures gracefully
- `error-graceful-degradation` - Fallback strategies when detection fails

## Real-World Example

```python
# User uploads "report.pdf" but it's actually a renamed DOCX
# ❌ Without auto-detection:
#    → Tries to parse as PDF
#    → Fails with cryptic error: "PDF header not found"

# ✅ With auto-detection:
format_type, metadata = detect_format("report.pdf")
# → Returns: ('docx', {warnings: ['Extension mismatch: file is docx but named .pdf']})
# → Processes correctly with DOCX parser
# → Warns user about the mismatch
```

## Testing

```python
def test_format_auto_detect():
    # Test PDF
    assert detect_format('tests/fixtures/sample.pdf')[0] == 'pdf'

    # Test renamed file
    format_type, metadata = detect_format('tests/fixtures/renamed.pdf')
    assert format_type == 'docx'
    assert len(metadata['warnings']) > 0

    # Test corrupted file
    with pytest.raises(ValueError):
        detect_format('tests/fixtures/corrupted.docx')
```
