"""Integration test: compile the C++ engine and play one exchange."""
import shutil

import pytest

from loa.ai_client import AIClient, AIError

pytestmark = pytest.mark.skipif(
    not (shutil.which("g++") or shutil.which("clang++") or shutil.which("c++")),
    reason="no C++ compiler available",
)


def test_engine_replies_with_legal_looking_move():
    ai = AIClient(6, 6)
    try:
        # Human (black) plays (0,1) -> (2,1): a legal opening move.
        move = ai.get_move(0, 1, 2, 1)
    finally:
        ai.close()
    assert move is not None
    sx, sy, tx, ty = move
    assert all(0 <= v < 6 for v in move)
    assert (sx, sy) != (tx, ty)
    # White pieces start on columns 0 and 5, rows 1..4.
    assert sy in (0, 5) and 1 <= sx <= 4


def test_engine_rejects_bad_header():
    import subprocess
    from loa.ai_client import ensure_binary

    binary = ensure_binary()
    proc = subprocess.run([str(binary)], input="x\n", capture_output=True, text=True)
    assert proc.returncode == 1
