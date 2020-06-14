from utils import *
from datasets import SRDataset
from PIL import Image
import matplotlib.pyplot as plt
from torch import argmax

from PIL import Image, ImageDraw, ImageFont


# device = torch.device("cuda" if torch.cuda.is_available())
device = "cpu"


def enhance(url):

    srgan_checkpoint = "checkpoint_srgan.pth.tar"

    srgan_generator = torch.load(srgan_checkpoint, map_location='cpu')[
        'generator'].to(device)

    srgan_generator.eval()

    model = srgan_generator

    # Custom dataloader
    test_dataset = SRDataset(url=url,
                             split='test',
                             crop_size=0,
                             scaling_factor=2,
                             lr_img_type='imagenet-norm',
                             hr_img_type='[-1, 1]'
                             )
    test_loader = torch.utils.data.DataLoader(test_dataset, batch_size=1, shuffle=False, num_workers=4,
                                              pin_memory=True)

    with torch.no_grad():
        # Batches
        for i, (lr_imgs, hr_imgs) in enumerate(test_loader):
            # Move to default device

            lr_imgs = lr_imgs.to(device)

            hr_imgs = hr_imgs.to(device)
            # Forward prop.
            sr_imgs = model(lr_imgs)

            sr_img_srgan = sr_imgs.squeeze(0).cpu().detach()
            sr_img_srgan = convert_image(
                sr_img_srgan, source='[-1, 1]', target='pil')

            plt.axis('off')
            plt.imshow(sr_img_srgan)
            plt.savefig('super.png')
