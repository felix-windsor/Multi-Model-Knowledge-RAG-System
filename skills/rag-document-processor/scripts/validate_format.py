#!/usr/bin/env python3
"""
Document format validation script.

Usage:
    python validate_format.py <file_path>
    python validate_format.py <file_path> --verbose
    python validate_format.py <directory> --batch

Applies: format-auto-detect, format-validate-structure
"""

import sys
import argparse
from pathlib import Path
from typing import Dict, Any, Tuple, Literal
import json

DocumentFormat = Literal['pdf', 'docx', 'pptx', 'xlsx', 'jpg', 'png', 'txt', 'md']

# Magic byte signatures
MAGIC_SIGNATURES = {
    b'%PDF': 'pdf',
    b'PK\x03\x04': 'office',  # ZIP-based formats
    b'\xff\xd8\xff': 'jpg',
    b'\x89PNG': 'png',
}

SUPPORTED_FORMATS = ['pdf', 'docx', 'pptx', 'xlsx', 'jpg', 'png', 'txt', 'md']


def detect_format(file_path: str) -> Tuple[DocumentFormat, Dict[str, Any]]:
    """
    Auto-detect document format from magic bytes.

    Returns:
        (format, metadata) with detection confidence and warnings
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    # Read magic bytes
    with open(file_path, 'rb') as f:
        magic_bytes = f.read(8)

    # Detect from magic bytes
    detected_format = None
    for signature, fmt in MAGIC_SIGNATURES.items():
        if magic_bytes.startswith(signature):
            detected_format = fmt
            break

    # For Office formats, check specific type
    if detected_format == 'office':
        try:
            detected_format = detect_office_type(file_path)
        except Exception as e:
            detected_format = 'unknown'

    # Plain text formats (no magic bytes)
    if detected_format is None:
        extension = path.suffix.lower().lstrip('.')
        if extension in ['txt', 'md']:
            detected_format = extension

    # Get extension for validation
    extension = path.suffix.lower().lstrip('.')

    metadata = {
        'detected_format': detected_format,
        'extension': extension,
        'file_size': path.stat().st_size,
        'confidence': 'high',
        'warnings': [],
        'supported': detected_format in SUPPORTED_FORMATS
    }

    # Validate consistency
    if extension != detected_format:
        metadata['warnings'].append(
            f"Extension mismatch: file is '{detected_format}' but named '.{extension}'"
        )
        metadata['confidence'] = 'medium'

    if not metadata['supported']:
        metadata['warnings'].append(
            f"Unsupported format: '{detected_format}'"
        )

    return detected_format, metadata


def detect_office_type(file_path: str) -> DocumentFormat:
    """Detect specific Office document type from ZIP structure."""
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

    return 'unknown'


def validate_structure(file_path: str, format_type: str) -> Dict[str, Any]:
    """
    Validate document structure integrity.

    Returns:
        Validation results with any structural issues
    """
    issues = []

    if format_type == 'pdf':
        issues.extend(validate_pdf_structure(file_path))
    elif format_type in ['docx', 'pptx', 'xlsx']:
        issues.extend(validate_office_structure(file_path))
    elif format_type in ['jpg', 'png']:
        issues.extend(validate_image_structure(file_path))

    return {
        'valid': len(issues) == 0,
        'issues': issues
    }


def validate_pdf_structure(file_path: str) -> list:
    """Validate PDF structure."""
    issues = []

    try:
        import PyPDF2
        with open(file_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            num_pages = len(reader.pages)

            if num_pages == 0:
                issues.append("PDF has no pages")

            # Check if encrypted
            if reader.is_encrypted:
                issues.append("PDF is encrypted")

    except Exception as e:
        issues.append(f"PDF validation failed: {str(e)}")

    return issues


def validate_office_structure(file_path: str) -> list:
    """Validate Office document structure."""
    import zipfile
    issues = []

    try:
        with zipfile.ZipFile(file_path, 'r') as zf:
            # Check for required files
            required_files = ['[Content_Types].xml', '_rels/.rels']
            for req_file in required_files:
                if req_file not in zf.namelist():
                    issues.append(f"Missing required file: {req_file}")

            # Test ZIP integrity
            bad_files = zf.testzip()
            if bad_files:
                issues.append(f"Corrupted ZIP entries: {bad_files}")

    except zipfile.BadZipFile:
        issues.append("Invalid ZIP structure")
    except Exception as e:
        issues.append(f"Office validation failed: {str(e)}")

    return issues


def validate_image_structure(file_path: str) -> list:
    """Validate image file structure."""
    issues = []

    try:
        from PIL import Image
        with Image.open(file_path) as img:
            # Check if image can be loaded
            img.verify()

            # Check dimensions
            if img.size[0] == 0 or img.size[1] == 0:
                issues.append("Image has zero dimensions")

    except Exception as e:
        issues.append(f"Image validation failed: {str(e)}")

    return issues


def validate_file(file_path: str, verbose: bool = False) -> Dict[str, Any]:
    """
    Validate a single file.

    Returns:
        Complete validation report
    """
    try:
        # Detect format
        format_type, format_meta = detect_format(file_path)

        # Validate structure
        structure_validation = validate_structure(file_path, format_type)

        result = {
            'file': str(file_path),
            'format': format_type,
            'format_metadata': format_meta,
            'structure_validation': structure_validation,
            'overall_valid': (
                format_meta['supported'] and
                structure_validation['valid'] and
                len(format_meta['warnings']) == 0
            )
        }

        return result

    except Exception as e:
        return {
            'file': str(file_path),
            'error': str(e),
            'overall_valid': False
        }


def validate_batch(directory: str, verbose: bool = False) -> Dict[str, Any]:
    """Validate all files in a directory."""
    path = Path(directory)
    results = []
    summary = {
        'total': 0,
        'valid': 0,
        'invalid': 0,
        'unsupported': 0
    }

    for file_path in path.rglob('*'):
        if file_path.is_file():
            result = validate_file(str(file_path), verbose)
            results.append(result)
            summary['total'] += 1

            if result.get('overall_valid'):
                summary['valid'] += 1
            elif result.get('format_metadata', {}).get('supported') == False:
                summary['unsupported'] += 1
            else:
                summary['invalid'] += 1

    return {
        'summary': summary,
        'results': results
    }


def print_result(result: Dict[str, Any], verbose: bool = False):
    """Print validation result in human-readable format."""
    file_name = Path(result['file']).name

    if 'error' in result:
        print(f"❌ {file_name}: ERROR - {result['error']}")
        return

    format_type = result['format']
    format_meta = result['format_metadata']
    structure = result['structure_validation']

    # Overall status
    if result['overall_valid']:
        status = "✅"
    elif not format_meta['supported']:
        status = "⚠️"
    else:
        status = "❌"

    print(f"{status} {file_name} ({format_type}, {format_meta['file_size']:,} bytes)")

    # Warnings
    if format_meta['warnings']:
        for warning in format_meta['warnings']:
            print(f"   ⚠️  {warning}")

    # Structure issues
    if structure['issues']:
        for issue in structure['issues']:
            print(f"   ❌ {issue}")

    # Verbose details
    if verbose:
        print(f"   Confidence: {format_meta['confidence']}")
        print(f"   Extension: .{format_meta['extension']}")


def main():
    parser = argparse.ArgumentParser(
        description='Validate document format and structure',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python validate_format.py document.pdf
    python validate_format.py document.pdf --verbose
    python validate_format.py /path/to/documents --batch
    python validate_format.py /path/to/documents --batch --json
        """
    )
    parser.add_argument('path', help='File or directory to validate')
    parser.add_argument('--batch', action='store_true', help='Batch validate directory')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    parser.add_argument('--json', action='store_true', help='Output JSON format')

    args = parser.parse_args()

    # Batch or single file
    if args.batch:
        results = validate_batch(args.path, args.verbose)

        if args.json:
            print(json.dumps(results, indent=2))
        else:
            print(f"\n📊 Validation Summary")
            print(f"   Total files: {results['summary']['total']}")
            print(f"   ✅ Valid: {results['summary']['valid']}")
            print(f"   ❌ Invalid: {results['summary']['invalid']}")
            print(f"   ⚠️  Unsupported: {results['summary']['unsupported']}\n")

            for result in results['results']:
                print_result(result, args.verbose)

    else:
        result = validate_file(args.path, args.verbose)

        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print_result(result, args.verbose)

        # Exit code
        sys.exit(0 if result['overall_valid'] else 1)


if __name__ == '__main__':
    main()
