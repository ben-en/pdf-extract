import bottle
import hashlib
import argparse
import platform
import subprocess
def hash_url(url):
    md5 = hashlib.md5()
    md5.update(bytes(url))
    return md5.hexdigest()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Takes a pdf in and gets a cover image from the first page'
    )
    parser.add_argument('pdf', metavar='FILE', help='pdf file to extract')
    parser.add_argument('description', metavar='FILE', default=None, help=
                        'description to use on pdf download page')
    args = parser.parse_args()

    bottle.TEMPLATE_PATH.insert(0, original_dir)
    # Identify OS
    OS = platform.system()
    if OS == 'Windows':
        subprocess.call(["convert", join(path, args.pdf) + "[0]",
                         join(path, "cover.jpg")], shell = True)
    else:
        subprocess.call("convert " + join(path, args.pdf) + "[0] " +
                         join(path, "cover.jpg"), shell=True)

    # Build landing page
    html = bottle.template('template', title=args.pdf[:-4], desc=args.description)
    with open(join(path, 'index.html'), 'w') as f:
        f.write(html)
    print html
