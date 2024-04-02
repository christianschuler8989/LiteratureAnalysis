
import csv
import requests
#import urllib.request
import os
import sys
import time


""" Usage:
[Install]
pip install requests

cd /media/CrazyProjects/LowResDialectology/LiteratureAnalysis/DataCollector/src

source ./../../venvLA/bin/activate

python3 main.py

"""

"""
Helper-Function to create new directories (if not existing)
"""
def create_directory(directory_path):
  if not os.path.exists(directory_path):
    os.mkdir(directory_path)
    print("Folder %s created!" % directory_path)
  else:
    print("Folder %s already exists" % directory_path)

project_name = "SeleniumToZotero_2024_04_02"

project_path = f'./../{project_name}/'
create_directory(project_path)
selenium_input_path = f'./../{project_name}/input_to_selenium/' # TODO: Queries and such
create_directory(selenium_input_path)
selenium_output_path = f'./../{project_name}/output_from_selenium/' # Post-Crawl
create_directory(selenium_output_path)

intermediate_files_path = f'./../{project_name}/intermediate_files/'
create_directory(intermediate_files_path)
intermediate_sorted_path = f'{intermediate_files_path}sorted_csvs/'
create_directory(intermediate_sorted_path)
intermediate_cleaned_path = f'{intermediate_files_path}cleaned_csvs/'
create_directory(intermediate_cleaned_path)

output_path = f'./../{project_name}/output/'
create_directory(output_path)
document_output_path = f'./../{project_name}/output/documents/'
create_directory(document_output_path)
information_output_path = f'./../{project_name}/output/information/'
create_directory(information_output_path)


# NOTE: Rename .csv files from Selenium to start wird "selenium_googlescholar_" 
#       and move them into selenium_input_path = f'./../{project_name}/input_to_selenium/'

"""
Helper Function to keep track of variables with exceptions constantly stopping the script
"""
def append_line_to_txt_file(text_line, output_file):
   with open(f'{output_file}','a+') as text_file:
      text_file.write(text_line.replace('\n','')+'\n')


