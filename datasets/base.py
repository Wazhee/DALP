from torch.utils.data import Dataset
import torchvision.transforms as transforms
from PIL import Image
from pathlib import Path
import pydicom as dicom
import numpy as np


def convert2binary(tmp):
    for i in range(len(tmp)): 
        for j in range(len(tmp[0])):
            if(tmp[i][j] > 0):
                tmp[i][j] = 1
            else:
                tmp[i][j] = 0
    return tmp
class ImagePathDataset(Dataset):
    def __init__(self, image_paths, image_size=(256, 256), flip=False, to_normal=False):
        self.image_size = image_size
        self.image_paths = image_paths
        self._length = len(image_paths)
        self.flip = flip
        self.to_normal = to_normal # 是否归一化到[-1, 1]

    def __len__(self):
        if self.flip:
            return self._length * 2
        return self._length

    def __getitem__(self, index):
        p = 0.0
        if index >= self._length:
            index = index - self._length
            p = 1.0

        transform = transforms.Compose([
            # transforms.RandomHorizontalFlip(p=p),
            # transforms.Resize(self.image_size),
            transforms.ToTensor()
        ])

        img_path = self.image_paths[index]
        image = None
        try:
            if(img_path.split('.')[1] == 'dcm'): # run dicom code
                image = dicom.dcmread(img_path).pixel_array
            else:
                image = Image.open(img_path)
        except BaseException as e:
            print(e, img_path)

        # if not image.mode == 'RGB':
        #     image = image.convert('RGB')
        if('/C/' in img_path):
            image = convert2binary(np.array(image))
        image = transform(image)
 
        # if self.to_normal:
        #     image = (image - 0.5) * 2.
        #     image.clamp_(-1., 1.)

        image_name = Path(img_path).stem
        return image, image_name

