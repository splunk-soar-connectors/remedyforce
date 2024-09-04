[comment]: # "Auto-generated SOAR connector documentation"
# RemedyForce

Publisher: Splunk  
Connector Version: 2.0.4  
Product Vendor: BMC Software  
Product Name: RemedyForce  
Product Version Supported (regex): ".\*"  
Minimum Product Version: 4.9.39220  

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
[create ticket](#action-create-ticket) - Create a ticket (incident)  
[update ticket](#action-update-ticket) - Attach a note to a ticket (incident)  

## action: 'test connectivity'
Validates connectivity by retrieving a valid SessionID

Type: **test**  
Read only: **True**

#### Action Parameters
No parameters are required for this action

#### Action Output
No Output  

## action: 'create ticket'
Create a ticket (incident)

Type: **generic**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**description** |  required  | Description of ticket (incident) | string | 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.data.\*.id | string |  `remedyforce incident id`  |  
action_result.data.\*.number | string |  |  
action_result.data.\*.created_date | string |  |  
action_result.status | string |  |   success  failed 
action_result.message | string |  |   Successfully created ticket (incident) 
action_result.parameter.description | string |  |  
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1   

## action: 'update ticket'
Attach a note to a ticket (incident)

Type: **generic**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**id** |  required  | Incident ID | string |  `remedyforce incident id` 
**summary** |  required  | Summary of note | string | 
**notes** |  optional  | Full note text | string | 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.parameter.notes | string |  |  
action_result.parameter.id | string |  `remedyforce incident id`  |   a2U5e0000005nRKEAY 
action_result.parameter.summary | string |  |  
action_result.data.\*.activity_log.\*.id | string |  |  
action_result.data.\*.activity_log.\*.sr_id | string |  `remedyforce incident id`  |  
action_result.data.\*.activity_log.\*.notes | string |  |  
action_result.data.\*.activity_log.\*.summary | string |  |  
action_result.data.\*.activity_log.\*.submitter | string |  |  
action_result.data.\*.activity_log.\*.created_date | string |  |  
action_result.data.\*.activity_log.\*.modified_date | string |  |  
action_result.data.\*.activity_log.\*.work_info_type | string |  |  
action_result.data.\*.activity_log.\*.view_access | string |  |  
action_result.data.\*.activity_log.\*.submitter_username | string |  |  
action_result.data.\*.activity_log.\*.submitter_id | string |  |  
action_result.data.\*.activity_log.\*.submitter_user_img_url | string |  |  
action_result.status | string |  |   success  failed 
action_result.message | string |  |   Successfully added note to ticket (incident) 
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1 