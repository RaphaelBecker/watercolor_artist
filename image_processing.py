import numpy as np
from PIL import Image, ImageFilter, ImageEnhance


def process_image(image, brightness_threshold, invert_mode):
    # Convert non-RGB images to RGB
    if image.mode != 'RGB':
        image = image.convert('RGB')

    # Convert PIL Image to NumPy array
    np_image = np.array(image)

    # Calculate brightness and apply threshold
    brightness = np_image.mean(axis=2)
    mask = brightness > brightness_threshold

    if invert_mode:
        # Invert the mask
        mask = ~mask

    # Apply the mask to all channels
    np_image[mask] = [255, 255, 255]

    # Convert back to PIL Image
    processed_image = Image.fromarray(np_image, 'RGB')

    return processed_image


def watercolor_effect(image):
    """
    Apply an enhanced watercolor effect to an image.
    """

    # Ensure image is in RGB mode
    if image.mode != 'RGB':
        image = image.convert('RGB')

        # Apply a Gaussian blur to soften the image
    blurred_image = image.filter(ImageFilter.GaussianBlur(radius=1))

    # Reduce the image's color palette
    blurred_image = blurred_image.quantize(colors=64, method=Image.MEDIANCUT)

    # Convert back to RGB after quantizing
    blurred_image = blurred_image.convert('RGB')

    # Increase color saturation to give more vibrant colors
    enhanced_image = ImageEnhance.Color(blurred_image).enhance(1.5)

    # Step 4: Edge enhancement to simulate the watercolor edge effects
    edge_enhanced_image = enhanced_image.filter(ImageFilter.EDGE_ENHANCE)

    # Step 5: Soften the edges using another mild blur
    final_image = edge_enhanced_image.filter(ImageFilter.GaussianBlur(radius=1))

    return final_image