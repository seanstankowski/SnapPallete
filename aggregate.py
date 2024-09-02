import csv
import argparse
from collections import defaultdict

# Function to process the SnapSpectrum output
def process_snapspectrum_output(input_file, output_file):
    combined_data = defaultdict(list)
    headers = []
    num_circles = defaultdict(int)

    # Read the CSV file and gather data
    with open(input_file, 'r') as csvfile:
        reader = csv.reader(csvfile)
        original_headers = next(reader)[1:]  # Get the headers, skipping the image name column

        # Filter out the "Circle" header and index the remaining headers
        filtered_indices = [i for i, header in enumerate(original_headers) if not header.lower().startswith("circle")]
        headers = [original_headers[i] for i in filtered_indices]

        for row in reader:
            image_name = row[0]  # Get the image name (first column)
            # Filter out the data corresponding to the "Circle" header and strip percentage signs
            data = [row[i + 1].replace('%', '') for i in filtered_indices]
            combined_data[image_name].append(data)  # Append the filtered data for this circle
            num_circles[image_name] += 1

    # Write the processed data into a new CSV file
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)

        # Prepare the final headers by duplicating the filtered headers for each circle
        max_circles = max(num_circles.values())
        final_headers = ["Image Name"]
        for i in range(1, max_circles + 1):
            final_headers.extend([f"{header} (Circle {i})" for header in headers])

        # Write the headers
        writer.writerow(final_headers)

        # Write the data
        for image_name, circles_data in combined_data.items():
            row = [image_name]
            for data in circles_data:
                row.extend(data)
            writer.writerow(row)

if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Process SnapSpectrum output")
    parser.add_argument('-i', '--input', type=str, required=True, help="Input CSV file path")
    parser.add_argument('-o', '--output', type=str, required=True, help="Output CSV file path")

    # Parse the arguments
    args = parser.parse_args()

    # Call the processing function with the provided arguments
    process_snapspectrum_output(args.input, args.output)
