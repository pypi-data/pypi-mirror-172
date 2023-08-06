[![license](https://img.shields.io/badge/license-MIT-brightgreen)](https://spdx.org/licenses/MIT.html)
[![pipelines](https://gitlab.com/jlecomte/projects/python/pycov-convert-relative-filenames/badges/master/pipeline.svg)](https://gitlab.com/jlecomte/projects/python/pycov-convert-relative-filenames/pipelines)
[![coverage](https://gitlab.com/jlecomte/projects/python/pycov-convert-relative-filenames/badges/master/coverage.svg)](https://jlecomte.gitlab.io/projects/python/pycov-convert-relative-filenames/coverage/index.html)

# pycov-convert-relative-filenames

A quick and dirty helper script to convert a xml coverage report into a valid cobertura file that will be accepted by GitLab CI.

This enables the merge request pages to have coverage shown on the code review tab.

## Installation from PyPI

You can install the latest version from PyPI package repository.

~~~bash
python3 -mpip install -U pycov-convert-relative-filenames
~~~

## GitLab CI Usage

Sample gitlab-ci.yml snippet for coverage:

~~~yaml
coverage:
  script:
    - python3 -m pytest --cov-report=xml:coverage.tmp.xml -- tests
    - pycov-convert-relative-filenames < coverage.tmp.xml > coverage.xml
  artifacts:
    when: always
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage.xml
~~~

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Locations

  * GitLab: [https://gitlab.com/jlecomte/projects/python/pycov-convert-relative-filenames](https://gitlab.com/jlecomte/projects/python/pycov-convert-relative-filenames)
  * PyPi: [https://pypi.org/project/pycov-convert-relative-filenames](https://pypi.org/project/pycov-convert-relative-filenames)

