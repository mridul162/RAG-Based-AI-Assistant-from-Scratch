from pathlib import Path
import subprocess
import sys


METADATA_DIR = Path(__file__).parent.parent / "metadata_enrichment"


def get_scripts():
    """
    Find all metadata enrichment scripts and sort them.
    """

    return sorted(
        [
            file
            for file in METADATA_DIR.glob("*.py")
            if file.name != "metadata_pipeline.py"
        ]
    )


def run_script(script_path: Path):

    print(f"\n{'=' * 60}")
    print(f"Running: {script_path.name}")
    print(f"{'=' * 60}")

    result = subprocess.run(
        [sys.executable, str(script_path)],
        capture_output=False,
        text=True
    )

    if result.returncode != 0:
        raise RuntimeError(
            f"Pipeline stopped. Failed at {script_path.name}"
        )

    print(f"✓ Completed: {script_path.name}")


def main():

    scripts = get_scripts()

    if not scripts:
        print("No metadata enrichment scripts found.")
        return

    print("\nStarting Metadata Enrichment Pipeline\n")

    for script in scripts:
        run_script(script)

    print("\n🎉 Metadata enrichment pipeline completed successfully.")


if __name__ == "__main__":
    main()