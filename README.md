[Daily Coding Problem](https://www.dailycodingproblem.com/)

[![](https://github.com/asarkar/daily-coding-problem/workflows/Daily%20Coding%20Problem/badge.svg)](https://github.com/asarkar/daily-coding-problem/actions)

Solutions to questions 1 through 125 are found [here](https://github.com/asarkar/coding-interview). I will try to add
Python solutions here as time permits.

## Run in Docker Container

```
$ docker run -it --name python -v /path/to/daily-coding-problem:/srv/daily-coding-problem \
    -w /srv/daily-coding-problem python:3.8-slim-buster /bin/bash
$ pip install -r requirements.txt
```

To disable stdout/stderr output by Pytest

```
$ pytest -s
```

## Install pyenv

```
$ xcode-select --install
$ brew update && brew install pyenv
$ pyenv install <version>
$ pyenv global <version>
```

Add `eval "$(pyenv init -)"` to `~/.bash_profile`. Relaunch Terminal.

Check that `pyenv` managed version is used

```
which python
```

Upgrade `pip`

```
pip install --upgrade pip
```

Install `pytest` and `flake8`
 
 ```
$ pip install -U pytest flake8
 ```