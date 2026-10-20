"""Talks to the C++ minimax engine (ai/ai.cpp) over stdin/stdout.

Protocol (one integer per whitespace-separated token):
  -> "<rows> <cols>"              once, after start
  -> "<sx> <sy> <tx> <ty>"        the human's move
  <- "<sx> <sy> <tx> <ty>"        the engine's reply ("-1 -1 -1 -1" = no move)
"""
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
AI_SRC = ROOT / "ai" / "ai.cpp"
AI_BIN = ROOT / "ai" / ("loa_ai.exe" if os.name == "nt" else "loa_ai")

NO_MOVE = (-1, -1, -1, -1)


class AIError(RuntimeError):
    pass


def ensure_binary():
    """Return the path to the compiled engine, compiling it if necessary."""
    if AI_BIN.exists() and AI_BIN.stat().st_mtime >= AI_SRC.stat().st_mtime:
        return AI_BIN

    cxx = os.environ.get("CXX") or shutil.which("g++") or shutil.which("clang++") or shutil.which("c++")
    if cxx is None:
        raise AIError(
            "No C++ compiler found. Install one (Xcode CLT / build-essential / MinGW) "
            "or run `make ai` on a machine that has one."
        )
    cmd = [cxx, "-O2", "-std=c++17", str(AI_SRC), "-o", str(AI_BIN)]
    print("Compiling AI engine:", " ".join(cmd), file=sys.stderr, flush=True)
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise AIError(f"Failed to compile AI engine:\n{result.stderr}")
    return AI_BIN


class AIClient:
    def __init__(self, rows, cols):
        binary = ensure_binary()
        self.proc = subprocess.Popen(
            [str(binary)],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=sys.stderr,
            text=True,
            bufsize=1,
        )
        self._send(f"{rows} {cols}")

    def _send(self, line):
        if self.proc.poll() is not None:
            raise AIError("AI engine exited unexpectedly")
        self.proc.stdin.write(line + "\n")
        self.proc.stdin.flush()

    def _read_int(self):
        line = self.proc.stdout.readline()
        if not line:
            raise AIError("AI engine closed its output")
        return int(line.strip())

    def get_move(self, sx, sy, tx, ty):
        """Report the human's move, return the AI's (sx, sy, tx, ty) or None."""
        self._send(f"{sx} {sy} {tx} {ty}")
        move = tuple(self._read_int() for _ in range(4))
        return None if move == NO_MOVE else move

    def close(self):
        if self.proc.poll() is None:
            try:
                self.proc.stdin.close()
            except OSError:
                pass
            try:
                self.proc.wait(timeout=1)
            except subprocess.TimeoutExpired:
                self.proc.kill()

    def __del__(self):
        try:
            self.close()
        except Exception:
            pass
