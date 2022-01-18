# CSM_Object

This script creates and reads an object in CSM.  

More info:
https://www.cisco.com/c/en/us/support/docs/security/security-manager/216550-extract-acl-from-csm-in-csv-format-throu.html


The output looks similar:  


```
python3 csm_object.py
Login: 
CSM login was successful.
Device Config: 
Device IP:10.1.2.3
Device Config:access-list cached ACL log flows: total 0, denied 0 (deny-flow-max 4096)
            alert-interval 300
access-list VPN_ESM_cb; 1 elements; name hash: 0xa26130e2
access-list VPN_ESM_cb line 1 extended permit ip any any (hitcnt=0) 0x7866ba00 
access-list CSM_FW_ACL_inside; 1 elements; name hash: 0xf218cf2c
access-list CSM_FW_ACL_inside line 1 extended permit tcp object inside-net any4 eq https (hitcnt=0) 0x21160f7d 
  access-list CSM_FW_ACL_inside line 1 extended permit tcp 10.0.0.0 255.0.0.0 any4 eq https (hitcnt=0) 0x21160f7d 

                                                                                
Get Session ID: 
00000000-0000-0000-0000-154613823365
                                                                                
Adding Object: 
CREATE Policy Object Operation Successful!
                                                                                
Validate the session: 
Validation successful with no warnings or errors
                                                                                
Submit the session: 
CSM Session submitted successfully
                                                                                
Read Object: 
name:27_NO_12
 ipData:1.19.0.3
 ipData:1.19.0.4
                                                                                
Logout ...
Logout was successful.
```
