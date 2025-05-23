.. _ref_mapdl_user_guide:

==========================
PyMAPDL language and usage
==========================

This page gives you an overview of the PyMAPDL API for the
:class:`Mapdl <ansys.mapdl.core.mapdl.MapdlBase>` class.
For more information, see :ref:`ref_mapdl_api`.

Overview
========
When calling MAPDL commands as functions, each command has been
translated from its original MAPDL all CAPS format to a PEP8
compatible format. For example, ``ESEL`` is now the
:func:`Mapdl.esel() <ansys.mapdl.core.Mapdl.esel>` method.


.. tab-set::

    .. tab-item:: APDL
        :sync: key1

        .. code:: apdl

            ! Selecting elements whose centroid x coordinate
            ! is between 1 and 2.
            ESEL, S, CENT, X, 1, 2

    .. tab-item:: Python
        :sync: key2

        .. code:: python

            # Selecting elements whose centroid x coordinate
            # is between 1 and 2.
            # returns an array of selected elements ids
            mapdl.esel("S", "CENT", "X", 1, 2)
    

Additionally, MAPDL commands
containing a ``/`` or ``*`` have had those characters removed, unless
this causes a conflict with an existing name. Most notable is
``/SOLU``, which would conflict with ``SOLU``. Therefore,
``/SOLU`` is renamed to the
:func:`Mapdl.slashsolu() <ansys.mapdl.core.Mapdl.slashsolu>`
method to differentiate it from ``solu``.
Out of the 1500 MAPDL commands, about 15 start with ``slash (/)`` and 8
start with ``star (*)``.


.. tab-set::

    .. tab-item:: APDL
        :sync: key1

        .. code:: apdl

            *STATUS
            /SOLU

    .. tab-item:: Python
        :sync: key2

        .. code:: python

            mapdl.startstatus()
            mapdl.slashsolu()
    

MAPDL commands that can accept an empty space as argument, such as 
``ESEL,S,TYPE,,1``, should include an empty string when called by Python,
or, these commands can be called using keyword arguments:

.. tab-set::

    .. tab-item:: APDL
        :sync: key1

        .. code:: apdl

            ESEL,S,TYPE,,1

    .. tab-item:: Python
        :sync: key2

        .. code:: python

            mapdl.esel("s", "type", "", 1)
            mapdl.esel("s", "type", vmin=1)
    

None of these restrictions apply to commands run with the :func:`Mapdl.run()
<ansys.mapdl.core.Mapdl.run>` method. It might be easier to run some of
these commands, such as ``"/SOLU"``:

.. tab-set::

    .. tab-item:: APDL
        :sync: key1

        .. code:: apdl

            /SOLU

    .. tab-item:: Python
        :sync: key2

        .. code:: python

            # The next three functions are equivalent. Enter the solution processor.
            mapdl.run("/SOLU")
            mapdl.slashsolu()
            mapdl.solution()


Selecting entities
------------------
You can select entities such as nodes or lines using these methods:

* :func:`Mapdl.nsel() <ansys.mapdl.core.Mapdl.nsel>`
* :func:`Mapdl.esel() <ansys.mapdl.core.Mapdl.esel>`
* :func:`Mapdl.ksel() <ansys.mapdl.core.Mapdl.ksel>`
* :func:`Mapdl.lsel() <ansys.mapdl.core.Mapdl.lsel>`
* :func:`Mapdl.asel() <ansys.mapdl.core.Mapdl.asel>`
* :func:`Mapdl.vsel() <ansys.mapdl.core.Mapdl.vsel>`

The preceding methods return the IDs of the selected entities. For example:

.. code:: pycon

    >>> selected_nodes = mapdl.nsel("S", "NODE", vmin=1, vmax=2000)
    >>> print(selected_nodes)
    array([   1    2    3 ... 1998 1999 2000])

.. code:: pycon

    >>> mapdl.ksel("all")
    array([1, 2, 3, ..., 1998, 1999, 2000])


Running in non-interactive mode
-------------------------------

Some commands can only be run non-interactively from within a
script. PyMAPDL gets around this restriction by writing the commands
to a temporary input file and then reading the input file. To run a
group of commands that must be run non-interactively, set the
:class:`Mapdl <ansys.mapdl.core.mapdl.MapdlBase>` class to run a series
of commands as an input file by using the
:func:`Mapdl.non_interactive() <ansys.mapdl.core.Mapdl.non_interactive>`
method. Here is an example:

.. code:: python

    with mapdl.non_interactive:
        mapdl.run("*VWRITE,LABEL(1),VALUE(1,1),VALUE(1,2),VALUE(1,3)")
        mapdl.run("(1X,A8,'   ',F10.1,'  ',F10.1,'   ',1F5.3)")


You can then view the final response of the non-interactive context with the
:attr:`Mapdl.last_response <ansys.mapdl.core.Mapdl.last_response>` attribute.

Using the :meth:`Mapdl.non_interactive() <ansys.mapdl.core.Mapdl.non_interactive>`
method can also be useful to run commands on the server side without the interaction
of Python. This can speed up things greatly, but you should be aware of how
APDL works. An interesting discussion about speed comparison between PyMAPDL and APDL
can be found in `Speed comparison between PyMAPDL and APDL <pymapdl_discussion_speed_pymapdl_mapdl_>`_.

You should use the
:meth:`Mapdl.non_interactive() <ansys.mapdl.core.Mapdl.non_interactive>` method with caution.

How the non-interactive context manager works
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The :meth:`Mapdl.non_interactive() <ansys.mapdl.core.Mapdl.non_interactive>` method is implemented
as a `context manager <python_context_manager_>`_, which means that there are some actions
happening when entering and exit the context.
When entering the context, the :class:`Mapdl <ansys.mapdl.core.mapdl._MapdlCore>` instance stops sending any APDL
command to the MAPDL instance.
Instead, it allocates a buffer for those APDL commands.
For each PyMAPDL command inside that context, PyMAPDL stores the equivalent MAPDL command
inside that buffer.
Right before exiting the context, PyMAPDL creates a text file with all these APDL commands, sends it to
the MAPDL instance, and runs it using the
:meth:`Mapdl.input() <ansys.mapdl.core.Mapdl.input>` method.


For instance, this example code uses the :meth:`non_interactive context <ansys.mapdl.core.Mapdl.non_interactive>` method to generate input for MAPDL:

