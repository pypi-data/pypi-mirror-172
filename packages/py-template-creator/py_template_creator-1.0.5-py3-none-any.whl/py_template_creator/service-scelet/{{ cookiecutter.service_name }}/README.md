# {{ cookiecutter.service_name }} service

## Setup service

- create virtualenv with virtualenv wrapper
```
cd {{ cookiecutter.service_name }}
mkvirtualenv <env name> --python=/path/to/python/executable/python3.10.*
```

- install packages needed for the project
```
make env
```


## Start service

- stop docker container for this service
```
cd <project root>
docker-compose stop {{ cookiecutter.service_name }}
```

- start service from virtual environment
```
cd {{ cookiecutter.service_name }}
workon <env name>
make run
```


## Run tests

- tests are run on virtual environment
```
cd {{ cookiecutter.service_name }}
workon <env name>
```

- run all tests
```
make test
```

- run all tests in single file
```
make test module="--addopts package/tests/test_health.py"
```

- run single test in specific file
```
make test module="--addopts package/tests/test_health.py::HealthTest::test_health"
```

