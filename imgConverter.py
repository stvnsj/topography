
"""
The possible problems that might be encountered:
Why might the picture of annex2_detail be rotated in some cases?

"""

from PIL import Image, ImageDraw, ImageFont, ImageOps
from image.badge import open_png_or_badge as open_or_draw


def adjust_annex9_geo (filename, output_file, HEIGHT = 5.31, WIDTH = 8.122, POINT = "PR31_g"):
    adjust_img(filename, output_file, HEIGHT, WIDTH, GEO=True, POINT=POINT)
def adjust_annex9_panoramic (filename, output_file, HEIGHT = 5.31, WIDTH  = 7.45) :
    adjust_img (filename, output_file, HEIGHT, WIDTH )
def adjust_annex9_detail (filename, output_file, HEIGHT=3.5, WIDTH=4.05, crop_zoom=1.5) :
    adjust_img (filename, output_file, HEIGHT , WIDTH,crop_zoom=crop_zoom)


######################
# ANNEX 2 ADJUSTMENT #
######################
def adjust_annex2_geo (filename, output_file, HEIGHT = 5.31, WIDTH=8.0, POINT="G241_g"):
    adjust_img (filename, output_file, HEIGHT, WIDTH, GEO=True, POINT=POINT)

def adjust_annex2_panoramic (filename, output_file, HEIGHT = 5.31, WIDTH  = 7.52) :
    adjust_img (filename, output_file, HEIGHT, WIDTH )

def adjust_annex2_detail (filename, output_file, HEIGHT=3.5, WIDTH=4.0, crop_zoom=1.5) :
    adjust_img (filename, output_file, HEIGHT , WIDTH, crop_zoom=crop_zoom)


######################
# ANNEX 5 ADJUSTMENT #
######################
def adjust_annex5_geo (filename, output_file, HEIGHT = 5.31, WIDTH= 8.122, POINT="T241_g"):
    adjust_img (filename, output_file, HEIGHT, WIDTH, GEO=True, POINT=POINT)

def adjust_annex5_panoramic (filename, output_file, HEIGHT = 5.31, WIDTH  = 7.45) :
    adjust_img (filename, output_file, HEIGHT, WIDTH )

def adjust_annex5_detail (filename, output_file, HEIGHT=3.5, WIDTH=4.05, crop_zoom=1.5) :
    adjust_img (filename, output_file, HEIGHT , WIDTH, crop_zoom=crop_zoom)



###################################################
# Functions used the create the annotation images #
# to be inserted in the georeferenced images of   #
# Annex 2, 4, 5                                   #
###################################################
def create_annotation (PREFIX = "R") :
    
    font_size = 12
    font_path = "/usr/share/fonts/truetype/lato/Lato-Medium.ttf"

    try:
        font = ImageFont.truetype(font_path, font_size)  # Adjust font size as needed
    except IOError:
        font = ImageFont.load_default()
        
        
    for i in range(1,1000):
        box_width, box_height = 45, 20
        image = Image.new("RGB", (box_width, box_height), "white")
        draw = ImageDraw.Draw(image)
        
        text = f"{PREFIX}-{i}"
        text_height = font_size
        text_width = draw.textlength(text, font=font)
        border_thickness = 1
        draw.rectangle(
            [(0, 0), (box_width - 1, box_height - 1)],  # Coordinates of the rectangle
            outline="black",
            width=border_thickness
        )
        
        text_x = (box_width - text_width) // 2
        text_y = (box_height - text_height) // 2
        
        draw.text((text_x, text_y + 1), text, fill="black", font=font)
        
        image.save(f"annotation/{PREFIX}{i}_g.png")


