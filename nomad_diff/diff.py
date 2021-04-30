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
    for task_group in job.TaskGroups or []:
        _, diff_string = get_diff_string(task_group.Type)
        if diff_string > longest_marker:
            longest_marker = diff_string

    # Only show the job's field and object diffs if the job is edited or
    # verbose mode is set.
    if job.Type == "Edited" or verbose:
        aligned = aligned_field_and_objects(job.Fields, job.Objects, 0, longest_field, longest_marker)
        out += aligned
        if len(aligned) > 0:
            out += "\n"

    # Print the task groups
    for task_group in job.TaskGroups or []:
        _, market_length = get_diff_string(task_group.Type)
        key_prefix = longest_marker - market_length
        out += f'{format_task_group_diff(task_group, key_prefix, verbose)}\n'

    return out


# https://github.com/hashicorp/nomad/blob/v0.12.3/command/job_plan.go#L408
def format_task_group_diff(task_group: TaskGroupDiff, task_group_prefix: int, verbose: bool) -> str:
    marker, _ = get_diff_string(task_group.Type)
    out = f'{marker}{" " * task_group_prefix}[bold]Task Group: "{task_group.Name}"[reset]'

    if task_group.Updates:
        order = list(task_group.Updates.keys())
        order.sort()

        updates = []
        for update_type in order:
            count = task_group.Updates[update_type]
            color = COLOR_UPDATE_TYPE_MAPPING.get(update_type, "")

            updates.append(f'[reset]{color}{count} {update_type}')
        out += f' ({", ".join(updates)}[reset])\n'
    else:
        out += "[reset]\n"

    # Determine the longest field and markers so the output is properly
    # aligned
    longest_field, longest_marker = get_longest_prefixes(task_group.Fields, task_group.Objects)
    for task in task_group.Tasks or []:
        _, diff_string = get_diff_string(task.Type)
        if diff_string > longest_marker:
            longest_marker = diff_string

    # Only show the task groups's field and object diffs if the group is edited or
    # verbose mode is set.
    sub_start_prefix = task_group_prefix + 2
    if task_group.Type == "Edited" or verbose:
        aligned = aligned_field_and_objects(
            task_group.Fields, task_group.Objects, sub_start_prefix, longest_field, longest_marker
        )
        out += aligned
        if len(aligned) > 0:
            out += "\n"

    # Output the tasks
    for task in task_group.Tasks or []:
        _, market_length = get_diff_string(task.Type)
        prefix = longest_marker - market_length
        out += f'{format_task_diff(task, sub_start_prefix, prefix, verbose)}'

    return out


# https://github.com/hashicorp/nomad/blob/v0.12.3/command/job_plan.go#L481
def format_task_diff(task: TaskDiff, start_prefix: int, task_prefix: int, verbose: bool) -> str:
    marker, _ = get_diff_string(task.Type)
    out = f'{" " * start_prefix}{marker}{" " * task_prefix}[bold]Task: "{task.Name}"'

    if task.Annotations:
        out += f' [reset]({color_annotations(task.Annotations)})'

    # Exit early if the job was not edited and it isn't verbose output
    if task.Type == "None":
        return out

    if task.Type in ("Deleted", "Added") and not verbose:
        return out

    out += "\n"

    sub_start_prefix = start_prefix + 2
    longest_field, longest_marker = get_longest_prefixes(task.Fields, task.Objects)
    out += aligned_field_and_objects(task.Fields, task.Objects, sub_start_prefix, longest_field, longest_marker)

    return out


# https://github.com/hashicorp/nomad/blob/v0.12.3/command/job_plan.go#L507
def format_object_diff(diff: ObjectDiff, start_prefix: int, key_prefix: int) -> str:
    start = " " * start_prefix
    marker, market_length = get_diff_string(diff.Type)
    out = f'{start}{marker}{" " * key_prefix}{diff.Name} {{\n'

    # Determine the length of the longest name and longest diff marker to
    # properly align names and values
    longest_field, longest_marker = get_longest_prefixes(diff.Fields, diff.Objects)
    sub_start_prefix = start_prefix + key_prefix + 2
    out += aligned_field_and_objects(diff.Fields, diff.Objects, sub_start_prefix, longest_field, longest_marker)

    endprefix = " " * (start_prefix + market_length + key_prefix)
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
        length = len(field.Name)
        if length > longest_field:
            longest_field = length

        _, length = get_diff_string(field.Type)
        if length > longest_marker:
            longest_marker = length

    for obj in objects:
        _, length = get_diff_string(obj.Type)
        if length > longest_marker:
            longest_marker = length

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
        _, market_length = get_diff_string(field.Type)
        key_prefix = longest_marker - market_length
        value_prefix = longest_field - len(field.Name)
        out += format_field_diff(field, start_prefix, key_prefix, value_prefix)

        # Avoid a dangling new line
        if i + 1 != num_fields or have_objects:
            out += "\n"

    for i, obj in enumerate(objects):
        _, market_length = get_diff_string(obj.Type)
        key_prefix = longest_marker - market_length
        out += format_object_diff(obj, start_prefix, key_prefix)

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
