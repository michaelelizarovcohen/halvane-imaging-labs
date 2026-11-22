"""Derive JPEG previews/thumbnails from published evidence files without modifying them.

Previews are *derivatives*: resized, sRGB, and saved WITHOUT any metadata. Originals are opened read-only.
RAW: largest embedded preview (via exiftool) or LibRaw demosaic; GoPro GPR: decoded with GoPro's gpr_tools
(set GPR_TOOLS=/path/to/gpr_tools); HEIC/HEIF: pillow-heif.
"""
import io, os, shutil, subprocess, tempfile
from PIL import Image, ImageOps

try:
    import pillow_heif
    pillow_heif.register_heif_opener()
except ImportError:  # pragma: no cover
    pillow_heif = None

RAW_EXT = {"cr2", "cr3", "crw", "nef", "nrw", "arw", "raf", "rw2", "rwl", "orf", "pef", "dng", "srw", "x3f",
           "erf", "dcr", "kdc", "mrw", "iiq", "gpr", "3fr"}
ORIENT = {3: Image.Transpose.ROTATE_180, 6: Image.Transpose.ROTATE_270, 8: Image.Transpose.ROTATE_90}


def _orientation(path):
    r = subprocess.run(["exiftool", "-n", "-s3", "-IFD0:Orientation", path], capture_output=True, text=True)
    try:
        return int(r.stdout.split()[0])
    except (ValueError, IndexError):
        return 1


def _embedded(path):
    best = None
    for tag in ("JpgFromRaw", "PreviewImage", "OtherImage", "ThumbnailImage"):
        r = subprocess.run(["exiftool", "-b", f"-{tag}", path], capture_output=True)
        if len(r.stdout) > 2000 and (best is None or len(r.stdout) > len(best)):
            best = r.stdout
    if not best:
        return None
    try:
        im = Image.open(io.BytesIO(best))
        im.load()
    except Exception:
        return None
    if max(im.size) < 600:
        return None
    o = _orientation(path)
    return im.transpose(ORIENT[o]) if o in ORIENT else im


def _rawpy(path):
    import rawpy
    with rawpy.imread(path) as raw:
        rgb = raw.postprocess(half_size=True, use_camera_wb=True, output_bps=8)
    return Image.fromarray(rgb)


def _gpr(path):
    tool = os.environ.get("GPR_TOOLS", "gpr_tools")
    if not shutil.which(tool) and not os.path.exists(tool):
        raise RuntimeError("GoPro gpr_tools not available (set GPR_TOOLS)")
    with tempfile.TemporaryDirectory() as td:
        out = os.path.join(td, "x.dng")
        subprocess.run([tool, "-i", path, "-o", out], check=True, capture_output=True)
        return _rawpy(out)


def load_image(path):
    ext = path.rsplit(".", 1)[-1].lower()
    if ext == "gpr":
        return _gpr(path)
    if ext in RAW_EXT:
        im = _embedded(path)
        return im if im is not None else _rawpy(path)
    im = Image.open(path)
    return ImageOps.exif_transpose(im)


def render(path, outputs):
    """outputs: list of (dest_path, max_edge, quality)."""
    im = load_image(path).convert("RGB")
    for dest, edge, q in outputs:
        c = im.copy()
        c.thumbnail((edge, edge), Image.Resampling.LANCZOS)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        c.save(dest, "JPEG", quality=q, optimize=True, progressive=True)  # no exif/xmp/icc copied
