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

import sys

import click

from ansys.mapdl.core import GraphicsBackend


@click.command(
    short_help="Convert APDL code to PyMAPDL code.",
    help="""PyMAPDL CLI tool for converting MAPDL scripts to PyMAPDL scripts.

    USAGE:

    This example demonstrates the main use of this tool:

        $ pymapdl convert -f mapdl.dat -o python.py

    If you omit the output argument, the converted code is shown on the screen.

    You can use any option from ``ansys.mapdl.core.convert.convert_apdl_block`` function:

        $ pymapdl convert -f mapdl.dat --auto-exit False
        \"\"\"Script generated by ansys-mapdl-core version 0.69.dev0\"\"\"

        from ansys.mapdl.core import launch_mapdl
        mapdl = launch_mapdl(loglevel="WARNING", print_com=True, check_parameter_names=False)
        mapdl.prep7()

        mapdl.exit()

    You can skip the imports, and the launching and exit calls if the option `--only-code` (`-oc`)
    is given.

        $ pymapdl convert -f mapdl.dat -oc
        mapdl.prep7()

    You can also pipe content from files o command line into the converter.

        $ echo -ne "/prep7" | pymapdl convert -oc
        mapdl.prep7()

        $ echo -ne "/prep7" > my_file.inp
        $ pymapdl convert -oc < my_file.inp
        mapdl.prep7()
""",
)
@click.option(
    "--file",
    "-f",
    help="Name of the APDL input file to convert to PyMAPDL code.",
    type=click.File("r"),
    default=sys.stdin,
)
@click.option(
    "--output",
    "-o",
    default=sys.stdout,
    type=click.File("at"),
    help="Name of the output Python script.",
)
@click.option(
    "--loglevel",
    "-ll",
    default="WARNING",
    help="Logging level of the ansys object within the script.",
)
@click.option(
    "--auto_exit",
    "-ae",
    default=True,
    type=bool,
    help="Adds a line to the end of the script to exit MAPDL. Default ``True``",
)
@click.option(
    "--line_ending",
    "-le",
    type=str,
    default=None,
    help="When None, automatically is ``\n.``",
)
@click.option(
    "--exec_file",
    "-e",
    default=None,
    type=str,
    help="Specify the location of the ANSYS executable and include it in the converter output ``launch_mapdl`` call.",
)
@click.option(
    "--macros_as_functions",
    "-mf",
    default=True,
    type=bool,
    help="Attempt to convert MAPDL macros to python functions.",
)
@click.option(
    "--use_function_names",
    "-fn",
    default=True,
    type=bool,
    help="Convert MAPDL functions to ansys.mapdl.core.Mapdl class methods.  When ``True``, the MAPDL command ``K`` will be converted to ``mapdl.k``.  When ``False``, it will be converted to ``mapdl.run('k')``.",
)
@click.option(
    "--show_log",
    "-sl",
    default=False,
    type=bool,
    help="Print the converted commands using a logger (from ``logging`` Python module).",
)
@click.option(
    "--add_imports",
    "-ai",
    default=True,
    type=bool,
    help='If ``True``, add the lines ``from ansys.mapdl.core import launch_mapdl`` and ``mapdl = launch_mapdl(loglevel="WARNING")`` to the beginning of the output file. This option is useful if you are planning to use the output script from another mapdl session. See examples section. This option overrides ``auto_exit``.',
)
@click.option(
    "--comment_solve",
    "-cs",
    default=False,
    type=bool,
    help='If ``True``, it will pythonically comment the lines that contain ``"SOLVE"`` or ``"/EOF"``.',
)
@click.option(
    "--cleanup_output",
    "-co",
    default=True,
    type=bool,
    help="If ``True`` the output is formatted using ``autopep8`` before writing the file or returning the string. This requires ``autopep8`` to be installed.",
)
@click.option(
    "--header",
    "-h",
    default=True,
    help="If ``True``, the default header is written in the first line of the output. If a string is provided, this string will be used as header.",
)
@click.option(
    "--print_com",
    "-pc",
    default=True,
    type=bool,
    help="Print command ``/COM`` arguments to python console. Defaults to ``True``.",
)
@click.option(
    "--only_commands",
    "-oc",
    default=False,
    is_flag=True,
    flag_value=True,
    type=bool,
    help="""If ``True``, it converts only the commands, meaning that header
(``header=False``), imports (``add_imports=False``),
and exit commands are NOT included (``auto_exit=False``).
Overrides ``header``, ``add_imports`` and ``auto_exit``.""",
)
@click.option(
    "--graphics_backend",
    default=None,
    type=str,
    help="""It sets the `mapdl.graphics_backend` argument depending on
this value. Defaults to `None` which is Mapdl class default.""",
)
@click.option(
    "--clear_at_start",
    default=False,
    help="""Add a `mapdl.clear()` after the Mapdl object initialization. Defaults to
`False`.""",
)
@click.option(
    "--check_parameter_names",
    "--cpn",
    default=False,
    help="""Set MAPDL object to avoid parameter name checks (do not raise leading underscored parameter exceptions). Defaults to `False`.""",
)
def convert(
    file: str,
    output: str,
    loglevel: str,
    auto_exit: bool,
    line_ending: str,
    exec_file: str,
    macros_as_functions: bool,
    use_function_names: bool,
    show_log: bool,
    add_imports: bool,
    comment_solve: bool,
    cleanup_output: bool,
    header: str,
    print_com: bool,
    only_commands: bool,
    graphics_backend: bool,
    clear_at_start: bool,
    check_parameter_names: bool,
) -> None:
    """Convert MAPDL code to PyMAPDL"""
    from ansys.mapdl.core.convert import convert_apdl_block

    backend = None
    if graphics_backend is not None:
        if graphics_backend == "pyvista":
            backend = GraphicsBackend.PYVISTA
        elif graphics_backend == "mapdl":
            backend = GraphicsBackend.MAPDL
        else:
            backend = None

    converted_code = convert_apdl_block(
        apdl_strings=file.read(),
        loglevel=loglevel,
        auto_exit=auto_exit,
        line_ending=line_ending,
        exec_file=exec_file,
        macros_as_functions=macros_as_functions,
        use_function_names=use_function_names,
        show_log=show_log,
        add_imports=add_imports,
        comment_solve=comment_solve,
        cleanup_output=cleanup_output,
        header=header,
        print_com=print_com,
        only_commands=only_commands,
        graphics_backend=backend,
        clear_at_start=clear_at_start,
        check_parameter_names=check_parameter_names,
    )

    click.echo(converted_code, file=output)
