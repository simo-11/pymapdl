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


class Annotation:
    def an3d(self, kywrd="", key="", **kwargs):
        """Specifies 3-D annotation functions

        APDL Command: /AN3D

        Parameters
        ----------
        num
            Unique number assigned as each annotation is applied to a model.
            These numbers are applied sequentially, although when an annotation
            entity is deleted, its number is reassigned.

        type
            Annotation internal type number (101 = text, 102 = line, 103 =
            point, 104 = area, 105 = arrow, 106 = symbol, 108 = bitmap).

        xhot, yhot, zhot
            X, Y, Z coordinates for hot spot location.

        Notes
        -----
        Because 3-D annotation is applied in relation to the XYZ coordinates of
        the anchor, you can transform your model, and the annotation will
        maintain the spatial relationship with the model. This works within
        reason, and there are instances where changing the perspective or the
        size of the model will change the apparent relationship between the
        annotation and the model.

        The overall 3-D dimensions of your model are defined by a bounding
        box.  If portions of your model's bounding box lie outside of the
        visible area of your graphics window (if you are zoomed in on a
        specific area of your model), it can affect the placement of your 3-D
        annotations.  Zooming out will usually overcome this problem.

        3-D annotation is valid for the Cartesian (CSYS,0) coordinate system
        only. If you want to annotate a model you created in another coordinate
        system, use 2-D annotation (note that 2-D annotations do not remain
        anchored for dynamic rotations or transformations).

        When you apply user defined bitmaps, the size of the annotation can
        vary. Use the options menu of the 3-D annotation widget to adjust the
        size and placement of your bitmaps.

        You cannot use the "!" and "$" characters in ANSYS text annotation.

        The GUI generates this command during 3-D annotation operations and
        inserts the command into the log file (Jobname.LOG). You should NOT
        type this command directly during an ANSYS session (although the
        command can be included in an input file for batch input or for use
        with the /INPUT command).
        """
        command = f"/AN3D,{kywrd},{key}"
        return self.run(command, **kwargs)

    def annot(self, lab="", val1="", val2="", **kwargs):
        """Activates graphics for annotating displays (GUI).

        APDL Command: /ANNOT

        Parameters
        ----------
        lab
            Annotation control key:

            OFF
                Turns off annotation for each subsequent display (default).

            ON
                Turns on annotation for each subsequent display.

            DELE
                Deletes all annotation.

            SAVE
                Saves annotation on a file.  Use VAL1 for file name (defaults to Jobname) and
                VAL2 for the extension (defaults to ANO).

            SCALE
                Sets annotation scale factor (direct input only).  Use VAL1 for value (0.1 to
                10.0) (defaults to 1.0).

            XORIG
                Sets the annotation x origin (direct input only).  Use VAL1 for value (-3.0 to
                3.0).

            YORIG
                Sets annotation y origin (direct input only).  Use VAL1 for value (-3.0 to
                3.0).

            SNAP
                Sets annotation snap (menu button input only).  Use VAL1 for value (0.002 to
                0.2) (defaults to 0.002).

            STAT
                Displays current annotation status.

            DEFA
                Sets annotation specifications to the default values.

            REFR
                Redisplays annotation graphics.

            TMOD
                Sets the annotation text mode. If VAL1 = 1, annotation text will be drawn in
                scalable bitmap fonts (default). If VAL1 = 0, annotation
                text will be drawn with stroke text.

        val1
            Value (or file name) as noted with label above.

        val2
            Value (or file name extension) as noted with label above.

        Notes
        -----
        This is a command generated by the GUI and will appear in the log file
        (Jobname.LOG) if annotation is used.  This command is not intended to
        be typed in directly in an ANSYS session (although it can be included
        in an input file for batch input or for use with the /INPUT command).

        You cannot use the "!" and "$" characters in ANSYS text annotation.

        /ANNOT activates annotation graphics for adding annotation to displays.
        Commands representing the annotation instructions are automatically
        created by the annotation functions in the GUI and written to
        Jobname.LOG.  The annotation commands are /ANNOT, /ANUM, /TLABEL,
        /LINE, /LARC, /LSYMBOL, /POLYGON, /PMORE, /PCIRCLE, /PWEDGE, /TSPEC,
        /LSPEC, and /PSPEC.  Annotation graphics are relative to the full
        Graphics Window and are not affected by ANSYS window-specific commands
        (/WINDOW, /VIEW, etc.).

        This command is valid in any processor.
        """
        command = f"/ANNOT,{lab},{val1},{val2}"
        return self.run(command, **kwargs)

    def anum(self, num="", type_="", xhot="", yhot="", **kwargs):
        """Specifies the annotation number, type, and hot spot (GUI).

        APDL Command: /ANUM

        Parameters
        ----------
        num
            Annotation number.  ANSYS automatically assigns the lowest
            available number.  You cannot assign a higher number if a lower
            number is available; ANSYS will substitute the lowest available
            number in place of any user-specified higher number.

        type\\_
            Annotation internal type number.  If TYPE = DELE, delete annotation
            NUM.

            1
                Text

            2
                Block text (not available in GUI)

            3
                Dimensions

            4
                Lines

            5
                Rectangles

            6
                Circles

            7
                Polygons

            8
                Arcs

            9
                Wedges, pies

            11
                Symbols

            12
                Arrows

            13
                Bitmap

        xhot
            X hot spot (-1.0 < X < 2.0).  Used for menu button item delete.

        yhot
            Y hot spot (-1.0 < Y < 1.0).  Used for menu button item delete.

        Notes
        -----
        This is a command generated by the GUI and will appear in the log file
        (Jobname.LOG) if annotation is used.  This command is not intended to
        be typed in directly in an ANSYS session (although it can be included
        in an input file for batch input or for use with the /INPUT command).

        Type 13 (bitmap) annotation applies user defined bitmaps defined using
        the FILE option of the /TXTRE command.

        This command is valid in any processor.
        """
        command = f"/ANUM,{num},{type_},{xhot},{yhot}"
        return self.run(command, **kwargs)

    def slashlarc(self, xcentr="", ycentr="", xlrad="", angle1="", angle2="", **kwargs):
        """Creates annotation arcs (GUI).

        APDL Command: /LARC

        Parameters
        ----------
        xcentr
            Arc X center location (-1.0 < X < 1.0).

        ycentr
            Arc Y center location (-1.0 < Y < 1.0).

        xlrad
            Arc radius length.

        angle1
            Starting angle of arc.

        angle2
            Ending angle of arc. The arc is drawn counterclockwise from the
            starting angle, `angle1`, to the ending angle, `angle2`.

        Notes
        -----
        This command defines annotation arcs to be written directly onto the
        display at a specified location. The command is generated by the Graphical
        User Interface (GUI) and will appear in the log file (`Jobname.LOG`) if
        annotation is used. It is not intended to be typed in directly in a
        Mechanical APDL session (although it can be included in an input file
        for batch input or for use with the `/INPUT` command).
        All arcs are shown on subsequent displays unless the annotation is
        turned off or deleted. Issueu `/LSPEC` to set the attributes
        of the arc.

        This command is valid in any processor.
        """
        command = f"/LARC, {xcentr}, {ycentr}, {xlrad}, {angle1}, {angle2}"
        return self.run(command, **kwargs)

    def slashline(self, x1="", y1="", x2="", y2="", **kwargs):
        """Creates annotation lines (GUI).

        APDL Command: /LINE

        Parameters
        ----------
        X1
            Line X starting location (-1.0 < X < 2.0).
        Y1
            Line Y starting location (-1.0 < Y < 1.0).
        X2
            Line X ending location (-1.0 < X < 2.0).
        Y2
            Line Y ending location (-1.0 < Y < 1.0).

        Notes
        -----
        This command defines annotation lines to be written directly onto the
        display at a specified location. The command is generated by the Graphical
        User Interface (GUI) and appears in the log file (`Job-name.LOG`) if
        annotation is used. It is not intended to be typed in directly in a
        Mechanical APDL session (although it can be included in an input file
        for batch input or for use with the `/INPUT` command). All lines are
        shown on subsequent displays unless the annotation is turned off or
        deleted. Issue `/LSPEC` to set the attributes of the line.

        This command is valid in any processor.
        """
        command = f"/LINE, {x1}, {y1}, {x2}, {y2}"
        return self.run(command, **kwargs)

    def lspec(self, lcolor="", linstl="", xlnwid="", **kwargs):
        """Specifies annotation line attributes (GUI).

        APDL Command: /LSPEC

        Parameters
        ----------
        lcolor
            Line color:

            0
                Black

            1
                Red-Magenta

            2
                Magenta

            3
                Blue-Magenta

            4
                Blue

            5
                Cyan-Blue

            6
                Cyan

            7
                Green-Cyan

            8
                Green

            9
                Yellow-Green

            10
                Yellow

            11
                Orange

            12
                Red

            13
                Dark Gray

            14
                Light Gray

            15
                White

        linstl
            Line style:

            0
                Solid line.

            1
                Dashed line.

        xlnwid
            Line width multiplier (1.0 to 20.0).  Defaults to 1.0.

        Notes
        -----
        Specifies annotation line attributes to control certain characteristics
        of the lines created via the /LINE, /LARC, /LSYMBOL, /POLYGON, /PMORE,
        /PCIRCLE, and /PWEDGE commands.  This is a command generated by the
        Graphical User Interface (GUI) and will appear in the log file
        (Jobname.LOG) if annotation is used.  This command is not intended to
        be typed in directly in an ANSYS session (although it can be included
        in an input file for batch input or for use with the /INPUT command).

        This command is valid in any processor.
        """
        command = f"/LSPEC,{lcolor},{linstl},{xlnwid}"
        return self.run(command, **kwargs)

    def lsymbol(self, x="", y="", symang="", symtyp="", symsiz="", keybmp="", **kwargs):
        """Creates annotation symbols (GUI).

        APDL Command: /LSYMBOL

        Parameters
        ----------
        x
            X location for symbol (-1.0 < X < 2.0).

        y
            Y location for symbol (-1.0 < Y < 1.0).

        symang
            Symbol orientation angle.

        symtyp
            Symbol type:

            1
                Arrow.

            2
                Tee.

            3
                Circle.

            4
                Triangle.

            5
                Star.

        symsiz
            Symbol size multiplier (0.1 to 20.0).  Defaults to 1.0.

        keybmp
            If KEYBMP = 1, the annotation is a bitmap. SYMTYP will then be a
            number from 1-99, indicating the bitmap type (see notes), and X and
            Y will define the lower left corner of the bitmap. The SYMANG,
            SYMSIZarguments are ignored. If KEYBMP = 0, or blank, then the
            argument definitions above apply.

        Notes
        -----
        Defines annotation symbols to be written directly onto the display at a
        specified location.  This is a command generated by the GUI and will
        appear in the log file (Jobname.LOG) if annotation is used.  This
        command is not intended to be typed in directly in an ANSYS session
        (although it can be included in an input file for batch input or for
        use with the /INPUT command).

        All symbols are shown on subsequent displays unless the annotation is
        turned off or deleted.  Use the /LSPEC command to set the attributes of
        the symbol.

        The KEYBMP argument reads the symtype argument to determine which
        bitmap to insert. This bitmap is defined by an integer between 1 and
        99. Numbers 1 through 40 correspond to the standard texture values
        found in the /TXTRE  command, while numbers 51 through 99 correspond to
        user supplied bitmaps, as defined using the Filename option of the
        /TXTRE command. Numbers 51 through 57 are predefined (the logos, clamps
        and arrows available from the GUI) but can be overridden. Numbers 41
        through 50 are reserved.

        This command is valid in any processor.
        """
        command = f"/LSYMBOL,{x},{y},{symang},{symtyp},{symsiz},{keybmp}"
        return self.run(command, **kwargs)

    def slash_pcircle(self, xcentr="", ycentr="", xlrad="", **kwargs):
        """Creates an annotation circle (GUI).

        APDL Command: /PCIRCLE

        Parameters
        ----------
        xcentr
            Circle X center location (-1.0 < X < 2.0).

        ycentr
            Circle Y center location (-1.0 < Y < 1.0).

        xlrad
            Circle radius length.

        Notes
        -----
        Creates an annotation circle to be written directly onto the display at
        a specified location.  This is a command generated by the Graphical
        User Interface (GUI) and will appear in the log file (Jobname.LOG) if
        annotation is used.  This command is not intended to be typed in
        directly in an ANSYS session (although it can be included in an input
        file for batch input or for use with the /INPUT command).

        All circles are shown on subsequent displays unless the annotation is
        turned off or deleted.  Use the /LSPEC and the /PSPEC command to set
        the attributes of the circle.

        This command is valid in any processor.
        """
        command = f"/PCIRCLE,{xcentr},{ycentr},{xlrad}"
        return self.run(command, **kwargs)

    def pmore(self, x5="", y5="", x6="", y6="", x7="", y7="", x8="", y8="", **kwargs):
        """Creates an annotation polygon (GUI).

        APDL Command: /PMORE

        Parameters
        ----------
        x5
            X location for vertex 5 of polygon (-1.0 < X < 2.0).

        y5
            Y location for vertex 5 of polygon (-1.0 < Y < 1.0).

        x6
            X location for vertex 6 of polygon (-1.0 < X < 2.0).

        y6
            Y location for vertex 6 of polygon (-1.0 < Y < 1.0).

        x7
            X location for vertex 7 of polygon (-1.0 < X < 2.0).

        y7
            Y location for vertex 7 of polygon (-1.0 < Y < 1.0).

        x8
            X location for vertex 8 of polygon (-1.0 < X < 2.0).

        y8
            Y location for vertex 8 of polygon (-1.0 < Y < 1.0).

        Notes
        -----
        Defines the 5th through 8th vertices of an annotation polygon
        [/POLYGON].  This is a command generated by the Graphical User
        Interface (GUI) and will appear in the log file (Jobname.LOG) if
        annotation is used.  This command is not intended to be typed in
        directly in an ANSYS session (although it can be included in an input
        file for batch input or for use with the /INPUT command).

        This command is valid in any processor.
        """
        command = f"/PMORE,,{x5},{y5},{x6},{y6},{x7},{y7},{x8},{y8}"
        return self.run(command, **kwargs)

    def polygon(
        self,
        nvert="",
        x1="",
        y1="",
        x2="",
        y2="",
        x3="",
        y3="",
        x4="",
        y4="",
        **kwargs,
    ):
        """Creates annotation polygons (GUI).

        APDL Command: /POLYGON

        Parameters
        ----------
        nvert
            Number of vertices of polygon (3  NVERT   8).  Use /PMORE for
            polygons with more than 4 vertices.

        x1
            X location for vertex 1 of polygon (-1.0 < X < 2.0).

        y1
            Y location for vertex 1 of polygon (-1.0 < Y < 1.0).

        x2
            X location for vertex 2 of polygon (-1.0 < X < 2.0).

        y2
            Y location for vertex 2 of polygon (-1.0 < Y < 1.0).

        x3
            X location for vertex 3 of polygon (-1.0 < X < 2.0).

        y3
            Y location for vertex 3 of polygon (-1.0 < Y < 1.0).

        x4
            X location for vertex 4 of polygon (-1.0 < X < 2.0).

        y4
            Y location for vertex 4 of polygon (-1.0 < Y < 1.0).

        Notes
        -----
        Creates annotation polygons to be written directly onto the display at
        a specified location.  This is a command generated by the Graphical
        User Interface (GUI) and will appear in the log file (Jobname.LOG) if
        annotation is used.  This command is not intended to be typed in
        directly in an ANSYS session (although it can be included in an input
        file for batch input or for use with the /INPUT command).

        All polygons are shown on subsequent displays unless the annotation is
        turned off or deleted.  Use the /LSPEC and the /PSPEC command to set
        the attributes of the polygon.  Use the /PMORE command to define the
        5th through 8th vertices of the polygon.

        This command is valid in any processor.
        """
        command = f"/POLYGON,{nvert},{x1},{y1},{x2},{y2},{x3},{y3},{x4},{y4}"
        return self.run(command, **kwargs)

    def pspec(self, pcolor="", kfill="", kbordr="", **kwargs):
        """Creates annotation polygon attributes (GUI).

        APDL Command: /PSPEC

        Parameters
        ----------
        pcolor
            Polygon color (0  PCOLOR   15):

            0
                Black.

            1
                Red-Magenta.

            2
                Magenta.

            3
                Blue-Magenta.

            4
                Blue.

            5
                Cyan-Blue.

            6
                Cyan.

            7
                Green-Cyan.

            8
                Green.

            9
                Yellow-Green.

            10
                Yellow.

            11
                Orange.

            12
                Red.

            13
                Dark Gray.

            14
                Light Gray.

            15
                White.

        kfill
            Polygon fill key:

            0
                Hollow polygon.

            1
                Filled polygon.

        kbordr
            Polygon border key:

            0
                No border.

            1
                Border.

        Notes
        -----
        Creates annotation polygon attributes to control certain
        characteristics of the polygons created via the /POLYGON, /PMORE,
        /PCIRCLE and /PWEDGE commands.  This is a command generated by the
        Graphical User Interface (GUI) and will appear in the log file
        (Jobname.LOG) if annotation is used.  This command is not intended to
        be typed in directly in an ANSYS session (although it can be included
        in an input file for batch input or for use with the /INPUT command).

        This command is valid in any processor.
        """
        command = f"/PSPEC,{pcolor},{kfill},{kbordr}"
        return self.run(command, **kwargs)

    def pwedge(self, xcentr="", ycentr="", xlrad="", angle1="", angle2="", **kwargs):
        """Creates an annotation wedge (GUI).

        APDL Command: /PWEDGE

        Parameters
        ----------
        xcentr
            Wedge X center location (-1.0 < X < 2.0).

        ycentr
            Wedge Y center location (-1.0 < Y < 1.0).

        xlrad
            Wedge radius length.

        angle1
            Starting angle of wedge.

        angle2
            Ending angle of wedge.  The wedge is drawn counterclockwise from
            the starting angle, ANGLE1, to the ending angle, ANGLE2.

        Notes
        -----
        Creates an annotation wedge to be written directly onto the display at
        a specified location.  This is a command generated by the Graphical
        User Interface (GUI) and will appear in the log file (Jobname.LOG) if
        annotation is used.  This command is not intended to be typed in
        directly in an ANSYS session (although it can be included in an input
        file for batch input or for use with the /INPUT command).

        All wedges are shown on subsequent displays unless the annotation is
        turned off or deleted.  Use the /LSPEC and the /PSPEC command to set
        the attributes of the wedge.

        This command is valid in any processor.
        """
        command = f"/PWEDGE,{xcentr},{ycentr},{xlrad},{angle1},{angle2}"
        return self.run(command, **kwargs)

    def tlabel(self, xloc="", yloc="", text="", **kwargs):
        """Creates annotation text (GUI).

        APDL Command: /TLABEL

        Parameters
        ----------
        xloc
            Text X starting location (-1.0 < X < 1.6).

        yloc
            Text Y starting location (-1.0 < Y < 1.0).

        text
            Text string (60 characters maximum).  Parameter substitution may be
            forced within the text by enclosing the parameter name or
            parametric expression within percent (%) signs.

        Notes
        -----
        Defines annotation text to be written directly onto the display at a
        specified location.  This is a command generated by the Graphical User
        Interface (GUI) and will appear in the log file (Jobname.LOG) if
        annotation is used.  This command is not intended to be typed in
        directly in an ANSYS session (although it can be included in an input
        file for batch input or for use with the /INPUT command).

        All text is shown on subsequent displays unless the annotation is
        turned off or deleted.  Use the /TSPEC command to set the attributes of
        the text.

        This command is valid in any processor.
        """
        command = f"/TLABEL,{xloc},{yloc},{text}"
        return self.run(command, **kwargs)

    def tspec(self, tcolor="", tsize="", txthic="", pangle="", iangle="", **kwargs):
        """Creates annotation text attributes (GUI).

        APDL Command: /TSPEC

        Parameters
        ----------
        tcolor
            Text color (0  TCOLOR   15):

            0
                Black.

            1
                Red-Magenta.

            2
                Magenta.

            3
                Blue-Magenta.

            4
                Blue.

            5
                Cyan-Blue.

            6
                Cyan.

            7
                Green-Cyan.

            8
                Green.

            9
                Yellow-Green.

            10
                Yellow.

            11
                Orange.

            12
                Red.

            13
                Dark Gray.

            14
                Light Gray.

            15
                White.

        tsize
            Text size factor.

        txthic
            Text thickness key:

            1
                normal.

            2
                twice as thick.

            3
                three times as thick.

            4
                four times as thick.

        pangle
            Text path angle (0.0 < angle < 360.0).

        iangle
            Text italic angle (0.0 < angle < 45.0).

        Notes
        -----
        Defines annotation text attributes to control certain characteristics
        of the text created via the /TLABEL command.  This is a command
        generated by the Graphical User Interface (GUI) and will appear in the
        log file (Jobname.LOG) if annotation is used.  This command is not
        intended to be typed in directly in an ANSYS session (although it can
        be included in an input file for batch input or for use with the /INPUT
        command).

        This command is valid in any processor.
        """
        command = f"/TSPEC,{tcolor},{tsize},{txthic},{pangle},{iangle}"
        return self.run(command, **kwargs)
