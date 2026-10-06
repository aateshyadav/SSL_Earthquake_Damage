import cv2
import numpy as np
import os
import glob

image_dir = r"C:\Users\Asus\Downloads\EARTHQUAKE-TURKEY\EARTHQUAKE-TURKEY\images"
mask_dir = r"C:\Users\Asus\Downloads\EARTHQUAKE-TURKEY\EARTHQUAKE-TURKEY\masks"
out_dir = r"C:\Users\Asus\Downloads\EARTHQUAKE-TURKEY\EARTHQUAKE-TURKEY"
os.makedirs(out_dir, exist_ok=True)

for img_path in glob.glob(os.path.join(image_dir, "*_post_disaster.png")):
    base = os.path.basename(img_path).replace("_post_disaster.png", "")
    building_mask = cv2.imread(os.path.join(mask_dir, f"building_{base}.png"), 0)
    damage_mask = cv2.imread(os.path.join(mask_dir, f"damage_{base}.png"), 0)
    img = cv2.imread(img_path)

    # find building contours
    contours, _ = cv2.findContours((building_mask==255).astype("uint8"), 
                                   cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for i, cnt in enumerate(contours):
        x,y,w,h = cv2.boundingRect(cnt)
        building_patch = img[y:y+h, x:x+w]

        # crop corresponding damage mask
        damage_crop = damage_mask[y:y+h, x:x+w]
        vals, counts = np.unique(damage_crop, return_counts=True)
        vals = vals[vals>0]  # ignore background
        if len(vals)==0:
            continue
        damage_class = vals[np.argmax(counts[1:])]  # majority label

        save_path = os.path.join(out_dir, f"{base}_{i}_class{damage_class}.png")
        cv2.imwrite(save_path, building_patch)