.. code:: python

    with mapdl.non_interactive:
        mapdl.nsel("all")
        mapdl.nsel("R", "LOC", "Z", 10)

The preceding code generates this input for MAPDL:

.. code:: apdl

    NSEL,ALL   
    NSEL,R,LOC,Z,10

This MAPDL input is executed with a :meth:`Mapdl.input() <ansys.mapdl.core.Mapdl.input>` method call.

Because of the non-interactive context not running all the commands until the end,
you might find issues interacting inside it, with Python for instance.
For example, running Python commands such as the
:meth:`Mapdl.get_array() <ansys.mapdl.core.Mapdl.get_array>` method
inside the context can give you out-of-sync responses.
The following code snippet is a demonstration of this kind of problem:

.. code:: python

    # Create some keypoints
    mapdl.clear()
    mapdl.k(1, 0, 0, 0)
    mapdl.k(2, 1, 0, 0)

    with mapdl.non_interactive:
        mapdl.k(3, 2, 0, 0)
        klist_inside = mapdl.get_array("KP", item1="KLIST")
        # Here is where PyMAPDL sends the commands to the MAPDL instance and execute 'mapdl.k(3,2,0,0)' (`K,3,2,0,0`

    klist_outside = mapdl.get_array("KP", item1="KLIST")

    assert klist_inside != klist_outside  # Evaluates to true

In the preceding script, the values obtained by the
:meth:`Mapdl.get_array() <ansys.mapdl.core.Mapdl.get_array>` method are different:

.. code:: pycon

    >>> print(klist_inside)
    array([1., 2.])
    >>> print(klist_outside)
    array([1., 2., 3.])

This is because the first :meth:`Mapdl.get_array() <ansys.mapdl.core.Mapdl.get_array>`
method call is executed *before* the :meth:`Mapdl.k() <ansys.mapdl.core.Mapdl.k>` method call.

You should not retrieve any data in a Pythonic way from the MAPDL instance while using the
:meth:`non_interactive context <ansys.mapdl.core.Mapdl.non_interactive>` method.
Being aware of this kind of behavior and how the :meth:`non_interactive context <ansys.mapdl.core.Mapdl.non_interactive>` method
works is crucial for advanced usage of PyMAPDL.


MAPDL macros
------------
Note that macros created within PyMAPDL (rather than loaded from
a file) do not appear to run correctly. For example, here is the ``DISP``
macro created using the ``*CREATE`` command within APDL and within PyMAPDL:


.. tab-set::

    .. tab-item:: APDL
        :sync: key1

        .. code:: apdl

            ! SELECT NODES AT Z = 10 TO APPLY DISPLACEMENT
            *CREATE,DISP
            NSEL,R,LOC,Z,10
            D,ALL,UZ,ARG1
            NSEL,ALL
            /OUT,SCRATCH
            SOLVE
            *END

            ! Call the function
            *USE,DISP,-.032
            *USE,DISP,-.05
            *USE,DISP,-.1

    .. tab-item:: Python
        :sync: key2

        .. code:: python

            def DISP(
                ARG1="",
                ARG2="",
                ARG3="",
                ARG4="",
                ARG5="",
                ARG6="",
                ARG7="",
                ARG8="",
                ARG9="",
                ARG10="",
                ARG11="",
                ARG12="",
                ARG13="",
                ARG14="",
                ARG15="",
                ARG16="",
                ARG17="",
                ARG18="",
            ):
                mapdl.nsel("R", "LOC", "Z", 10)  # SELECT NODES AT Z = 10 TO APPLY DISPLACEMENT
                mapdl.d("ALL", "UZ", ARG1)
                mapdl.nsel("ALL")
                mapdl.run("/OUT,SCRATCH")
                mapdl.solve()


            DISP(-0.032)
            DISP(-0.05)
            DISP(-0.1)

If you have an existing input file with a macro, you can convert it
using the :func:`convert_script() <ansys.mapdl.core.convert_script>`
method, setting``macros_as_functions=True``:

.. code:: pycon

    >>> from ansys.mapdl import core as pymapdl
    >>> pymapdl.convert_script(apdl_inputfile, pyscript, macros_as_functions=True)



Additional options when running commands
----------------------------------------
Commands can be run in ``mute`` or ``verbose`` mode, which allows you
to suppress or print the output as it is being run for any MAPDL
command. This can be especially helpful for long-running commands
like ``SOLVE``. This works for the Pythonic wrapping of all commands
and when using the :func:`Mapdl.run() <ansys.mapdl.core.Mapdl.run>` method.

Run a command and suppress its output:

.. code:: pycon

    >>> mapdl.run("/PREP7", mute=True)
    >>> mapdl.prep7(mute=True)

Run a command and stream its output while it is being run:

.. code:: pycon

    >>> mapdl.run("SOLVE", mute=True)
    >>> mapdl.solve(verbose=True)

.. note::
    The ``verbose`` and ``mute`` features are only available when
    running MAPDL in gRPC mode.


Running several commands or an input file
-----------------------------------------
You can run several MAPDL commands as a unified block using the
:func:`Mapdl.input_strings() <ansys.mapdl.core.Mapdl.input_strings>` method.
This is useful when using PyMAPDL with older MAPDL scripts. For example:

.. code:: python

    cmd = """/prep7
    ! Mat
    MP,EX,1,200000
    MP,NUXY,1,0.3
    MP,DENS,1,7.85e-09
    ! Elements
    et,1,186
    ! Geometry
    BLC4,0,0,1000,100,10
    ! Mesh
    esize,5
    vmesh,all"""

