
#--------------------------------

# Imports
import json
import subprocess
from pathlib import Path
#--------------------------------

NEWS_FLASH_DIR = Path(__file__).resolve().parent.parent.parent / "news_flash"
print(NEWS_FLASH_DIR)

# Something about science
def gather_papers(topic: str = "particle physics", days: int = 90, limit: int = 20):
    """Run the Node news pipeline and return the result as a Python list of dicts."""
    result = subprocess.run(
        [
            "node",
            "src/example.js",
            "--json",
        ],
        cwd=NEWS_FLASH_DIR,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )

    papers = json.loads(result.stdout.strip())
    return papers
#--------------------------------


# Main
if __name__ == "__main__":
    paper_list = gather_papers()
    print(json.dumps(paper_list, indent=2))
#--------------------------------

