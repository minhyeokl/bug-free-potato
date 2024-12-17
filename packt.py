import os
import glob
from bs4 import BeautifulSoup
from bs4.element import NavigableString

import argparse
import shutil

def edit_figcaption(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    # find all class=IMG---Caption in the html content
    for figure in soup.find_all('figure', class_='IMG---Caption'):
        figure.name = 'figcaption'
    html_content = str(soup)
    return html_content

def edit_links(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    # find all a tag in the html content
    for a_tag in soup.find_all('a'):
        if a_tag.get('href') is None:
            continue
        if a_tag.get('href').startswith('http'):
            href = a_tag['href']
            text = a_tag.text.strip()
            # create new elements
            new_text = NavigableString(f'{text}(')
            new_code = soup.new_tag('code')
            new_code.string = href.strip()
            new_paren = NavigableString(')')
            
            # combine new_text, new_code, and new_paren
            combined = BeautifulSoup(str(new_text) + str(new_code) + str(new_paren), 'html.parser')
            
            # replace the a tag with the new structure
            a_tag.replace_with(combined)
    html_content = str(soup)
    return html_content

def edit_pre_tags(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    # find all pre tag in the html content
    for pre_tag in soup.find_all('pre'):
        # add xml:space="preserve" attribute to the pre tag
        pre_tag['xml:space'] = 'preserve'
    html_content = str(soup)
    return html_content

def edit_html_files(file, output_dir):
    if os.path.isfile(file) and file.endswith(('.html', '.txt', '.css', '.js')):
        with open(file, 'r') as f:
            content = f.read()
        if file.endswith('.html'):
            content = edit_figcaption(content)
            content = edit_pre_tags(content)
            content = edit_links(content)
        output_file = os.path.join(output_dir, os.path.basename(file))
        with open(output_file, 'w') as f:
            f.write(content)
    else:
        output_file = os.path.join(output_dir, os.path.basename(file))
        if os.path.isdir(file):
            if not os.path.exists(output_file):
                shutil.copytree(file, output_file)
        else:
            shutil.copy(file, output_file)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Edit HTML content')
    parser.add_argument('--input', help='input directory', required=True)
    parser.add_argument('--output', help='output directory', required=False)
    args = parser.parse_args()

    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_dir = os.path.join(script_dir, args.input)
    output_dir = args.output

    if os.path.isdir(input_dir):
        subdirectories = [subdir for subdir in os.listdir(input_dir) if os.path.isdir(os.path.join(input_dir, subdir))]
    else:
        print(f"Directory {input_dir} does not exist.")
        # handle error here

    if output_dir is None:
        output_dir = os.path.join(script_dir, 'output', os.path.basename(input_dir))
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # get all files of input_dir itself not subdirectories.
    for file in glob.glob(os.path.join(input_dir, '*')):
        if os.path.isfile(file) and file.endswith(('.html', '.txt', '.css', '.js')):
            edit_html_files(file, output_dir)
        
    for subdir in subdirectories:
        input_subdir = os.path.join(input_dir, subdir)
        output_subdir = os.path.join(output_dir, subdir)
        if not os.path.exists(output_subdir):
            os.makedirs(output_subdir)
        for file in glob.glob(os.path.join(input_subdir, '**'), recursive=True):
            edit_html_files(file, output_subdir)