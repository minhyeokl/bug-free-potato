import os
import glob
from bs4 import BeautifulSoup
from bs4.element import NavigableString

import argparse
import shutil

def edit_header(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    # find all sections in the html content and check data-type attribute.
    # if data-type is chapter then pass
    # if data-type is sect1 then replace the h1 tag to h2 tag
    # if data-type is sect2 then replace the h2 tag to h3 tag
    # if data-type is sect3 then replace the h3 tag to h4 tag
    for section in soup.find_all('section'):
        data_type = section.get('data-type')
        if data_type == 'sect1':
            h1_tag = section.find('h1')
            if h1_tag:
                h1_tag.name = 'h2'
        elif data_type == 'sect2':
            h2_tag = section.find('h2')
            if h2_tag:
                h2_tag.name = 'h3'
        elif data_type == 'sect3':
            h3_tag = section.find('h3')
            if h3_tag:
                h3_tag.name = 'h4'
    html_content = str(soup)
    return html_content

def sidebar_edit(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    # find all aside tag in the html content
    # if aside tag's data-type attribute is sidebar replace aside tag into p tag
    for aside in soup.find_all('aside'):
        data_type = aside.get('data-type')
        if data_type == 'sidebar':
            aside.name = 'section'
            # replace first h1 tag to p tag and add custom-style attribute 박스_제목
            # add blank p tag with custom-style attribute 박스_끝 at the end of the aside tag
            h1_tag = aside.find('h1')
            if h1_tag:
                h1_tag.name = 'div'
                h1_tag['custom-style'] = '박스_제목'
            else:
                div_tag = soup.new_tag('div')
                div_tag['custom-style'] = '박스_제목'
                div_tag.string = '<박스>'
                aside.insert(0, div_tag)
            div_tag = soup.new_tag('div')
            div_tag['custom-style'] = '박스_끝'
            # add &nbsp to div_tag content
            div_tag.string = '</박스>'
            aside.append(div_tag)
            # remove aside tag and keep the content
            aside.unwrap()
    html_content = str(soup)
    return html_content

def edit_note(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    # find all data-type="note" tag in the html content
    # add custom-style attribute 노트 to the div tag
    for note in soup.find_all('div', {'data-type': 'note'}):
        note['custom-style'] = '노트'
        # make the h6 tag to bold p tag and apply b tag to text
        h6_tag = note.find('h6')
        if h6_tag:
            h6_tag.name = 'p'
            b_tag = soup.new_tag('b')
            b_tag.string = "Note_ " + h6_tag.text
            h6_tag.string = ''
            h6_tag.append(b_tag)
    html_content = str(soup)
    return html_content

def edit_tip(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    # find all data-type="tip" tag in the html content
    # add custom-style attribute 노트 to the div tag
    for tip in soup.find_all('div', {'data-type': 'tip'}):
        tip['custom-style'] = '팁'
        # make the h6 tag to bold p tag and apply b tag to text
        h6_tag = tip.find('h6')
        if h6_tag:
            h6_tag.name = 'p'
            b_tag = soup.new_tag('b')
            b_tag.string = "Tip_ " + h6_tag.text
            h6_tag.string = ''
            h6_tag.append(b_tag)
    html_content = str(soup)
    return html_content

def edit_warning(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    # find all data-type="warning" tag in the html content
    # add custom-style attribute 노트 to the div tag
    for warning in soup.find_all('div', {'data-type': 'warning'}):
        warning['custom-style'] = '경고'
        # make the h6 tag to bold p tag and apply b tag to text
        h6_tag = warning.find('h6')
        if h6_tag:
            h6_tag.name = 'p'
            b_tag = soup.new_tag('b')
            b_tag.string = "Warning_ " + h6_tag.text
            h6_tag.string = ''
            h6_tag.append(b_tag)
    html_content = str(soup)
    return html_content

def edit_figcaption(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    # find all figure tag in the html content
    for figure in soup.find_all('figure'):
        figcaption = figure.find('h6')
        if figcaption:
            figcaption.name = 'figcaption'
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
            content = edit_header(content)
            content = sidebar_edit(content)
            content = edit_note(content)
            content = edit_tip(content)
            content = edit_warning(content)
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