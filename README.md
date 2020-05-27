# Document Generation for Microservices

Generates documentation by pulling latest README.md files and aggregating all endpoint information into a single file.
This file is then used by [Slate](https://github.com/slatedocs/slate) to build a Docker image and deployed as per the [CircleCI config](.circleci/config.yml).

## Usage

* Create/update a repo which includes a file specifying endpoint usage:
    * Format endpoints section similarly to the [Slate docs example](https://github.com/slatedocs/slate/blob/master/source/index.html.md) which generates https://slatedocs.github.io/slate.
    * Ensure that the *Endpoints* section is clearly identified, either with the default identifier and section separator or a custom choice (see below). 

* Add repo and file details to `repos` array in [generation config file](generate/config.toml).
    * NOTE: url and path must point to raw file.
    * e.g.
    ``` toml
        [[repos]]
        url = "https://raw.githubusercontent.com/<org>/<repo>/<branch>/"
        path = "README.md"
        section_separator = '\n## '         # optional        
        endpoints_identifier = 'Endpoints'  # optional
    ```

* Add Github action to trigger Docker image rebuild on push to repo, eg. `.github/workflows/circleci-doc-gen-workflow.yml`

    ```yml 
    name: Trigger Doc Generation CircleCi job

    on:
    push:
        branches:
            - master

    jobs:
    build:
        runs-on: ubuntu-latest

        steps:
        - uses: actions/checkout@master

        - name: Trigger doc generation CircleCI job
            uses: zivkaziv/circleci-trigger-github-action@V1.0
            with:
            token: ${{ secrets.CIRCLE_CI_TOKEN }}
            org: SKOOTUK
            repo: microservice_api_doc_generator
            branch: master
    ```