.. code:: pycon

    >>> resp = mapdl.input_strings(cmd)
    >>> resp
    You have already entered the general preprocessor (PREP7).

    MATERIAL          1     EX   =   200000.0

    MATERIAL          1     NUXY =  0.3000000

    MATERIAL          1     DENS =  0.7850000E-08

    ELEMENT TYPE          1 IS SOLID186     3-D 20-NODE STRUCTURAL SOLID
    KEYOPT( 1- 6)=        0      0      0        0      0      0
    KEYOPT( 7-12)=        0      0      0        0      0      0
    KEYOPT(13-18)=        0      0      0        0      0      0

    CURRENT NODAL DOF SET IS  UX    UY    UZ
    THREE-DIMENSIONAL MODEL

    CREATE A HEXAHEDRAL VOLUME WITH
    X-DISTANCES FROM      0.000000000     TO      1000.000000
    Y-DISTANCES FROM      0.000000000     TO      100.0000000
    Z-DISTANCES FROM      0.000000000     TO      10.00000000

        OUTPUT VOLUME =     1

    DEFAULT ELEMENT DIVISIONS PER LINE BASED ON ELEMENT SIZE =   5.00

    GENERATE NODES AND ELEMENTS   IN  ALL  SELECTED VOLUMES

    NUMBER OF VOLUMES MESHED   =         1
    MAXIMUM NODE NUMBER        =     45765
    MAXIMUM ELEMENT NUMBER     =      8000

Alternatively, you can simply write the commands to a file and then
run the file using the :func:`Mapdl.input() <ansys.mapdl.core.Mapdl.input>`
method. For example, if you have a ``"ds.dat"`` file generated from Ansys
Mechanical, you can run that with:

.. code:: pycon

    >>> resp = mapdl.input("ds.dat")


Conditional statements and loops
--------------------------------
APDL conditional statements such as ``*IF`` must be either implemented
Pythonically or by using the :attr:`Mapdl.non_interactive <ansys.mapdl.core.Mapdl.non_interactive>`
attribute. For example:

.. tab-set::

    .. tab-item:: APDL
        :sync: key1

        .. code:: apdl

            *IF,ARG1,EQ,0,THEN
            *GET,ARG4,NX,ARG2     ! RETRIEVE COORDINATE LOCATIONS OF BOTH NODES
            *GET,ARG5,NY,ARG2
            *GET,ARG6,NZ,ARG2
            *GET,ARG7,NX,ARG3
            *GET,ARG8,NY,ARG3
            *GET,ARG9,NZ,ARG3
            *ELSE
            *GET,ARG4,KX,ARG2     ! RETRIEVE COORDINATE LOCATIONS OF BOTH KEYPOINTS
            *GET,ARG5,KY,ARG2
            *GET,ARG6,KZ,ARG2
            *GET,ARG7,KX,ARG3
            *GET,ARG8,KY,ARG3
            *GET,ARG9,KZ,ARG3
            *ENDIF

    .. tab-item:: Python-Non interactive
        :sync: key3

        .. code:: python

            with mapdl.non_interactive:
                mapdl.run("*IF,ARG1,EQ,0,THEN")
                mapdl.run("*GET,ARG4,NX,ARG2     ")  # RETRIEVE COORDINATE LOCATIONS OF BOTH NODES
                mapdl.run("*GET,ARG5,NY,ARG2")
                mapdl.run("*GET,ARG6,NZ,ARG2")
                mapdl.run("*GET,ARG7,NX,ARG3")
                mapdl.run("*GET,ARG8,NY,ARG3")
                mapdl.run("*GET,ARG9,NZ,ARG3")
                mapdl.run("*ELSE")
                mapdl.run(
                    "*GET,ARG4,KX,ARG2     "
                )  # RETRIEVE COORDINATE LOCATIONS OF BOTH KEYPOINTS
                mapdl.run("*GET,ARG5,KY,ARG2")
                mapdl.run("*GET,ARG6,KZ,ARG2")
                mapdl.run("*GET,ARG7,KX,ARG3")
                mapdl.run("*GET,ARG8,KY,ARG3")
                mapdl.run("*GET,ARG9,KZ,ARG3")
                mapdl.run("*ENDIF")


    .. tab-item:: Python
        :sync: key2

        .. code:: python

            if ARG1 == 0:
                mapdl.get(ARG4, "NX", ARG2)  # RETRIEVE COORDINATE LOCATIONS OF BOTH NODES
                mapdl.get(ARG5, "NY", ARG2)
                mapdl.get(ARG6, "NZ", ARG2)
                mapdl.get(ARG7, "NX", ARG3)
                mapdl.get(ARG8, "NY", ARG3)
                mapdl.get(ARG9, "NZ", ARG3)
            else:
                mapdl.get(ARG4, "KX", ARG2)  # RETRIEVE COORDINATE LOCATIONS OF BOTH KEYPOINTS
                mapdl.get(ARG5, "KY", ARG2)
                mapdl.get(ARG6, "KZ", ARG2)
                mapdl.get(ARG7, "KX", ARG3)
                mapdl.get(ARG8, "KY", ARG3)
                mapdl.get(ARG9, "KZ", ARG3)

The values of ``ARGX`` parameters are not retrieved from the MAPDL instance.
Hence you cannot use those arguments in Python code unless you use the following commands:

.. code:: python

   ARG4 = mapdl.parameters["ARG4"]
   ARG5 = mapdl.parameters["ARG5"]
   # ...
   # etc

APDL loops using ``*DO`` or ``*DOWHILE`` should also be implemented
using the :attr:`Mapdl.non_interactive <ansys.mapdl.core.Mapdl.non_interactive>`
attribute or implemented Pythonically.


Warnings and errors
-------------------
Errors are handled Pythonically. For example:

.. code:: python

    try:
        mapdl.solve()
    except:
        # do something else with MAPDL
        pass

Commands that are ignored within MAPDL are flagged as errors. This is
different than MAPDL's default behavior where commands that are
ignored are treated as warnings. For example, in ``ansys-mapdl-core``
running a command in the wrong session raises an error:

.. code:: pycon

    >>> mapdl.finish()
    >>> mapdl.k()

    Exception: 
    K, , , , 

     *** WARNING ***                         CP =       0.307   TIME= 11:05:01
     K is not a recognized BEGIN command, abbreviation, or macro.  This      
     command will be ignored.

You can change this behavior so ignored commands can be logged as
warnings and not raised as exceptions by using the
:func:`Mapdl.ignore_errors() <ansys.mapdl.core.Mapdl.ignore_errors>` function. For
example:

.. code:: pycon

   >>> mapdl.ignore_errors = True
   >>> mapdl.k()  # warning silently ignored


Prompts
-------
Prompts from MAPDL automatically continued as if MAPDL is in batch
mode. Commands requiring user input, such as the
:meth:`Mapdl.vwrite() <ansys.mapdl.core.Mapdl.vwrite>` method, fail
and must be entered in non-interactively.