# =============================================================================
#
# Detect duplicates inside the .csv files from Selenium and group them in general
#
def detect_and_group_duplicates(selenium_output_path, intermediate_sorted_path):
  create_directory(f'{intermediate_sorted_path}')
  input_file_paths = []

  # Iterate over files in that directory
  for filename in os.listdir(selenium_output_path):
    f = os.path.join(selenium_output_path, filename)
    # Checking if it is a file
    if os.path.isfile(f):
       input_file_paths.append(f)
  """
  input_file_paths = [
    f'{selenium_output_path}selenium_googlescholar_central_kurdish_output-data-0823.csv',
    f'{selenium_output_path}selenium_googlescholar_gorani_kurdish_output-data-1611.csv',
    f'{selenium_output_path}selenium_googlescholar_laki_kurdish_output-data-0011.csv',
    f'{selenium_output_path}selenium_googlescholar_lori_kurdish_output-data-2251.csv',
    f'{selenium_output_path}selenium_googlescholar_northern_kurdish_output-data-2109.csv',
    f'{selenium_output_path}selenium_googlescholar_southern_kurdish_output-data-1607.csv',
    f'{selenium_output_path}selenium_googlescholar_zazaki_kurdish_output-data-1955.csv',
  ]
  """
  # NOTE: A List of Lists of Rows from the .csv files in order to sort out the duplicates
  """
  all_rows_list = [ 
    [ # The first .csv file
      [file1_row1_item1, file1_row1_item2, ...],
      [file1_row2_item1, file1_row2_item2, ...],
    ],
    [ # The second .csv file
      [file2_row1_item1, file2_row1_item2, ...],
      [file2_row2_item1, file2_row2_item2, ...],
    ], ...
    [ # The duplicates found in more than one .csv file
      [new_row1_item1, new_row1_item2, ...],
      [new_row2_item1, new_row2_item2, ...],
    ]
  ]
  """
  all_rows_lists = []

  for input_file in input_file_paths:
    current_file_rows = []
    # Keep filename for later writing intermediate files
    input_file_basename = os.path.basename(input_file).split('.')[0] # Without .csv extension
    input_name_part = input_file_basename.split('_')[2]
    current_file_rows.append(input_name_part)

    # Read the .csv file and process each row
    with open(input_file, newline='') as csv_file:
      csv_reader = csv.reader(csv_file, delimiter=',', quotechar='"')
      
      # Get all rows
      for row in csv_reader:
        clean_row = []
        for item in row:
          clean_item = item.replace('\n','')
          clean_row.append(clean_item)
        current_file_rows.append(clean_row)

    all_rows_lists.append(current_file_rows)

  # Once all rows from all files are collected, check for duplicates
  duplicate_rows_list = []
  duplicate_rows_list.append('duplicates')
  # Walk through all lists of row-lists (.csv files)
  for list_index in range(len(all_rows_lists)):
    # For the current row-list
    row_list = all_rows_lists[list_index]
    # From index 1 (0 is name of output file for corresponding list)
    for row in row_list[1:]:
      # Check all still remaining lists
      for row_remaining_list in all_rows_lists[list_index+1:]:
         # Row-by-Row (starting at index 1, since 0 is the header)
        for remaining_row in row_remaining_list[1:]:
          # For duplicate rows (without 1 element, which is the search query)
          if row[1:] == remaining_row[1:]:
            duplicate_rows_list.append(row[1:])
       
  all_rows_lists.append(duplicate_rows_list)

  # Safe new assortment of lists to intermediate .csv files
  for row_list in all_rows_lists:
    # First element of list is name of output file
    with open(f'{intermediate_sorted_path}{row_list[0]}.csv', 'w', newline='') as csv_file:
      csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
      for row in row_list[1:]:
        csv_writer.writerow(row)
    print(f'Number of items in {row_list[0]}: {len(row_list)-1}')


# =============================================================================
#
# Remove detected duplicates inside the .csv files from Selenium
#
def remove_duplicates(intermediate_sorted_path, intermediate_cleaned_path):
  create_directory(f'{intermediate_cleaned_path}')
  input_file_paths = []

  # Iterate over files in that directory
  for filename in os.listdir(f'{intermediate_sorted_path}'):
    f = os.path.join(f'{intermediate_sorted_path}', filename)
    # Checking if it is a file
    if os.path.isfile(f):
      input_file_paths.append(f)
    """
    Filenames inside of
    input_file_paths = [
      'central.csv',
      'duplicates.csv',
      'gorani.csv'
      'laki.csv',
      'lori.csv',
      'northern.csv',
      'southern.csv',
      'zazaki.csv'
    ]
    """
  
  # Read duplicates for comparing with each of the other files
  duplicate_file_rows = []
  with open(f'{intermediate_sorted_path}duplicates.csv',newline='') as csv_file:
     csv_reader = csv.reader(csv_file, delimiter=',', quotechar='"')
     for row in csv_reader:
        duplicate_file_rows.append(row)

  for input_file in input_file_paths:
    current_file_rows = []
    if not input_file.endswith('duplicates.csv'):
      input_file_basename = os.path.basename(input_file)
      
      # Read the .csv file and process each row
      with open(input_file, newline='') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',', quotechar='"')
        # Get all rows
        for row in csv_reader:
          clean_row = []
          for item in row:
            clean_item = item.replace('\n','')
            clean_row.append(clean_item)
          current_file_rows.append(clean_row)

      unique_current_file_rows = current_file_rows
      # Check against duplicates (ignoring the header row)
      for row in current_file_rows[1:]:
        for duplicate_row in duplicate_file_rows[1:]:
          # Check row without the query (query already removed from duplicate rowes)
          if row[1:] == duplicate_row:
            #print(f'Removing row: {row}') # Debugging
            if row in unique_current_file_rows:
              unique_current_file_rows.remove(row)  

    # Safe the (now only unique rows containing) data to file
    with open(f'{intermediate_cleaned_path}{input_file_basename}', 'w', newline='') as csv_file:
      csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
      for row in unique_current_file_rows:
        csv_writer.writerow(row)
    print(f'Number of unique items in {input_file_basename}: {len(unique_current_file_rows)-1}')


