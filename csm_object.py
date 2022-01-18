# CSM Object Read-Write demo
#
# More info:
# https://www.cisco.com/c/en/us/support/docs/security/security-manager/216550-extract-acl-from-csm-in-csv-format-throu.html
# 

import requests
import sys	
import xml.etree.ElementTree as ET

import urllib3
urllib3.disable_warnings()

url  = 'https://csm/nbi/'
username='admin'
password='secret'

object_name='27_NO_12'
device_ip= '10.1.2.3'



# Login
print("Login: ")
data= '<?xml version="1.0" encoding="UTF-8"?><csm:loginRequest xmlns:csm="csm">\
<protVersion>1.0</protVersion><reqId>123</reqId><username>'+username+'</username>\
<password>'+password+'</password></csm:loginRequest>'

headers = {
  'Content-Type': 'text/xml'
}

session = requests.Session()
response = session.post(url+'login', data=data, headers=headers, verify=False)
#print(response,response.text)


#Login was successful
if response.status_code == 200:
  print("CSM login was succesful.")


  print("Device Config: ")
  #https://www.cisco.com/c/en/us/support/docs/security/security-manager/216550-extract-acl-from-csm-in-csv-format-throu.html
  device_config='utilservice/execDeviceReadOnlyCLICmds'
  data='<?xml version="1.0" encoding="UTF-8"?><csm:execDeviceReadOnlyCLICmdsRequest xmlns:csm="csm">\
  <protVersion>1.0</protVersion><reqId>123</reqId><deviceReadOnlyCLICmd>\
  <deviceIP>'+device_ip+'</deviceIP><cmd>show</cmd><argument>access-list</argument>\
  </deviceReadOnlyCLICmd></csm:execDeviceReadOnlyCLICmdsRequest>'

  response = session.post(url+device_config, data=data, headers=headers, verify=False)
  #print(response,response.text)
  
  root = ET.fromstring(response.text)
  dev = root.find('deviceCmdResult/deviceIP')
  print(f'Device IP:{dev.text}')
  cfg = root.find('deviceCmdResult/resultContent')
  print(f'Device Config:{cfg.text}')


  print(" "*80)
  print("Get Session ID: ")
  data='<?xml version="1.0" encoding="UTF-8"?>\
  <p:newCSMSessionRequest xmlns:p="csm">\
  <csmSessionDescription>creating CSM API session to test</csmSessionDescription>\
  </p:newCSMSessionRequest>'

  response = session.post(url+'configservice/createCSMSession', data=data, headers=headers, verify=False)
  #print("SessionID:",response.text)
  root = ET.fromstring(response.text)
  sessionid = root.find('csmSessionGID').text
  print(sessionid)

  
  print(" "*80)
  print("Adding Object: ")
  data='<?xml version="1.0" encoding="UTF-8"?>\
  <csm:addPolicyObjectRequest xmlns:csm="csm">\
  <csmSessionGID>'+sessionid+'</csmSessionGID>\
  <enforceDuplicateDetection>false</enforceDuplicateDetection>\
  <networkPolicyObject>\
  <name>'+object_name+'</name> <parentGID>00000000-0000-0000-0000-000000000000</parentGID>\
  <updatedByUser>apiadmin</updatedByUser>\
  <type>NetworkPolicyObject</type>\
  <comment> </comment>\
  <nodeGID>00000000-0000-0000-0000-000000000001</nodeGID>\
  <isProperty>false</isProperty>\
  <subType></subType>\
  <isGroup>false</isGroup>\
  <ipData>1.19.0.3</ipData>\
  <ipData>1.19.0.4</ipData>\
  </networkPolicyObject>\
  </csm:addPolicyObjectRequest>'
  response = session.post(url+'configservice/addPolicyObject', data=data, headers=headers, verify=False)
  #print(response,response.text, response.cookies)
  root = ET.fromstring(response.text)
  msg = root.find('message').text
  print(msg)
  

  print(" "*80)
  print("Validate the session: ")
  data='<?xml version="1.0" encoding="UTF-8"?><ns1:csmSessionOperationRequest xmlns:ns1="csm">\
  <csmSessionGID>'+sessionid+'</csmSessionGID></ns1:csmSessionOperationRequest>'
  response = session.post(url+'configservice/validateCSMSession', data=data, headers=headers, verify=False)
  #print(response,response.text, response.cookies)
  #print(response.text)
  root = ET.fromstring(response.text)
  msg = root.find('validationMessage').text
  print(msg)  

  
  print(" "*80)
  print("Submit the session: ")
  data='<?xml version="1.0" encoding="UTF-8"?><csm:submitCSMSessionRequest xmlns:csm="csm" xmlns:xsi="http://www.w3.org/2001/XMLSchema- instance ">\
  <csmSessionGID>'+sessionid+'</csmSessionGID> <submitComments>Submission test</submitComments> <continueOnWarnings>true</continueOnWarnings></csm:submitCSMSessionRequest>'
  response = session.post(url+'configservice/submitCSMSession', data=data, headers=headers, verify=False)
  #print(response,response.text, response.cookies)
  #print(response.text)
  root = ET.fromstring(response.text)
  msg = root.find('validationMessage').text
  print(msg) 
  
  """
  print(" "*80)
  print("Close the session: ")
  data='<?xml version="1.0" encoding="UTF-8"?><ns1:csmSessionOperationRequest xmlns:ns1="csm">\
  <csmSessionGID>'+sessionid+'</csmSessionGID> </ns1:csmSessionOperationRequest>'
  response = session.post(url+'configservice/closeCSMSession', data=data, headers=headers, verify=False)
  print(response,response.text, response.cookies)
  root = ET.fromstring(response.text)
  """

  print(" "*80)
  print("Read Object: ")
  
  data= '<?xml version="1.0" encoding="UTF-8"?><p:getPolicyObjectRequest xmlns:p="csm">\
  <networkPolicyObject><name>'+object_name+'</name></networkPolicyObject></p:getPolicyObjectRequest>'
  response = session.post(url+'configservice/getPolicyObject', data=data, headers=headers, verify=False)
  #print(response,response.text, response.cookies)
  #print(response.text)

  root = ET.fromstring(response.text)   
  name = root.find('policyObject/networkPolicyObject/name')
  ipdata = root.findall('policyObject/networkPolicyObject/ipData')
  print(f'name:{name.text}')
  
  for s in ipdata:
    print(f' ipData:{s.text}')


  #logout
  print(" "*80)
  print("Logout ...")
  data='<?xml version="1.0" encoding="UTF-8"?><csm:logoutRequest xmlns:csm="csm">\
  <protVersion>1.0</protVersion><reqId>123</reqId></csm:logoutRequest>'

  response = session.post(url+'logout', data=data, headers=headers, verify=False)
  if response.status_code == 200:
    print("Logout was successful.")


else:
  print(response,response.text)



