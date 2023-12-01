import os
import re

import requests
from markdown import markdown
import argparse


def read_file(filename):
    try:
        with open(filename, 'r') as file:
            content = file.read()
            return content
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
        return None


def extract_links_from_markdown(markdown_text):
    if markdown_text is None:
        return [], []

    html = markdown(markdown_text)

    link_pattern = r'<a\s+(?:[^>]*?\s+)?href="([^"]*)"'
    image_pattern = r'<img\s+(?:[^>]*?\s+)?src="([^"]*)"'

    links = re.findall(link_pattern, html)
    images = re.findall(image_pattern, html)
    return links, images


def find_files(directory, filename):
    files_list = []

    for root, directories, files in os.walk(directory):
        for file in files:
            if file == filename:
                files_list.append(os.path.join(root, file))

    return files_list


def check_link(task_folder, link):
    try:

        if link.startswith('course://'):
            internal_resource_link = link[len('course://'):]
            internal_resource_path = f"{course_directory}/{internal_resource_link}"
            if not (os.path.isfile(internal_resource_path) or os.path.isdir(internal_resource_path)):
                return False, f"NO such file: {internal_resource_path}"
            else:
                return True, ""
        elif link.startswith(('http://', 'https://')):
            response = requests.head(link)
            if response.status_code != 200:
                return False, f"NOT valid url (returns {response.status_code}): {link}"
            else:
                return True, ""
        elif link.startswith(('file://', 'psi_element://', 'tool_window://', 'settings://')):
            return True, ""  # Not supported for now
        else:  # Assumes that it's a relative path
            path = f"{task_folder}/{link}"
            if not (os.path.isfile(path) or os.path.isdir(path)):
                return False, f"NO such file: {path}"
            return True, ""

    except Exception as e:
        return False, str(e)


if __name__ == '__main__':
    args = sys.argv
    if len(args) < 2:
        print("No path provided")
        exti(1)
    

    course_directory = args[1]
    task_description_name = 'task.md'

    print("\n===== Common info =====")
    print(f"Running for directory {course_directory} (absolute path: {os.path.abspath(course_directory)})")

    task_files = find_files(course_directory, task_description_name)

    print(f"\n===== The following links were found =====")
    errors_log = ""

    for file in task_files:
        print(f"FILE: {file}")
        links, images = extract_links_from_markdown(read_file(file))
        links.extend(images)
        task_folder = file[:file.rfind("/")]

        for link in links:
            print(f"\t LINK: {link}")
            result, log = check_link(task_folder, link)
            if not result:
                errors_log += f"Error in file: {file}\n\t{log}\n"

    print("\n===== ERRORS LOG =====")
    if len(errors_log) > 0:
        print(errors_log)
        exit(1)
    else:
        print("No errors found")
        exit(0)

# TODO:
# Remove path to course from input
# Make as linked github action
