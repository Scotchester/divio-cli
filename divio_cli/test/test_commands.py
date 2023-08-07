import os
import shutil
from tempfile import TemporaryDirectory

import pytest
from click.testing import CliRunner

from divio_cli import cli
from divio_cli.cloud import WritableNetRC


TEST_COMMANDS_CLICK = [
    ["doctor"],
    ["doctor", "-m"],
    ["doctor", "-c", "login"],
    ["login", "--check"],
    ["app"],
    ["app", "dashboard"],
    ["app", "deploy", "test"],
    ["app", "deploy-log"],
    ["app", "list"],
    ["app", "pull", "db"],
    ["app", "push", "db", "--noinput"],
    ["app", "export", "db"],
    ["app", "push", "db", "--noinput", "--dumpfile", "local_db.sql"],
    ["app", "pull", "media"],
    ["app", "push", "media", "--noinput"],
    ["app", "logs", "test"],
    ["app", "status"],
    ["app", "update"],
    ["app", "service-instances", "list"],
    ["version"],
    ["version", "-s"],
    ["version", "-m"],
    ["regions", "list"],
    ["organisations", "list"],
]


@pytest.mark.integration()
@pytest.mark.parametrize("command", TEST_COMMANDS_CLICK)
def test_call_click_commands(divio_project, command):
    runner = CliRunner()
    result = runner.invoke(cli.cli, command)
    assert result.exit_code == 0


@pytest.mark.integration()
def test_logout_command(divio_project):
    """
    The logout command has to be tested separately, and using a temporary
    netrc, because the following tests require the cli to be logged in.

    This test copies the global netrc into a temporary directory, sets the
    temporary netrc globally, and then checks if the "logout" command causes
    the "login --check" command to return an exit code of 1.
    """

    temporary_directory = TemporaryDirectory()
    original_netrc_path = WritableNetRC.get_netrc_path()

    temporary_netrc_path = os.path.join(
        temporary_directory.name,
        os.path.basename(original_netrc_path),
    )

    shutil.copy(original_netrc_path, temporary_netrc_path)

    try:
        os.environ["NETRC_PATH"] = temporary_netrc_path

        runner = CliRunner()

        result = runner.invoke(cli.cli, ["login", "--check"])
        assert result.exit_code == 0, result.stdout

        result = runner.invoke(cli.cli, ["logout", "--non-interactive"])
        assert result.exit_code == 0, result.stdout

        result = runner.invoke(cli.cli, ["login", "--check"])
        assert result.exit_code == 1, result.stdout

    finally:
        os.environ.pop("NETRC_PATH")
