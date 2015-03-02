import os
import subprocess


def get_cover(path, pdf):
    """ Takes the first page of the pdf and writes it to an image (cover.jpg)
    """
    subprocess.call('convert %s%s[0] %scover.jpg' % (path, pdf, path), shell=True)
# identify working directory
# identify OS (win/lin)
if __name__ == "__main__":
    get_cover(r'd:\\', 'test.pdf')

