import os
import re
import shutil
from datetime import datetime

# Read main HTML content and styles.css from static-src directory
static_src_dir = "static-src"
with open(os.path.join(static_src_dir, "main.html"), "r") as file:
    main_html = file.read()

with open(os.path.join(static_src_dir, "styles.css"), "r") as file:
    styles_css = file.read()

# Read all text files from domain-lists directory
domain_lists_dir = "domain-lists"
domain_lists = {}
for filename in os.listdir(domain_lists_dir):
    if filename.endswith(".txt"):
        with open(os.path.join(domain_lists_dir, filename), "r") as file:
            domains = [line.strip() for line in file]
            domain_lists[filename] = sorted(domains, key=lambda s: s.lower())

# Create output directory
output_dir = "output"
if not os.path.exists(output_dir):
    os.mkdir(output_dir)

# Write styles.css to output directory
with open(os.path.join(output_dir, "styles.css"), "w") as file:
    file.write(styles_css)

# Generate domains_html for each domain list
domains_html = ""
list_options = ""
for filename, domains in domain_lists.items():
    list_name = filename[:-4]  # Remove .txt extension
    domains_html += f'<div class="domains" id="{list_name}" style="display:none;">\n'
    domains_html += f'    <p>Domain count: {len(domains)}</p>\n'
    if domains:
        domains_html += '    <ul class="domain-list">\n'
        for domain in domains:
            domains_html += f'        <li class="domain">{domain}</li>\n'
        domains_html += '    </ul>\n'
    else:
        domains_html += '    <p>Currently, there is no free domain on this list</p>\n'
    domains_html += '</div>\n'
    list_options += f'<option value="{list_name}">{list_name}</option>\n'

# Create index.html with main_html, list_options, and domains_html
with open(os.path.join(output_dir, "index.html"), "w") as file:
    file.write(main_html.format(list_options=list_options, domains_html=domains_html))