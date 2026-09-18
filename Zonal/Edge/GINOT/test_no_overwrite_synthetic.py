from __future__ import annotations

import importlib.util
import tempfile
from pathlib import Path


def _load_module(module_path: Path):
    spec = importlib.util.spec_from_file_location(module_path.stem, module_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def run_no_overwrite_smoke_test() -> None:
    repo_root = Path(__file__).resolve().parents[3]
    training_scripts = [
        repo_root / "Zonal/Edge/GINOT/Training_script.py",
        repo_root / "Uniform/Edge/GINOT/Training_script.py",
        repo_root / "Zonal/Edge_no_stress/GINOT/Training_script.py",
        repo_root / "Zonal/Edge_arc_feat/GINOT/Training_script.py",
    ]

    for script_path in training_scripts:
        module = _load_module(script_path)
        guard = getattr(module, "_prohibit_resume_or_overwrite")

        with tempfile.TemporaryDirectory() as td:
            ckpt_path = Path(td) / "dummy.pt"
            ckpt_path.touch()

            try:
                guard("MATCH_250K", ckpt_path)
                raise AssertionError(f"Expected RuntimeError for existing checkpoint in {script_path}")
            except RuntimeError as exc:
                msg = str(exc)
                assert "GINOT-A" in msg
                assert "MATCH_250K" in msg
                assert str(ckpt_path) in msg
                assert "overwrite and resume are prohibited" in msg

        try:
            guard("MATCH_250K", Path("/tmp/nonexistent.pt"), resume_request="--resume")
            raise AssertionError(f"Expected RuntimeError for resume request in {script_path}")
        except RuntimeError as exc:
            msg = str(exc)
            assert "GINOT-A" in msg
            assert "MATCH_250K" in msg
            assert "overwrite and resume are prohibited" in msg


if __name__ == "__main__":
    run_no_overwrite_smoke_test()
    print("No-overwrite synthetic checks passed for all GINOT training scripts.")
