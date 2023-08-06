
from typing import Optional
import logging

import numpy as np
from sklearn.model_selection import train_test_split
import torch
from torch.utils.data import DataLoader
import pytorch_lightning as pl
from torchvision import transforms

import albumentations as A
from albumentations.pytorch import ToTensorV2

from pytorch_galaxy_datasets import galaxy_dataset


# https://pytorch-lightning.readthedocs.io/en/stable/extensions/datamodules.html
class GalaxyDataModule(pl.LightningDataModule):
    # takes generic catalogs (which are already downloaded and happy),
    # splits if needed, and creates generic datasets->dataloaders etc
    # easy to make dataset-specific default transforms if desired
    def __init__(
        self,
        label_cols,
        # provide full catalog for automatic split, or...
        catalog=None,
        train_fraction=0.7,
        val_fraction=0.1,
        test_fraction=0.2,
        # provide train/val/test catalogs for your own previous split
        train_catalog=None,
        val_catalog=None,
        test_catalog=None,
        # augmentation params (sensible supervised defaults)
        greyscale=True,
        album=False,
        resize_size=224,
        crop_scale_bounds=(0.7, 0.8),
        crop_ratio_bounds=(0.9, 1.1),
        # hardware params
        batch_size=256,  # careful - will affect final performance
        use_memory=False,  # deprecated
        num_workers=4,
        prefetch_factor=4,
        seed=42
    ):
        super().__init__()

        if catalog is not None:  # catalog provided, should not also provide explicit split catalogs
            assert train_catalog is None
            assert val_catalog is None
            assert test_catalog is None
        else:  # catalog not provided, must provide explicit split catalogs
            assert train_catalog is not None
            assert val_catalog is not None
            assert test_catalog is not None

        self.label_cols = label_cols

        self.catalog = catalog
        self.train_catalog = train_catalog
        self.val_catalog = val_catalog
        self.test_catalog = test_catalog

        self.batch_size = batch_size

        self.resize_size = resize_size
        self.crop_scale_bounds = crop_scale_bounds
        self.crop_ratio_bounds = crop_ratio_bounds

        self.use_memory = use_memory
        if self.use_memory:
            raise NotImplementedError

        self.num_workers = num_workers
        self.seed = seed

        assert np.isclose(train_fraction + val_fraction + test_fraction, 1.)
        self.train_fraction = train_fraction
        self.val_fraction = val_fraction
        self.test_fraction = test_fraction

        self.greyscale = greyscale
        self.album = album

        if self.album:
            logging.info('Using albumentations for augmentations')
            self.transform_with_album()
        else:
            logging.info('Using torchvision for augmentations')
            self.transform_with_torchvision()

        self.prefetch_factor = prefetch_factor
        self.dataloader_timeout = 240  # seconds

        logging.info('Num workers: {}'.format(self.num_workers))
        logging.info('Prefetch factor: {}'.format(self.prefetch_factor))

    def transform_with_torchvision(self):

        transforms_to_apply = default_torchvision_transforms(self.greyscale, self.resize_size, self.crop_scale_bounds, self.crop_ratio_bounds)

        self.transform = transforms.Compose(transforms_to_apply)


    def transform_with_album(self):

        if self.greyscale:
            transforms_to_apply = [A.Lambda(name='ToGray', image=ToGray(
                reduce_channels=True), always_apply=True)]
        else:
            transforms_to_apply = []

            transforms_to_apply += [
                A.ToFloat(),
                # anything outside of the original image is set to 0.
                A.Rotate(limit=180, interpolation=1,
                         always_apply=True, border_mode=0, value=0),
                A.RandomResizedCrop(
                    height=self.resize_size,  # after crop resize
                    width=self.resize_size,
                    scale=self.crop_scale_bounds,  # crop factor
                    ratio=self.crop_ratio_bounds,  # crop aspect ratio
                    interpolation=1,  # This is "INTER_LINEAR" == BILINEAR interpolation. See: https://docs.opencv.org/3.4/da/d54/group__imgproc__transform.html
                    always_apply=True
                ),  # new aspect ratio
                A.VerticalFlip(p=0.5),
                ToTensorV2()
            ]

        albumentations_transform = A.Compose(transforms_to_apply)

        # warning - might need a transpose check
        # albumentations expects np array, and returns dict keyed by "image"
        self.transform = lambda img: albumentations_transform(image=np.array(img))["image"]


    # only called on main process
    def prepare_data(self):
        pass   # could include some basic checks

    # called on every gpu

    def setup(self, stage: Optional[str] = None):

        if self.catalog is not None:
            self.train_catalog, hidden_catalog = train_test_split(
                self.catalog, train_size=self.train_fraction, random_state=self.seed
            )
            self.val_catalog, self.test_catalog = train_test_split(
                hidden_catalog, train_size=self.val_fraction/(self.val_fraction + self.test_fraction), random_state=self.seed
            )
            del hidden_catalog
        else:
            assert self.train_catalog is not None
            assert self.val_catalog is not None
            assert self.test_catalog is not None

        # Assign train/val datasets for use in dataloaders
        # assumes dataset_class has these standard args
        if stage == "fit" or stage is None:
            self.train_dataset = galaxy_dataset.GalaxyDataset(
                catalog=self.train_catalog, label_cols=self.label_cols, transform=self.transform
            )
            self.val_dataset = galaxy_dataset.GalaxyDataset(
                catalog=self.val_catalog, label_cols=self.label_cols, transform=self.transform
            )

        # Assign test dataset for use in dataloader(s)
        if stage == "test" or stage is None:
            self.test_dataset = galaxy_dataset.GalaxyDataset(
                catalog=self.test_catalog, label_cols=self.label_cols, transform=self.transform
            )

    def train_dataloader(self):
        return DataLoader(self.train_dataset, batch_size=self.batch_size, shuffle=True, num_workers=self.num_workers, pin_memory=True, persistent_workers=self.num_workers > 0, prefetch_factor=self.prefetch_factor, timeout=self.dataloader_timeout)

    def val_dataloader(self):
        return DataLoader(self.val_dataset, batch_size=self.batch_size, shuffle=False, num_workers=self.num_workers, pin_memory=True, persistent_workers=self.num_workers > 0, prefetch_factor=self.prefetch_factor, timeout=self.dataloader_timeout)

    def test_dataloader(self):
        return DataLoader(self.test_dataset, batch_size=self.batch_size, shuffle=False, num_workers=self.num_workers, pin_memory=True, persistent_workers=self.num_workers > 0, prefetch_factor=self.prefetch_factor, timeout=self.dataloader_timeout)

    # def predict_dataloader(self, )



