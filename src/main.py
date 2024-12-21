import textnode
import htmlnode
from markdown_to_html import *
import os
import shutil
import re


def clean_and_copy(src_dir, dest_dir):
    if not os.path.exists(src_dir):
        raise FileNotFoundError(f"dir: {src_dir} not found")

    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)

    
    shutil.copytree(src_dir,dest_dir)

def get_file_content(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()  # Read the entire content of the file
    return content

def extract_title(html):
    h1 = re.findall(r"<h1>.*?</h1>",html,re.DOTALL)[0].replace("\n","")
    return h1[h1.find(">")+1:-5]
    
    
    
    


def generate_page(from_path, template_path, dest_path):
    html_template = get_file_content(template_path)

    for file in os.listdir(from_path): 
        
        if os.path.isdir(os.path.join(from_path,file)):
            print(file)
            new_dest = os.path.join(dest_path,file)
            new_from = os.path.join(from_path,file)
            os.mkdir(new_dest)
            generate_page(new_from,template_path,new_dest)
            continue

        file_content = get_file_content(os.path.join(from_path,file))
        markdown_file_name = os.path.basename(file)
        
        content_as_html = markdown_to_html(file_content)
        title = extract_title(content_as_html)

        html = html_template.replace("{{ Content }}",content_as_html).replace("{{ Title }}", title)
        html_file_path = os.path.join(dest_path,markdown_file_name.replace(".md",".html"))
        with open(html_file_path,"w") as html_file:
            html_file.write(html)



         



def main():
    cwd = os.getcwd()
    
    src =  os.path.join(cwd,"static")
    dest = os.path.join(cwd,"public")

    clean_and_copy(src,dest)


    template = os.path.join(cwd,"template.html")
    markdown_path = os.path.join(cwd,"content")
    html_path = os.path.join(cwd,"public")

    generate_page(markdown_path, template, html_path)


main()

