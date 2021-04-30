from colorama import Fore, Style  # type: ignore

from .diff import format_job_diff, JobDiff


COLORS = {
    '[green]': Fore.GREEN,
    '[red]': Fore.RED,
    '[blue]': Fore.BLUE,
    '[cyan]': Fore.CYAN,
    '[yellow]': Fore.YELLOW,
    '[light_yellow]': Fore.LIGHTYELLOW_EX,
    '[bold]': Style.BRIGHT,
    '[reset]': Style.RESET_ALL,
}


# Note that the pylint check below should not be disabled. We could potentially simply change it,
# but it would mean changing things in wand. Let's start from working around this.
def format(diff: dict, colors: bool, verbose: bool):  # pylint: disable= redefined-builtin
    diff_dict = JobDiff(**diff)
    out = format_job_diff(diff_dict, verbose)

    if not colors:
        return strip_colors(out)

    return colorize(out)


def strip_colors(diff: str):
    for e in COLORS:
        diff = diff.replace(e, '')

    return diff


def colorize(diff: str):
    for diff_color, real_color in COLORS.items():
        diff = diff.replace(diff_color, real_color)

    return diff