def default_torchvision_transforms(greyscale, resize_size, crop_scale_bounds, crop_ratio_bounds):
    # refactored out for use elsewhere, if need exactly these transforms
    # assume input is 0-255 uint8 tensor

    # automatically normalises from 0-255 int to 0-1 float
    transforms_to_apply = [transforms.ToTensor()]  # dataset gives PIL image currently

    if greyscale:
        # transforms.Grayscale() adds perceptual weighting to rgb channels
        transforms_to_apply += [GrayscaleUnweighted()]

    transforms_to_apply += [
        transforms.RandomResizedCrop(
            size=resize_size,  # assumed square
            scale=crop_scale_bounds,  # crop factor
            ratio=crop_ratio_bounds,  # crop aspect ratio
            interpolation=transforms.InterpolationMode.BILINEAR),  # new aspect ratio
        transforms.RandomHorizontalFlip(),
        transforms.RandomRotation(
            degrees=180., interpolation=transforms.InterpolationMode.BILINEAR)
    ]
    
    return transforms_to_apply

# torchvision
class GrayscaleUnweighted(torch.nn.Module):

    def __init__(self, num_output_channels=1):
        super().__init__()
        self.num_output_channels = num_output_channels

    def forward(self, img):
        """
        PyTorch (and tensorflow) does greyscale conversion as a *weighted* mean by default (as colours have different perceptual brightnesses).
        Here, do a simple mean.
        Args:
            img (Tensor): Image to be converted to grayscale.

        Returns:
            Tensor: Grayscaled image.
        """
        # https://pytorch.org/docs/stable/generated/torch.mean.html
        return img.mean(dim=-3, keepdim=True)  # (..., C, H, W) convention

    def __repr__(self):
        return self.__class__.__name__ + '(num_output_channels={0})'.format(self.num_output_channels)


# albumentations versuib of GrayscaleUnweighted
class ToGray():

    def __init__(self, reduce_channels=False):
        if reduce_channels:
            self.mean = lambda arr: arr.mean(axis=2, keepdims=True)
        else:
            self.mean = lambda arr: arr.mean(
                axis=2, keepdims=True).repeat(3, axis=2)

    def __call__(self, image, **kwargs):
        return self.mean(image)