APDL command logging
====================
While ``ansys-mapdl-core`` is designed to make it easier to control an
APDL session by calling it using Python, it might be necessary to call
MAPDL again using an input file generated from a PyMAPDL script. This
is automatically enabled with the ``log_apdl='apdl.log'`` parameter.
Enabling this parameter causes the
:class:`Mapdl <ansys.mapdl.core.mapdl.MapdlBase>` class to write each
command run into a log file named ``"apdl.log"`` in the active
:attr:`Mapdl.directory <ansys.mapdl.core.Mapdl.directory>`. 
For example:

.. code:: pycon

    >>> from ansys.mapdl.core import launch_mapdl

    >>> ansys = launch_mapdl(log_apdl="apdl.log")
    >>> ansys.prep7()
    >>> ansys.k(1, 0, 0, 0)
    >>> ansys.k(2, 1, 0, 0)
    >>> ansys.k(3, 1, 1, 0)
    >>> ansys.k(4, 0, 1, 0)

This code writes the following to the ``"apdl.log"`` file:

.. code:: apdl

    /PREP7,
    K,1,0,0,0
    K,2,1,0,0
    K,3,1,1,0
    K,4,0,1,0

This allows for the translation of a Python script to an APDL script
except for conditional statements, loops, or functions.

Use the ``lgwrite`` method
--------------------------
Alternatively, if you only want the database command output, you can use the
:func:`Mapdl.lgwrite <Mapdl.ansys.mapdl.core.Mapdl.lgwrite>` method to write the
entire database command log to a file.


Interactive breakpoint
======================
In most circumstances, it is necessary or preferable to open up the
MAPDL GUI. The :class:`Mapdl <ansys.mapdl.core.mapdl.MapdlBase>` class
has the :func:`Mapdl.open_gui() <ansys.mapdl.core.Mapdl.open_gui>` method, which
allows you to seamlessly open up the GUI without losing work or
having to restart your session. For example:

.. code:: pycon

    >>> from ansys.mapdl.core import launch_mapdl
    >>> mapdl = launch_mapdl()

Create a square area using keypoints

.. code:: pycon

    >>> mapdl.prep7()
    >>> mapdl.k(1, 0, 0, 0)
    >>> mapdl.k(2, 1, 0, 0)
    >>> mapdl.k(3, 1, 1, 0)
    >>> mapdl.k(4, 0, 1, 0)
    >>> mapdl.l(1, 2)
    >>> mapdl.l(2, 3)
    >>> mapdl.l(3, 4)
    >>> mapdl.l(4, 1)
    >>> mapdl.al(1, 2, 3, 4)

Open up the GUI

.. code:: pycon

    >>> mapdl.open_gui()

Resume where you left off

.. code:: pycon

    >>> mapdl.et(1, "MESH200", 6)
    >>> mapdl.amesh("all")
    >>> mapdl.eplot()

This approach avoids the hassle of having to switch back and forth
between an interactive session and a scripting session. Instead, you
can have one scripting session and open up a GUI from the scripting
session without losing work or progress. Additionally, none of the
changes made in the GUI affect the script. You can experiment in
the GUI, and the script is left unaffected.


Run a batch job
===============
Instead of running a MAPDL batch by calling MAPDL with an input file,
you can instead define a function that runs MAPDL. This example runs
a mesh convergence study based on the maximum stress of a cylinder
with torsional loading.

.. code:: python

    import numpy as np
    from ansys.mapdl.core import launch_mapdl


    def cylinder_batch(elemsize, plot=False):
        """Report the maximum von Mises stress of a Cantilever supported cylinder"""

        # clear
        mapdl.finish()
        mapdl.clear()

        # cylinder parameters
        radius = 2
        h_tip = 2
        height = 20
        force = 100 / radius
        pressure = force / (h_tip * 2 * np.pi * radius)

        mapdl.prep7()
        mapdl.et(1, 186)
        mapdl.et(2, 154)
        mapdl.r(1)
        mapdl.r(2)

        # Aluminum properties (or something)
        mapdl.mp("ex", 1, 10e6)
        mapdl.mp("nuxy", 1, 0.3)
        mapdl.mp("dens", 1, 0.1 / 386.1)
        mapdl.mp("dens", 2, 0)

        # Simple cylinder
        for i in range(4):
            mapdl.cylind(radius, "", "", height, 90 * (i - 1), 90 * i)

        mapdl.nummrg("kp")

        # mesh cylinder
        mapdl.lsel("s", "loc", "x", 0)
        mapdl.lsel("r", "loc", "y", 0)
        mapdl.lsel("r", "loc", "z", 0, height - h_tip)
        # mapdl.lesize('all', elemsize*2)
        mapdl.mshape(0)
        mapdl.mshkey(1)
        mapdl.esize(elemsize)
        mapdl.allsel("all")
        mapdl.vsweep("ALL")
        mapdl.csys(1)
        mapdl.asel("s", "loc", "z", "", height - h_tip + 0.0001)
        mapdl.asel("r", "loc", "x", radius)
        mapdl.local(11, 1)
        mapdl.csys(0)
        mapdl.aatt(2, 2, 2, 11)
        mapdl.amesh("all")
        mapdl.finish()

        if plot:
            mapdl.view(1, 1, 1, 1)
            mapdl.eplot()

        # new solution
        mapdl.slashsolu()
        mapdl.antype("static", "new")
        mapdl.eqslv("pcg", 1e-8)

        # Apply tangential pressure
        mapdl.esel("s", "type", "", 2)
        mapdl.sfe("all", 2, "pres", "", pressure)

        # Constrain bottom of cylinder/rod
        mapdl.asel("s", "loc", "z", 0)
        mapdl.nsla("s", 1)

        mapdl.d("all", "all")
        mapdl.allsel()
        mapdl.psf("pres", "", 2)
        mapdl.pbc("u", 1)
        mapdl.solve()
        mapdl.finish()

        # access results using MAPDL object
        result = mapdl.result

        # to access the results you could have run:
        # from ansys.mapdl import reader as pymapdl_reader
        # resultfile = os.path.join(mapdl.path, '%s.rst' % mapdl.jobname)
        # result = pymapdl_reader.read_binary(result file)

        # Get maximum von Mises stress at result 1
        # Index 0 as it's zero based indexing
        nodenum, stress = result.principal_nodal_stress(0)

        # von Mises stress is the last column
        # must be nanmax as the shell element stress is not recorded
        maxstress = np.nanmax(stress[:, -1])

        # return number of nodes and max stress
        return nodenum.size, maxstress


    # initialize MAPDL
    mapdl = launch_mapdl(override=True, loglevel="ERROR")

    # call MAPDL to solve repeatedly
    result_summ = []
    for elemsize in np.linspace(0.6, 0.15, 15):
        # run the batch and report the results
        nnode, maxstress = cylinder_batch(elemsize, plot=False)
        result_summ.append([nnode, maxstress])
        print(
            "Element size %f: %6d nodes and maximum vom Mises stress %f"
            % (elemsize, nnode, maxstress)
        )

    # Exit MAPDL
    mapdl.exit()

