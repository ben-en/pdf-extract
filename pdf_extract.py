import bottle
import shutil
import hashlib
import argparse
import platform
import subprocess
import os
from os import getcwd
from os.path import join


def hash_url(url):
    md5 = hashlib.md5()
    md5.update(bytes(url))
    return md5.hexdigest()


def assemble_path(path, pdf):
    # Assemble path
    pdf_hash = hash_url(args.pdf)
    path = join(getcwd(), pdf_hash)
    if os.path.exists(path):
        shutil.rmtree(path)
        os.mkdir(path)
    else:
        os.mkdir(path)
    shutil.move(join(original_dir, args.pdf), join(path, args.pdf))


def get_cover(path, pdf):
    # Identify OS
    OS = platform.system()
    if OS == 'Windows':
        subprocess.call(["convert", join(path, args.pdf) + "[0]",
                         join(path, "cover.jpg")], shell = True)
    else:
        subprocess.call("convert " + join(path, args.pdf) + "[0] " +
                         join(path, "cover.jpg"), shell=True)


def build_landing(path, pdf, desc):
    # Build landing page
    html = bottle.template('template', title=pdf[:-4], desc=desc)
    with open(join(path, 'index.html'), 'w') as f:
        f.write(html)
    print html


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Takes a pdf in and gets a cover image from the first page'
    )
    parser.add_argument('pdf', metavar='FILE', help='pdf file to extract')
    parser.add_argument('description', metavar='FILE', default=None, help=
                        'description to use on pdf download page')
    args = parser.parse_args()

    original_dir = getcwd()
    bottle.TEMPLATE_PATH.insert(0, original_dir)
    shell = True

    assemble_path(path, pdf)

    get_cover(path, pdf)

    build_landing(path, pdf, description)