# =============================================================================
#
# Download .pdf files with filename and origin URL from .csv file
#
""" 
INPUT such as:
input_file = 'selenium_googlescholar_central_1457.csv'
input_file_basename = 'selenium_googlescholar_central_1457'
input_name_part = 'central'
output_path = './../SeleniumToZotero/OutputFromSelenium/'
starting_row_position = 249
"""
def csv_to_download(input_file, input_file_basename, document_output_path, information_output_path, starting_row_position=1):
  
  #print(f'Debugging: Enter csv_to_download() with')
  #print(f'input_file: {input_file}\n input_file_basename:{input_file_basename}\n input_name_part:{input_name_part}\n document_output_path:{document_output_path}\n information_output_path:{information_output_path}\n starting_row_position:{starting_row_position}')
  
  # Check whether output directory for current file already exists
  output_path = f'{document_output_path}{input_file_basename}'
  if not os.path.isdir(output_path):
    create_directory(output_path)
  intermediate_path = f'{information_output_path}{input_file_basename}'
  if not os.path.isdir(intermediate_path):
    create_directory(intermediate_path)

  # Intermediate files to write to
  inter_title = f'{intermediate_path}/inter_titles.txt'
  inter_url = f'{intermediate_path}/inter_url.txt'
  inter_author = f'{intermediate_path}/inter_author.txt'
  inter_author_modified = f'{intermediate_path}/inter_author_mod.txt'
  inter_title_modified = f'{intermediate_path}/inter_titles_mod.txt'
  inter_url_failed = f'{intermediate_path}/inter_url_failed.txt'

  # Read .csv file with following structure:
  # → "Topic","hauptTitelText","HauptTitelAlsLink","HaupttitelExtendPDF","hauptTitelExtendPDFLink","BeschreibungAlsText"
  csv_rows_list = []

  with open(input_file, newline='') as csv_file: # Central
    csv_reader = csv.reader(csv_file, delimiter=',', quotechar='"')

    # Debugging for Sanity
    #print(f'Entered csv_reader.')
    #sanity_counter = 0

    # Get all rows
    for row in csv_reader:
      csv_rows_list.append(row)
      # Debugging for Sanity
      #print(f'title: {row[1]}')
      #print(f'sanity_counter: {sanity_counter}')
      #sanity_counter += 1

  # Debugging for Sanity
  #print(f'len(csv_rows_list): {len(csv_rows_list)}')

  # Process each row from .csv file- but skip the header row
  for row in csv_rows_list[starting_row_position:]:
    
    # Safe original strings to file for easy tracking of links later on
    original_titel = row[1]
    append_line_to_txt_file(original_titel, inter_title)
    original_url = row[4]
    append_line_to_txt_file(original_url, inter_url)
    original_author = row[6]
    append_line_to_txt_file(original_author, inter_author)

    # Get crucial variable values
    current_author = row[6].replace('\n','').replace('.','').replace(',','') \
      .replace(':','').replace(';','').replace("'","").replace('"','') \
      .replace('“','').replace('-','').replace('?','').replace('!','') \
      .replace('(','').replace(')','').replace('[','').replace(']','') \
      .replace('{','').replace('}','').replace('®','').replace('/','') \
      .replace(' ','_')
    current_title = row[1].replace('\n','').replace('.','').replace(',','') \
      .replace(':','').replace(';','').replace("'","").replace('"','') \
      .replace('“','').replace('-','').replace('?','').replace('!','') \
      .replace('(','').replace(')','').replace('[','').replace(']','') \
      .replace('{','').replace('}','').replace('®','').replace('/','') \
      .replace(' ','_')
    # Reduce length for output .pdf filename in length
    current_author = current_author[:30]
    current_title = current_title[:30]
    output_author_title = f'{current_author}-{current_title}'
    
    # Safe modified strings to file for easy tracking of links later on
    append_line_to_txt_file(current_author, inter_author_modified)
    append_line_to_txt_file(current_title, inter_title_modified)
    
    current_url = row[4].replace('\n','').replace(' ','')
    current_extension = 'pdf' # NOTE: Not every URL ends with .pdf → How to handle those cases?

    # Debugging for Sanity
    #print(f'current_title: {current_title}')

    # Check if URL for download exists (without URL, no download possible)
    if not current_url == '':
      
      # File-Naming Variable
      output_file_name = f'{input_file_basename}-{output_author_title}'

      # Path and name of new file after download
      # Such as: 'selenium_googlescholar_central_1457/On_the_linguistic_history_of_Kurdish'
      new_file_destination = f'{output_path}/{output_file_name}'

      # Debugging
      print(f'==== Attempt to download from: {current_url}')
      print(f'        To destination: {new_file_destination}')
      
      # Base write_mode on file extension ("write binary" for "non-text" file extensions)
      write_mode = 'wb' if current_extension in ('gz','zip','jpg','png','exe','pdf') else 'w'

      # NOTE: Retry-Function to prevent script interruption due to exception with ConnectionError
      # Based on https://stackoverflow.com/questions/44448625/how-to-handle-a-connection-error-gracefully-in-requests
      connection_timeout = 30 # seconds
      start_time = time.time()
      while True:
        # Trying to connect in order to download the pdf file
        try:
          #get_updates = json.loads(requests.get(url + 'getUpdates').content) #NOTE: From online example code
          # Server response handling
          response = requests.get(current_url, verify=False) #NOTE: Not the best idea, but the exceptions are very annoying!

          if response.status_code == 200:
              
              # Write downloaded data to file (either binary content or text)
              with open(f'{new_file_destination}.{current_extension}', write_mode) as file:
                  file.write(response.content if write_mode == 'wb' else response.text)
              print(f"File downloaded successfully and saved at: {output_path}")
          else:
              print(f"Failed to download file. Status code: {response.status_code}")
          break

        # If the connection encounters an exception with a ConnectionError, retry a few times
        except ConnectionError:
          if time.time() > start_time + connection_timeout:
            raise Exception('Unable to get updates after {} seconds of ConnectionErrors'.format(connection_timeout))
          else:
            time.sleep(8) # attempting once every 8 seconds

    # Skip .csv file entries missing an URL
    else:
      #print("Found empty String, continue with next row.")
       # TODO: Handle missing/faulty URLs
       failed_url_title_url = row[2]
       append_line_to_txt_file(failed_url_title_url, inter_url_failed)

