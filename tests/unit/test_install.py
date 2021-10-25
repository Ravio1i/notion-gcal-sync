import pytest
from notion_gcal_sync import install


@pytest.mark.parametrize(
    "test_answer, expected",
    [(True, True), (None, False), (False, False)],
)
def test_confirm_path(mocker, test_answer, expected):
    mocker.patch("click.confirm", return_value=test_answer)
    assert install.confirm_create_path("/tmp/some/path") == expected


@pytest.mark.parametrize(
    "path_exists, create_config_path, expected",
    [(True, True, True), (True, False, True), (False, False, False), (False, True, True)],
)
def test_config_path_created(mocker, path_exists, create_config_path, expected):
    mocker.patch("notion_gcal_sync.install.confirm_create_path", return_value=create_config_path)
    mocker.patch("os.path.exists", return_value=path_exists)
    mocker.patch("os.mkdir")
    assert install.config_path_created() == expected


@pytest.mark.parametrize(
    "path_exists, create_config_path, expected",
    [(True, True, True), (True, False, True), (False, False, False), (False, True, True)],
)
def test_config_file_created(mocker, path_exists, create_config_path, expected):
    def prompt(text, default):
        if default:
            return default
        if text == "google_mail (e.g name@gmail.com)":
            return "test@gmail.com"
        return None

    assert prompt("", "default") == "default"
    assert prompt("google_mail (e.g name@gmail.com)", "") == "test@gmail.com"
    assert prompt("text", "") is None

    mocker.patch("os.path.exists", return_value=path_exists)
    mocker.patch("notion_gcal_sync.install.confirm_create_path", return_value=create_config_path)
    mocker.patch("notion_gcal_sync.config.Config.to_yaml")
    mocker.patch("click.prompt", side_effect=prompt)
    assert install.config_file_created() is expected


@pytest.mark.parametrize(
    "credentials_path_exists, token_path_exists, expected",
    [(False, False, False), (False, True, True), (True, False, False), (True, True, True)],
)
def test_credentials_created(mocker, credentials_path_exists, token_path_exists, expected):
    def path_exists(path):
        if path == install.TOKEN_FILE:
            return token_path_exists
        if path == install.CREDENTIALS_FILE:
            return credentials_path_exists

    mocker.patch("os.path.exists", side_effect=path_exists)
    mocker.patch("notion_gcal_sync.clients.GCalClient.GCalClient.get_credentials")
    assert install.credentials_created() is expected


def test_configure(mocker, config_dict_fixture):
    mocker.patch("notion_gcal_sync.install.config_path_created", return_value=True)
    mocker.patch("notion_gcal_sync.install.config_file_created", return_value=True)
    mocker.patch("notion_gcal_sync.install.credentials_created", return_value=True)
    mocker.patch("builtins.open", mocker.mock_open(read_data=str(config_dict_fixture)))
    assert install.configure().to_dict() == config_dict_fixture


@pytest.mark.parametrize(
    "config_path_created, config_file_created, credentials_created",
    [
        (False, False, False),
        (False, False, True),
        (False, True, False),
        (True, False, False),
        (False, True, True),
        (True, True, False),
    ],
)
def test_configure_not_confirmed(mocker, config_path_created, config_file_created, credentials_created):
    mocker.patch("notion_gcal_sync.install.config_path_created", return_value=config_path_created)
    mocker.patch("notion_gcal_sync.install.config_file_created", return_value=config_file_created)
    mocker.patch("notion_gcal_sync.install.credentials_created", return_value=credentials_created)
    with pytest.raises(SystemExit):
        install.configure()
