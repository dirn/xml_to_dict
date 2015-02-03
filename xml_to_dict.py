"""Utilities to covert XML to a dict."""

from xml.etree import ElementTree

__all__ = ('get_child', 'get_children', 'parse', 'parse_file')


def get_child(d, tag):
    """Return the first child with the specified tag."""
    try:
        return next(get_children(d, tag))
    except StopIteration:
        # No child matched tag.
        return None


def get_children(d, tag):
    """Return a generator of all children with the specified tag."""
    for child in d['children']:
        if child['tag'] == tag:
            yield child


def node_to_dict(node):
    d = {'tag': node.tag}
    children = node.getchildren()
    if children:
        d['children'] = [node_to_dict(child) for child in children]
    else:
        d['text'] = node.text
    d['attrs'] = {k: v for k, v in node.items()}
    return d


def parse(xml_string):
    """Return the XML string as a dict."""
    root = ElementTree.XML(xml_string)
    return node_to_dict(root)


def parse_file(filename):
    """Return the XML file as a dict."""
    tree = ElementTree.parse(filename)
    return node_to_dict(tree.getroot())
