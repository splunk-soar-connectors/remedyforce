[comment]: # "Auto-generated SOAR connector documentation"
# RemedyForce

Publisher: Splunk  
Connector Version: 2\.0\.2  
Product Vendor: BMC Software  
Product Name: RemedyForce  
Product Version Supported (regex): "\.\*"  
Minimum Product Version: 4\.9\.39220  

This app allows ticket management on RemedyForce by implementing generic actions

### Configuration Variables
The below configuration variables are required for this Connector to operate.  These variables are specified when configuring a RemedyForce asset in SOAR.

VARIABLE | REQUIRED | TYPE | DESCRIPTION
-------- | -------- | ---- | -----------
**username** |  required  | string | Username
**password** |  required  | password | Password
**sandbox** |  optional  | boolean | Check to use sandbox environment

### Supported Actions  
[test connectivity](#action-test-connectivity) - Validates connectivity by retrieving a valid SessionID  
[create ticket](#action-create-ticket) - Create a ticket \(incident\)  
[update ticket](#action-update-ticket) - Attach a note to a ticket \(incident\)  

## action: 'test connectivity'
Validates connectivity by retrieving a valid SessionID

Type: **test**  
Read only: **True**

#### Action Parameters
No parameters are required for this action

#### Action Output
No Output  

## action: 'create ticket'
Create a ticket \(incident\)

Type: **generic**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**description** |  required  | Description of ticket \(incident\) | string | 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.data\.\*\.id | string |  `remedyforce incident id` 
action\_result\.data\.\*\.number | string | 
action\_result\.data\.\*\.created\_date | string | 
action\_result\.status | string | 
action\_result\.message | string | 
action\_result\.parameter\.description | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'update ticket'
Attach a note to a ticket \(incident\)

Type: **generic**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**id** |  required  | Incident ID | string |  `remedyforce incident id` 
**summary** |  required  | Summary of note | string | 
**notes** |  optional  | Full note text | string | 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.parameter\.notes | string | 
action\_result\.parameter\.id | string |  `remedyforce incident id` 
action\_result\.parameter\.summary | string | 
action\_result\.data\.\*\.activity\_log\.\*\.id | string | 
action\_result\.data\.\*\.activity\_log\.\*\.sr\_id | string |  `remedyforce incident id` 
action\_result\.data\.\*\.activity\_log\.\*\.notes | string | 
action\_result\.data\.\*\.activity\_log\.\*\.summary | string | 
action\_result\.data\.\*\.activity\_log\.\*\.submitter | string | 
action\_result\.data\.\*\.activity\_log\.\*\.created\_date | string | 
action\_result\.data\.\*\.activity\_log\.\*\.modified\_date | string | 
action\_result\.data\.\*\.activity\_log\.\*\.work\_info\_type | string | 
action\_result\.data\.\*\.activity\_log\.\*\.view\_access | string | 
action\_result\.data\.\*\.activity\_log\.\*\.submitter\_username | string | 
action\_result\.data\.\*\.activity\_log\.\*\.submitter\_id | string | 
action\_result\.data\.\*\.activity\_log\.\*\.submitter\_user\_img\_url | string | 
action\_result\.status | string | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric | 