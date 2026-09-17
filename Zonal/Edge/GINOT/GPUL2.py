import sys
import time
import argparse
import torch
from pathlib import Path

this_dir = Path(__file__).parent.resolve()
if str(this_dir) not in sys.path:
    sys.path.insert(0, str(this_dir))

from Training_script import main as train_main  # noqa: E402
from model_presets import list_presets  # noqa: E402

PRESETS_GPU0 = ["M"]


def run_with_fallback(preset: str, initial_batch: int, dry_run: bool = False) -> bool:
    if dry_run:
        print(f"\n[GPU0] Preset={preset} | dry-run")
        train_main(preset, initial_batch, dry_run=True)
        return True

    iterative = max(1, int(initial_batch * 0.1))
    batch_plan = list(range(initial_batch, 0, -iterative))
    if 1 not in batch_plan:
        batch_plan.append(1)

    for b in batch_plan:
        try:
            print(f"\n[GPU0] Preset={preset} | Trying batch={b}")
            train_main(preset, b, dry_run=False)
            print(f"[GPU0] Preset={preset} | Completed with batch={b}")
            return True
        except RuntimeError as e:
            low = str(e).lower()
            if ("out of memory" in low or "cuda" in low) and b != 1:
                print(f"[GPU0] OOM/CUDA at batch {b}; reducing and retrying...")
                try:
                    torch.cuda.empty_cache()
                except Exception:
                    pass
                time.sleep(2)
                continue
            print(f"[GPU0] Non-recoverable RuntimeError for preset {preset}: {e}")
            return False
        except Exception as e:
            print(f"[GPU0] Unexpected error for preset {preset}: {e}")
            return False
    return False


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run one or more GINOT-A presets with optional dry-run."
    )
    parser.add_argument(
        "--preset",
        nargs="+",
        default=None,
        help=(
            "Preset name(s) to run. Use one or many values, or comma-separated values. "
            "Use 'all' to run all presets."
        ),
    )
    parser.add_argument(
        "--initial-batch",
        type=int,
        default=40,
        help="Initial batch size to try before fallback reductions.",
    )
    parser.add_argument("--dry-run", action="store_true", help="Instantiate model and print config only")
    parser.add_argument(
        "--list-presets",
        action="store_true",
        help="Print available presets and exit.",
    )
    return parser.parse_args()


def resolve_requested_presets(raw_presets, available_presets: list[str]) -> list[str]:
    if not raw_presets:
        return PRESETS_GPU0

    parsed = []
    for token in raw_presets:
        for item in token.split(","):
            name = item.strip()
            if name:
                parsed.append(name)

    if len(parsed) == 1 and parsed[0].lower() == "all":
        return available_presets

    allowed = set(available_presets)
    unknown = [p for p in parsed if p not in allowed]
    if unknown:
        raise ValueError(
            "Unknown preset(s): "
            + ", ".join(unknown)
            + "\nAvailable presets: "
            + ", ".join(available_presets)
        )
    return parsed


def main() -> None:
    args = parse_args()
    available_presets = list_presets()

    if args.list_presets:
        print("Available presets:")
        for preset in available_presets:
            print(f"- {preset}")
        return

    if args.initial_batch < 1:
        raise ValueError("--initial-batch must be >= 1")

    selected_presets = resolve_requested_presets(args.preset, available_presets)

    print("Starting GPU0 preset run set...")
    for preset in selected_presets:
        run_with_fallback(preset, initial_batch=args.initial_batch, dry_run=args.dry_run)
    print("GPU0 run set finished.")


if __name__ == "__main__":
    main()
