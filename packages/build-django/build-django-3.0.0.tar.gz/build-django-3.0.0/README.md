# build-django

Command line utility to build Django projects

## Features

- Async
- Flexible

## Installation 
```bash
pip install build-django
```

## Usage
```bash
build-django my_project --dir my_project_path  --debug --hosts localhost,127.0.0.1,example.com --python python3  --migrate --git --commit --commit-message "My first commit!" --packages bjcli djangorestframework

```

| Argument | Description | Required | Default | Type |
| ------ | ------ | ------ | ------ | ------ |
| --version | Show version and exit | False | False | bool
| --dir | Django project directory | False | ./ | str
| --debug | Should initialize env with DEBUG=True | False | False | bool 
| --no-compile | pip: Do not compile Python source files to bytecode | False | False | bool 
| --hosts | List of comma sperated Django ALLOWED_HOSTS values | False | '' | str
| --python | Python command for initializing virtual environment. If not set, the Python used to run the program will be used | False | None | str
| --migrate | Should apply initial migrations after project built | False | False | bool
| --git | Should initialize git repository | False | False | bool
| --commit | Should create initial commit after project built and git initialized | False | False | bool
| --commit-message | Initial commit message | False | 'Initial commit' | str
| --packages | List of additional pip packages to be installed | False | [] | [str]
