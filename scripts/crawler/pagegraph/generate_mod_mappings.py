import os
import csv

def make_mod_mapping():
    def create_dict(file_path):
        string_list = []
        with open(file_path, 'r') as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                if row:
                    
                    html_fname = row[0].split("/")[-1]
                    mapping_dict[".".join(html_fname.split(".")[:-1])] = row[1]

    def get_filenames_in_directory(directory_path):
        filenames = []
        urlnames = []
        for filename in os.listdir(directory_path):
            if os.path.isfile(os.path.join(directory_path, filename)):
                filenames.append(filename.split(".html")[0])
                # urlnames.append("_" + filename.split("_", 1)[1])
        return filenames, urlnames

    mapping_dict = {}

    dir_path = "/yopo-artifact/data/rendering_stream/modified_html_pagegraph"
    csv_file_path = "/yopo-artifact/data/rendering_stream/map_local_list_mod_final.csv"
    new_csv_file_path = "/yopo-artifact/data/rendering_stream/mod_mappings_pagegraph/map_mod_0.csv"
    
    filenames, urlnames = get_filenames_in_directory(dir_path)
    create_dict(csv_file_path)
    
    lines = []
    prefix = "/yopo-artifact/data/rendering_stream/modified_html_pagegraph/"
    for fname in enumerate(filenames):
        key = "_".join(fname[1].split("_")[:-1])
        # final_url = mapping_dict[fname[1]]
        final_url = mapping_dict[key]
        if final_url:
            lines.append([prefix + fname[1] + ".html", final_url])
        else:
            raise("No elements in mapping dict!")
    
    with open(new_csv_file_path, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        for line in lines:
            writer.writerow(line)
    
    
def split_csv():
    turn = 0
    while(True):
        # Specify the path to the original CSV file
        # original_csv_file = '/yopo-artifact/data/rendering_stream/mod_mappings_adgraph/map_mod_{}.csv'.format(turn)
        original_csv_file = '/yopo-artifact/data/rendering_stream/mod_mappings_pagegraph/map_mod_{}.csv'.format(turn)

        # Create two separate lists for unique and duplicate values
        unique_domain = []
        unique_values = []
        duplicate_values = []

        # Read the original CSV file and split it based on the second column
        with open(original_csv_file, 'r') as csv_file:
            reader = csv.reader(csv_file)
            
            for row in reader:
                if row[1] not in unique_domain:
                    unique_domain.append(row[1])
                    unique_values.append(row)
                else:
                    duplicate_values.append(row)
                    print(row[1])
        if len(duplicate_values) == 0:
            break

        # Write the remaining values to another CSV file
        with open('/yopo-artifact/data/rendering_stream/mod_mappings_pagegraph/map_mod_{}.csv'.format(turn), 'w', newline='') as remaining_file:
            writer = csv.writer(remaining_file)
            writer.writerows([[row[0], row[1]] for row in unique_values])
            
        # Write the unique values to a new CSV file
        with open('/yopo-artifact/data/rendering_stream/mod_mappings_pagegraph/map_mod_{}.csv'.format(turn + 1), 'w', newline='') as unique_file:
            writer = csv.writer(unique_file)
            writer.writerows([[row[0], row[1]] for row in duplicate_values])
        

        turn += 1

make_mod_mapping()
split_csv()