import json
from pathlib import Path

_dir = Path(__file__).resolve().parent
SEGMENTS = {}
for _f in sorted(_dir.glob("narr_vi_*.json")):
    SEGMENTS.update(json.loads(_f.read_text(encoding="utf-8")))
# keep deterministic order by id
SEGMENTS = dict(sorted(SEGMENTS.items()))

try:
    from drill_data import drill_segments
    SEGMENTS.update(drill_segments())
except ImportError:
    pass
