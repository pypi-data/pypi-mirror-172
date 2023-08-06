import PIL
import shutil
import os
import unittest


class Testing_resize(unittest.TestCase):

  def test_interpolate_antialias(self, debug=True):
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
    from tl2.proj.pytorch.downsampler import Downsampler

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
    up_size = (1024, 1024)
    down_size = (down_h, down_h)
    img_down_pil = pil_utils.pil_resize(img_pil, down_size)
    img_down_pil = img_down_pil.resize(up_size, PIL.Image.Resampling.NEAREST)
    img_down_pil.save(f"{outdir}/img_down.png")
    
    # img_tensor = tv_f.pil_to_tensor(img_pil)
    img_tensor = tv_f.to_tensor(img_pil).to(device)[None, ...]
    img_tensor = (img_tensor - 0.5) * 2
    
    no_antialias_tensor = torch.nn.functional.interpolate(img_tensor, scale_factor=down_h / img_pil.size[1],
                                                      recompute_scale_factor=False,
                                                      mode='bilinear',
                                                      antialias=False)
    no_antialias_pil = torch_utils.img_tensor_to_pil(no_antialias_tensor, )
    no_antialias_pil = no_antialias_pil.resize(up_size, PIL.Image.Resampling.NEAREST)
    no_antialias_pil.save(f"{outdir}/no_antialias.png")

    # bilinear
    mode = 'bilinear'
    antialias_tensor = torch.nn.functional.interpolate(img_tensor, scale_factor=down_h / img_pil.size[1],
                                                       recompute_scale_factor=False,
                                                       mode=mode,
                                                       antialias=True)
    antialias_pil = torch_utils.img_tensor_to_pil(antialias_tensor, )
    antialias_pil.save(f"{outdir}/antialias_{mode}.png")

    # bicubic
    mode = 'bicubic'
    antialias_tensor = torch.nn.functional.interpolate(img_tensor, scale_factor=down_h / img_pil.size[1],
                                                       recompute_scale_factor=False,
                                                       mode=mode,
                                                       antialias=True,
                                                       align_corners=False)
    antialias_pil = torch_utils.img_tensor_to_pil(antialias_tensor, )
    antialias_pil.save(f"{outdir}/antialias_{mode}_no_align_corners.png")

    # antialias_tensor = torch.nn.functional.interpolate(img_tensor, scale_factor=down_h / img_pil.size[1],
    #                                                    recompute_scale_factor=False,
    #                                                    mode=mode,
    #                                                    antialias=True,
    #                                                    align_corners=True)
    # antialias_pil = torch_utils.img_tensor_to_pil(antialias_tensor, )
    # antialias_pil.save(f"{outdir}/antialias_{mode}_align_corners.png")

    # area
    mode = 'area'
    antialias_tensor = torch.nn.functional.interpolate(img_tensor, scale_factor=down_h / img_pil.size[1],
                                                       recompute_scale_factor=False,
                                                       mode=mode,
                                                       antialias=False,)
    antialias_pil = torch_utils.img_tensor_to_pil(antialias_tensor, )
    antialias_pil.save(f"{outdir}/antialias_{mode}.png")
    
    # lanczos_tensor = tv_f.resize(img_tensor, size=(down_h, down_h),
    #                              interpolation=torchvision.transforms.InterpolationMode.LANCZOS,
    #                              antialias=True)
    
    # lanczos2
    mode = 'lanczos2'
    down_sampler = Downsampler(n_planes=3,
                               factor=1024//down_h,
                               kernel_type=mode,
                               phase=0.5,
                               preserve_size=True).to(device)
    with torch.no_grad():
      lanczos_tensor = down_sampler(img_tensor)
    lanczos_pil = torch_utils.img_tensor_to_pil(lanczos_tensor, )
    lanczos_pil = lanczos_pil.resize(up_size, PIL.Image.Resampling.NEAREST)
    lanczos_pil.save(f"{outdir}/{mode}.png")

    # lanczos3
    mode = 'lanczos3'
    down_sampler = Downsampler(n_planes=3,
                               factor=1024 // down_h,
                               kernel_type=mode,
                               phase=0.5,
                               preserve_size=True).to(device)
    with torch.no_grad():
      lanczos_tensor = down_sampler(img_tensor)
    lanczos_pil = torch_utils.img_tensor_to_pil(lanczos_tensor, )
    lanczos_pil = lanczos_pil.resize(up_size, PIL.Image.Resampling.NEAREST)
    lanczos_pil.save(f"{outdir}/{mode}.png")
    pass














