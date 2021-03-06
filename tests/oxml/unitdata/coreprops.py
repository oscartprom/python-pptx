# encoding: utf-8

"""
Test data for core properties unit tests.
"""

from __future__ import absolute_import

from pptx.oxml import parse_xml_bytes
from pptx.oxml.ns import nsdecls


class CT_CorePropertiesBuilder(object):
    """
    Test data builder for CT_CoreProperties (cp:coreProperties) XML element
    """
    properties = (
        ('author',           'dc:creator'),
        ('category',         'cp:category'),
        ('comments',         'dc:description'),
        ('content_status',   'cp:contentStatus'),
        ('created',          'dcterms:created'),
        ('identifier',       'dc:identifier'),
        ('keywords',         'cp:keywords'),
        ('language',         'dc:language'),
        ('last_modified_by', 'cp:lastModifiedBy'),
        ('last_printed',     'cp:lastPrinted'),
        ('modified',         'dcterms:modified'),
        ('revision',         'cp:revision'),
        ('subject',          'dc:subject'),
        ('title',            'dc:title'),
        ('version',          'cp:version'),
    )

    def __init__(self):
        """Establish instance variables with default values"""
        for propname, tag in self.properties:
            setattr(self, '_%s' % propname, None)

    @property
    def _ns_prefixes(self):
        ns_prefixes = ['cp', 'dc', 'dcterms']
        for propname, tag in self.properties:
            value = getattr(self, '_%s' % propname)
            if value is None:
                continue
            ns_prefix = tag.split(':')[0]
            if ns_prefix not in ns_prefixes:
                ns_prefixes.append(ns_prefix)
            if ns_prefix == 'dcterms' and 'xsi' not in ns_prefixes:
                ns_prefixes.append('xsi')
        return tuple(ns_prefixes)

    @property
    def props_xml(self):
        props_xml = ''
        for propname, tag in self.properties:
            value = getattr(self, '_%s' % propname)
            if value is None:
                continue
            if value == '':
                xml = '  <%s/>\n' % tag
            else:
                if tag.startswith('dcterms:'):
                    xml = ('  <%s xsi:type="dcterms:W3CDTF">%s</%s>\n' %
                           (tag, value, tag))
                else:
                    xml = '  <%s>%s</%s>\n' % (tag, value, tag)
            props_xml += xml
        return props_xml

    @property
    def coreProperties(self):
        if self.props_xml:
            coreProperties = (
                '<cp:coreProperties %s>\n%s</cp:coreProperties>\n' %
                (nsdecls(*self._ns_prefixes), self.props_xml)
            )
        else:
            coreProperties = (
                '<cp:coreProperties %s/>\n' % nsdecls('cp', 'dc', 'dcterms')
            )
        return coreProperties

    @property
    def element(self):
        """Return element based on XML generated by builder"""
        return parse_xml_bytes(self.xml)

    def with_child(self, name, value):
        """add property element for *name* set to *value*"""
        setattr(self, '_%s' % name, value)
        return self

    def with_date_prop(self, name, value):
        """add date property element for *name* set to *value*"""
        setattr(self, '_%s' % name, value)
        return self

    def with_revision(self, value):
        """add revision element set to *value*"""
        self._revision = value
        return self

    @property
    def xml(self):
        """
        Return XML string based on settings accumulated via method calls
        """
        return self.coreProperties


def a_coreProperties():
    """Syntactic sugar to construct a CT_CorePropertiesBuilder instance"""
    return CT_CorePropertiesBuilder()
