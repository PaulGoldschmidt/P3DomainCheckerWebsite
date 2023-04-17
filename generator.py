import os
import json
from collections import defaultdict
from datetime import datetime
from jinja2 import Template

input_files_dir = "input-files"
domain_lists_dir = os.path.join(input_files_dir, "domain-lists")
log_dir = os.path.join(input_files_dir, "logs")
static_src_dir = "static-src"
output_dir = "output"

# Read the main.html template
with open(os.path.join(static_src_dir, "main.html"), "r") as file:
    main_html = file.read()

# Read the style.css content
with open(os.path.join(static_src_dir, "style.css"), "r") as file:
    style = file.read()

template = Template(main_html)

list_options = []
letter_counts = defaultdict(lambda: defaultdict(int))
max_datetime = None
max_log_date = ""

# Find the latest log file
for log_file in os.listdir(log_dir):
    if log_file.endswith(".log"):
        date_str = log_file[:15]
        current_datetime = datetime.strptime(date_str, "%Y%m%d_%H%M%S")

        if max_datetime is None or current_datetime > max_datetime:
            max_datetime = current_datetime
            max_log_date = date_str

# Read domain list files
for file_id, domain_list_file in enumerate(sorted(os.listdir(domain_lists_dir))):
    if domain_list_file.endswith(".txt"):
        with open(os.path.join(domain_lists_dir, domain_list_file), 'r') as file:
            domains = [line.strip() for line in file.readlines()]
            domain_count = len(domains)

            for domain in domains:
                first_letter = domain[0].lower()
                letter_counts[file_id][first_letter] += 1

            list_options.append('<option value="{}" data-letter-counts=\'{}\'>{} ({})</option>'.format(file_id, json.dumps(letter_counts[file_id]), domain_list_file, domain_count))

last_update_datetime = max_datetime.strftime("%Y-%m-%d %H:%M:%S")

# Generate the HTML content
content = template.render(style=style, list_options=list_options, domains_html=domains_html, last_update_datetime=last_update_datetime)

# Write the output HTML file
with open(os.path.join(output_dir, "index.html"), "w") as file:
    file.write(content)