Here is the output from the script:

.. code:: output

    Element size 0.600000:   9657 nodes and maximum vom Mises stress 142.623505
    Element size 0.567857:  10213 nodes and maximum vom Mises stress 142.697800
    Element size 0.535714:  10769 nodes and maximum vom Mises stress 142.766510
    Element size 0.503571:  14177 nodes and maximum vom Mises stress 142.585388
    Element size 0.471429:  18371 nodes and maximum vom Mises stress 142.825684
    Element size 0.439286:  19724 nodes and maximum vom Mises stress 142.841202
    Element size 0.407143:  21412 nodes and maximum vom Mises stress 142.945984
    Element size 0.375000:  33502 nodes and maximum vom Mises stress 142.913437
    Element size 0.342857:  37877 nodes and maximum vom Mises stress 143.033401
    Element size 0.310714:  59432 nodes and maximum vom Mises stress 143.328842
    Element size 0.278571:  69106 nodes and maximum vom Mises stress 143.176086
    Element size 0.246429: 110547 nodes and maximum vom Mises stress 143.499329
    Element size 0.214286: 142496 nodes and maximum vom Mises stress 143.559128
    Element size 0.182143: 211966 nodes and maximum vom Mises stress 143.953430
    Element size 0.150000: 412324 nodes and maximum vom Mises stress 144.275406


Chain commands in MAPDL
=======================

MAPDL permits several commands on one line by using the separation
character ``"$"``. This can be utilized within PyMAPDL to effectively
chain several commands together and send them to MAPDL for execution
rather than executing them individually. Chaining commands can be helpful
when you need to execute thousands of commands in a Python
loop and don't need the individual results for each command. For
example, if you want to create 1000 key points along the X axis, you
would run:

.. code:: python

    xloc = np.linspace(0, 1, 1000)
    for x in xloc:
        mapdl.k(x=x)


However, because each command executes individually and returns a
response, it is much faster to send the commands to be executed by
MAPDL in groups and have the :class:`Mapdl
<ansys.mapdl.core.mapdl.MapdlBase>` class handle grouping the commands by
using the :attr:`Mapdl.chain_commands <ansys.mapdl.core.Mapdl.chain_commands>` attribute.

.. code:: python

    xloc = np.linspace(0, 1, 1000)
    with mapdl.chain_commands:
        for x in xloc:
            mapdl.k(x=x)

The execution time using this approach is generally 4 to 10 times faster than running
each command individually. You can then view the final response of
the chained commands with the
:attr:`Mapdl.last_response <ansys.mapdl.core.Mapdl.last_response>` attribute.

.. note::
   Command chaining is not supported in distributed MAPDL.  To improve
   performances, use the ``mute=True`` or 
   :attr:`Mapdl.non_interactive <ansys.mapdl.core.Mapdl.non_interactive>`
   context manager.


Sending arrays to MAPDL
=======================
You can send ``numpy`` arrays or Python lists directly to MAPDL using
the :attr:`Mapdl.Parameters <ansys.mapdl.core.Mapdl.parameters>` attribute.
This is far more efficient than individually sending parameters to
MAPDL through Python with the :func:`Mapdl.run()
<ansys.mapdl.core.Mapdl.run>` method because it uses the :func:`Mapdl.vread()
<ansys.mapdl.core._commands.ParameterDefinition>` method behind the scenes.

.. code:: python

    from ansys.mapdl.core import launch_mapdl
    import numpy as np

    mapdl = launch_mapdl()
    arr = np.random.random((5, 3))
    mapdl.parameters["MYARR"] = arr

Verify that the data has been properly loaded to MAPDL by indexing the
:attr:`Mapdl.Parameters <ansys.mapdl.core.Mapdl.parameters>` attribute as if it
was a Python dictionary:

.. code:: pycon

   >>> array_from_mapdl = mapdl.parameters["MYARR"]
   >>> array_from_mapdl
   array([[0.65516567, 0.96977939, 0.3224993 ],
          [0.58634927, 0.84392263, 0.18152529],
          [0.76719759, 0.45748876, 0.56432361],
          [0.78548338, 0.01042177, 0.57420062],
          [0.33189362, 0.9681039 , 0.47525875]])


Download a remote MAPDL file
----------------------------
When running MAPDL in gRPC mode, remote MAPDL files can be listed and
downloaded using the :class:`Mapdl <ansys.mapdl.core.mapdl.MapdlBase>`
class with the :func:`Mapdl.download() <ansys.mapdl.core.mapdl_grpc.MapdlGrpc.download>`
function. For example, the following code lists the remote files and downloads one of them:

.. code:: python

    remote_files = mapdl.list_files()

    # ensure the result file is one of the remote files
    assert "file.rst" in remote_files

    # download the remote result file
    mapdl.download("file.rst")

.. note::

   This feature is only available in MAPDL 2021 R1 and later.

Alternatively, you can download several files at once using the glob pattern 
or a list of file names in the :func:`Mapdl.download() <ansys.mapdl.core.mapdl_grpc.MapdlGrpc.download>`
method:

.. code:: python

    # Using a list of file names
    mapdl.download(["file0.log", "file1.out"])

    # Using glob pattern to match the list_files
    mapdl.download("file*")

You can also download all files in the MAPDL working directory
(:func:`Mapdl.directory <ansys.mapdl.core.Mapdl.directory>`) using
this function:

.. code:: python

    mapdl.download_project()

Or, filter by extensions as shown in this example:

