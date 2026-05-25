from __future__ import annotations

import hashlib
import hmac
import json
from dataclasses import dataclass, asdict
from pathlib import Path


@dataclass(frozen=True)
class FileEntry:
    path: str
    size: int
    sha256: str


def file_digest(path: str | Path) -> str:
    h = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def build_manifest(root: str | Path) -> list[FileEntry]:
    base = Path(root)
    entries: list[FileEntry] = []
    for path in sorted(p for p in base.rglob("*") if p.is_file()):
        rel = path.relative_to(base).as_posix()
        entries.append(FileEntry(rel, path.stat().st_size, file_digest(path)))
    return entries


def manifest_json(root: str | Path) -> str:
    return json.dumps([asdict(item) for item in build_manifest(root)], indent=2)


def share_token(secret: str, relative_path: str, expires_at: int) -> str:
    message = f"{relative_path}:{expires_at}".encode()
    digest = hmac.new(secret.encode(), message, hashlib.sha256).hexdigest()
    return f"{expires_at}:{digest}"


def verify_token(secret: str, relative_path: str, token: str, now: int) -> bool:
    try:
        expires_raw, digest = token.split(":", 1)
        expires_at = int(expires_raw)
    except ValueError:
        return False
    if now > expires_at:
        return False
    expected = share_token(secret, relative_path, expires_at).split(":", 1)[1]
    return hmac.compare_digest(expected, digest)
