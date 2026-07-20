import hashlib
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "hermes_miner.py"
CANDIDATES = ROOT / "docs" / "mine" / "candidates.md"
DOMAINS = (
    "architecture",
    "fleet",
    "business",
    "skills",
    "integrations",
    "research",
    "references",
    "sessions",
)


def durable_brain_fingerprint() -> str:
    digest = hashlib.sha256()
    paths = [ROOT / "catalog.md"]
    for domain in DOMAINS:
        paths.extend(sorted((ROOT / domain).rglob("*.md")))
    for path in paths:
        digest.update(path.relative_to(ROOT).as_posix().encode("utf-8"))
        digest.update(path.read_bytes())
    return digest.hexdigest()


class HermesMinerCliTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tempdir.cleanup)
        self.hermes_home = Path(self.tempdir.name) / "hermes"
        self.memories = self.hermes_home / "memories"
        self.memories.mkdir(parents=True)
        CANDIDATES.unlink(missing_ok=True)
        self.addCleanup(CANDIDATES.unlink, missing_ok=True)

    def run_miner(self, *args: str) -> subprocess.CompletedProcess[str]:
        return self.run_miner_with_home(self.hermes_home, *args)

    def run_miner_with_home(
        self, hermes_home: Path, *args: str
    ) -> subprocess.CompletedProcess[str]:
        env = os.environ.copy()
        env["HERMES_HOME"] = str(hermes_home)
        return subprocess.run(
            [sys.executable, str(SCRIPT), *args],
            cwd=ROOT,
            env=env,
            text=True,
            capture_output=True,
            check=False,
        )

    def write_memories(self, *blocks: str) -> None:
        (self.memories / "MEMORY.md").write_text(
            "\n\n".join(blocks), encoding="utf-8"
        )

    def test_rejects_a_different_directory_named_memories(self) -> None:
        other = Path(self.tempdir.name) / "untrusted" / "memories"
        other.mkdir(parents=True)
        (other / "MEMORY.md").write_text(
            "This claim must never be read from an untrusted source root.",
            encoding="utf-8",
        )

        result = self.run_miner("--memories", str(other), "--dry-run")

        self.assertEqual(2, result.returncode)
        self.assertIn("configured Hermes memory root", result.stderr)
        self.assertNotIn("This claim must never be read", result.stdout)

    def test_rejects_secrets_and_honors_candidate_cap(self) -> None:
        self.write_memories(
            "The Docker VM is the durable workflow plane for internal automation.",
            "api_key=sk-synthetic-secret-that-must-never-appear",
            "Morning Brief, Lab Pulse, and Super Brain form the daily ops stack.",
            "Tailscale is the approved path for fleet access and maintenance.",
        )

        result = self.run_miner("--dry-run", "--max", "2")

        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn("C-001", result.stdout)
        self.assertIn("C-002", result.stdout)
        self.assertNotIn("C-003", result.stdout)
        self.assertNotIn("synthetic-secret", result.stdout)
        self.assertIn("secret blocks skipped: 1", result.stdout)

    def test_rejects_generic_credentials_and_connection_strings(self) -> None:
        self.write_memories(
            "TOKEN=synthetic-token-value-that-must-not-be-staged",
            "CLIENT_SECRET=synthetic-client-secret-that-must-not-be-staged",
            "postgresql://brain_user:synthetic-password@localhost/brain",
            "The deterministic catalogue remains the durable retrieval index.",
        )

        result = self.run_miner("--dry-run")

        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn("The deterministic catalogue", result.stdout)
        self.assertNotIn("synthetic-token", result.stdout)
        self.assertNotIn("synthetic-client-secret", result.stdout)
        self.assertNotIn("synthetic-password", result.stdout)
        self.assertIn("secret blocks skipped: 3", result.stdout)

    def test_rejects_provider_prefixed_and_json_credentials(self) -> None:
        self.write_memories(
            "OPENAI_API_KEY=synthetic-prefixed-key-that-must-not-be-staged",
            "CUSTOM_PROVIDER_TOKEN=synthetic-prefixed-token-that-must-not-be-staged",
            '\"token\": \"synthetic-json-token-that-must-not-be-staged\"',
            "The deterministic catalogue remains the durable retrieval index.",
        )

        result = self.run_miner("--dry-run")

        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn("The deterministic catalogue", result.stdout)
        self.assertNotIn("synthetic-prefixed", result.stdout)
        self.assertNotIn("synthetic-json-token", result.stdout)
        self.assertIn("secret blocks skipped: 3", result.stdout)

    def test_rejects_modern_provider_token_formats(self) -> None:
        self.write_memories(
            "sk-proj-synthetic_openai_project_token_that_must_not_be_staged",
            "sk-ant-api03-synthetic_anthropic_token_that_must_not_be_staged",
            "xoxb-123456789012-synthetic-slack-token-that-must-not-be-staged",
            "123456789:syntheticTelegramBotTokenThatMustNotBeStaged123",
            "The deterministic catalogue remains the durable retrieval index.",
        )

        result = self.run_miner("--dry-run")

        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn("The deterministic catalogue", result.stdout)
        self.assertNotIn("synthetic_openai", result.stdout)
        self.assertNotIn("synthetic_anthropic", result.stdout)
        self.assertNotIn("synthetic-slack", result.stdout)
        self.assertNotIn("syntheticTelegram", result.stdout)
        self.assertIn("secret blocks skipped: 4", result.stdout)

    def test_does_not_censor_non_secret_persona_words(self) -> None:
        self.write_memories(
            "Hormozi-style offer analysis is part of the current business research workflow.",
            "See sk-customer-support-playbook for ordinary operating guidance.",
            "The sk-long-form-documentation label is not a credential.",
        )

        result = self.run_miner("--dry-run")

        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn("Hormozi-style offer analysis", result.stdout)
        self.assertIn("sk-customer-support-playbook", result.stdout)
        self.assertIn("sk-long-form-documentation", result.stdout)

    def test_excludes_symlinked_markdown_sources(self) -> None:
        target = self.memories / "linked-source.txt"
        target.write_text(
            "This same-directory symlink target must not be mined.", encoding="utf-8"
        )
        link = self.memories / "linked.md"
        try:
            link.symlink_to(target)
        except OSError as exc:
            self.skipTest(f"symlinks unavailable on this system: {exc}")

        result = self.run_miner("--dry-run")

        self.assertEqual(1, result.returncode)
        self.assertNotIn("symlink target", result.stdout)

    def test_rejects_variant_backup_roots(self) -> None:
        backup_home = Path(self.tempdir.name) / "backup-2026" / "hermes"
        backup_memories = backup_home / "memories"
        backup_memories.mkdir(parents=True)
        (backup_memories / "MEMORY.md").write_text(
            "This backup-root claim must not be mined.", encoding="utf-8"
        )

        result = self.run_miner_with_home(backup_home, "--dry-run")

        self.assertEqual(1, result.returncode)
        self.assertNotIn("backup-root claim", result.stdout)

    def test_rejects_a_symlinked_memories_root(self) -> None:
        real_home = Path(self.tempdir.name) / "real-hermes"
        real_memories = real_home / "memories"
        real_memories.mkdir(parents=True)
        (real_memories / "MEMORY.md").write_text(
            "This symlinked-root claim must not be mined.", encoding="utf-8"
        )
        linked_home = Path(self.tempdir.name) / "linked-hermes"
        linked_home.mkdir()
        try:
            (linked_home / "memories").symlink_to(
                real_memories, target_is_directory=True
            )
        except OSError as exc:
            self.skipTest(f"directory symlinks unavailable on this system: {exc}")

        result = self.run_miner_with_home(linked_home, "--dry-run")

        self.assertEqual(1, result.returncode)
        self.assertNotIn("symlinked-root claim", result.stdout)

    def test_refuses_output_outside_the_mine_staging_file(self) -> None:
        self.write_memories(
            "The Docker VM is the durable workflow plane for internal automation."
        )
        outside = Path(self.tempdir.name) / "outside.md"

        result = self.run_miner("--out", str(outside))

        self.assertEqual(2, result.returncode)
        self.assertIn("output must be", result.stderr)
        self.assertFalse(outside.exists())

    def test_default_run_writes_staging_without_mutating_durable_brain(self) -> None:
        self.write_memories(
            "The Docker VM is the durable workflow plane for internal automation."
        )
        before = durable_brain_fingerprint()

        result = self.run_miner()

        self.assertEqual(0, result.returncode, result.stderr)
        self.assertTrue(CANDIDATES.is_file())
        self.assertIn("The Docker VM", CANDIDATES.read_text(encoding="utf-8"))
        self.assertEqual(before, durable_brain_fingerprint())


if __name__ == "__main__":
    unittest.main()
