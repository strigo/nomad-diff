# nomad-diff

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
 