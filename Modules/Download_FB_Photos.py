#!/usr/bin/env python
# encoding=utf-8
#
# Script that allows batch-downloading a person's full Facebook photo
# collection if the person is you or if you are friends with that person
# and have permission to see them.
#
# BEFORE YOU USE THIS:
#     pytz must be installed.
#
#     Make sure that `TIMEZONE`, `TOKEN`, `USER_ID`, and `DATE_FILTER` are
#     set the way you want them -- see below.
#
#     Then simply execute this script.
#

import json
import os
from urllib.request import urlopen, build_opener, HTTPSHandler
from urllib.parse import urlencode, quote
from datetime import datetime
from pytz import utc, timezone

# Change this to the time zone you want the resulting timestamps to be displayed in
TIMEZONE = timezone("US/Eastern")

# Your OAuth access token
# If you need a token, see `README.mdown` in this gist
TOKEN = "EAACtdwAhfgYBAGlXJhvpWL4WHhYDKLGSVJb2To7guvCpbbYBUBaS4DGLSdCZCi6AqCyUpOoZAXfVMduWoaqUaY3615artnuZA0UQ4EschDXRZAgRRTQ7wX7Op8jZArBXD70krrFvJfbSwXvVXwFmZCigJXARtm6JwZD"

# User ID of the person whose albums you want to download
USER_ID = "100001311647240"  # can be a FB profile "username" (URL alias) or ID number

# If you want to only download albums that have been updated since a certain date.
# DATE_FILTER = datetime(2010,12,1)
DATE_FILTER = None

# =========================================================================

PROFILE_URL = "https://graph.facebook.com/%s/albums/" % USER_ID
ALBUM_URL = "https://graph.facebook.com/%d/photos/"

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))


