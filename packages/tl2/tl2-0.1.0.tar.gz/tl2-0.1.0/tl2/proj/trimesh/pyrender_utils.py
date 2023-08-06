"""
- Install:
  pip install pyrender PyOpenGL-accelerate
  sudo apt install -y libosmesa6-dev freeglut3-dev

- ImportError: cannot import name 'EGLPlatform' from 'pyrender.platforms'
  pip install -I pyrender==0.1.45
  pyrender==0.1.45

- ImportError: cannot import name 'OSMesaCreateContextAttribs' from 'OpenGL.osmesa'
  pip install -I pyopengl==3.1.5
  pip install -I pyopengl==3.1.6

export EGL_DEVICE_ID=1

"""
import trimesh
import math
import copy
import pyrender
from pyrender.constants import RenderFlags
import numpy as np


def show_smpl(verts,
              faces,
              joints=None,
              show=False
              ):
  
  geometries = []
  # mesh
  vertex_colors = np.ones([verts.shape[0], 4]) * [0.3, 0.3, 0.3, 0.8]
  tri_mesh = trimesh.Trimesh(verts,
                             faces,
                             vertex_colors=vertex_colors)
  
  mesh = pyrender.Mesh.from_trimesh(tri_mesh)
  geometries.append(mesh)
  
  # joints
  if joints is not None:
    sm = trimesh.creation.uv_sphere(radius=0.005)
    sm.visual.vertex_colors = [0.9, 0.1, 0.1, 1.0]
    tfs = np.tile(np.eye(4), (len(joints), 1, 1))
    tfs[:, :3, 3] = joints
    joints_pcl = pyrender.Mesh.from_trimesh(sm, poses=tfs)
    
    geometries.append(joints_pcl)
  
  if show:
    scene = pyrender.Scene()
    for geo in geometries:
      scene.add(geo)
    pyrender.Viewer(scene, use_raymond_lighting=True)
  
  
def create_scene():
  """
  scene.add(mesh)
  pyrender.Viewer(scene, use_raymond_lighting=True)
  
  :return:
  """
  scene = pyrender.Scene()
  return scene


def viewer(scene):
  pyrender.Viewer(scene, use_raymond_lighting=True)
  pass


class WeakPerspectiveCamera(pyrender.Camera):
  def __init__(self,
               scale,
               translation,
               znear=pyrender.camera.DEFAULT_Z_NEAR,
               zfar=None,
               name=None):
    super(WeakPerspectiveCamera, self).__init__(
      znear=znear,
      zfar=zfar,
      name=name,
    )
    self.scale = scale
    self.translation = translation
    pass
  
  def get_projection_matrix(self, width=None, height=None):
    P = np.eye(4)
    P[0, 0] = self.scale[0]
    P[1, 1] = self.scale[1]
    P[0, 3] = self.translation[0] * self.scale[0]
    P[1, 3] = -self.translation[1] * self.scale[1]
    P[2, 2] = -1
    return P