#def adjust_img (filename, output_file, HEIGHT , WIDTH, GEO=False, POINT = "T242_g"):
#    
#    
#    W_RATIO  = WIDTH / HEIGHT  # Width Ratio to be obtained.
#    H_RATIO = HEIGHT / WIDTH   # Height Ratio to be obtained.
#    
#    # img = Image.open(filename) # Input image
#
#
#    img = Image.open(filename)  # Input image
#    # Apply EXIF orientation (if present) to pixels and clear the flag
#    try:
#        img = ImageOps.exif_transpose(img)
#    except Exception:
#        pass
#    # Ensure a consistent mode for later save/crop
#    if img.mode not in ("RGB", "RGBA"):
#        img = img.convert("RGB")
#
#
#
#
# 
#    dpi = 300 * 0.32 
#    
#    cm_to_px = lambda cm: int((cm * dpi) / 2.54)
# 
#    img_w_ratio = img.width  / img.height # Width ratio of input file.
#    img_h_ratio = img.height / img.width  # Height ratio of input file.
#    
#    W_DIFF = W_RATIO - img_w_ratio # Width Ratio delta
#    H_DIFF = H_RATIO - img_h_ratio # Height Ratio delta
#    
#    TOP = 0
#    RIGHT = 0
#    BOTTOM = 0
#    LEFT = 0
# 
#    if W_DIFF < 0:
#        DELTA  =  - W_DIFF * img.height * 0.5
#        LEFT   = DELTA
#        RIGHT  = img.width - DELTA
#        TOP    = 0
#        BOTTOM = img.height
#        cropped_img = img.crop((LEFT, TOP, RIGHT, BOTTOM))
#        resized_img = cropped_img.resize((cm_to_px(WIDTH), cm_to_px(HEIGHT)))
#    
# 
#    if H_DIFF < 0:
#        DELTA = - H_DIFF * img.width * 0.5
#        LEFT = 0
#        RIGHT = img.width
#        TOP = DELTA
#        BOTTOM = img.height - DELTA
#        cropped_img = img.crop((LEFT, TOP, RIGHT, BOTTOM))
#        resized_img = cropped_img.resize((cm_to_px(WIDTH),cm_to_px(HEIGHT)))
#   
#    
#    if GEO:
#
#        overlay = Image.open("annotation/NORTH.png")
#
#
#
#
#        # annot   = Image.open(f"annotation/{POINT}.png")
#
#
#
#        annot_path = f"annotation/{POINT}.png"
#        annot = open_or_draw(annot_path, POINT)
#
#
#
#
#
#        annot_x =  resized_img.width  - annot.width  - 3
#        annot_y =  resized_img.height - annot.height - 3
#        
#        x_offset = resized_img.width - overlay.width - 4
#        y_offset = 4
#        
#        position = (x_offset,y_offset)
#        resized_img.paste(overlay, position, mask=overlay)
#        resized_img.paste(annot, (annot_x, annot_y))
#        draw = ImageDraw.Draw(resized_img)
#        draw.rectangle(
#            [(0, 0), (resized_img.width-1, resized_img.height-1)],  # Coordinates of the rectangle
#            outline="black",
#            width=1
#        )
#        
#        resized_img.save(output_file, format="PNG",quality=95)
#        
#        return
#    
#    draw = ImageDraw.Draw(resized_img)
#    draw.rectangle(
#            [(0, 0), (resized_img.width-1, resized_img.height-1)],  # Coordinates of the rectangle
#            outline="black",
#            width=1
#        )
#    
#    # resized_img.save(output_file, format="JPEG",quality=95)
#    # Ensure downstream viewers won't re-rotate: set EXIF Orientation to 1
#    exif = resized_img.getexif()
#    try:
#        ORIENTATION_TAG = 274  # EXIF Orientation
#        exif[ORIENTATION_TAG] = 1
#    except Exception:
#        pass
#    resized_img.save(
#        output_file,
#        format="JPEG",
#        quality=95,
#        exif=exif.tobytes() if exif else None
#    )
#
#    
#
#
#if __name__ == "__main__":
#    print("imgConverter")
#    create_annotation(PREFIX="PR")
#
#
#




def adjust_img(filename, output_file, HEIGHT, WIDTH, GEO=False, POINT="T242_g", crop_zoom=1.0):
    """
    crop_zoom >= 1.0
      1.0 -> minimal crop to match aspect (current behavior)
      >1.0 -> crop tighter while preserving the same aspect ratio
    """

    # --- desired aspect ---
    aspect = WIDTH / HEIGHT

    # --- open & normalize orientation/mode ---
    img = Image.open(filename)
    try:
        img = ImageOps.exif_transpose(img)
    except Exception:
        pass
    if img.mode not in ("RGB", "RGBA"):
        img = img.convert("RGB")

    # --- px size we will finally resize to (via your cm->px rule) ---
    dpi = 300 * 0.32
    cm_to_px = lambda cm: int((cm * dpi) / 2.54)
    out_w_px = cm_to_px(WIDTH)
    out_h_px = cm_to_px(HEIGHT)

    # --- compute a centered crop with the same aspect, optionally tighter ---
    w, h = img.size
    crop_zoom = max(1.0, float(crop_zoom))  # clamp

    if (w / h) >= aspect:
        # Image is wider than target aspect: base crop uses full height.
        crop_h = int(round(h / crop_zoom))
        crop_w = int(round(crop_h * aspect))
    else:
        # Image is taller than target aspect: base crop uses full width.
        crop_w = int(round(w / crop_zoom))
        crop_h = int(round(crop_w / aspect))

    # Ensure at least 1px
    crop_w = max(1, min(crop_w, w))
    crop_h = max(1, min(crop_h, h))

    # Center the crop rectangle
    left   = max(0, (w - crop_w) // 2)
    top    = max(0, (h - crop_h) // 2)
    right  = min(w, left + crop_w)
    bottom = min(h, top + crop_h)

    cropped_img = img.crop((left, top, right, bottom))

    # High-quality resize to the requested physical size
    resized_img = cropped_img.resize((out_w_px, out_h_px), resample=Image.LANCZOS)

    # --- overlays / borders / saving (unchanged) ---
    if GEO:
        overlay = Image.open("annotation/NORTH.png")
        annot_path = f"annotation/{POINT}.png"
        annot = open_or_draw(annot_path, POINT)

        annot_x = resized_img.width  - annot.width  - 3
        annot_y = resized_img.height - annot.height - 3

        x_offset = resized_img.width - overlay.width - 4
        y_offset = 4
        resized_img.paste(overlay, (x_offset, y_offset), mask=overlay)
        resized_img.paste(annot, (annot_x, annot_y))

        draw = ImageDraw.Draw(resized_img)
        draw.rectangle([(0, 0), (resized_img.width-1, resized_img.height-1)],
                       outline="black", width=1)

        resized_img.save(output_file, format="PNG", quality=95)
        return

    draw = ImageDraw.Draw(resized_img)
    draw.rectangle([(0, 0), (resized_img.width-1, resized_img.height-1)],
                   outline="black", width=1)

    exif = resized_img.getexif()
    try:
        ORIENTATION_TAG = 274
        exif[ORIENTATION_TAG] = 1
    except Exception:
        pass

    resized_img.save(
        output_file,
        format="JPEG",
        quality=95,
        exif=exif.tobytes() if exif else None
    )