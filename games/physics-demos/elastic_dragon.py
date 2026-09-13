import argparse
import numpy as np
import genesis as gs
from time import time

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--vis", action="store_true", default=True)
    parser.add_argument("-c", "--cpu", action="store_true", default=False)
    return parser.parse_args()

def run_sim(scene, steps):
    t_prev = time()
    for i in range(steps):
        scene.step()
        if i % 100 == 0:  # Print FPS every 100 steps
            t_now = time()
            print(f"Step {i + 1}/{steps} | {1 / (t_now - t_prev):.2f} FPS")
            t_prev = t_now

def main():
    args = parse_arguments()

    ########################## init ##########################
    gs.init(backend=gs.cpu if args.cpu else gs.gpu, logging_level="debug")

    ########################## create a scene ##########################
    scene = gs.Scene(
        sim_options=gs.options.SimOptions(
            substeps=10,
            gravity=(0, 0, -9.8),
        ),
        viewer_options=gs.options.ViewerOptions(
            camera_pos=(8, 8, 1.5),
            camera_lookat=(0, 0, 0.5),
            camera_up=(0, 0, 1),
        ),
        show_viewer=args.vis,
    )

    ########################## materials ##########################
    mat_elastic = gs.materials.PBD.Elastic()

    ########################## entities ##########################
    bunny = scene.add_entity(
        material=mat_elastic,
        morph=gs.morphs.Mesh(
            file="meshes/dragon/dragon.obj",
            scale=0.003,
            pos=(0, 0, 0.8),
        ),
        surface=gs.surfaces.Default(),
    )

    ########################## build ##########################
    scene.build()

    ########################## Run Simulation in Separate Thread ##########################
    horizon = 1000
    gs.tools.run_in_another_thread(
        fn=run_sim,
        args=(scene, horizon)
    )

    ########################## Start Viewer if Visualization Enabled ##########################
    if args.vis:
        scene.viewer.start()

if __name__ == "__main__":
    main()