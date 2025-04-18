# Copyright (C) 2016 - 2025 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from typing import Optional

import click


@click.command(
    short_help="Stop MAPDL instances.",
    help="""This command stop MAPDL instances running on a given port or with a given process id (PID).

By default, it stops instances running on the port 50052.""",
)
@click.option(
    "--port",
    default=None,
    type=int,
    help="Port where the MAPDL instance is running.",
)
@click.option(
    "--pid",
    default=None,
    type=int,
    help="Process PID where the MAPDL instance is running.",
)
@click.option(
    "--all",
    is_flag=True,
    flag_value=True,
    type=bool,
    default=False,
    help="Kill all MAPDL instances",
)
def stop(port: int, pid: Optional[int], all: bool) -> None:
    """Stop MAPDL instances running on a given port or with a given process id (PID).

    This command stops MAPDL instances running on a given port or with a given process id (PID).
    By default, it stops instances running on the port 50052.

    Parameters
    ----------
    port : int
        Port where the MAPDL instance is running.
    pid : Optional[int]
        PID of the MAPDL instance
    all : bool
        If :class:`True`, kill all the instances regardless their port or PID.
    """
    import psutil

    PROCESS_OK_STATUS = [
        # List of all process status, comment out the ones that means that
        # process is not OK.
        # If process is OK, it means it can be killed normally.
        psutil.STATUS_RUNNING,  #
        psutil.STATUS_SLEEPING,  #
        psutil.STATUS_DISK_SLEEP,  #
        # psutil.STATUS_STOPPED, #
        # psutil.STATUS_TRACING_STOP, #
        # psutil.STATUS_ZOMBIE, #
        psutil.STATUS_DEAD,  #
        # psutil.STATUS_WAKE_KILL, #
        # psutil.STATUS_WAKING, #
        psutil.STATUS_PARKED,  # (Linux)
        psutil.STATUS_IDLE,  # (Linux, macOS, FreeBSD)
        # psutil.STATUS_LOCKED, # (FreeBSD)
        # psutil.STATUS_WAITING, # (FreeBSD)
        # psutil.STATUS_SUSPENDED, # (NetBSD)
    ]

    if not pid and not port:
        port = 50052

    if port or all:
        killed_ = False
        for proc in psutil.process_iter():
            try:
                if _is_valid_ansys_process(PROCESS_OK_STATUS, proc):
                    # Killing "all"
                    if all:
                        try:
                            _kill_process(proc)
                            killed_ = True
                        except psutil.NoSuchProcess:
                            pass

                    else:
                        # Killing by ports
                        if str(port) in proc.cmdline():
                            try:
                                _kill_process(proc)
                                killed_ = True
                            except psutil.NoSuchProcess:
                                pass

            except psutil.NoSuchProcess:
                continue

        if all:
            str_ = ""
        else:
            str_ = f" running on port {port}"

        if not killed_:
            click.echo(
                click.style("ERROR: ", fg="red")
                + "No Ansys instances"
                + str_
                + " have been found."
            )
        else:
            click.echo(
                click.style("Success: ", fg="green")
                + "Ansys instances"
                + str_
                + " have been stopped."
            )
        return

    if pid:
        try:
            pid = int(pid)
        except ValueError:
            click.echo(
                click.style("ERROR: ", fg="red")
                + "PID provided could not be converted to int."
            )

        p = psutil.Process(pid)
        for child in p.children(recursive=True):
            _kill_process(child)

        _kill_process(p)

        if p.status == "running":
            click.echo(
                click.style("ERROR: ", fg="red")
                + f"The process with PID {pid} and its children could not be killed."
            )
        else:
            click.echo(
                click.style("Success: ", fg="green")
                + f"The process with PID {pid} and its children have been stopped."
            )
        return


def _kill_process(proc):
    proc.kill()


def _is_valid_ansys_process(PROCESS_OK_STATUS, proc):
    import psutil

    from ansys.mapdl.core.launcher import is_ansys_process

    return (
        psutil.pid_exists(proc.pid)
        and proc.status() in PROCESS_OK_STATUS
        and is_ansys_process(proc)
    )
