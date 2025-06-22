"""
LivePush Protocol

- Custom protocol for resumable, chunked, encrypted transfer
- Diff/patch algorithm implementation
- Signing and verification
"""

import hashlib
import hmac
from typing import Optional, Iterable

def compute_patch(old: bytes, new: bytes) -> bytes:
    """
    Computes a binary diff between old and new.
    Production deployment must use a robust algorithm (e.g., bsdiff, xdelta).
    """
    raise NotImplementedError("Implement compute_patch using a binary diff algorithm for production.")

def apply_patch(old_path: str, patch: bytes, out_path: str):
    """
    Applies a binary patch to old_path, writes to out_path.
    Real implementation must support robust patching (e.g., using bsdiff/xdelta).
    """
    raise NotImplementedError("Implement apply_patch using a binary patch algorithm for production.")

def sign_data(data: bytes, secret_key: bytes) -> bytes:
    return hmac.new(secret_key, data, hashlib.sha256).digest()

def verify_signature(data: bytes, sig: bytes, pubkey: bytes) -> bool:
    expected = hmac.new(pubkey, data, hashlib.sha256).digest()
    return hmac.compare_digest(sig, expected)

class ChunkedTransfer:
    def __init__(self, chunk_size: int = 1024*1024):
        self.chunk_size = chunk_size

    def split(self, data: bytes) -> Iterable[bytes]:
        for i in range(0, len(data), self.chunk_size):
            yield data[i:i+self.chunk_size]

    def join(self, chunks: Iterable[bytes]) -> bytes:
        return b"".join(chunks)

    # For production: add encryption, resume, and integrity checks.