.. code:: python

    mapdl.download_project(
        ["log", "out"], target_dir="myfiles"
    )  # Download the files to 'myfiles' directory


Upload a local MAPDL file
-------------------------
You can upload a local MAPDL file as the remote MAPDL instance with the
:func:`Mapdl.upload() <ansys.mapdl.core.mapdl_grpc.MapdlGrpc.upload>` method:

.. code:: python

    # upload a local file
    mapdl.upload("sample.db")

    # ensure the uploaded file is one of the remote files
    remote_files = mapdl.list_files()
    assert "sample.db" in remote_files

.. note::

   This feature is only available in MAPDL 2021 R1 and later.


Unsupported MAPDL commands and other considerations
===================================================
Most MAPDL commands have been mapped Pythonically into their
equivalent methods. Some commands, however, are not supported
because either they are not applicable to an interactive session or they require
additional commands that are incompatible with the way inputs are
handled on the MAPDL server.


.. _ref_unsupported_commands:

Unavailable commands
--------------------
Some commands are unavailable in PyMAPDL for a variety of reasons.

Some of these commands do not make sense in a Python context.
Here are some examples:

- The ``*ASK`` command can be replaced with a Python ``input``.
- The ``*IF`` command can be replaced with a Python ``if`` statement.
- The ``*CREATE`` and ``*USE`` commands can be replaced with calls to another Python function or module.

Other commands do not make sense in a non-GUI session. For example, the ``/ERASE``
and ``ERASE`` commands that clear the graphics screen are not needed in a non-GUI session.

Other commands are quietly ignored by MAPDL, but you can still
use them. For example, the ``/BATCH`` command can be run using the
:func:`mapdl.run("/BATCH") <ansys.mapdl.core.Mapdl.run>` method,
which returns the following warning:

.. code:: output

    *** WARNING ***                         CP =       0.519   TIME= 12:04:16
    The /BATCH command must be the first line of input.  The /BATCH command
    is ignored.



Table-1_ Comprehensive information on commands that are unavailable

.. _Table-1:

**Table 1. Non-available commands.**

.. table:: 
  :class: longtable

  +---------------------------+-------------------+------------------------+-----------------------------------------+----------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------+
  |                           | MAPDL command     | Interactive            | Non-interactive                         | Direct run                                   | Notes                                                                                                                                                   |
  +===========================+===================+========================+=========================================+==============================================+=========================================================================================================================================================+
  | **GUI commands**          | * ``*ASK``        | |:x:| Not available    | |:x:| Not available                     | |:white_check_mark:| Works                   | When used in :func:`mapdl.run() <ansys.mapdl.core.Mapdl.run>` it automatically assumes the user input is 0. Use Python ``input`` instead.               |
  |                           +-------------------+------------------------+-----------------------------------------+----------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------+
  |                           | * ``*VEDIT``      | |:x:| Not available    | |:x:| Not available                     | |:exclamation:| MAPDL shows a warning        | It requires a GUI session to work.                                                                                                                      |
  |                           +-------------------+------------------------+-----------------------------------------+----------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------+
  |                           | * ``/ERASE``      | |:x:| Not available    | |:x:| Not available                     | |:white_check_mark:| Works                   | It does not make sense in a non-GUI session.                                                                                                            |
  |                           +-------------------+------------------------+-----------------------------------------+----------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------+
  |                           | * ``ERASE``       | |:x:| Not available    | |:x:| Not available                     | |:exclamation:| MAPDL shows a warning        | It does not make sense in a non-GUI session.                                                                                                            |
  |                           +-------------------+------------------------+-----------------------------------------+----------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------+
  |                           | * ``HELP``        | |:x:| Not available    | |:x:| Not available                     | |:exclamation:| Ignored by MAPDL             | It requires a GUI session to work.                                                                                                                      |
  |                           +-------------------+------------------------+-----------------------------------------+----------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------+
  |                           | * ``HELPDISP``    | |:x:| Not available    | |:x:| Not available                     | |:exclamation:| Ignored by MAPDL             | It requires a GUI session to work.                                                                                                                      |
  |                           +-------------------+------------------------+-----------------------------------------+----------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------+
  |                           | * ``NOERASE``     | |:x:| Not available    | |:x:| Not available                     | |:white_check_mark:| Works                   | It does not make sense in a non-GUI session.                                                                                                            |
  +---------------------------+-------------------+------------------------+-----------------------------------------+----------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------+
  | **Control flow commands** | * ``*CYCLE``      | |:x:| Not available    | |:x:| Not available                     | |:white_check_mark:| Works                   | It is recommended to use Python control flow keywords, in this case ``continue``.                                                                       |
  |                           +-------------------+------------------------+-----------------------------------------+----------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------+
  |                           | * ``*DO``         | |:x:| Not available    | |:x:| Not available                     | |:white_check_mark:| Works                   | It is recommended to use Python control flow keywords, in this case ``for``.                                                                            |
  |                           +-------------------+------------------------+-----------------------------------------+----------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------+
  |                           | * ``*DOWHILE``    | |:x:| Not available    | |:x:| Not available                     | |:white_check_mark:| Works                   | It is recommended to use Python control flow keywords, in this case ``while``.                                                                          |
  |                           +-------------------+------------------------+-----------------------------------------+----------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------+
  |                           | * ``*ELSE``       | |:x:| Not available    | |:x:| Not available                     | |:white_check_mark:| Works                   | It is recommended to use Python control flow keywords, in this case ``else``.                                                                           |
  |                           +-------------------+------------------------+-----------------------------------------+----------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------+
  |                           | * ``*ELSEIF``     | |:x:| Not available    | |:x:| Not available                     | |:white_check_mark:| Works                   | It is recommended to use Python control flow keywords, in this case ``elif``.                                                                           |
  |                           +-------------------+------------------------+-----------------------------------------+----------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------+
  |                           | * ``*ENDDO``      | |:x:| Not available    | |:x:| Not available                     | |:white_check_mark:| Works                   | It is recommended to use Python control flow keywords.                                                                                                  |
  |                           +-------------------+------------------------+-----------------------------------------+----------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------+
  |                           | * ``*GO``         | |:x:| Not available    | |:x:| Not available                     | |:white_check_mark:| Works                   | It is recommended to use Python control flow keywords, such as ``if`` or functions.                                                                     |
  |                           +-------------------+------------------------+-----------------------------------------+----------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------+
  |                           | * ``*IF``         | |:x:| Not available    | |:x:| Not available                     | |:white_check_mark:| Works                   | It is recommended to use Python control flow keywords, in this case ``continue``.                                                                       |
  |                           +-------------------+------------------------+-----------------------------------------+----------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------+
  |                           | * ``*REPEAT``     | |:x:| Not available    | |:x:| Not available                     | |:white_check_mark:| Works                   | It is recommended to use Python control flow keywords such as ``for`` or ``while``                                                                      |
  |                           +-------------------+------------------------+-----------------------------------------+----------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------+
  |                           | * ``*RETURN``     | |:x:| Not available    | |:x:| Not available                     | |:white_check_mark:| Works                   | It is recommended to use Python control flow keywords such as ``break``, ``continue`` or ``return``                                                     |
  +---------------------------+-------------------+------------------------+-----------------------------------------+----------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------+
  | **Others commands**       | * ``*DEL``        | |:x:| Not available    | |:x:| Not available                     | |:white_check_mark:| Works                   | It is recommended to use Python variables (use Python memory) instead of MAPDL variables.                                                               |
  |                           +-------------------+------------------------+-----------------------------------------+----------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------+
  |                           | * ``/BATCH``      | |:x:| Not available    | |:x:| Not available                     | |:exclamation:| Ignored by MAPDL.            | It does not make sense in a PyMAPDL session.                                                                                                            |
  |                           +-------------------+------------------------+-----------------------------------------+----------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------+
  |                           | * ``/EOF``        | |:x:| Not available    | |:x:| Not available                     | |:x:| PyMAPDL shows an exception             | To stop the server, use :func:`mapdl.exit() <ansys.mapdl.core.Mapdl.exit>`                                                                              |
  |                           +-------------------+------------------------+-----------------------------------------+----------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------+
  |                           | * ``UNDO``        | |:x:| Not available    | |:x:| Not available                     | |:exclamation:| MAPDL shows a warning        | It does not undo any command.                                                                                                                           |
  +---------------------------+-------------------+------------------------+-----------------------------------------+----------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------+


