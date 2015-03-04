import os
import sys
import bottle
import shutil
import hashlib
import argparse
import platform
import subprocess
from os import getcwd
from os.path import join

sys.path.insert(0, os.path.normpath('../artexin'))

from artexin.pack import zipdir


def hash_url(url):
    md5 = hashlib.md5()
    md5.update(bytes(url, 'utf-8'))
    return md5.hexdigest()


def assemble_path(path, pdf, pdf_dir):
    # Assemble path
    if os.path.exists(path):
        shutil.rmtree(path)
        os.mkdir(path)
    else:
        os.mkdir(path)
    shutil.move(join(pdf_dir, pdf), join(path, pdf))


def get_cover(path, pdf):
    # Identify OS
    OS = platform.system()
    if OS == 'Windows':
        subprocess.call(["convert", join(path, pdf) + "[0]",
                         join(path, "cover.jpg")], shell=True)
    else:
        subprocess.call("convert '" + os.path.normpath(join(path, pdf)) +
                        "'[0] '" + os.path.normpath(join(path, "cover.jpg")) +
                        "'", shell=True)


def build_landing(path, pdf, desc):
    # Build landing page
    html = bottle.template('template', title=pdf[:-4].title(), desc=desc)
    with open(join(path, 'index.html'), 'w') as f:
        f.write(html)


def worker(pdf):
    shell = True
    pdf_hash = hash_url(pdf)
    path = join(pdf_dir, pdf_hash)

    desc = "This PDF was gathered in bulk from KARI.org. As a result, no "\
            "information is available for this file."

    assemble_path(path, pdf, pdf_dir)

    get_cover(path, pdf)

    build_landing(path, pdf, desc)

    zipdir(path + '.zip', path)


def process_pdf(pdf, desc):
    pdf_dir = os.path.dirname(os.path.abspath(pdf))
    print(pdf_dir)
    pdf_hash = hash_url(pdf)
    path = join(getcwd(), pdf_hash)

    assemble_path(path, pdf, pdf_dir)

    get_cover(path, pdf)

    build_landing(path, pdf, desc)

    zipdir(path + '.zip', path)


def process_dir(pdfdir, desc):
    import multiprocessing
    global pdf_dir
    pdf_dir = pdfdir

    # Prepare list to process
    pdfs = []
    for pdf in os.listdir(pdf_dir):
        if pdf.endswith(".pdf"):
            pdfs.append(pdf)

    # Begin processing
    print('Beginning multiprocessing')
    manager = multiprocessing.Manager()

    oklog = manager.list()
    faillog = manager.list()

    if not len(pdfs) > 10:
        pool_size = len(pdfs)
    else:
        pool_size = 10

    pool = multiprocessing.Pool(pool_size)
    results = pool.map(worker, pdfs)
    pool.close()
    pool.join()
    print('Multiprocessing complete, writing results')

    # Process Results
    failed_urls = open('failed.urls', 'w')
    succeeded_urls = open('succeeded.urls', 'w')
    for url in faillog:
        failed_urls.write(url)
    for url in oklog:
        succeeded_urls.write(url)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Takes a pdf in and gets a cover image from the first page'
    )
    parser.add_argument('pdf', metavar='FILE', help='pdf file to extract')
    parser.add_argument('-d', help='indicates directory of pdfs',
                        action='store_true')
    parser.add_argument('--desc', metavar='STRING', default=None, help=
                        'description to use on pdf download page')
    args = parser.parse_args()

    script_dir = os.path.dirname(os.path.realpath(__file__))
    bottle.TEMPLATE_PATH.insert(0, script_dir)

    if args.d:
        process_dir(args.pdf, args.desc)
    elif not args.d:
        process_pdf(args.pdf, args.desc)
