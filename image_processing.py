from PIL import ImageFilter, ImageOps, Image
import numpy as np

def alpha_to_rgba(alpha, r=50, g=130, b=184):
    r_channel = Image.new('L', alpha.size, r)
    g_channel = Image.new('L', alpha.size, g)
    b_channel = Image.new('L', alpha.size, b)
    
    return Image.merge('RGBA', [r_channel, g_channel, b_channel, alpha])

def salient(img):
    grayscale = img.convert('L').split()[0]
    alpha = img.split()[-1]

    gray_arr = 255 - np.array(grayscale)
    alpha_arr = np.array(alpha)

    final_arr = np.minimum(gray_arr, alpha_arr)

    return Image.fromarray(final_arr, mode='L')

def bloomify(img):
    # Make sure we have an rgba image
    img = img.convert('RGBA')
    
    # First of all make space that will be necessary later for blurring
    img = ImageOps.expand(img, border=10, fill=(0,0,0,0))
    
    alpha = img.split()[-1]
    alpha = salient(img).split()[0]
    
    recolored_image = alpha_to_rgba(alpha, r=255, g=255, b=255)
    bloom_layer = alpha_to_rgba(alpha, r=50, g=130, b=184).filter(ImageFilter.GaussianBlur(radius=5))
    
    final_image = Image.blend(recolored_image, bloom_layer, 0.5)
    
    return final_image

def process(processor_name, image):
    if processor_name == 'bloomify':
        return bloomify(image)

    return image
    