# Document Generation for Microservices

Generates documentation by pulling latest README.md files and aggregating all endpoint information into a single file.
This file is then used by [Slate](https://github.com/slatedocs/slate) to build a Docker image and deployed as per the [CircleCI config](.circleci/config.yml).

## Usage

* Create/update a repo which includes a file specifying endpoint usage:
    * Format endpoints section according to [Slate docs](...).
        TODO
    * Example:
        TODO local?
* Add repo and file details to `repos` array in [generation config file](generate/config.toml).
    * NOTE: url and path must point to raw file.
    * e.g.
    ``` toml
        [[repos]]
        url = "https://raw.githubusercontent.com/{{user}}/{{repo}}/{{branch}}/"
        path = "README.md"
        section_separator = '\n## '         # optional        
        endpoints_identifier = 'Endpoints'  # optional
    ```
* Add Github action to trigger Docker image rebuild on push to repo
        TODO local example?
