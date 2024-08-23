import cv2
import numpy as np
import csv
import os
import sys
import argparse

def setup_image_for_selection(img_path):
    global img
    img = cv2.imread(img_path)
    if img is None:
        print(f"Failed to load image: {img_path}")
        return False
    cv2.imshow('image', img)
    cv2.setMouseCallback('image', click_event)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return True

def click_event(event, x, y, flags, param):
    global centers, img, max_circles
    if event == cv2.EVENT_LBUTTONDOWN:
        if len(centers) < max_circles:
            centers.append((x, y))
            display_image_with_circles(img, centers)
    elif event == cv2.EVENT_RBUTTONDOWN and centers:
        centers.pop()
        display_image_with_circles(img, centers)

def display_image_with_circles(image, centers):
    updated_img = image.copy()
    for center in centers:
        cv2.circle(updated_img, center, radius, (0, 255, 0), 2)
    cv2.imshow('image', updated_img)
    if len(centers) == max_circles:
        cv2.waitKey(0)
        cv2.destroyAllWindows()

def process_circles(centers, hsv_image, img_path):
    results = []
    filename = img_path.split('/')[-1]
    csv_file_path = 'color_analysis_results.csv'
    
    file_exists = os.path.isfile(csv_file_path)
    with open(csv_file_path, 'a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            header = ['Image Name', 'Circle', 'Mean Hue', 'Std Dev Hue', 'Mean Saturation', 'Std Dev Saturation', 'Mean Brightness', 'Std Dev Brightness'] + list(color_ranges.keys())
            writer.writerow(header)

        for index, center in enumerate(centers):
            circle_mask = np.zeros_like(hsv_image[:, :, 0], dtype=np.uint8)
            cv2.circle(circle_mask, center, radius, 255, thickness=-1)
            hsv_masked = cv2.bitwise_and(hsv_image, hsv_image, mask=circle_mask)

            hue_values = hsv_masked[:, :, 0][circle_mask == 255]
            sat_values = hsv_masked[:, :, 1][circle_mask == 255]
            val_values = hsv_masked[:, :, 2][circle_mask == 255]  # Value/Brightness
            mean_hue = np.mean(hue_values) if hue_values.size > 0 else 0
            std_dev_hue = np.std(hue_values) if hue_values.size > 0 else 0
            mean_saturation = np.mean(sat_values) if sat_values.size > 0 else 0
            std_dev_saturation = np.std(sat_values) if sat_values.size > 0 else 0
            mean_brightness = np.mean(val_values) if val_values.size > 0 else 0
            std_dev_brightness = np.std(val_values) if val_values.size > 0 else 0

            row = [filename, f"Circle {index+1}", f"{mean_hue:.2f}", f"{std_dev_hue:.2f}", f"{mean_saturation:.2f}", f"{std_dev_saturation:.2f}", f"{mean_brightness:.2f}", f"{std_dev_brightness:.2f}"]

            for color, ranges in color_ranges.items():
                if isinstance(ranges, list):
                    mask = np.zeros_like(circle_mask, dtype=np.uint8)
                    for lower, upper in ranges:
                        temp_mask = cv2.inRange(hsv_masked, np.array(lower), np.array(upper))
                        mask |= cv2.bitwise_and(temp_mask, temp_mask, mask=circle_mask)
                else:
                    mask = cv2.inRange(hsv_masked, np.array(ranges[0]), np.array(ranges[1]))
                    mask = cv2.bitwise_and(mask, mask, mask=circle_mask)

                color_ratio = np.sum(mask > 0) / np.sum(circle_mask > 0) if np.sum(circle_mask > 0) > 0 else 0
                row.append(f"{color_ratio:.2%}")

            writer.writerow(row)
            results.append(row)

    return results

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some images.')
    parser.add_argument('image_path', type=str, help='Path to the image file')
    parser.add_argument('-d', '--diameter', type=float, default=1.0, help='Diameter multiplier for the circles')
    parser.add_argument('-c', '--circles', type=int, default=6, help='Number of circles to analyze, up to a maximum of 6')
    args = parser.parse_args()

    img_path = args.image_path
    diameter_multiplier = args.diameter
    max_circles = min(args.circles, 6)  # Ensure it does not exceed 6
    centers = []
    global radius
    radius = int(100 * diameter_multiplier)  # Adjust the radius based on the diameter multiplier

    if not setup_image_for_selection(img_path):
        print("Image setup failed, exiting.")
        sys.exit(1)

    hsv_image = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    color_ranges = {
        'Red': [((0, 50, 50), (15, 255, 255)), ((170, 50, 50), (195, 255, 255))],
        'Yellow': ((25, 15, 100), (40, 255, 255)),
        'Magenta': ((140, 100, 100), (170, 255, 255)),
        'Pink': ((120, 15, 100), (160, 80, 255)),
        'White': ((0, 0, 200), (180, 17, 255)),
        'Orange': ((15, 15, 100), (26, 255, 255))
    }

    results = process_circles(centers, hsv_image, img_path)

    # Optionally display results
    for result in results:
        print(', '.join(result))
