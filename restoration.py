import cv2
import numpy as np
import matplotlib.pyplot as plt

def clip(img):
    return np.clip(img, 0, 255).astype(np.uint8)

img = cv2.imread("input/test_image_lena_noisy.png", cv2.IMREAD_COLOR)
if img is None:
    raise FileNotFoundError("Could not open image file: input/test_image_lena_noisy.png")

def median_filter(img, k=3):
    pad = k // 2
    padded = np.pad(img, pad, mode='edge')
    output = np.zeros_like(img)

    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            window = padded[i:i+k, j:j+k]
            output[i, j] = np.median(window)

    return output

def gaussian_kernel(size=3, sigma=1):
    k = size // 2
    kernel = np.zeros((size, size))

    for i in range(size):
        for j in range(size):
            x = i - k
            y = j - k
            kernel[i,j] = np.exp(-(x**2 + y**2)/(2*sigma**2))

    kernel /= np.sum(kernel)
    return kernel

def convolution(img, kernel):
    k = kernel.shape[0] // 2
    padded = np.pad(img, k, mode='edge')
    output = np.zeros_like(img, dtype=float)

    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            region = padded[i:i+kernel.shape[0], j:j+kernel.shape[1]]
            output[i,j] = np.sum(region * kernel)

    return output

def gaussian_filter(img, size=3, sigma=1):
    kernel = gaussian_kernel(size, sigma)
    return convolution(img, kernel)

def hist_equalization(img):
    hist = np.zeros(256)

    for pixel in img.flatten():
        hist[int(pixel)] += 1

    hist = hist / np.sum(hist)
    cdf = np.cumsum(hist)

    new_img = np.zeros_like(img)

    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            new_img[i,j] = int(cdf[int(img[i,j])] * 255)

    return new_img.astype(np.uint8)

def unsharp_mask(img):
    img_float = img.astype(float)
    blurred = gaussian_filter(img_float, size=3, sigma=1)
    mask = img_float - blurred
    sharpened = img_float + mask
    return sharpened

def process_channel(channel):

    median1 = median_filter(channel, k=5)
    median2 = median_filter(median1, k=5)

    gaussian = gaussian_filter(median2, size=7, sigma=1.8)
    gaussian = clip(gaussian)

    smooth = gaussian_filter(gaussian, size=5, sigma=1.0)
    smooth = clip(smooth)

    equalized = hist_equalization(smooth)
    blend = (0.7 * smooth + 0.3 * equalized).astype(np.uint8)

    sharp = unsharp_mask(blend)
    result = (0.3 * sharp + 0.7 * blend)

    result = np.round(result / 8) * 8

    return clip(result)

def main():
    global img
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    R, G, B = img[:, :, 0], img[:, :, 1], img[:, :, 2]

    R_p = process_channel(R)
    G_p = process_channel(G)
    B_p = process_channel(B)

    result = np.stack([R_p, G_p, B_p], axis=2)

    result_bgr = cv2.cvtColor(result, cv2.COLOR_RGB2BGR)
    cv2.imwrite("output/lena_restored.png", result_bgr)

    plt.subplot(1,2,1)
    plt.title("Original")
    plt.imshow(img)

    plt.subplot(1,2,2)
    plt.title("Restored")
    plt.imshow(result)

    plt.figure(figsize=(12,5))

    # histogram sebelum
    plt.subplot(1,2,1)
    plt.title("Histogram Before")
    plt.hist(img.flatten(), bins=256, range=[0,256])
    plt.xlabel("Intensity")
    plt.ylabel("Frequency")

    # histogram sesudah
    plt.subplot(1,2,2)
    plt.title("Histogram After")
    plt.hist(result.flatten(), bins=256, range=[0,256])
    plt.xlabel("Intensity")
    plt.ylabel("Frequency")

    plt.show()

if __name__ == "__main__":
    main()