# =============================================================================
def execute_csv_to_download(intermediate_cleaned_path):
  #print(f'Debugging: Enter execute_csv_to_download() with')
  #print(f'intermediate_cleaned_path: {intermediate_cleaned_path}')

  # =============================================================================
  # Input files from Ramans Selenium run on GoogleScholar
  # → "Topic","hauptTitelText","HauptTitelAlsLink","HaupttitelExtendPDF","hauptTitelExtendPDFLink","BeschreibungAlsText"
  #input_path = './../SeleniumToZotero/InputFromSelenium/' # Replaced by selenium_output_path
  input_file_paths = []

  # Iterate over files in that directory
  for filename in os.listdir(intermediate_cleaned_path):
    f = os.path.join(intermediate_cleaned_path, filename)
    # Checking if it is a file
    if os.path.isfile(f):
       input_file_paths.append(f)
  #input_file_names = [
  #  f'{intermediate_cleaned_path}central.csv',
  #  f'{intermediate_cleaned_path}gorani.csv
  #  f'{intermediate_cleaned_path}laki.csv',
  #  f'{intermediate_cleaned_path}lori.csv',
  #  f'{intermediate_cleaned_path}northern.csv',
  #  f'{intermediate_cleaned_path}southern.csv',
  #  f'{intermediate_cleaned_path}zazaki.csv'
  #]
  
  # =============================================================================
  # Downloading the pdf files into output_path  # NOTE: Huh? → Output files only containing the URLs based on the input file naming
  #output_path = './../SeleniumToZotero/OutputFromSelenium/' # Replaced by document_output_path

  for input_file in input_file_paths:
    # Get file basename
    # input_file_basename == "selenium_googlescholar_central_1457.csv"
    # input_file_basename[0].split('.') == "selenium_googlescholar_central_1457"
    # input_name_part == "central"
    input_file_basename = os.path.basename(input_file).split('.')[0] # Without .csv extension
    #print(f'input_file_basename: {input_file_basename}')

    starting_row_position = 1 # Default Value
    # NOTE: Handling problematic items by skipping them and rerun script
    if input_file_basename == 'german':
      starting_row_position = 53
      csv_to_download(input_file, input_file_basename, document_output_path, information_output_path, starting_row_position)

    # if input_file_basename == 'central':
    #   starting_row_position = 1
    #   # NOTE: 
    #   #csv_to_download(input_file, input_file_basename, document_output_path, information_output_path, starting_row_position)

    # elif input_file_basename == 'gorani':
    #   starting_row_position = 1 
    #   #csv_to_download(input_file, input_file_basename, document_output_path, information_output_path, starting_row_position)

    # elif input_file_basename == 'laki':
    #   #starting_row_position = 1 
    #   #starting_row_position = 122 
    #   #starting_row_position = 167
    #   starting_row_position = 206
    #   csv_to_download(input_file, input_file_basename, document_output_path, information_output_path, starting_row_position)

    # elif input_file_basename == 'lori':
    #   starting_row_position = 1 
    #   #starting_row_position = 103
    #   #starting_row_position = 188
    #   #starting_row_position = 301
    #   #csv_to_download(input_file, input_file_basename, document_output_path, information_output_path, starting_row_position)

    # elif input_file_basename == 'northern':
    #   starting_row_position = 1
    #   # NOTE: DONE
    #   #csv_to_download(input_file, input_file_basename, document_output_path, information_output_path, starting_row_position)
    
    # elif input_file_basename == 'southern':
    #   starting_row_position = 1
    #   # NOTE: DONE
    #   #csv_to_download(input_file, input_file_basename, document_output_path, information_output_path, starting_row_position)

    # elif input_file_basename == 'zazaki':
    #   starting_row_position = 1 
    #   #csv_to_download(input_file, input_file_basename, document_output_path, information_output_path, starting_row_position)


""" ===========================================================================
Download .pdf files via requests directly from .csv file using the original titles
"""
# =============================================================================
# EXECUTION NOTE: One at a time!

# NOTE: Make sure to take care of file naming such as: selenium_googlesholar_german_german_output-data-1735.csv
# General clean up of formats and data transformations
#detect_and_group_duplicates(selenium_output_path, intermediate_sorted_path)

# TODO: Fix problem in cae of 0 duplicates . . .
"""
Traceback (most recent call last):
  File "/media/CrazyProjects/LowResDialectology/LiteratureAnalysis/DataCollector/src/main.py", line 466, in <module>
    remove_duplicates(intermediate_sorted_path, intermediate_cleaned_path)
  File "/media/CrazyProjects/LowResDialectology/LiteratureAnalysis/DataCollector/src/main.py", line 223, in remove_duplicates
    with open(f'{intermediate_cleaned_path}{input_file_basename}', 'w', newline='') as csv_file:
UnboundLocalError: local variable 'input_file_basename' referenced before assignment
"""
# Reducing the load on the network by removing duplicates
#remove_duplicates(intermediate_sorted_path, intermediate_cleaned_path)

# Execute the downloading for each of these new files (might take some time)
execute_csv_to_download(intermediate_cleaned_path)


