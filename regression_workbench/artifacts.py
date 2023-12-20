"""Fetch explicitly pinned public model files without trusting cache contents."""
import hashlib
from pathlib import Path
from urllib.request import urlopen


def download(manifest, destination, fetch=urlopen):
    destination = Path(destination)
    destination.mkdir(parents=True, exist_ok=True)
    downloaded = []
    for row in manifest:
        name = row["file"]
        if Path(name).name != name or name in {".", ".."}:
            raise ValueError("artifact filename must be local")
        target = destination / name
        if (
            target.exists()
            and hashlib.sha256(target.read_bytes()).hexdigest() == row["sha256"]
        ):
            downloaded.append(str(target))
            continue
        temporary = target.with_suffix(target.suffix + ".partial")
        digest = hashlib.sha256()
        size = 0
        try:
            with fetch(row["url"], timeout=60) as response, temporary.open(
                "wb"
            ) as output:
                while True:
                    chunk = response.read(1024 * 1024)
                    if not chunk:
                        break
                    digest.update(chunk)
                    size += len(chunk)
                    output.write(chunk)
                    if size > row["bytes"]:
                        raise ValueError("artifact exceeds declared size")
            if digest.hexdigest() != row["sha256"] or size != row["bytes"]:
                raise ValueError("artifact hash or size mismatch")
            temporary.replace(target)
            downloaded.append(str(target))
        finally:
            if temporary.exists():
                temporary.unlink()
    return downloaded
