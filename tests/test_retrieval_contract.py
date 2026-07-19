import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BRAIN = ROOT / "scripts" / "brain.py"
QUESTIONS = ROOT / "scripts" / "bench-questions.json"


class DeterministicRetrievalContractTests(unittest.TestCase):
    def test_all_benchmark_questions_still_return_expected_evidence(self) -> None:
        questions = json.loads(QUESTIONS.read_text(encoding="utf-8"))

        for item in questions:
            with self.subTest(question=item["question"]):
                result = subprocess.run(
                    [
                        sys.executable,
                        str(BRAIN),
                        "ask",
                        item["question"],
                        "--json",
                    ],
                    cwd=ROOT,
                    text=True,
                    capture_output=True,
                    check=False,
                )

                self.assertEqual(0, result.returncode, result.stderr)
                answer = json.loads(result.stdout)
                self.assertTrue(answer["matched"])
                self.assertIn(item["expect"].casefold(), answer["evidence"].casefold())


if __name__ == "__main__":
    unittest.main()
