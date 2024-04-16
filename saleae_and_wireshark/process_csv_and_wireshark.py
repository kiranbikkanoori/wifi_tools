import csv
from dateutil import parser
from sys import argv as argv
import pyshark

#test commnet
def process_saleae_raw_data(ip_file_path):
    # Initialize row index and lists
    row_index = 0
    row_list = []
    debug_list = []
    prev_line = ['0', '0']

    # Open the input file in read mode
    ip_file = open(ip_file_path, mode='r')
    csvfile = csv.reader(ip_file)

    # Open the output file in write mode
    op_file = open('processed_data.csv', mode='w')
    writer = csv.writer(op_file)
    # Define the field names for the output file
    field = ["Timestamp", "RelativeTS", "LogicData", "Width(us)"]
    # Write the field names to the output file
    writer.writerow(field)

    # Loop through each line in the input file
    for lines in csvfile:
        # Append the line to the row list
        row_list.append(lines)
        # If this is not the first line
        if row_index > 0:
            # If this is the second line
            if row_index == 1:
                # Parse the timestamp from the line
                start_timestamp = parser.isoparse(lines[0])
                # Store the line as the previous line
                prev_line = lines
            else:
                # If the LogicData value has changed
                if lines[1] != prev_line[1]:
                    # Calculate the width in microseconds
                    width = parser.isoparse(lines[0]) - parser.isoparse(prev_line[0])
                    width = int(width.total_seconds() * 1000000)
                    # Calculate the relative timestamp in microseconds
                    relative_timestamp = parser.isoparse(prev_line[0]) - start_timestamp
                    relative_timestamp = int(relative_timestamp.total_seconds() * 1000000)
                    # Write the data to the output file
                    writer.writerow([str(start_timestamp), str(relative_timestamp), str(prev_line[1]), str(width)])
                    # Append the data to the debug list
                    debug_list.append([str(prev_line), str(lines), str(width)])
                    # Store the line as the previous line
                    prev_line = lines
        # Increment the row index
        row_index += 1
    # Close the input and output files
    ip_file.close()
    op_file.close()


def read_wireshark_capture(ip_file_path):
    capture = pyshark.FileCapture(ip_file_path)
    return capture


def get_packet(capture, packet_number):
    if not packet_number:
        return None
    return capture[packet_number - 1]


if __name__ == '__main__':
    saleae_file_path = argv[1]
    wireshark_file_path = argv[2]
    process_saleae_raw_data(saleae_file_path)
    wireshark_capture = read_wireshark_capture(wireshark_file_path)
    print(wireshark_capture[0])
