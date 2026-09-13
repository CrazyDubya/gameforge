import genesis as gs
import argparse
gs.init()

scene = gs.Scene(
    show_viewer=True,
    viewer_options=gs.options.ViewerOptions(
        res=(1280, 960),
        camera_pos=(3.5, 0.0, 2.5),
        camera_lookat=(0.0, 0.0, 0.5),
        camera_fov=40,
        max_FPS=60,
    ),
    vis_options=gs.options.VisOptions(
        show_world_frame=True,
        world_frame_size=1.0,
        show_link_frame=False,
        show_cameras=False,
        plane_reflection=True,
        ambient_light=(0.1, 0.1, 0.1),
    ),
    # renderer=gs.renderers.RayTracer(),
    renderer=gs.renderers.Rasterizer(),
)

plane = scene.add_entity(
    gs.morphs.Plane(),
)
franka = scene.add_entity(
    gs.morphs.MJCF(file="xml/franka_emika_panda/panda.xml"),
)

cam = scene.add_camera(
    res=(640, 480),
    pos=(3.5, 0.0, 2.5),
    lookat=(0, 0, 0.5),
    fov=30,
    GUI=True,
)
def run_sim(scene, enable_vis):
    from time import time

    t_prev = time()
    i = 0
    while True:
        i += 1

        scene.step()

        t_now = time()
        print(1 / (t_now - t_prev), "FPS")
        t_prev = t_now
        if i > 200:
            break

    if enable_vis:
        scene.viewer.stop()

scene.build()

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Genesis visualization demo with camera recording")
    parser.add_argument("-v", "--vis", action="store_true", default=True, help="Enable visualization")
    args = parser.parse_args()
    
    gs.tools.run_in_another_thread(fn=run_sim, args=(scene, args.vis))
    if args.vis:
        scene.viewer.start()

if __name__ == "__main__":
    main()


# render rgb, depth, segmentation, normal
rgb, depth, segmentation, normal = cam.render(rgb=True, depth=True, segmentation=True, normal=True)

cam.start_recording()
import numpy as np

for i in range(120):
    scene.step()
    cam.set_pose(
        pos=(3.0 * np.sin(i / 60), 3.0 * np.cos(i / 60), 2.5),
        lookat=(0, 0, 0.5),
    )
    cam.render()
cam.stop_recording(save_to_filename="video.mp4", fps=60)