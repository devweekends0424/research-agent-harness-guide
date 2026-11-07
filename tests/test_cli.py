"""Offline tests; these never contact Google or read credentials."""

import contextlib
import io
import subprocess
import unittest
from unittest.mock import patch

from harness import cli


class HarnessTests(unittest.TestCase):
    @patch("harness.cli.subprocess.run")
    @patch("harness.cli.shutil.which", return_value="/usr/bin/example")
    def test_doctor_offline_does_not_call_provider(self, _which, run):
        with contextlib.redirect_stdout(io.StringIO()):
            code = cli.main(["doctor"])
        self.assertEqual(code, 0)
        run.assert_not_called()

    @patch("harness.cli.subprocess.run")
    @patch("harness.cli.shutil.which", return_value=None)
    def test_missing_cli_fails_offline(self, _which, run):
        with contextlib.redirect_stdout(io.StringIO()):
            code = cli.main(["doctor"])
        self.assertEqual(code, 1)
        run.assert_not_called()

    @patch("harness.cli.subprocess.run")
    @patch("harness.cli.shutil.which", return_value="/bin/example")
    def test_doctor_online_does_not_print_private_output(self, _which, run):
        run.return_value = subprocess.CompletedProcess(
            args=[], returncode=0, stdout="SECRET_NOTEBOOK_TITLE", stderr="token=SECRET"
        )
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            code = cli.main(["doctor", "--online"])
        self.assertEqual(code, 0)
        self.assertNotIn("SECRET_NOTEBOOK_TITLE", output.getvalue())
        self.assertNotIn("token=SECRET", output.getvalue())
        self.assertEqual(run.call_count, 3)
        self.assertTrue(all(call.kwargs.get("shell") is False for call in run.call_args_list))

    @patch("harness.cli.subprocess.run")
    def test_research_dry_run_does_not_call_provider(self, run):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            code = cli.main(
                [
                    "research",
                    "--notebook",
                    "PRIVATE_ID",
                    "--query",
                    "PRIVATE_QUERY",
                    "--mode",
                    "deep",
                ]
            )
        self.assertEqual(code, 0)
        run.assert_not_called()
        self.assertNotIn("PRIVATE_ID", output.getvalue())
        self.assertNotIn("PRIVATE_QUERY", output.getvalue())

    @patch("harness.cli.sys.stdin")
    @patch("harness.cli.subprocess.run")
    def test_research_refuses_unattended_execution(self, run, stdin):
        stdin.isatty.return_value = False
        with contextlib.redirect_stderr(io.StringIO()):
            code = cli.main(
                [
                    "research",
                    "--notebook",
                    "EXAMPLE",
                    "--query",
                    "public topic",
                    "--execute",
                ]
            )
        self.assertEqual(code, 2)
        run.assert_not_called()

    @patch("harness.cli.sys.stdin")
    @patch("builtins.input", return_value="START NOTEBOOKLM RESEARCH")
    @patch("harness.cli.subprocess.run")
    def test_research_with_approval_never_auto_imports(self, run, _input, stdin):
        stdin.isatty.return_value = True
        run.return_value = subprocess.CompletedProcess(
            args=[], returncode=0, stdout='{"status":"started"}', stderr=""
        )
        with contextlib.redirect_stdout(io.StringIO()):
            code = cli.main(
                [
                    "research",
                    "--notebook",
                    "EXAMPLE",
                    "--query",
                    "public topic",
                    "--mode",
                    "fast",
                    "--execute",
                ]
            )
        self.assertEqual(code, 0)
        command = run.call_args.args[0]
        self.assertEqual(command[:3], ["notebooklm", "source", "add-research"])
        self.assertNotIn("--import-all", command)
        self.assertIn("--no-wait", command)
        self.assertIs(run.call_args.kwargs.get("shell"), False)

    @patch("harness.cli.subprocess.run")
    def test_structured_provider_error_is_failure(self, run):
        run.return_value = subprocess.CompletedProcess(
            args=[], returncode=0, stdout='{"error":true,"code":"AUTH_REQUIRED"}', stderr=""
        )
        self.assertFalse(cli._invoke(["notebooklm", "list", "--json"]))

    @patch("harness.cli.subprocess.run")
    def test_nonzero_exit_is_failure(self, run):
        run.return_value = subprocess.CompletedProcess(
            args=[], returncode=1, stdout="private data", stderr="secret"
        )
        self.assertFalse(cli._invoke(["notebooklm", "list", "--json"]))


if __name__ == "__main__":
    unittest.main()
