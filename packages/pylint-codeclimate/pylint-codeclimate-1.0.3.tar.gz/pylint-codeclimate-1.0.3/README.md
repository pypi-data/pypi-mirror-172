[![license](https://img.shields.io/badge/license-MIT-brightgreen)](https://spdx.org/licenses/MIT.html)
[![pipelines](https://gitlab.com/jlecomte/projects/python/pylint-codeclimate/badges/master/pipeline.svg)](https://gitlab.com/jlecomte/projects/python/pylint-codeclimate/pipelines)
[![coverage](https://gitlab.com/jlecomte/projects/python/pylint-codeclimate/badges/master/coverage.svg)](https://jlecomte.gitlab.io/projects/python/pylint-codeclimate/coverage/index.html)

# pylint code climate

A quick and dirty helper script to report pylint results in a json file that will be accepted by GitLab CI.

## Installation from PyPI

You can install the latest version from PyPI package repository.

~~~bash
python3 -mpip install -U pylint-codeclimate
~~~

## GitLab CI Usage

Sample gitlab-ci.yml snippet for coverage:

~~~yaml
coverage:
  script:
    - python3 -m pylint  --recursive y --output-format=codeclimate:pylint.json myproject
  artifacts:
    when: always
    reports:
      codequality: pylint.json
~~~

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Locations

  * GitLab: [https://gitlab.com/jlecomte/projects/python/pylint-codeclimate](https://gitlab.com/jlecomte/projects/python/pylint-codeclimate)
  * PyPi: [https://pypi.org/project/pylint-codeclimate](https://pypi.org/project/pylint-codeclimate)

