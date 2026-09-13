import argparse
import torch
import genesis as gs
import numpy as np
from time import time
import math


def parse_arguments():
    parser = argparse.ArgumentParser(description="Run a Genesis simulation with fluid and robot.")
    parser.add_argument("-v", "--vis", action="store_true", default=True, help="Enable visualization.")
    parser.add_argument("--gravity", type=float, nargs=3, default=(0.0, 0.0, -10.0), help="Gravity vector.")
    parser.add_argument("--steps", type=int, default=2000, help="Number of simulation steps.")
    return parser.parse_args()


def run_sim(scene, enable_vis, steps):
    t_prev = time()

    # Add liquid simulation parameters
    scene.sim_options = gs.options.SimOptions(dt=2e-3)
    scene.pbd_options = gs.options.PBDOptions(
        lower_bound=(0.0, 0.0, 0.0),
        upper_bound=(1.0, 1.0, 1.0),
        max_density_solver_iterations=10,
        max_viscosity_solver_iterations=1,
    )

    for i in range(steps):
        scene.step()
        t_now = time()
        print(f"Step {i + 1}/{steps} | {1 / (t_now - t_prev):.2f} FPS")
        t_prev = t_now

    if enable_vis:
        scene.viewer.stop()


def main():
    args = parse_arguments()

    ########################## Init ##########################
    gs.init(backend=gs.cpu, seed=0, precision="32", logging_level="debug")

    ########################## Create a Scene ##########################
    scene = gs.Scene(
        sim_options=gs.options.SimOptions(),
        viewer_options=gs.options.ViewerOptions(
            # Adjusted camera position for better view
            camera_pos=(5.0, 2.0, 3.5),
            camera_lookat=(0.0, 0.0, 0.5),
            camera_fov=65,
        ),
        show_viewer=args.vis,
        rigid_options=gs.options.RigidOptions(
            dt=0.01,
            gravity=tuple(args.gravity),
        ),
        pbd_options=gs.options.PBDOptions(
            lower_bound=(0.0, 0.0, 0.0),
            upper_bound=(1.0, 1.0, 1.0),
            max_density_solver_iterations=10,
            max_viscosity_solver_iterations=1,
        ),
    )

    ########################## Entities ##########################
    # Add plane
    plane = scene.add_entity(gs.morphs.Plane())

    # Add robot
    r0 = scene.add_entity(gs.morphs.MJCF(file="xml/franka_emika_panda/panda.xml"))

    # Add liquid
    liquid = scene.add_entity(
        material=gs.materials.PBD.Liquid(
            rho=1.0,
            density_relaxation=1.0,
            viscosity_relaxation=0.2,
            sampler="regular",
        ),
        morph=gs.morphs.Box(
            lower=(0.2, 0.1, 0.1),
            upper=(0.4, 0.3, 0.5)
        ),
    )

    ########################## Build ##########################
    scene.build()

    ########################## Run Simulation in Separate Thread ##########################
    gs.tools.run_in_another_thread(
        fn=run_sim,
        args=(scene, args.vis, args.steps)
    )

    ########################## Start Viewer if Visualization Enabled ##########################
    if args.vis:
        scene.viewer.start()


if __name__ == "__main__":
    main()