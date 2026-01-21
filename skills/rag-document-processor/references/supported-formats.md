# Supported Document Formats

Complete reference for formats supported by the RAG Document Processor.

## Quick Reference

| Format | Extensions | Magic Bytes | Processing Method | OCR Required |
|--------|-----------|-------------|-------------------|--------------|
| PDF | `.pdf` | `%PDF` | PyPDF2, MinerU | Sometimes* |
| Word | `.docx` | `PK\x03\x04` | LibreOffice → PDF | No |
| PowerPoint | `.pptx` | `PK\x03\x04` | LibreOffice → PDF | No |
| Excel | `.xlsx` | `PK\x03\x04` | LibreOffice → PDF | No |
| JPEG | `.jpg`, `.jpeg` | `\xff\xd8\xff` | Tesseract OCR | Yes |
| PNG | `.png` | `\x89PNG` | Tesseract OCR | Yes |
| Plain Text | `.txt` | N/A | Direct read | No |
| Markdown | `.md` | N/A | Direct read | No |

*OCR required for scanned PDFs (detected automatically)

## Detailed Format Support

### 1. PDF Documents

**Full Support**: ✅

**Capabilities**:
- Text extraction (native PDFs)
- OCR for scanned/image-based PDFs
- Table detection and preservation
- Metadata extraction (author, date, title)
- Multi-page streaming processing

**Processing Pipeline**:
```
PDF → Auto-detect (native vs scanned)
    ├─ Native PDF → PyPDF2 text extraction
    └─ Scanned PDF → MinerU OCR pipeline
         → Text + layout preservation
```

**Limitations**:
- Encrypted PDFs require password
- Some complex layouts may lose formatting
- Handwritten text recognition limited

**Configuration**:
```bash
PDF_STREAM_CHUNK_SIZE=4096
PDF_PARALLEL_PAGES=True
PDF_OCR_AUTO_DETECT=True
PDF_OCR_LANGUAGE=chi_sim+eng
```

**Related Rules**:
- `format-auto-detect` - Detect native vs scanned
- `extract-streaming` - Memory-efficient processing
- `extract-ocr-smart` - Automatic OCR triggering
- `extract-table-detection` - Preserve table structures

### 2. Microsoft Word (.docx)

**Full Support**: ✅

**Capabilities**:
- Full text extraction including headers/footers
- Preserve formatting (bold, italic, lists)
- Extract images embedded in document
- Track changes and comments (optional)

**Processing Pipeline**:
```
DOCX → LibreOffice headless conversion
     → PDF
     → Text extraction (via PDF pipeline)
```

**Why Convert to PDF First?**
- Consistent layout preservation
- Reuse PDF extraction pipeline
- Better table handling
- Metadata preservation

**Limitations**:
- Complex Word features may be simplified (macros, custom styles)
- Conversion adds ~2-3s per document
- Requires LibreOffice installation

**Configuration**:
```bash
LIBREOFFICE_PATH=/usr/bin/libreoffice
LIBREOFFICE_TIMEOUT=30
DOCX_PRESERVE_FORMATTING=True
DOCX_EXTRACT_IMAGES=True
```

**Related Rules**:
- `format-office-libreoffice` - Conversion setup
- `extract-preserve-layout` - Formatting preservation
- `error-retry-strategy` - Handle conversion failures

### 3. Microsoft PowerPoint (.pptx)

**Full Support**: ✅

**Capabilities**:
- Extract text from slides
- Extract speaker notes
- Preserve slide order
- Extract embedded images

**Processing Pipeline**:
```
PPTX → LibreOffice conversion
     → PDF (1 slide = 1 page)
     → Text + layout extraction
```

**Special Considerations**:
- Slide transitions/animations ignored
- Text in images requires OCR
- Speaker notes extracted separately

**Configuration**:
```bash
PPTX_INCLUDE_NOTES=True
PPTX_SLIDES_PER_BATCH=10
```

**Related Rules**:
- `format-office-libreoffice`
- `extract-parallel-pages` - Process slides in parallel

### 4. Microsoft Excel (.xlsx)

**Partial Support**: ⚠️

**Capabilities**:
- Extract cell text content
- Preserve sheet structure
- Extract formulas (as text)

**Limitations**:
- Complex formulas not evaluated
- Charts and graphs converted to images (require OCR)
- Pivot tables simplified
- Macros ignored

**Processing Pipeline**:
```
XLSX → LibreOffice conversion
     → PDF (1 sheet = 1 page)
     → Table extraction
```

**Recommended Alternative**:
For data-heavy Excel files, consider direct pandas/openpyxl parsing instead of PDF conversion.

**Configuration**:
```bash
XLSX_EXTRACT_FORMULAS=True
XLSX_SHEETS_FILTER=all  # or "Sheet1,Sheet2"
```

### 5. Images (JPG, PNG)

**Full Support**: ✅ (via OCR)

**Capabilities**:
- OCR text extraction (Tesseract)
- Multi-language support
- Image preprocessing for better accuracy
- Layout detection

**Processing Pipeline**:
```
Image → Preprocessing (resize, denoise, deskew)
      → Tesseract OCR
      → Text + bounding boxes
```

