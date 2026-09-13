# Genesis Physics Simulation

A comprehensive physics simulation framework using Genesis that demonstrates various simulation capabilities including rigid body dynamics, elastic materials, fluid simulation, and robotics control.

## Features

- **Rigid Body Dynamics**: Robot arm simulation with physics-based interactions
- **Elastic Materials**: Deformable object simulation with PBD (Position Based Dynamics)
- **Fluid Simulation**: Real-time liquid dynamics with density and viscosity solving
- **Robotics Control**: Inverse kinematics, path planning, and grasping simulation
- **Real-time Visualization**: GPU-accelerated rendering with customizable camera controls
- **Multi-threaded Simulation**: Efficient parallel execution for optimal performance

## Requirements

```
genesis-sim>=1.0.0
torch>=1.9.0
numpy>=1.21.0
argparse
```

## Installation

1. Install Genesis simulation framework:
```bash
pip install genesis-sim
```

2. Install other dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Robot Simulation
```bash
# Run with visualization (default)
python main.py --vis

# Run headless (no visualization)
python main.py
```

### Elastic Dragon Simulation
```bash
# Run with GPU acceleration (default)
python elastic_dragon.py --vis

# Force CPU backend
python elastic_dragon.py --vis --cpu
```

### Robotics Manipulation
```bash
# Advanced robot grasping simulation
python robo.py
```

### Fluid Dynamics
```bash
# Fluid simulation with robot interaction
python eunnmac.py --vis --steps 1000

# Custom gravity settings
python eunnmac.py --vis --gravity 0.0 0.0 -9.8
```

### Advanced Visualization
```bash
# Enhanced visualization with camera recording
python visualization.py --vis
```

## Scripts Overview

### main.py
- Basic rigid body simulation with Franka Panda robot arm
- Demonstrates scene setup, entity creation, and simulation loop
- Configurable visualization and physics parameters

### elastic_dragon.py
- Elastic material simulation using PBD solver
- Deformable mesh object with realistic material properties
- GPU/CPU backend selection for performance optimization

### robo.py
- Advanced robotics simulation with inverse kinematics
- Path planning and execution for pick-and-place tasks
- Force control for realistic grasping behavior

### eunnmac.py
- Combined fluid and rigid body simulation
- Liquid dynamics with density and viscosity solving
- Robot-fluid interaction demonstration

### visualization.py
- Advanced rendering and camera control
- Multi-camera setup with different viewpoints
- Video recording capabilities for simulation analysis

## Configuration

### Scene Options
- **Viewer Options**: Camera position, field of view, rendering resolution
- **Simulation Options**: Time step, substeps, gravity vector
- **Rigid Options**: Solver parameters for rigid body dynamics
- **PBD Options**: Fluid simulation boundaries and solver iterations

### Performance Tuning
- Use `gs.gpu` backend for better performance on compatible hardware
- Adjust `substeps` parameter for simulation stability vs speed tradeoff
- Modify solver iterations for accuracy vs performance balance

## Asset Requirements

The simulation requires the following asset files:
- `xml/franka_emika_panda/panda.xml` - Robot model definition
- `meshes/dragon/dragon.obj` - 3D mesh for elastic simulation

Ensure these assets are available in your Genesis installation or provide alternative paths.

## Troubleshooting

### Common Issues
1. **Missing Assets**: Ensure robot XML files and mesh objects are available
2. **GPU Backend**: If GPU acceleration fails, use `--cpu` flag to force CPU backend
3. **Visualization**: If viewer doesn't start, check display settings and OpenGL support

### Performance Optimization
- Reduce simulation resolution for faster execution
- Lower solver iterations for real-time performance
- Use headless mode for batch processing

## Examples

### Basic Physics Simulation
```python
import genesis as gs

gs.init(backend=gs.gpu)
scene = gs.Scene(show_viewer=True)
plane = scene.add_entity(gs.morphs.Plane())
robot = scene.add_entity(gs.morphs.MJCF(file="robot.xml"))
scene.build()
scene.viewer.start()
```

### Fluid Simulation Setup
```python
liquid = scene.add_entity(
    material=gs.materials.PBD.Liquid(rho=1.0),
    morph=gs.morphs.Box(lower=(0.2, 0.1, 0.1), upper=(0.4, 0.3, 0.5))
)
```

## License

This project demonstrates Genesis simulation capabilities and is intended for educational and research purposes.

## Contributing

Contributions are welcome! Please ensure:
- Code follows existing style conventions
- New features include appropriate documentation
- Performance optimizations are tested across different backends

## Support

For Genesis-specific issues, refer to the [Genesis documentation](https://genesis-sim.org).
For simulation questions, create an issue with detailed reproduction steps.