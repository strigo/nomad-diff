from .diff import format_job_diff, JobDiff
from colorama import Fore, Style  # type: ignore


COLORS = {
    '[green]': Fore.GREEN,
    '[red]': Fore.RED,
    '[blue]': Fore.BLUE,
    '[cyan]': Fore.CYAN,
    '[yellow]': Fore.YELLOW,
    '[light_yellow]': Fore.LIGHTYELLOW_EX,
    '[bold]': Style.BRIGHT,
    '[reset]': Style.RESET_ALL
}


def format(diff: dict, colors: bool, verbose: bool):
    diff_dict = JobDiff(**diff)
    out = format_job_diff(diff_dict, verbose)

    if not colors:
        return strip_colors(out)

    return colorize(out)


def strip_colors(diff: str):
    for e in COLORS.keys():
        diff = diff.replace(e, '')

    return diff


def colorize(diff: str):
    for p, color in COLORS.items():
        diff = diff.replace(p, color)

    return diff