**Image Preprocessing**:
- Auto-rotation (fix upside-down)
- Deskewing (straighten tilted scans)
- Denoising (remove artifacts)
- Contrast enhancement

**OCR Accuracy Factors**:
- ✅ High quality scans (300+ DPI): 95-98% accuracy
- ⚠️ Photos of documents: 80-90% accuracy
- ❌ Handwritten text: 60-70% accuracy

**Configuration**:
```bash
OCR_ENGINE=tesseract
OCR_LANGUAGE=chi_sim+eng
OCR_DPI=300
IMAGE_PREPROCESSING=True
```

**Related Rules**:
- `format-image-preprocessing` - Improve OCR accuracy
- `extract-ocr-smart` - Automatic triggering

### 6. Plain Text (.txt, .md)

**Full Support**: ✅

**Capabilities**:
- Direct text reading
- Encoding detection (UTF-8, GBK, etc.)
- Markdown parsing (for .md files)

**Processing Pipeline**:
```
TXT/MD → Encoding detection
       → Direct read
       → Chunking (if large)
```

**Special Handling**:
- Markdown files preserve structure (headers, lists)
- Large text files (>10MB) use streaming
- Auto-detect encoding (fallback to UTF-8)

**Configuration**:
```bash
TEXT_ENCODING_DETECT=True
TEXT_CHUNK_SIZE=10000  # chars
MARKDOWN_PARSE_STRUCTURE=True
```

## Format Detection Priority

The system uses this detection priority:

1. **Magic Bytes** (highest priority)
   - Read first 8 bytes of file
   - Match against known signatures

2. **ZIP Structure** (for Office formats)
   - Check internal XML structure
   - Differentiate DOCX/PPTX/XLSX

3. **File Extension** (fallback)
   - Used for validation only
   - Warning if mismatch with magic bytes

**Example**:
```python
# User uploads "report.pdf" (actually a renamed DOCX)

# Detection process:
magic_bytes = b'PK\x03\x04'  # ZIP signature
zip_contents = ['word/document.xml']  # DOCX structure
extension = 'pdf'

# Result: Detected as DOCX with warning
# "Extension mismatch: file is 'docx' but named '.pdf'"
```

## Unsupported Formats

These formats are **not supported**:

| Format | Reason | Alternative |
|--------|--------|-------------|
| `.doc` (Old Word) | Legacy binary format | Convert to .docx first |
| `.xls` (Old Excel) | Legacy format | Convert to .xlsx first |
| `.ppt` (Old PowerPoint) | Legacy format | Convert to .pptx first |
| `.rtf` | Complex formatting | Convert to .docx |
| `.odt`, `.ods` | LibreOffice native | Convert to PDF manually |
| `.epub`, `.mobi` | eBook formats | Not planned |
| Video/Audio | Multimedia | Not applicable for text RAG |

**Workaround for Legacy Formats**:
```bash
# Convert using LibreOffice
libreoffice --headless --convert-to docx old-file.doc
```

## Adding New Format Support

To add a new format:

1. **Add magic byte signature** to `format-auto-detect`
2. **Implement extraction method** following `extract-streaming` pattern
3. **Add validation** to `format-validate-structure`
4. **Update this documentation**
5. **Add test fixtures**

**Template**:
```python
# In extract_content.py
def extract_NEW_FORMAT(file_path: str) -> Iterator[dict]:
    """Extract content from NEW_FORMAT files."""
    # 1. Validate format
    # 2. Stream content
    # 3. Yield chunks
    pass
```

## Performance by Format

Average processing time (Intel i5, 16GB RAM):

| Format | File Size | Processing Time | Memory Usage |
|--------|-----------|----------------|--------------|
| PDF (native) | 10MB (50 pages) | 2-3s | 50MB |
| PDF (scanned) | 10MB (50 pages) | 30-40s | 200MB |
| DOCX | 5MB (100 pages) | 8-10s | 100MB |
| PPTX | 10MB (50 slides) | 10-12s | 150MB |
| XLSX | 2MB (10 sheets) | 5-7s | 80MB |
| JPG (image) | 2MB | 3-5s | 100MB |

*Times include conversion, extraction, and embedding generation

## Troubleshooting

### "Unsupported format" Error

**Cause**: Format not in supported list or corrupted file

**Solution**:
1. Run `python scripts/validate_format.py <file>`
2. Check magic bytes detection
3. Verify file isn't corrupted
4. Convert to supported format if needed

### "LibreOffice conversion failed"

**Cause**: LibreOffice not installed or path incorrect

**Solution**:
```bash
# Install LibreOffice
sudo apt-get install libreoffice

# Set path in .env
LIBREOFFICE_PATH=/usr/bin/libreoffice
```

### "OCR accuracy is poor"

**Cause**: Low quality image or wrong language setting

**Solution**:
1. Enable image preprocessing: `IMAGE_PREPROCESSING=True`
2. Set correct language: `OCR_LANGUAGE=chi_sim+eng`
3. Increase DPI if possible: `OCR_DPI=300`
4. Check image quality (should be 300+ DPI)

## See Also

- `format-auto-detect.md` - Format detection implementation
- `extraction-pipeline.md` - Complete processing workflow
- `libreoffice-setup.md` - LibreOffice configuration
- `mineru-guide.md` - MinerU OCR tuning
