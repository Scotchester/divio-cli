import pytest
from click.testing import CliRunner

from divio_cli import cli


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
    ["services", "list"],
]


@pytest.mark.integration
@pytest.mark.parametrize("command", TEST_COMMANDS_CLICK)
def test_call_click_commands(divio_project, command):
    runner = CliRunner()
    result = runner.invoke(cli.cli, command)
    assert result.exit_code == 0
