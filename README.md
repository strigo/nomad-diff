# nomad-diff

[![CircleCI](https://circleci.com/gh/strigo/nomad-diff/tree/master.svg?style=svg)](https://circleci.com/gh/strigo/nomad-diff/tree/master)
[![PyPI Version](http://img.shields.io/pypi/v/nomad-diff.svg)](http://img.shields.io/pypi/v/nomad-diff.svg)
[![Supported Python Versions](https://img.shields.io/pypi/pyversions/nomad-diff.svg)](https://img.shields.io/pypi/pyversions/nomad-diff.svg)
[![Requirements Status](https://requires.io/github/strigo/nomad-diff/requirements.svg?branch=master)](https://requires.io/github/strigo/nomad-diff/requirements/?branch=master)
[![Code Coverage](https://codecov.io/github/strigo/nomad-diff/coverage.svg?branch=master)](https://codecov.io/github/strigo/nomad-diff?branch=master)
[![Is Wheel](https://img.shields.io/pypi/wheel/nomad-diff.svg?style=flat)](https://pypi.python.org/pypi/nomad-diff)

A one to one Python re-write of the Job diff formatter [from Nomad's source](https://github.com/hashicorp/nomad/blob/v0.12.3/command/job_plan.go#L371).
Use this if you communicate with Nomad over HTTP API and want to output the diff in the same format like the Nomad CLI & UI does.

## Installation

```
$ pip install nomad-diff
```

## Usage

```
>>> import nomad_diff
>>>
>>> data = .. # Nomad's job diff
>>>
>>> print(nomad_diff.format(data, colors=True, verbose=False))
+/- Job: "example"
+/- Task Group: "cache" (2 destroy, 1 in-place update)
  +/- Count: "3" => "1" (forces destroy)
      Task: "redis"
```