.. note::
    * **Interactive** means there is a method in MAPDL, such as the
      :func:`Mapdl.prep7() <ansys.mapdl.core.Mapdl.prep7>` method.
    * **Non-interactive** means it is run inside a 
      :attr:`Mapdl.non_interactive <ansys.mapdl.core.Mapdl.non_interactive>` context block,
      the :func:`Mapdl.input() <ansys.mapdl.core.Mapdl.input>` method, or
      the :func:`Mapdl.input_strings() <ansys.mapdl.core.Mapdl.input_strings>` method.
      For example:

      .. code:: python

          with mapdl.non_interactive:
              mapdl.prep7()

    * **Direct run** means that the :func:`mapdl.run() <ansys.mapdl.core.Mapdl.run>` 
      method is used to run the MAPDL command.
      An example is the :func:`mapdl.run("/PREP7") <ansys.mapdl.core.Mapdl.run>` method.


Note that running these commands with the
:func:`mapdl.run() <ansys.mapdl.core.Mapdl.run>` method does
not cause MAPDL to exit. However, it might raise exceptions.

These MAPDL commands can also be executed using the
:func:`mapdl.input() <ansys.mapdl.core.Mapdl.input>` method
or the
:func:`mapdl.input_strings() <ansys.mapdl.core.Mapdl.input_strings>`
method. The results should be same as running them in a normal batch MAPDL session.


.. _ref_unsupported_interactive_commands:

Unsupported "interactive" commands
----------------------------------

The following commands can be only run in non-interactive mode (inside a
:attr:`Mapdl.non_interactive <ansys.mapdl.core.Mapdl.non_interactive>` block or
using the :func:`mapdl.input() <ansys.mapdl.core.Mapdl.input>` method).

Table-2_ provides comprehensive information on the "interactive" commands that
are unsupported.


.. _Table-2:

**Table 2. Non-interactive only commands.**

+---------------+---------------------------------------------------------------------------------------------------------------------------------+----------------------------------+----------------------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------+
|               | Interactive                                                                                                                     | Non-interactive                  | Direct Run                                                                                                           | Notes                                                                                               |
+===============+=================================================================================================================================+==================================+======================================================================================================================+=====================================================================================================+
| * ``*CREATE`` | |:x:| Not available                                                                                                             | |:white_check_mark:| Available   | |:exclamation:| Only in :attr:`Mapdl.non_interactive <ansys.mapdl.core.Mapdl.non_interactive>`                       | It is recommended to create Python functions instead.                                               |
+---------------+---------------------------------------------------------------------------------------------------------------------------------+----------------------------------+----------------------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------+
| * ``CFOPEN``  | |:x:| Not available                                                                                                             | |:white_check_mark:| Available   | |:exclamation:| Only in :attr:`Mapdl.non_interactive <ansys.mapdl.core.Mapdl.non_interactive>`                       | It is recommended to use Python functions such as ``open``.                                         |
+---------------+---------------------------------------------------------------------------------------------------------------------------------+----------------------------------+----------------------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------+
| * ``CFCLOSE`` | |:x:| Not available                                                                                                             | |:white_check_mark:| Available   | |:exclamation:| Only in :attr:`Mapdl.non_interactive <ansys.mapdl.core.Mapdl.non_interactive>`                       | It is recommended to use Python functions such as ``open``.                                         |
+---------------+---------------------------------------------------------------------------------------------------------------------------------+----------------------------------+----------------------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------+
| * ``*VWRITE`` | |:x:| Not available                                                                                                             | |:white_check_mark:| Available   | |:exclamation:| Only in :attr:`Mapdl.non_interactive <ansys.mapdl.core.Mapdl.non_interactive>`                       | If you are working in a local session, it is recommended you use Python function such as ``open``.  |
+---------------+---------------------------------------------------------------------------------------------------------------------------------+----------------------------------+----------------------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------+
| * ``*MWRITE`` | |:x:| Not available                                                                                                             | |:white_check_mark:| Available   | |:exclamation:| Only in :attr:`Mapdl.non_interactive <ansys.mapdl.core.Mapdl.non_interactive>`                       | If you are working in a local session, it is recommended you use Python function such as ``open``.  |
+---------------+---------------------------------------------------------------------------------------------------------------------------------+----------------------------------+----------------------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------+
| * ``LSWRITE`` | |:white_check_mark:| Available (Internally running in :attr:`Mapdl.non_interactive <ansys.mapdl.core.Mapdl.non_interactive>`)   | |:white_check_mark:| Available   | |:exclamation:| Only in :attr:`Mapdl.non_interactive <ansys.mapdl.core.Mapdl.non_interactive>`                       |                                                                                                     |
+---------------+---------------------------------------------------------------------------------------------------------------------------------+----------------------------------+----------------------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------+

