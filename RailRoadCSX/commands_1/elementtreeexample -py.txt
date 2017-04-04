#!/usr/bin/env python

from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import Element
import xml.etree.ElementTree as etree
 
root=Element('person')
tree=ElementTree(root)

name=Element('name')
root.append(name)

firstname=Element('firstname')
lastname=Element('lastname')

name.append(firstname)
name.append(lastname)

# name.text='Arunabh Chowdhury'
lastname.text='Chowdhury'
firstname.text='Arunabh'
root.set('id', '123')

print etree.tostring(root)
tree.write(open(r'/home/t8054/Arunabh_sandbox/python_scripts/person.xml', 'w'))

