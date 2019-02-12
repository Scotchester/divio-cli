import pytest

import click

from divio_cli.localdev import utils


def test_get_project_home(tmp_path):

    # Loud fail to get the aldryn file
    with pytest.raises(click.exceptions.ClickException):
        home = utils.get_project_home(str(tmp_path))

    # Silent fail to find the aldryn file
    home = utils.get_project_home(str(tmp_path), silent=True)
    assert not home

    p = tmp_path / ".aldryn"
    p.write_text(u"#Examplecontent")
    home = utils.get_project_home(str(tmp_path))
    assert home
