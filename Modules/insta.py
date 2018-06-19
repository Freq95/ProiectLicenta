#! /usr/bin/env python

# Welcome in the "dinsta" source code!
#
# If you have any suggestion for improve the code (I know, json module)
# or if you found a bug, please contact me
# twitter: @marko_nix
# my blog: https://lucidimarco.blogspot.it/
#
# Have a nice day!

import urllib2 as ul
import os
import argparse
import time

# --- Arguments parser --- #

parser = argparse.ArgumentParser(prog="dinsta", usage="%(prog)s [username] -l \
[link] -d [path] -v -h", description="With dinsta you can download all public \
photos of an user of Instagram. Downloads are incremental if you don't rename \
the images or the directory created the first time. For any issue you can \
contact me on Twitter: @marko_nix or on my blog: https://lucidimarco.blogspot.it/", \
epilog="WARNING: use this tool for photos that weren\'t uploaded by you could \
be a violation of Instagram Terms of Use \"http://instagram.com/legal/terms/\" \
or Privacy Policy \"http://instagram.com/legal/privacy/\", the developer \
(@marko_nix) does not assume any responsibility in case of uses not permitted of this tool." )

parser.add_argument("username", type=str, nargs="?", help="the username from which you want download photos (should be YOUR username)")
parser.add_argument("-l", "--link", type=str, action="store", nargs="?", help="link of a single photo to download")
parser.add_argument("-d", "--directory", type=str, nargs="?", default=os.getcwd(), help="path of directory where save photos")
parser.add_argument("-v", "--verbose", action="store_true", help="increase output verbosity")
parser.add_argument("--version", action="version", version="1.0")

# --- Utility --- #

def check_path(path):
    """Checks if the entered path exists"""
    if path != os.getcwd():
        if not os.path.exists(path):
            parser.error("path " + '"'+path+'"' + " does not exist!")
        else: return True

def find_image_link(str_):
    """Return the photo name, date and photo link, extracts by a
    piece of script"""
    date = str_.split('"date":')[1]   # finds the upload date expressed in timestamp
    i_enddate = date.find('.0,"') + 1
    date = float(date[:i_enddate])
    date = time.strftime("%Y%m%d%H%M", time.gmtime(date))   # converts the date (year, month, day, hour, minute)
    http = str_.split('"display_src":"')[1]   # finds the full resolution link
    i_jpg = http.find('.jpg') + 4
    photo_link = ''.join(http[:i_jpg].split('\\'))
    photo_name = photo_link[photo_link.rfind("/")+1:]   # the name is the last part of the link
    photo_name = date + "_" + photo_name
    return photo_name, photo_link

def show_status(number, length, verbosity):
    """Return the progress of the download
    according the verbosity argument"""
    stat = str(number) + "/" + str(length)
    if verbosity == True:
        return stat
    elif number % 100 == 0:
        return stat

def save_photos(link, filename, path, dir_name):
    """Checks the image link.
    Checks if a photo is already saved (incremental download).
    Saves the photos in a directory (called like username)
    placed in the path."""
    if path[-1] == "/": pass   # adjusts the path
    else: path = path + "/"
    if path.split("/")[-2] == dir_name:
        path = path[:path.rfind(dir_name)]
    if dir_name != None:
        p_dir = path + dir_name
        if not os.path.exists(p_dir):   # if directory doesn't exist
            os.makedirs(p_dir)   # make it!
        p_file = p_dir + "/" + filename
    else:
        p_file = path + filename
    if not os.path.exists(p_file):   # incremental
        try:
            img = ul.urlopen(link)
        except ul.HTTPError, e:
            print "error: " + str(e.code) + ' sorry, image at link: "' + link + '" can not be downloaded, it will be skipped'
            return -1   # -1 is for the counter
        with open(p_file, 'wb') as f:
            f.write(img.read())
        img.close()
        return
    else: return -1   # as before

# --- Arguments --- #

early = "https://instagram.com/"
args = parser.parse_args()
if args.link != None and not args.link.startswith("https://"): parser.error("Insert a valid link!")
if args.link:
    username = args.link[args.link.find(".com/") + 5 : ]   # username become the numbers of link
    dir_name = None   # directory name == None
else:
    username = args.username
    dir_name = username
if username == None: parser.error("Insert a username!")   # username can't be None!
path = args.directory
check_path(path)

# --- Tree of user --- #

class insta_tree(object):
    """Tree organization of links"""
    def __init__(self, url):
        self.url = url   # URL of page where extract the photos links, the root is username link
        self.name_links = {}   # dictionary of links: key = photo_name, value = photo_link
        self.more = None   # URL of next page where grab photos! It'll be next tree node
    def __str__(self):
        return self.url
    def __repr__(self):
        return 'insta_tree("' + self.url + '")'

    def get_full_script(self):
        """Return a splitted list of the javascript
        where there are photo information"""
        try:
            page = ul.urlopen(self.url)
        except ul.HTTPError, e:
            exit("error: " + str(e.code) + ' link "' + self.url + '" not found')
        source = page.read().decode("utf-8")
        page.close()
        source = source.split('<script type="text/javascript">window._sharedData')
        full_script = source[1].split('</script>')[0].split('"code":"')   # every piece contain information of one single photo
        return full_script[1:]

    def get_all_links(self, dic = {}):
        """Return a dictionary of all photos links by the user"""
        for k,v in self.name_links.items():
            dic[k] = v
        if self.more != None:
            self.more.get_all_links(dic)
        return dic

# --- Functions --- #

def gen_insta_tree(num = None):
    """Generates the links tree"""
    query = "?max_id="   # for the more link
    if num != None: url = early + username + query + num   # next link
    else: url = early + username   # first link
    root = insta_tree(url)
    full_script = root.get_full_script()
    for p_script in full_script:
        photo_name, photo_link = find_image_link(p_script)   # unpacking
        if not photo_name in root.name_links:
            root.name_links[photo_name] = photo_link      # add the links at the dictionary
        if p_script == full_script[-1] and len(root.name_links) == 24:   # 24 is the max number of photos in a page source code
            num = p_script.split(',"id":"')[1]   # extracts the more link in the last photo
            num = num[: num.find('"')]
            if num[-1] in "0123456789":
                root.more = gen_insta_tree(num)   # the tree is generated recursively
        else: continue
    return root

def dinsta():
    """Calls the previous functions and generates output"""
    if args.verbose: print 'Getting all photos links from "' + early + username + '" this may take a while...'
    tree = gen_insta_tree()
    all_links = tree.get_all_links()
    tot = len(all_links)
    print "Total photos found:", tot
    print "Download started:"
    cnt = 1
    for k, v in all_links.items():
        filename, link = k, v
        if save_photos(link, filename, path, dir_name) == -1:
            cnt -= 1
        else:
            status = show_status(cnt, tot, args.verbose)
            if args.verbose:
                print "Saved: {0:60}".format(filename), '%15s' % status
            else:
                if status != None:
                    print status, "photos saved"
        cnt += 1
    exit(str(cnt -1) + '/' + str(tot) + ' photos saved' + '\nDone!')

if __name__ == '__main__':
    dinsta()