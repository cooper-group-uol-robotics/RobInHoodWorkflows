from frankx import Affine, Robot

robot = Robot("172.16.0.2")
robot.set_default_behavior()

state = robot.read_once()
print('\nPose: ', robot.current_pose())
#print('O_TT_E: ', state.O_T_EE)
print('Joints: ', state.q)
#print('Elbow: ', state.elbow)