.. _ref_environment_variables:

Environment variables
=====================

There are several PyMAPDL-specific environment variables that can be
used to control the default behavior of PyMAPDL or launching MAPDL.

These environment variables do not have
priority over the arguments given in the corresponding functions.
Consider this command:

.. code-block:: console
    
    user@machine:~$ export PYMAPDL_PORT=50052
    user@machine:~$ python -c "from ansys.mapdl.core import launch_mapdl; mapdl=launch_mapdl(port=60053)"

This command launches an MAPDL instance on port 60053
because the ``port`` argument has priority over the :envvar:`PYMAPDL_PORT`
environment variable. The following table describes all arguments.


+---------------------------------------+----------------------------------------------------------------------------------+
| :envvar:`PYMAPDL_START_INSTANCE`      | Override the behavior of the                                                     |
|                                       | :func:`ansys.mapdl.core.launcher.launch_mapdl` function                          |
|                                       | to only attempt to connect to existing                                           |
|                                       | instances of PyMAPDL. Generally used                                             |
|                                       | in combination with ``PYMAPDL_PORT``.                                            |
|                                       |                                                                                  |
|                                       | **Example:**                                                                     |
|                                       |                                                                                  |
|                                       | .. code-block:: console                                                          |
|                                       |                                                                                  |
|                                       |    user@machine:~$ export PYMAPDL_START_INSTANCE=True                            |
|                                       |                                                                                  |
+---------------------------------------+----------------------------------------------------------------------------------+
| :envvar:`PYMAPDL_PORT`                | Default port for PyMAPDL to connect to.                                          |
|                                       |                                                                                  |
|                                       | **Example:**                                                                     |
|                                       |                                                                                  |
|                                       | .. code-block:: console                                                          |
|                                       |                                                                                  |
|                                       |    user@machine:~$ export PYMAPDL_PORT=50052                                     |
|                                       |                                                                                  |
+---------------------------------------+----------------------------------------------------------------------------------+
| :envvar:`PYMAPDL_IP`                  | Default IP for PyMAPDL to connect to.                                            |
|                                       |                                                                                  |
|                                       | **Example:**                                                                     |
|                                       |                                                                                  |
|                                       | .. code-block:: console                                                          |
|                                       |                                                                                  |
|                                       |    user@machine:~$ export PYMAPDL_IP=123.45.67.89                                |
|                                       |                                                                                  |
+---------------------------------------+----------------------------------------------------------------------------------+
| :envvar:`PYMAPDL_NPROC`               | Default number of cores for MAPDL to use.                                        |
|                                       |                                                                                  |
|                                       | **Example:**                                                                     |
|                                       |                                                                                  |
|                                       | .. code-block:: console                                                          |
|                                       |                                                                                  |
|                                       |    user@machine:~$ export PYMAPDL_NPROC=10                                       |
|                                       |                                                                                  |
+---------------------------------------+----------------------------------------------------------------------------------+
| :envvar:`ANSYSLMD_LICENSE_FILE`       | License file or IP address with port in the format                               |
|                                       | ``PORT@IP``. Do not confuse with the ``IP`` and                                  |
|                                       | ``PORT`` where the MAPDL instance is running, which                              |
|                                       | are specified using :envvar:`PYMAPDL_IP` and                                     |
|                                       | :envvar:`PYMAPDL_PORT`.                                                          |
|                                       | This is helpful for supplying licensing for                                      |
|                                       | Docker.                                                                          |
|                                       |                                                                                  |
|                                       | **Example:**                                                                     |
|                                       |                                                                                  |
|                                       | .. code-block:: console                                                          |
|                                       |                                                                                  |
|                                       |    user@machine:~$ export ANSYSLMD_LICENSE_FILE=1055@123.45.89                   |
|                                       |                                                                                  |
+---------------------------------------+----------------------------------------------------------------------------------+
| :envvar:`PYMAPDL_MAPDL_EXEC`          | Executable path from where to launch MAPDL                                       |
|                                       | instances.                                                                       |
|                                       |                                                                                  |
|                                       | **Example:**                                                                     |
|                                       |                                                                                  |
|                                       | .. code-block:: console                                                          |
|                                       |                                                                                  |
|                                       |    user@machine:~$ export PYMAPDL_MAPDL_EXEC=/ansys_inc/v241/ansys/bin/mapdl     |
|                                       |                                                                                  |
+---------------------------------------+----------------------------------------------------------------------------------+
| :envvar:`PYMAPDL_MAPDL_VERSION`       | Default MAPDL version to launch in case there                                    |
|                                       | are several versions availables.                                                 |
|                                       |                                                                                  |
|                                       | **Example:**                                                                     |
|                                       |                                                                                  |
|                                       | .. code-block:: console                                                          |
|                                       |                                                                                  |
|                                       |    user@machine:~$ export PYMAPDL_MAPDL_VERSION=22.2                             |
|                                       |                                                                                  |
+---------------------------------------+----------------------------------------------------------------------------------+
| :envvar:`PYMAPDL_RUNNING_ON_HPC`      | With this environment variable set to ``FALSE``, you can avoid                   |
|                                       | PyMAPDL from detecting that it is running on a SLURM HPC cluster.                |
+---------------------------------------+----------------------------------------------------------------------------------+
| :envvar:`PYMAPDL_MAX_MESSAGE_LENGTH`  | Maximum gRPC message length. If your                                             |
|                                       | connection terminates when running                                               |
|                                       | PRNSOL or NLIST, raise this. In bytes,                                           |
|                                       | defaults to 256 MB.                                                              |
|                                       |                                                                                  |
|                                       | Only for developing purposes.                                                    |
+---------------------------------------+----------------------------------------------------------------------------------+
