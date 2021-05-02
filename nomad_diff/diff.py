# pylint: disable=invalid-name
# The above is disabled in favor of keeping this file in line with the original diff code at:
# https://github.com/hashicorp/nomad/blob/v0.12.3/command/job_plan.go#L371

from typing import List, Optional, Tuple
from .models import JobDiff, TaskGroupDiff, FieldDiff, ObjectDiff, TaskDiff


COLOR_UPDATE_TYPE_MAPPING = {
    "ignore": '[green]',
    "create": '[green]',
    "destroy": '[red]',
    "migrate": '[blue]',
    "in-place update": '[cyan]',
    "create/destroy update": '[yellow]',
    "canary": '[light_yellow]',
}

# https://github.com/hashicorp/nomad/blob/v0.12.3/command/job_plan.go#L371
def format_job_diff(job: JobDiff, verbose: bool) -> str:
    marker, _ = get_diff_string(job.Type)
    out = f'{marker}[bold]Job: "{job.ID}"\n'

    # Determine the longest markers and fields so that the output can be
    # properly aligned.
    longest_field, longest_marker = get_longest_prefixes(job.Fields, job.Objects)
    for tg in job.TaskGroups or []:
        _, l = get_diff_string(tg.Type)
        if l > longest_marker:
            longest_marker = l

    # Only show the job's field and object diffs if the job is edited or
    # verbose mode is set.
    if job.Type == "Edited" or verbose:
        fo = aligned_field_and_objects(job.Fields, job.Objects, 0, longest_field, longest_marker)
        out += fo
        if len(fo) > 0:
            out += "\n"

    # Print the task groups
    for tg in job.TaskGroups or []:
        _, mLength = get_diff_string(tg.Type)
        kPrefix = longest_marker - mLength
        out += f'{format_task_group_diff(tg, kPrefix, verbose)}\n'

    return out


# https://github.com/hashicorp/nomad/blob/v0.12.3/command/job_plan.go#L408
def format_task_group_diff(tg: TaskGroupDiff, tg_prefix: int, verbose: bool) -> str:
    marker, _ = get_diff_string(tg.Type)
    out = f'{marker}{" " * tg_prefix}[bold]Task Group: "{tg.Name}"[reset]'

    if tg.Updates:
        order = list(tg.Updates.keys())
        order.sort()

        updates = []
        for update_type in order:
            count = tg.Updates[update_type]
            color = COLOR_UPDATE_TYPE_MAPPING.get(update_type, "")

            updates.append(f'[reset]{color}{count} {update_type}')
        out += f' ({", ".join(updates)}[reset])\n'
    else:
        out += "[reset]\n"

    # Determine the longest field and markers so the output is properly
    # aligned
    longest_field, longest_marker = get_longest_prefixes(tg.Fields, tg.Objects)
    for task in tg.Tasks or []:
        _, l = get_diff_string(task.Type)
        if l > longest_marker:
            longest_marker = l

    # Only show the task groups's field and object diffs if the group is edited or
    # verbose mode is set.
    sub_start_prefix = tg_prefix + 2
    if tg.Type == "Edited" or verbose:
        fo = aligned_field_and_objects(tg.Fields, tg.Objects, sub_start_prefix, longest_field, longest_marker)
        out += fo
        if len(fo) > 0:
            out += "\n"

    # Output the tasks
    for task in tg.Tasks or []:
        _, mLength = get_diff_string(task.Type)
        prefix = longest_marker - mLength
        out += f'{format_task_diff(task, sub_start_prefix, prefix, verbose)}'

    return out


# https://github.com/hashicorp/nomad/blob/v0.12.3/command/job_plan.go#L481
def format_task_diff(task: TaskDiff, startPrefix: int, taskPrefix: int, verbose: bool) -> str:
    marker, _ = get_diff_string(task.Type)
    out = f'{" " * startPrefix}{marker}{" " * taskPrefix}[bold]Task: "{task.Name}"'

    if task.Annotations:
        out += f' [reset]({color_annotations(task.Annotations)})'

    if task.Type == "None":
        return out
    if task.Type in ("Deleted", "Added") and not verbose:
        # Exit early if the job was not edited and it isn't verbose output
        return out

    out += "\n"

    sub_start_prefix = startPrefix + 2
    longest_field, longest_marker = get_longest_prefixes(task.Fields, task.Objects)
    out += aligned_field_and_objects(task.Fields, task.Objects, sub_start_prefix, longest_field, longest_marker)

    return out


