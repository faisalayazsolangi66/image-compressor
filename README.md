# Image Compressor

Compress JPEG images by lowering quality. It re-saves each JPEG at the quality you choose and reports how much space each file saved.

## Requirements

- Python 3
- Pillow (`pip install -r requirements.txt`)

## How to run

```bash
pip install -r requirements.txt
python3 main.py --help
python3 main.py photos/ --quality 70 --output compressed/
```

Options:

- `--quality` — JPEG quality 1–95 (default: `75`, lower = smaller)
- `--output` — output folder (default: `compressed`)
- `--max-width` — also shrink images wider than this (default: `0` = keep size)
- `--in-place` — overwrite the original files instead of writing to `--output`

## Example

```bash
$ python3 main.py photos/ --quality 70 --output compressed/
photos/sunset.jpg -> compressed/sunset.jpg: 512.0 KB -> 148.2 KB (71% smaller)
Done: 1 file(s), 512.0 KB -> 148.2 KB (71% smaller overall).
```
