import numpy as np

WM = [2, 41]
GM = [3, 42]
BG = [0]


def efc(img, framemask=None):
    r"""
    Calculate the :abbr:`EFC (Entropy Focus Criterion)` [Atkinson1997]_.
    Uses the Shannon entropy of voxel intensities as an indication of ghosting
    and blurring induced by head motion. A range of low values is better,
    with EFC = 0 for all the energy concentrated in one pixel.

    .. math::

        \text{E} = - \sum_{j=1}^N \frac{x_j}{x_\text{max}}
        \ln \left[\frac{x_j}{x_\text{max}}\right]

    with :math:`x_\text{max} = \sqrt{\sum_{j=1}^N x^2_j}`.

    The original equation is normalized by the maximum entropy, so that the
    :abbr:`EFC (Entropy Focus Criterion)` can be compared across images with
    different dimensions:

    .. math::

        \text{EFC} = \left( \frac{N}{\sqrt{N}} \, \log{\sqrt{N}^{-1}} \right) \text{E}

    :param numpy.ndarray img: input data
    :param numpy.ndarray framemask: a mask of empty voxels inserted after a rotation of
      data

    copied from mriqc

    """

    if framemask is None:
        framemask = np.zeros_like(img, dtype=np.uint8)

    n_vox = np.sum(1 - framemask)
    # Calculate the maximum value of the EFC (which occurs any time all
    # voxels have the same value)
    efc_max = 1.0 * n_vox * (1.0 / np.sqrt(n_vox)) * np.log(1.0 / np.sqrt(n_vox))

    # Calculate the total image energy
    b_max = np.sqrt((img[framemask == 0] ** 2).sum())

    # Calculate EFC (add 1e-16 to the image data to keep log happy)
    res = float(
        (1.0 / efc_max)
        * np.sum((img[framemask == 0] / b_max) * np.log((img[framemask == 0] + 1e-16) / b_max))
    )

    return res


def anatomical_snr(img):
    r"""
    Calculate the anatomical Signal-to-Noise Ratio (SNR) of an MRI image. SNR is defined as the mean
    of the image divided by its standard deviation, adjusted for bias in finite samples. Higher SNR
    indicates better image quality with less random noise.

    :param numpy.ndarray img: The MRI image data as a NumPy array.

    :returns: The computed SNR value, adjusted for the bias in finite samples.
    """
    img_data = img
    mean = np.mean(img_data)
    std = np.std(img_data)

    n = img_data.size
    return mean / (std * np.sqrt(n/(n-1)))

def cnr(img, seg):
    r"""
    Calculate the Contrast-to-Noise Ratio (CNR) between white matter and gray matter in an MRI image.
    CNR is a measure of the ability to distinguish between different tissue types based on the
    contrast of their signal intensities relative to the noise level.

    :param numpy.ndarray img: The MRI image data as a NumPy array.
    :param numpy.ndarray seg: Segmentation array corresponding to the MRI image,
                              where different values represent different tissue types.

    :returns: The calculated CNR value for white matter versus gray matter.
    """
    wm_mask = np.isin(seg, WM)
    gm_mask = np.isin(seg, GM)
    bg_mask = np.isin(seg, BG)

    mean_wm = np.mean(img[wm_mask])
    std_wm = np.std(img[wm_mask])
    mean_gm = np.mean(img[gm_mask])
    std_gm = np.std(img[gm_mask])
    std_bg = np.std(img[bg_mask])

    return (mean_wm - mean_gm) / np.sqrt(std_bg**2 + std_wm**2 + std_gm**2)

def cjv(img, seg):
    r"""
    Calculate the Coefficient of Joint Variation (CJV) for white matter and gray matter in an MRI image.
    CJV is a measure of the combined variability of the signal intensities of two tissue types,
    normalized by the difference in their means. It is used as a metric for the homogeneity of
    voxel intensities within tissue types, with lower values indicating better homogeneity.

    :param numpy.ndarray img: The MRI image data as a NumPy array.
    :param numpy.ndarray seg: Segmentation array corresponding to the MRI image,
                              where different values represent different tissue types.

    :returns: The CJV value, indicating the variability relative to the mean difference between
              white and gray matter.
    """
    wm_mask = np.isin(seg, WM)
    gm_mask = np.isin(seg, GM)

    mean_wm = np.mean(img[wm_mask])
    std_wm = np.std(img[wm_mask])
    mean_gm = np.mean(img[gm_mask])
    std_gm = np.std(img[gm_mask])

    return (std_wm + std_gm) / abs(mean_wm - mean_gm)

