import os
import unittest
import numpy as np
import PIL
import shutil

import torch
import torch.nn as nn


def _get_kernel(factor,
                kernel_type,
                phase,
                kernel_width,
                support=None,
                sigma=None):
  assert kernel_type in ['lanczos', 'gauss', 'box']
  
  # factor  = float(factor)
  if phase == 0.5 and kernel_type != 'box':
    kernel = np.zeros([kernel_width - 1, kernel_width - 1])
  else:
    kernel = np.zeros([kernel_width, kernel_width])
  
  if kernel_type == 'box':
    assert phase == 0.5, 'Box filter is always half-phased'
    kernel[:] = 1. / (kernel_width * kernel_width)
  
  elif kernel_type == 'gauss':
    assert sigma, 'sigma is not specified'
    assert phase != 0.5, 'phase 1/2 for gauss not implemented'
    
    center = (kernel_width + 1.) / 2.
    print(center, kernel_width)
    sigma_sq = sigma * sigma
    
    for i in range(1, kernel.shape[0] + 1):
      for j in range(1, kernel.shape[1] + 1):
        di = (i - center) / 2.
        dj = (j - center) / 2.
        kernel[i - 1][j - 1] = np.exp(-(di * di + dj * dj) / (2 * sigma_sq))
        kernel[i - 1][j - 1] = kernel[i - 1][j - 1] / (2. * np.pi * sigma_sq)
  elif kernel_type == 'lanczos':
    assert support, 'support is not specified'
    center = (kernel_width + 1) / 2.
    
    for i in range(1, kernel.shape[0] + 1):
      for j in range(1, kernel.shape[1] + 1):
        
        if phase == 0.5:
          di = abs(i + 0.5 - center) / factor
          dj = abs(j + 0.5 - center) / factor
        else:
          di = abs(i - center) / factor
          dj = abs(j - center) / factor
        
        pi_sq = np.pi * np.pi
        
        val = 1
        if di != 0:
          val = val * support * np.sin(np.pi * di) * np.sin(np.pi * di / support)
          val = val / (np.pi * np.pi * di * di)
        
        if dj != 0:
          val = val * support * np.sin(np.pi * dj) * np.sin(np.pi * dj / support)
          val = val / (np.pi * np.pi * dj * dj)
        
        kernel[i - 1][j - 1] = val
  
  
  else:
    assert False, 'wrong method name'
  
  kernel /= kernel.sum()
  
  return kernel


class Downsampler(nn.Module):
  '''
  Downsampling method: lanczos.
  http://www.realitypixels.com/turk/computergraphics/ResamplingFilters.pdf
  
  '''
  
  def __init__(self,
               n_planes,
               factor,
               kernel_type,
               phase=0.,
               kernel_width=None,
               support=None,
               sigma=None,
               preserve_size=False):
    super(Downsampler, self).__init__()
    
    assert phase in [0, 0.5], 'phase should be 0 or 0.5'
    
    if kernel_type == 'lanczos2':
      support = 2
      kernel_width = 4 * factor + 1
      kernel_type_ = 'lanczos'
    
    elif kernel_type == 'lanczos3':
      support = 3
      kernel_width = 6 * factor + 1
      kernel_type_ = 'lanczos'
    
    elif kernel_type == 'gauss12':
      kernel_width = 7
      sigma = 1 / 2
      kernel_type_ = 'gauss'
    
    elif kernel_type == 'gauss1sq2':
      kernel_width = 9
      sigma = 1. / np.sqrt(2)
      kernel_type_ = 'gauss'
    
    elif kernel_type in ['lanczos', 'gauss', 'box']:
      kernel_type_ = kernel_type
    
    else:
      assert False, 'wrong name kernel'
    
    # note that `kernel width` will be different to actual size for phase = 1/2
    self.kernel = _get_kernel(factor, kernel_type_, phase, kernel_width, support=support, sigma=sigma)
    
    downsampler = nn.Conv2d(n_planes, n_planes, kernel_size=self.kernel.shape, stride=factor, padding=0)
    downsampler.weight.data[:] = 0
    downsampler.bias.data[:] = 0
    
    kernel_torch = torch.from_numpy(self.kernel)
    for i in range(n_planes):
      downsampler.weight.data[i, i] = kernel_torch
    
    self.downsampler_ = downsampler
    
    if preserve_size:
      
      if self.kernel.shape[0] % 2 == 1:
        pad = int((self.kernel.shape[0] - 1) / 2.)
      else:
        pad = int((self.kernel.shape[0] - factor) / 2.)
      
      self.padding = nn.ReplicationPad2d(pad)
    
    self.preserve_size = preserve_size
  
  def forward(self, input):
    if self.preserve_size:
      x = self.padding(input)
    else:
      x = input
    self.x = x
    return self.downsampler_(x)

