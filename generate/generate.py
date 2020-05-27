from os import environ
from pathlib import Path

import requests
import toml


GITHUB_PERSONAL_ACCESS_TOKEN = environ['GITHUB_PERSONAL_ACCESS_TOKEN']
DEFAULT_SEPARATOR = '\n# '
DEFAULT_IDENTIFIER = 'Endpoints'


def generate_slate_readme(config_path: str) -> None:
    """Generate single text file from given configs

    Arguments:
        config_path {str} -- relative path
    """
    config_path = Path.cwd() / config_path
    config = toml.load(config_path)

    output_file_path = Path.cwd() / config['output_file_path']

    write_to_file(
        output_file_path,
        config['base_file_path'],
        config['repos']
    )


def write_to_file(output_path: str, base_path: str, repos: dict) -> None:
    base_template = open(base_path, 'r')

    with open(output_path, 'w') as f:
        f.write(base_template.read())

        for repo in repos:
            # Currently not catching possible errors here so that
            # running job (on CircleCI, for example) will fail.
            # Triggerer should be notified
            content = get_repo_contents(**repo)
            endpoints = format_repo_contents(content, repo)

            f.write(endpoints)
            f.write('\n')


def get_repo_contents(url: str, path: str) -> str:
    headers = {'Authorization': f'token {GITHUB_PERSONAL_ACCESS_TOKEN}'}
    resp = requests.get(f'{url}{path}', headers=headers)

    resp.raise_for_status()

    return resp.text


def format_repo_contents(content: str, repo: dict) -> str:
    separator = repo.get('section_separator', DEFAULT_SEPARATOR)
    sects = [sect.strip() for sect in content.split(separator)]

    identifier = repo.get('endpoints_identifier', DEFAULT_IDENTIFIER)
    endpoints = list(filter(lambda x: x.startswith(identifier), sects))

    assert len(endpoints) == 1

    # Remove header and whitespace
    endpoints = endpoints[0]
    first_line_index = endpoints.index('\n')
    return endpoints[first_line_index:].strip()


if __name__ == '__main__':
    generate_slate_readme('config.toml')
