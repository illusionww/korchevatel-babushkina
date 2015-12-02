from lxml import etree
from lxml.etree import tostring
from itertools import chain


def stringify_children(node):
    parts = ([node.text] + list(chain(*([c.text, tostring(c), c.tail]
             for c in node.getchildren()))) + [node.tail])
    return ''.join(filter(None, parts))


def do(filepath, name):
    xml = etree.parse(filepath)
    root = xml.getroot()
    for page in root.findall("{http://www.mediawiki.org/xml/export-0.10/}page"):
        title = page.find("{http://www.mediawiki.org/xml/export-0.10/}title")
        text = page.find("{http://www.mediawiki.org/xml/export-0.10/}revision/"
                         "{http://www.mediawiki.org/xml/export-0.10/}text")
        u_title = stringify_children(title).strip().replace(u':', '_')\
            .replace(u'/', '_').replace(u'*', '_').replace(u'\"', '')\
            .replace(u'?', '_').replace(u'\\', '_')

        if len(u_title) > 30:
            u_title = u_title[:30]

        with open("./corpus/" + name + "/" + u_title + ".txt", 'wb') as f:
            u_text = stringify_children(text).encode('utf-8')
            f.write(u_text)


if __name__ == "__main__":
    filepath = "C:\\ruwiki-20151123-pages-articles1.xml"
    name = "ruwiki"

    print "Work..."
    do(filepath, name)
    print "Done!"