# https://github.com/hashicorp/nomad/blob/v0.12.3/command/job_plan.go#L507
def format_object_diff(diff: ObjectDiff, start_prefix: int, key_prefix: int) -> str:
    start = " " * start_prefix
    marker, markerLen = get_diff_string(diff.Type)
    out = f'{start}{marker}{" " * key_prefix}{diff.Name} {{\n'

    # Determine the length of the longest name and longest diff marker to
    # properly align names and values
    longest_field, longest_marker = get_longest_prefixes(diff.Fields, diff.Objects)
    sub_start_prefix = start_prefix + key_prefix + 2
    out += aligned_field_and_objects(diff.Fields, diff.Objects, sub_start_prefix, longest_field, longest_marker)

    endprefix = " " * (start_prefix + markerLen + key_prefix)
    return f'{out}\n{endprefix}}}'


# https://github.com/hashicorp/nomad/blob/v0.12.3/command/job_plan.go#L526
def format_field_diff(diff: FieldDiff, start_prefix: int, key_prefix: int, value_prefix: int) -> str:
    marker, _ = get_diff_string(diff.Type)
    out = f'{" " * start_prefix}{marker}{" " * key_prefix}{diff.Name}: {" " * value_prefix}'

    if diff.Type == "Added":
        out += f'"{diff.New}"'
    elif diff.Type == "Deleted":
        out += f'"{diff.Old}"'
    elif diff.Type == "Edited":
        out += f'"{diff.Old}" => "{diff.New}"'
    else:
        out += f'"{diff.New}"'

    # Color the annotations where possible
    if diff.Annotations:
        out += f' ({color_annotations(diff.Annotations)})'

    return out


# https://github.com/hashicorp/nomad/blob/v0.12.3/command/job_plan.go#L609
def get_diff_string(diff_type: str) -> Tuple[str, int]:
    if diff_type == "Added":
        return "[green]+[reset] ", 2
    if diff_type == "Deleted":
        return "[red]-[reset] ", 2
    if diff_type == "Edited":
        return "[light_yellow]+/-[reset] ", 4
    return "", 0


# https://github.com/hashicorp/nomad/blob/v0.12.3/command/job_plan.go#L590
def get_longest_prefixes(fields: Optional[List[FieldDiff]], objects: Optional[List[ObjectDiff]]) -> Tuple[int, int]:
    if fields is None:
        fields = []
    if objects is None:
        objects = []

    longest_field = longest_marker = 0

    for field in fields:
        l = len(field.Name)
        if l > longest_field:
            longest_field = l

        _, l = get_diff_string(field.Type)
        if l > longest_marker:
            longest_marker = l

    for obj in objects:
        _, l = get_diff_string(obj.Type)
        if l > longest_marker:
            longest_marker = l

    return longest_field, longest_marker


# https://github.com/hashicorp/nomad/blob/v0.12.3/command/job_plan.go#L555
def aligned_field_and_objects(
    fields: Optional[List[FieldDiff]],
    objects: Optional[List[ObjectDiff]],
    start_prefix: int,
    longest_field: int,
    longest_marker: int,
) -> str:

    if fields is None:
        fields = []
    if objects is None:
        objects = []

    out = ""
    num_fields = len(fields)
    num_objects = len(objects)
    have_objects = num_objects != 0

    for i, field in enumerate(fields):
        _, mLength = get_diff_string(field.Type)
        kPrefix = longest_marker - mLength
        vPrefix = longest_field - len(field.Name)
        out += format_field_diff(field, start_prefix, kPrefix, vPrefix)

        # Avoid a dangling new line
        if i + 1 != num_fields or have_objects:
            out += "\n"

    for i, object in enumerate(objects):  # pylint: disable=redefined-builtin
        _, mLength = get_diff_string(object.Type)
        kPrefix = longest_marker - mLength
        out += format_object_diff(object, start_prefix, kPrefix)

        # Avoid a dangling new line
        if i + 1 != num_objects:
            out += "\n"

    return out


# https://github.com/hashicorp/nomad/blob/v0.12.3/command/job_plan.go#L624
def color_annotations(annotations: Optional[List[str]]) -> str:
    if not annotations:
        return ""

    colord = []
    for annotation in annotations:
        if annotation == "forces create":
            colord.append(f'[green]{annotation}[reset]')
        elif annotation == "forces destroy":
            colord.append(f'[red]{annotation}[reset]')
        elif annotation == "forces in-place update":
            colord.append(f'[cyan]{annotation}[reset]')
        elif annotation == "forces create/destroy update":
            colord.append(f'[yellow]{annotation}[reset]')
        else:
            colord.append(annotation)

    return ", ".join(colord)
