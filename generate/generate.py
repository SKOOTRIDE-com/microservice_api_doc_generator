from pathlib import Path
import subprocess

import toml


DEFAULT_SEPARATOR = '\n# '
DEFAULT_IDENTIFIER = 'Endpoints'
REPO_DIR = 'repos'


def generate_slate_readme(config_path: str) -> None:
    """Generate single text file from given configs

    Arguments:
        config_path {str} -- relative path
    """
    config_path = Path.cwd() / config_path
    config = toml.load(config_path)

    output_file_path = Path.cwd() / config['output_file_path']

    with open(output_file_path, 'w') as f:
        # Add base
        base_template = open(config['base_file_path'], 'r')
        f.write(base_template.read())

        # Add repos
        for repo in config['repos']:
            write_to_file(f, config[repo], format_whole_readme)

        # Add endpoints base
        endpoints_template = open(config['endpoints_base_file_path'], 'r')
        f.write(endpoints_template.read())

        # Add endpoints
        write_to_file(f, config['endpoint_repos'], format_endpoint_repo_contents)


def write_to_file(f, repos: list, formatter) -> None:
    repos.sort(key=lambda repo: repo['url'])

    for repo in repos:
        # Currently not catching possible errors here so that
        # running job (on CircleCI, for example) will fail.
        # Triggerer should be notified
        content = get_repo_contents(**repo)
        print(content)
        endpoints = formatter(content, repo)

        f.write(endpoints)
        f.write('\n')


def get_repo_contents(url, branch, path):
    repo_name = url.split('/')[-1][:-4]
    repo_path = Path.cwd() / REPO_DIR / repo_name

    if not repo_path.exists():
        subprocess.run(
            f'git clone {url} {str(repo_path)}',
            shell=True
        )

    branch_exists_locally = subprocess.run(
        f'cd {str(repo_path)} && git show-ref refs/heads/{branch}',
        shell=True
    )
    if branch_exists_locally:
        subprocess.run(
            f'cd {str(repo_path)} && git checkout {branch} && git pull',
            shell=True
        )
    else:
        subprocess.run(
            f'cd {str(repo_path)} && git checkout --track origin/{branch}',
            shell=True
        )

    file_path = repo_path / path
    return open(file_path, 'r').read()


def format_endpoint_repo_contents(content: str, repo: dict) -> str:
    separator = repo.get('section_separator', DEFAULT_SEPARATOR)
    sects = [sect.strip() for sect in content.split(separator)]

    identifier = repo.get('endpoints_identifier', DEFAULT_IDENTIFIER)
    endpoints = list(filter(lambda x: x.startswith(identifier), sects))

    assert len(endpoints) == 1

    # Remove header and whitespace
    endpoints = endpoints[0]
    first_line_index = endpoints.index('\n')
    return endpoints[first_line_index:].strip()


def format_whole_readme(content: str, _repo) -> str:
    return content.strip() + '\n\n'


if __name__ == '__main__':
    generate_slate_readme('config.toml')
