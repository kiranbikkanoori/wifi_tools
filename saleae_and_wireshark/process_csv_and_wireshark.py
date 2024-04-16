import csv
from dateutil import parser
from sys import argv as argv
from datetime import datetime
import pyshark

month_dict = {
    'Jan': 1,
    'Feb': 2,
    'Mar': 3,
    'Apr': 4,
    'May': 5,
    'Jun': 6,
    'Jul': 7,
    'Aug': 8,
    'Sep': 9,
    'Oct' : 10,
    'Nov' : 11,
    'Dec' : 12,
}

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


def get_dt_object(time):
    time_split = time.split(' ')
    time_string = f'{time_split[3]}-{month_dict[time_split[0]]}-{time_split[2][:-1]} {time_split[4][:-3]}'
    # time_string = f'{time_split[2]}-{month_dict[time_split[0]]}-{time_split[1][:-1]} {time_split[3][:-3]}'
    time_dt_object = datetime.strptime(time_string, '%Y-%m-%d %H:%M:%S.%f')
    return time_dt_object

def get_rate_time(packet, starting_timestamp_dt_object):
    time_dt_object = get_dt_object(packet.frame_info.time)
    relative_time = time_dt_object - starting_timestamp_dt_object
    relative_time = relative_time.total_seconds() * 1000000
    duration = packet.layers[1].duration
    rate = packet.layers[1].data_rate
    return [int(relative_time), int(duration), float(rate)]



if __name__ == '__main__':
    saleae_file_path = argv[1]
    wireshark_file_path = argv[2]
    process_saleae_raw_data(saleae_file_path)
    wireshark_capture = read_wireshark_capture(wireshark_file_path)
    print(wireshark_capture[0])
