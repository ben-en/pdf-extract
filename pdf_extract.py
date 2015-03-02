import os
import argparse
import subprocess


def get_cover(path, pdf):
    """ Takes the first page of the pdf and writes it to an image (cover.jpg)
    """
    subprocess.call('convert %s%s[0] %scover.jpg' % (path, pdf, path), shell=True)
# identify working directory
# identify OS (win/lin)
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Takes a pdf in and gets a cover image from the first page'
    )
    parser.add_argument('pdf', metavar='FILE', help='pdf file to extract')
    parser.add_argument('description', metavar='FILE', default=None, help=
                        'description to use on pdf download page')
    args = parser.parse_args()
    get_cover(r'd:\\', 'test.pdf')