class Renderer(object):
  """
  Using WeakPerspectiveCamera;
  
  """
  def __init__(self,
               resolution=(224, 224),
               wireframe=False):
    self.resolution = resolution
    
    self.wireframe = wireframe
    self.renderer = pyrender.OffscreenRenderer(
      viewport_width=self.resolution[0],
      viewport_height=self.resolution[1],
      point_size=1.0
    )
    
    # set the scene
    self.scene = pyrender.Scene(bg_color=[0.0, 0.0, 0.0, 0.0], ambient_light=(0.3, 0.3, 0.3))
    
    light = pyrender.PointLight(color=[1.0, 1.0, 1.0], intensity=1)
    
    light_pose = np.eye(4)
    light_pose[:3, 3] = [0, -1, 1]
    self.scene.add(light, pose=light_pose)
    
    light_pose[:3, 3] = [0, 1, 1]
    self.scene.add(light, pose=light_pose)
    
    light_pose[:3, 3] = [1, 1, 2]
    self.scene.add(light, pose=light_pose)
    
    self.colors_dict = {
      'red': np.array([0.5, 0.2, 0.2]),
      'pink': np.array([0.7, 0.5, 0.5]),
      'neutral': np.array([0.7, 0.7, 0.6]),
      'purple': np.array([0.5, 0.5, 0.7]),
      'green': np.array([0.5, 0.55, 0.3]),
      'sky': np.array([0.3, 0.5, 0.55]),
      'white': np.array([1.0, 0.98, 0.94]),
    }
    pass
  
  def __call__(self,
               verts,
               faces,
               img=np.zeros((224, 224, 3)),
               cam=np.array([1, 0, 0]),
               angle=None,
               axis=None,
               mesh_filename=None,
               color_type=None,
               color=[1.0, 1.0, 0.9]):
    
    mesh = trimesh.Trimesh(vertices=verts, faces=faces, process=False)
    
    # Rx = trimesh.transformations.rotation_matrix(math.radians(180), [1, 0, 0])
    # mesh.apply_transform(Rx)
    
    if mesh_filename is not None:
      mesh.export(mesh_filename)
    
    if angle and axis:
      R = trimesh.transformations.rotation_matrix(math.radians(angle), axis)
      mesh.apply_transform(R)
    
    if len(cam) == 4:
      sx, sy, tx, ty = cam
    elif len(cam) == 3:
      sx, tx, ty = cam
      sy = sx
    
    camera = WeakPerspectiveCamera(
      scale=[sx, sy],
      translation=[tx, ty],
      zfar=1000.
    )
    
    if color_type != None:
      color = self.colors_dict[color_type]
    
    material = pyrender.MetallicRoughnessMaterial(
      metallicFactor=0.0,
      alphaMode='OPAQUE',
      baseColorFactor=(color[0], color[1], color[2], 1.0)
    )
    
    mesh = pyrender.Mesh.from_trimesh(mesh, material=material)
    
    mesh_node = self.scene.add(mesh, 'mesh')
    
    camera_pose = np.eye(4)
    cam_node = self.scene.add(camera, pose=camera_pose)
    
    if self.wireframe:
      render_flags = RenderFlags.RGBA | RenderFlags.ALL_WIREFRAME
    else:
      render_flags = RenderFlags.RGBA
    
    rgb, depth_im = self.renderer.render(self.scene, flags=render_flags)
    if rgb.shape[-1] == 3:
      depth_im = (depth_im.clip(0, 1) * 255).astype(np.uint8)[..., np.newaxis]
      rgb = np.concatenate([rgb, depth_im], axis=-1)
    valid_mask = (rgb[:, :, -1] > 0)[:, :, np.newaxis]
    
    image_list = [img] if type(img) is not list else img
    
    return_img = []
    for item in image_list:
      output_img = rgb[:, :, :-1] * valid_mask + (1 - valid_mask) * item
      image = output_img.astype(np.uint8)
      return_img.append(image)
    
    if type(img) is not list:
      return_img = return_img[0]
    
    self.scene.remove_node(mesh_node)
    self.scene.remove_node(cam_node)
    
    return return_img


