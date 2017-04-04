#!/usr/bin/env python

from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import Element
import xml.etree.ElementTree as etree
 
# Creating root

root=Element('NS1:SyncCSXRI')
root.set('xmlns:NS1', 'http://www.ibm.com/maximo')
tree=ElementTree(root)

# Creating all child elements

NS1_CSXRISet=Element('NS1:CSXRISet')
NS1_CHANGEBY=Element('NS1:CHANGEBY')
NS1_RELEASEITEM=Element('NS1:RELEASEITEM')
NS1_CHANGEDATE=Element('NS1:CHANGEDATE')
NS1_CSXEXTERNALSYSTEM=Element('NS1:CSXEXTERNALSYSTEM')
NS1_DESCRIPTION=Element('NS1:DESCRIPTION')
NS1_OBJECTTYPE=Element('NS1:OBJECTTYPE')
NS1_PARENT=Element('NS1:PARENT')
NS1_RELEASEITEMNUM=Element('NS1:RELEASEITEMNUM')
NS1_RFCNUM=Element('NS1:RFCNUM')
NS1_STATUS=Element('NS1:STATUS')
NS1_STATUSDATE=Element('NS1:STATUSDATE')

# Setting Release Item attribute
NS1_RELEASEITEM.set('action', 'AddChange')

# Setting parent-child relationship

root.append(NS1_CSXRISet)
NS1_CSXRISet.append(NS1_RELEASEITEM)
NS1_RELEASEITEM.append(NS1_CHANGEBY)
NS1_RELEASEITEM.append(NS1_CHANGEDATE)
NS1_RELEASEITEM.append(NS1_CSXEXTERNALSYSTEM)
NS1_RELEASEITEM.append(NS1_DESCRIPTION)
NS1_RELEASEITEM.append(NS1_OBJECTTYPE)
NS1_RELEASEITEM.append(NS1_PARENT)
NS1_RELEASEITEM.append(NS1_RELEASEITEMNUM)
NS1_RELEASEITEM.append(NS1_RFCNUM)
NS1_RELEASEITEM.append(NS1_STATUS)
NS1_RELEASEITEM.append(NS1_STATUSDATE)


# name.text='Arunabh Chowdhury'
# lastname.text='Chowdhury'
# firstname.text='Arunabh'


print etree.tostring(root)
tree.write(open(r'/home/t8054/Arunabh_sandbox/python_scripts/SM_Input_new.xml', 'w'))

