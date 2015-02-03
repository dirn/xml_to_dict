"""Tests for xml_to_dict."""

from xml.etree import ElementTree

import pytest

import xml_to_dict


@pytest.fixture
def node():
    """Return a single node."""
    node = ElementTree.Element('TAG')
    node.text = 'TEXT'
    return node


@pytest.fixture
def parent():
    """Return a node with children."""
    parent = ElementTree.Element('PARENT')
    child1 = ElementTree.SubElement(parent, 'CHILD1')
    child1.text = 'TEXT1'
    child2 = ElementTree.SubElement(parent, 'CHILD2')
    child2.text = 'TEXT2'
    return parent


@pytest.fixture
def xml_file(xml_string, tmpdir):
    """Return an XML file."""
    f = tmpdir.join('nodes.xml')
    f.write(xml_string)
    return f


@pytest.fixture
def xml_string():
    """Return a string containing XML."""
    return '<PARENT><CHILDREN><CHILD>TEXT</CHILD></CHILDREN></PARENT>'


def test_get_child(parent):
    """Test `get_child`."""
    c = xml_to_dict.get_child(xml_to_dict.node_to_dict(parent), 'CHILD1')

    assert c['tag'] == 'CHILD1'
    assert c['text'] == 'TEXT1'


def test_get_child_no_match(parent):
    """Test `get_child` when there's no matching child."""
    c = xml_to_dict.get_child(xml_to_dict.node_to_dict(parent), 'CHILD')

    assert c is None


def test_get_children(parent):
    """Test `get_children`."""
    cs = xml_to_dict.get_children(xml_to_dict.node_to_dict(parent), 'CHILD1')

    for c in cs:
        assert c['tag'] == 'CHILD1'


def test_get_children_no_match(parent):
    """Test `get_children` when there are no matching children."""
    cs = xml_to_dict.get_children(xml_to_dict.node_to_dict(parent), 'CHILD')

    assert len(list(cs)) == 0


def test_node_to_dict_with_children(parent):
    """Test `node_to_dict` with child nodes."""
    d = xml_to_dict.node_to_dict(parent)

    assert d['tag'] == 'PARENT'
    assert len(d['children'])
    for child in d['children']:
        assert child['tag'] in ['CHILD1', 'CHILD2']
    assert len(d['attrs'].keys()) == 0
    assert 'text' not in d


def test_node_to_dict_with_no_children(node):
    """Test `node_to_dict` with no child nodes."""
    d = xml_to_dict.node_to_dict(node)

    assert d['tag'] == 'TAG'
    assert d['text'] == 'TEXT'
    assert len(d['attrs'].keys()) == 0
    assert 'children' not in d


def test_parse(xml_string):
    """Test `parse`."""
    d = xml_to_dict.parse(xml_string)

    assert isinstance(d, dict)


def test_parse_file(xml_file):
    """Test `parse_file`."""
    d = xml_to_dict.parse_file(xml_file.strpath)

    assert isinstance(d, dict)