def do_album_download():
    # Custom urllib2 opener since we're going to be making HTTPS requests.
    opener = build_opener(HTTPSHandler)

    # Output goes to:  ./photos_for_$USERID
    MAINDIR = os.path.join(PROJECT_ROOT, "photos_for_%s" % USER_ID)
    if not (os.path.exists(MAINDIR) and os.path.isdir(MAINDIR)):
        os.makedirs(MAINDIR)

    # Open the Graph API URL for the user's albums.
    u = opener.open(PROFILE_URL + "?" + urlencode({
        'access_token': TOKEN
    }))
    profile_data = json.loads(u.read())
    u.close()

    # Pull out the `data` portion since that's where all album information comes from.
    album_set = profile_data['data']

    # Since Graph API can paginate results, see if we have a "next page" and keep pulling in
    temp_data = profile_data.copy()
    while temp_data.get("paging", {"next": None}).get("next", None):
        temp_u = opener.open(temp_data['paging']['next'])
        temp_data = json.loads(temp_u.read())
        temp_u.close()
        album_set.extend(temp_data['data'])

    # The timestamps are in UTC.
    for album in album_set:
        album['adj_time'] = utc.localize(datetime.strptime(album['updated_time'][:-5], "%Y-%m-%dT%H:%M:%S"))

    # If we have a DATE_FILTER, make sure we filter against that.
    if DATE_FILTER:
        date_filter = utc.localize(DATE_FILTER)
        album_set = filter(
            lambda item: item['adj_time'] >= date_filter,
            album_set
        )

    print
    print
    "Downloading %d albums..." % len(album_set)
    print

    # Counters that we can display at the end of the process
    total_albums = len(album_set)
    total_photos = 0

    # =====
    # Write out an index file for the root output directory.
    # Just contains a list of the albums we're going to download and links to the indexes
    # of the resulting album subdirectories.
    info_html = open(os.path.join(MAINDIR, "index.html"), "w")
    info_html.write(
        u"""<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<title>photos</title>\n<style type="text/css">img{max-width:100px;max-height:100px}</style>\n</head>\n\n<body>\n<h1>photos</h1>\n""")
    info_html.write("<ul>\n")
    for album in album_set:
        album_name = album['name'].encode("ascii", "xmlcharrefreplace")

        album_path = quote("%s - %s" % (album['id'], album['name'].encode('ascii', 'ignore')))
        info_html.write('<li><a href="%s/index.html">%s</a>: updated %s</li>' % (
        album_path, album_name, album['adj_time'].strftime("%b. %d, %Y")))
    info_html.write("\n</ul>\n</body>\n</html>")
    info_html.close()
    # =====

    # Go!
    for album in album_set:
        print
        print
        "Album: %s" % album['id']

        # Turn possible unicode into HTML-safe album name.
        album_name = album['name'].encode("ascii", "xmlcharrefreplace")

        # Make subdirectory for this album
        THISDIR = os.path.join(MAINDIR, "%s - %s" % (album['id'], album['name'].encode('ascii', 'ignore')))
        if not (os.path.exists(THISDIR) and os.path.isdir(THISDIR)):
            os.makedirs(THISDIR)

        # Get album from Graph API.
        album_u = opener.open(ALBUM_URL % int(album['id']) + "?" + urlencode({
            'access_token': TOKEN
        }))
        album_str = album_u.read()
        album_u.close()

        # Write this json out to a file in case we want to later parse out more of the metadata.
        album_json_file = open(os.path.join(THISDIR, "albumdata-00.json"), "w")
        album_json_file.write(album_str)
        album_json_file.close()

        # Parse out the set of photos.
        album_data = json.loads(album_str)
        photo_set = album_data['data']

        # Like above, we have to make sure we aggregate all paginated data.
        pagenum = 0
        temp_data = album_data.copy()
        while temp_data.get("paging", {"next": None}).get("next", None):
            pagenum += 1

            # Request next page
            temp_u = opener.open(temp_data['paging']['next'])
            album_str = temp_u.read()
            temp_u.close()

            # Write out this page's json
            album_json_file = open(os.path.join(THISDIR, "albumdata-%02d.json" % pagenum), "w")
            album_json_file.write(album_str)
            album_json_file.close()

            # Append photos from this page
            temp_data = json.loads(album_str)
            photo_set.extend(temp_data['data'])

        print
        "%d photos" % len(photo_set)
        total_photos += len(photo_set)

        # =====
        # Write out an HTML index for this album.
        info_html = open(os.path.join(THISDIR, "index.html"), "w")
        info_html.write(
            u"""<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<title>%s</title>\n<style type="text/css">img{max-width:100px;max-height:100px}</style>\n</head>\n\n<body>\n<h1>%s</h1>\n<h2>%d photos</h2>""" % (
            album_name, album_name, len(photo_set)))

        # Write out HTML for each photo in this album.
        for photo in photo_set:
            # Pull together comments on this photo.
            comment_str = u"<ul>"
            for comment in photo.get("comments", {'data': []})['data']:
                t = utc.localize(datetime.strptime(comment['created_time'][:-5], "%Y-%m-%dT%H:%M:%S"))
                t = t.astimezone(TIMEZONE).strftime("%b. %d, %Y %I:%M:%S %p %Z")
                comment_str += u"\n   <li>%s (%s): %s</li>" % (
                comment['from'].get("name", "(Private)"), t, comment['message'])
            comment_str += u"</ul>"

            # Pull together tags for this photo.
            tagged_people = []
            for person in photo.get("tags", {'data': []})['data']:
                tagged_people.append(person.get("name", "(Private)"))
            tag_str = u", ".join(tagged_people)
            tag_str = u"Tagged: %s" % tag_str.encode('ascii', "xmlcharrefreplace")

            # Make the caption HTML-safe.
            caption = photo.get("name", "").encode("ascii", "xmlcharrefreplace").replace("\n", "<br />\n")

            # Localize the time
            t = utc.localize(datetime.strptime(photo['created_time'][:-5], "%Y-%m-%dT%H:%M:%S"))
            t = t.astimezone(TIMEZONE).strftime("%b. %d, %Y %I:%M:%S %p %Z")

            # Write this photo out to the HTML file
            info_html.write(
                u'<p><a href="%s.jpg"><img src="%s.jpg"/><br />%s</a><br />%s<br />Uploaded: %s</p>\n%s\n<hr />\n\n' % (
                    photo['id'], photo['id'], caption, tag_str, t, comment_str.encode("ascii", "xmlcharrefreplace")
                ))
        info_html.write("\n\n</body>\n</html>")
        info_html.close()

        # =====

        # Actually download the photos in this album.
        for photo in photo_set:
            print
            u"\t" + photo['id']
            photo_u = opener.open(photo['source'])
            photo_file = open(os.path.join(THISDIR, "%d.jpg" % int(photo['id'])), "wb")
            photo_file.write(photo_u.read())
            photo_u.close()
            photo_file.close()

    print
    "%d total albums" % total_albums
    print
    "%d total photos" % total_photos


if __name__ == '__main__':
    do_album_download()