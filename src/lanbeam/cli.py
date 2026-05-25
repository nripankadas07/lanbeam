from __future__ import annotations

import argparse
import time
from .core import manifest_json, share_token


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Local network file drop helpers.")
    sub = parser.add_subparsers(dest="cmd", required=True)
    manifest = sub.add_parser("manifest")
    manifest.add_argument("directory")
    token = sub.add_parser("token")
    token.add_argument("secret")
    token.add_argument("path")
    token.add_argument("--ttl", type=int, default=900)
    args = parser.parse_args(argv)
    if args.cmd == "manifest":
        print(manifest_json(args.directory))
    else:
        print(share_token(args.secret, args.path, int(time.time()) + args.ttl))
    return 0