class Renderer_v1(object):
  """
  Using IntrinsicsCamera (fx, fy, cx, cy);
  
  """
  def __init__(self,
               intrinsic,
               width=224,
               height=224,
               wireframe=False,
               ):
    """
    :param wireframe:
    """
    self.height = height
    self.width = width
    
    from tl2.proj.trimesh import open3d_utils
    self.intrinsic = open3d_utils.update_intrinsic(intrinsic, height=height, width=width)
    
    self.wireframe = wireframe

    self.renderer = pyrender.OffscreenRenderer(
      viewport_width=width,
      viewport_height=height,
      point_size=1.0
    )

    self.colors_dict = {
      'red': np.array([0.5, 0.2, 0.2]),
      'pink': np.array([0.7, 0.5, 0.5]),
      'neutral': np.array([0.7, 0.7, 0.6]),
      # 'purple': np.array([0.5, 0.5, 0.7]),
      'purple': np.array([0.55, 0.4, 0.9]),
      'green': np.array([0.5, 0.55, 0.3]),
      'sky': np.array([0.3, 0.5, 0.55]),
      'white': np.array([1.0, 0.98, 0.94]),
    }
    
    self._setup_scene()
    pass
  
  def _setup_scene(self):
    # set the scene
    self.scene = pyrender.Scene(bg_color=[0.0, 0.0, 0.0, 0.0], ambient_light=(0.3, 0.3, 0.3))
    
    light = pyrender.PointLight(color=np.array([1.0, 1.0, 1.0]) * 0.2, intensity=15)
    
    yrot = np.radians(120)  # angle of lights
    
    light_pose = np.eye(4)
    light_pose[2, 2] = -1
    light_pose[:3, 3] = [0, -1, 1]
    self.scene.add(light, pose=light_pose)
    
    light_pose[:3, 3] = [0, 1, 1]
    self.scene.add(light, pose=light_pose)
    
    light_pose[:3, 3] = [1, 1, 2]
    self.scene.add(light, pose=light_pose)
    
    spot_l = pyrender.SpotLight(color=np.ones(3),
                                intensity=30.0,
                                innerConeAngle=np.pi / 4,
                                outerConeAngle=np.pi / 2)
    
    light_pose[:3, 3] = [1, 2, 2]
    self.scene.add(spot_l, pose=light_pose)
    
    light_pose[:3, 3] = [-1, 2, 2]
    self.scene.add(spot_l, pose=light_pose)
    
    # light_pose[:3, 3] = [-2, 2, 0]
    # self.scene.add(spot_l, pose=light_pose)
    
    # light_pose[:3, 3] = [-2, 2, 0]
    # self.scene.add(spot_l, pose=light_pose)
    pass
  
  def __call__(self,
               verts,
               faces,
               img=None,
               camera_rotation=np.eye(3),
               camera_translation=np.zeros(3),
               color_type='purple',
               color=[1.0, 1.0, 0.9],
               rgba_mode=False,
               mesh_filename=None,
               ):
    """
    sx, tx, ty = cam
    sy = sx
    camera_translation = np.array([- tx, ty, 2 * focal_length[0] / (resolution[0] * sy + 1e-9)])
    
    :param verts:
    :param faces:
    :param img:
    :param cam:
    :param focal_length:
    :param camera_rotation:
    :param camera_translation:
    :param mesh_filename:
    :param color_type:
    :param color:
    :param rgba_mode:
    :param return_cam_params:
    :return:
    """
    
    if img is None:
      img = np.zeros((self.height, self.width, 3)),
    assert img.shape[:2] == (self.height, self.width)
    
    # add mesh
    mesh = trimesh.Trimesh(vertices=verts, faces=faces, process=False)
    if mesh_filename is not None:
      mesh.export(mesh_filename)
    if color_type != None:
      color = self.colors_dict[color_type]
    material = pyrender.MetallicRoughnessMaterial(
      metallicFactor=0.2,
      roughnessFactor=0.6,
      alphaMode='OPAQUE',
      baseColorFactor=(color[0], color[1], color[2], 1.0)
    )
    mesh = pyrender.Mesh.from_trimesh(mesh, material=material)
    mesh_node = self.scene.add(mesh, 'mesh')
    
    # add camera
    fx, fy = self.intrinsic.get_focal_length()
    cx, cy = self.intrinsic.get_principal_point()
    camera = pyrender.IntrinsicsCamera(fx=fx,
                                       fy=fy,
                                       cx=cx,
                                       cy=cy)
    camera_pose = np.eye(4)
    camera_pose[:3, :3] = camera_rotation
    camera_pose[:3, 3] = camera_translation
    cam_node = self.scene.add(camera, pose=camera_pose)
    
    if self.wireframe:
      # render_flags = RenderFlags.RGBA | RenderFlags.ALL_WIREFRAME | RenderFlags.SHADOWS_SPOT
      render_flags = RenderFlags.RGBA | RenderFlags.ALL_WIREFRAME
    else:
      # render_flags = RenderFlags.RGBA | RenderFlags.SHADOWS_SPOT
      render_flags = RenderFlags.RGBA
    
    rgb, depth_im = self.renderer.render(self.scene, flags=render_flags)
    if rgb.shape[-1] == 3:
      depth_im = (depth_im.clip(0, 1) * 255).astype(np.uint8)[..., np.newaxis]
      rgb = np.concatenate([rgb, depth_im], axis=-1)
    valid_mask = (rgb[:, :, -1] > 0)[:, :, np.newaxis]
    
    image_list = [img] if type(img) is not list else img
    
    return_img = []
    for item in image_list:
      output_img = rgb[:, :, :-1] * valid_mask + (1 - valid_mask) * item
      
      if rgba_mode:
        output_img_rgba = np.zeros((output_img.shape[0], output_img.shape[1], 4))
        output_img_rgba[:, :, :3] = output_img
        output_img_rgba[:, :, 3][valid_mask[:, :, 0]] = 255
        output_img = output_img_rgba.astype(np.uint8)
      image = output_img.astype(np.uint8)
      return_img.append(image)
    
    if type(img) is not list:
      return_img = return_img[0]
    
    self.scene.remove_node(mesh_node)
    self.scene.remove_node(cam_node)
    
    return return_img

  def render(self, *args, **kwargs):
    self(*args, **kwargs)

