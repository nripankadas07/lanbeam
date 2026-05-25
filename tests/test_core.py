import time
from lanbeam.core import build_manifest, share_token, verify_token


def test_manifest_and_token(tmp_path):
    (tmp_path / "hello.txt").write_text("hello", encoding="utf-8")
    entries = build_manifest(tmp_path)
    assert entries[0].path == "hello.txt"
    assert entries[0].size == 5
    token = share_token("secret", "hello.txt", int(time.time()) + 60)
    assert verify_token("secret", "hello.txt", token, int(time.time()))
    assert not verify_token("secret", "other.txt", token, int(time.time()))