# a = Downsampler(n_planes=3, factor=2, kernel_type='lanczos2', phase='1', preserve_size=True)


def create_pil_lanczos_layer(downsample_factor,
                             channels=3,
                             device='cuda'):
  """
  Downsampling layer equal to PIL LANCZOS resize.
  
  :param downsample_factor: 2
  :param channels: 3
  :param device:
  :return:
  """
  
  down_sampler = Downsampler(n_planes=channels,
                             factor=downsample_factor,
                             kernel_type='lanczos3',
                             phase=0.5,
                             preserve_size=True).to(device)
  
  return down_sampler


class Testing_resize(unittest.TestCase):
  
  def test_create_pil_lanczos_layer(self, debug=True):
    """
    Usage:

        # export CUDA_VISIBLE_DEVICES=$cuda_devices
        # export RUN_NUM=$run_num

        export CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7
        export PORT=12345
        export TIME_STR=1
        export PYTHONPATH=.
        python -c "from tl2.launch.tests.test_launch import Testing_Launch_v1;\
          Testing_Launch_v1().test_launch_ddp(debug=False)" \
          --tl_opts root_obs s3://$bucket/ZhouPeng/ \
          --tl_outdir results/train_ffhq_256/train_ffhq_256-20210726_202423_412
          # --tl_outdir results/$resume_dir

    :return:
    """
    if 'CUDA_VISIBLE_DEVICES' not in os.environ:
      os.environ['CUDA_VISIBLE_DEVICES'] = '0'
    
    # os.environ['DISPLAY'] = '172.25.208.1:0.0'
    
    import torch
    import torchvision.transforms.functional as tv_f
    from tl2.proj.pil import pil_utils
    from tl2.proj.pytorch import torch_utils
    
    
    image_path = "datasets/test.png"
    if not os.path.exists(image_path):
      image_path = "tl2_lib/data/images_r512/194.png"
    
    device = 'cuda'
    
    outdir = "results/resize"
    shutil.rmtree(outdir, ignore_errors=True)
    os.makedirs(outdir, exist_ok=True)
    
    img_pil = pil_utils.pil_open_rgb(image_path)
    
    img_pil.save(f"{outdir}/img_origin.png")
    
    down_h = 64
    up_h = img_pil.size[0]
    down_size = (down_h, down_h)
    up_size = (up_h, up_h)
    
    img_down_pil = pil_utils.pil_resize(img_pil, down_size)
    img_down_pil.save(f"{outdir}/img_down.png")
    img_down_up_pil = img_down_pil.resize(up_size, PIL.Image.Resampling.NEAREST)
    img_down_up_pil.save(f"{outdir}/img_down_up.png")
    
    img_tensor = tv_f.to_tensor(img_pil).to(device)[None, ...]
    img_tensor = (img_tensor - 0.5) * 2
    
    # lanczos3
    down_layer = create_pil_lanczos_layer(downsample_factor=up_h // down_h, device=device)

    batch_img_tensor = img_tensor.expand(4, -1, -1, -1)
    with torch.no_grad():
      batch_lanczos_tensor = down_layer(batch_img_tensor)
      lanczos_tensor = batch_lanczos_tensor[0]
    lanczos_pil = torch_utils.img_tensor_to_pil(lanczos_tensor, )
    lanczos_pil.save(f"{outdir}/down_layer.png")
    
    lanczos_up_pil = lanczos_pil.resize(up_size, PIL.Image.Resampling.NEAREST)
    lanczos_up_pil.save(f"{outdir}/down_layer_up.png")
    
    img_down_pil_np = np.array(img_down_pil)
    lanczos_pil_np = np.array(lanczos_pil)
    err = np.abs(img_down_pil_np - lanczos_pil_np)
    pass


