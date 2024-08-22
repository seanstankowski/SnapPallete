# SnapSpectrum
A program for analysing the colour of snapdragon flowers

SnapSpectrum Usage Documentation
Overview
SnapSpectrum is a specialized script designed for the analysis of color variations in snapdragon flowers from the genus Antirrhinum. Utilizing advanced image processing techniques, SnapSpectrum quantifies different color metrics and saves the results in a CSV format for further analysis.

Requirements
Python 3.x
OpenCV library
NumPy library
matplotlib library (optional for additional plotting features)
Installation
Ensure Python is installed on your system along with the necessary libraries. You can install the required libraries using pip:

pip install opencv-python numpy matplotlib

Script Execution
To ensure accurate results, execute the SnapSpectrum script in the directory containing the target images. Results are automatically saved in the same directory as a CSV file.

Steps:
Place all images in a single directory.
Navigate to this directory in your command line interface (CLI).
Run the script using the command below.

python SnapSpectrum.py image_name.jpg

Flags and Options
-d, --diameter: Specifies a multiplier for the default circle diameter used in image analysis. This flag is optional. If omitted, the script uses a default multiplier of 1.0 (default size).
Examples

To run the script with half the default circle size:
python SnapSpectrum.py -d 0.5

Output
CSV File: After processing, the script outputs a CSV file named color_analysis_results.csv in the same directory. This file includes comprehensive details such as the image name, circle identifier, average hue, standard deviation of hue, average saturation, and standard deviation of saturation for each analyzed circle. Additional columns provide the percentage of different colors detected within each circle, based on predefined color ranges.
Additional Information
Color Ranges: Color ranges used for analysis are predefined within the script and include common colors observed in snapdragon flowers such as red, yellow, magenta, pink, white, and orange.
Circle Adjustment: Users can modify the radius of circles used for color analysis through the -d flag, allowing flexibility based on the size and scale of flower images.
