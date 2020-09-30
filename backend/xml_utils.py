from xml.dom.minidom import parse
import xml.dom.minidom

def getAttrValue(node, attrname):
    return node.getAttribute(attrname) if node else ""

def getXMLNode(node, name):
    return node.getElementsByTagName(name) if node else ""

def getNodeValue(node, index=0):
    return node.childNodes[index].nodeValue if node else ""