import importlib
import os
import sys
from inspect import currentframe, getframeinfo

# __all__ = ['setup_pyrender']


def get_pyopengl_platform():
  
  code_str = f'''\
    {sys.executable} -c\
    "import os;\
    os.environ['PYOPENGL_PLATFORM'] = 'egl';\
    os.environ['MESA_GL_VERSION_OVERRIDE'] = '4.1';\
    import pyrender;\
    _ = pyrender.OffscreenRenderer(\
      viewport_width=128,\
      viewport_height=128,\
      point_size=1.0\
      )"\
    '''.strip()
  
  ret = os.system(code_str)
  
  # fix bugs: munmap_chunk(): invalid pointer
  import torch
  
  if ret == 0:
    # fix bugs: err = 12297
    os.environ['MESA_GL_VERSION_OVERRIDE'] = '4.1'
    print(f"{'*' * 6} pyrender platform: egl {'*' * 6}")
    return 'egl'
  else:
    frameinfo = getframeinfo(currentframe())
    print(f"{__name__}, line{frameinfo.lineno}:")
    print(f"{'*' * 6} Failed to using egl {'*' * 6}")
    print(f"{'*' * 6} pyrender platform: osmesa {'*' * 6}")
    return 'osmesa'


def _setup_pyrender(platform):
  
  # fix bugs: munmap_chunk(): invalid pointer
  import torch
  
  if platform == 'egl':
    # fix bugs: err = 12297
    os.environ['MESA_GL_VERSION_OVERRIDE'] = '4.1'
    print(f"{'*' * 6} pyrender platform: egl {'*' * 6}")
    
  elif platform == 'osmesa':
    print(f"{'*' * 6} pyrender platform: osmesa {'*' * 6}")
  
  else:
    raise NotImplementedError

  os.environ['PYOPENGL_PLATFORM'] = platform
  
  pass

def setup_pyrender(platform=None):
  """
  
  :param platform: osmesa, egl
  :return:
  """
  if platform is None:
    platform = 'egl'

  _setup_pyrender(platform)

  # test
  import pyrender
  _ = pyrender.OffscreenRenderer(
    viewport_width=128,
    viewport_height=128,
    point_size=1.0
  )
  pass


def setup_aitviewer():
  tl2_dir = os.path.dirname(importlib.import_module('tl2').__file__)
  os.environ['AITVRC'] = f'{tl2_dir}/proj/trimesh/aitvconfig.yaml'
  pass

