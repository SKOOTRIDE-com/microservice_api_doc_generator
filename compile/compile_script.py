import requests
import toml
from pathlib import Path


GITHUB_PERSONAL_ACCESS_TOKEN = None  # TODO env variable
DEFAULT_SEPARATOR = '\n## '
DEFAULT_IDENTIFIER = 'Endpoints'


def generate_slate_readme(relative_config_path):
    config_path = Path.cwd() / relative_config_path
    config = toml.load(config_path)

    output_file_path = Path.cwd() / config['output_file_path']

    write_to_file(
        output_file_path,
        config['base_file_path'],
        config['readmes']
    )


def write_to_file(output_path, base_path, repos):
    base_template = open(base_path, 'r')

    with open(output_path, 'w') as f:
        f.write(base_template.read())

        for repo in repos:
            content = get_repo_contents(**repo)

            # TODO error handling and format func

            separator = repo.get('section_separator', DEFAULT_SEPARATOR)
            sections = [sect.strip() for sect in content.split(separator)]

            identifier = repo.get('endpoints_identifier', DEFAULT_IDENTIFIER)
            endpoints = list(filter(lambda x: x.startswith(identifier), sections))

            assert len(endpoints) == 1

            # Remove header and whitespace
            endpoints = endpoints[0]
            first_line_index = endpoints.index('\n')
            endpoints = endpoints[first_line_index:].strip()

            f.write(endpoints)
            f.write('\n')


def get_repo_contents(url, path):
    headers = {'Authorization': f'token {GITHUB_PERSONAL_ACCESS_TOKEN}'}
    resp = requests.get(f'{url}{path}', headers=headers)

    resp.raise_for_status()

    return resp.text


if __name__ == '__main__':
    generate_slate_readme('config.toml')
