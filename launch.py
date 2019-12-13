#! /usr/bin/env python

import re
import subprocess

from gi.repository import Gio


def show_menu(
    items, command='dmenu', bottom=None, fast=None, case_insensitive=None,
    lines=None, monitor=None, prompt=None, font=None, background=None,
    foreground=None, background_selected=None, foreground_selected=None
):
    args = [command]

    if bottom:
        args.append('-b')
    if fast:
        args.append('-f')
    if case_insensitive:
        args.append('-i')
    if lines is not None:
        args.extend(('-l', str(lines)))
    if monitor is not None:
        args.extend(('-m', str(monitor)))
    if prompt is not None:
        args.extend(('-p', prompt))
    if font is not None:
        args.extend(('-fn', font))
    if background is not None:
        args.extend(('-nb', background))
    if foreground is not None:
        args.extend(('-nf', foreground))
    if background_selected is not None:
        args.extend(('-sb', background_selected))
    if foreground_selected is not None:
        args.extend(('-sf', foreground_selected))

    proc = subprocess.Popen(
        args,
        universal_newlines=True,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)

    with proc.stdin:
        for item in items:
            proc.stdin.write(item)
            proc.stdin.write('\n')

    if proc.wait() == 0:
        return proc.stdout.read().rstrip('\n')

    stderr = proc.stderr.read()
    if stderr == '':
        # user hit escape
        return None

    raise Exception(stderr)


def get_apps():
    return (
        app for app in Gio.AppInfo.get_all()
        if not app.get_is_hidden()
    )


def main():
    apps = {app.get_name(): app for app in get_apps()}
    selected = show_menu(
        sorted(apps.keys()), case_insensitive=True, font="IBM Plex Sans"
    )
    if not selected:
        return

    app = apps[selected]
    command_line = re.sub("%\\w", "", app.get_commandline()).strip()
    print(command_line)
    subprocess.Popen([command_line])


if __name__ == '__main__':
    main()
