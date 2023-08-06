from tl2.proj.trimesh import setup_aitviewer
setup_aitviewer()

from aitviewer.renderables.smpl import SMPLSequence
from aitviewer.models.smpl import SMPLLayer
from aitviewer.viewer import Viewer


def main():
  smpl_layer = SMPLLayer(model_type='smplx', gender='neutral')
  smpl_template = SMPLSequence.t_pose(smpl_layer=smpl_layer)
  
  # Display in viewer.
  v = Viewer()
  v.scene.add(smpl_template)
  v.run()
  
if __name__ == '__main__':
  """
  export PYTHONPATH=.:./tl2_lib
  python tl2_lib/tl2/proj/trimesh/examples/aitviewer/quick_start.py
  
  """
  main()
  