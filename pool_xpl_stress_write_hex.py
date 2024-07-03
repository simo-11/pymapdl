import time

import numpy as np

POOL = True
solve = True


if len(sys.argv) > 1:
    POOL = True
    n_pool = int(sys.argv[1])

    print(f"Using pool with {n_pool} instances.")

else:
    POOL = False
    print(f"Using launch_mapdl")

n_iterations = int(n_pool * 2.5)


exec_file = r"C:\Program Files\ANSYS Inc\v212\ansys\bin\winx64\ANSYS212.exe"
exec_file = r"C:\Program Files\ANSYS Inc\v222\ansys\bin\winx64\ANSYS222.exe"
# exec_file = r"C:\Program Files\ANSYS Inc\v241\ansys\bin\winx64\ANSYS241.exe"


esize = 10.0
length = 100.0
width = 100.0
depth = 100.0
numsteps = 1

global total_time
total_time = []


def solve_model(mapdl, arg=None):
    mapdl.clear()
    if solve:
        mapdl.fcomp("rst", 0)
        # Write all data in double precision
        mapdl.run("/config,resuprec,0")
        mapdl.prep7()
        mapdl.k(1, 0.0, 0.0, 0.0)
        mapdl.k(2, length, 0.0, 0.0)
        mapdl.k(3, length, width, 0.0)
        mapdl.k(4, 0.0, width, 0.0)
        mapdl.k(5, 0.0, 0.0, depth)
        mapdl.k(6, length, 0.0, depth)
        mapdl.k(7, length, width, depth)
        mapdl.k(8, 0.0, width, depth)
        mapdl.v(1, 2, 3, 4, 5, 6, 7, 8)

        mapdl.et(1, 186)
        mapdl.mp("ex", 1, 210000.0)
        mapdl.mp("prxy", 1, 0.3)
        mapdl.mp("kxx", 1e-6)

        mapdl.esize(esize)
        mapdl.mshape(0, "3D")
        mapdl.vmesh("all")
        mapdl.finish()

        mapdl.slashsolu()
        # For some reason - with d,all,all - "ENS" block doesn't appear in XPL
        mapdl.d("all", "ux", 2.0)
        mapdl.d("all", "uy", 2.0)
        mapdl.d("all", "uz", 2.0)
        mapdl.bf("all", "temp", 100.0)
        mapdl.time(1.0)
        mapdl.nsubst(numsteps, numsteps, numsteps)
        mapdl.outres("all", "none")
        mapdl.outres("strs", "all")
        mapdl.outres("epel", "all")
        mapdl.outres("eppl", "all")
        mapdl.outres("nsol", "all")
        mapdl.solve()
        mapdl.finish()

        mapdl.aux2()
        mapdl.combine("FULL")
        mapdl.finish()

    xpl = mapdl.xpl
    mm = mapdl.math

    t0 = time.time()
    xpl.open("dummy_solve.rst")

    header = xpl.read("HEADER", asarray=True)
    # print(header)
    num_nodes = header[1]
    num_elems = header[5]
    xpl.close()

    # Get internal Element order
    xpl.open("dummy_solve.rst")
    internal_elem_order = xpl.read("ELM", "ELEM_ORDER")
    xpl.close()

    stress = [float(id) for id in range(1, 2001)]

    all_time_steps = []

    def get_elem_stress(eid):
        return stress[eid - 1]

    t0 = time.time()
    for i in range(1, numsteps + 1):
        t_elem = 0.0
        for u_eid in range(1, num_elems + 1):
            # for index, eid in enumerate(internal_elem_order):
            i_eid = internal_elem_order[u_eid - 1]
            xpl.open(r"dummy_solve.rst", "WRIT")
            xpl.step(f"DSI::SET{i}::ESL::ELEM{u_eid}")
            t0_elem = time.time()
            stress_elem = get_elem_stress(i_eid)
            myvec = np.ones(48, dtype=np.float64) * float(i * stress_elem)
            mm.set_vec(myvec, "NEWVEC")
            xpl.write("ENS", "NEWVEC")
            t1_elem = time.time()
            t_elem = t1_elem - t0_elem
            all_time_steps.append(t_elem)
            xpl.up()
            xpl.close()

    t1 = time.time()

    print(f"Total Time {t1 - t0}")
    total_time.append(t1 - t0)


print(f"Pool: {POOL}")

if POOL:
    from ansys.mapdl.core import MapdlPool

    pool = MapdlPool(
        n_pool,
        port=[50052 + i for i in range(0, n_pool)],
        start_instance=True,
        exec_file=exec_file,
        jobname="dummy_solve",
        override=True,
        start_timeout=90,
        # loglevel="DEBUG"
    )

    print(f"\n\n\n\n\n\n{pool._root_dir}")

    full_0 = time.time()
    pool.map(func=solve_model, iterable=[None for each in range(n_iterations)])
    full_1 = time.time()
    pool.exit()

else:
    from ansys.mapdl.core import launch_mapdl

    model_path = r"C:\Users\gayuso\pymapdl\tmp\Ayush\pymapdl"
    mapdl = launch_mapdl(exec_file, jobname="dummy_solve", override=True)

    full_0 = time.time()

    for i in range(n_iterations):
        print(f"Solving {i} model.")
        solve_model(mapdl, None)

    full_1 = time.time()
    mapdl.exit()

print(f"Total time: {full_1-full_0}")
print(total_time)
