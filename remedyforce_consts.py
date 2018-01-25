# --
# File: remedyforce_consts.py
#
# Copyright (c) Phantom Cyber Corporation, 2018
#
# This unpublished material is proprietary to Phantom Cyber.
# All rights reserved. The methods and
# techniques described herein are considered trade secrets
# and/or confidential. Reproduction or distribution, in whole
# or in part, is forbidden except by express written permission
# of Phantom Cyber.
#
# --REMEDY_JSON_USERNAME = "username"
REMEDY_JSON_PASSWORD = "password"
REMEDY_JSON_DESCRIPTION = "description"
REMEDY_JSON_ID = "id"
REMEDY_JSON_SUMMARY = "summary"
REMEDY_JSON_NOTES = "notes"

REMEDY_ERR_API_UNSUPPORTED_METHOD = "Unsupported method"
REMEDY_ERR_SERVER_CONNECTION = "Connection failed"
REMEDY_ERR_FROM_SERVER = "API failed, Status code: {status}, Detail: {detail}"
REMEDY_ERR_JSON_PARSE = "Unable to parse the fields parameter into a dictionary"

ENDPOINT_VERSION = "ServiceUtil/Version"
ENDPOINT_INCIDENT = "Incident"
ENDPOINT_SERVICE = "ServiceRequest"

RESP_SUCCESS = 'Success'
RESP_MESSAGE = 'ErrorMessage'
RESP_RESULT = 'Result'
RESP_VERSION = 'Version'

# Login XML to use which is needed to retrieve valid SessionID
# Note that the username and password fields need added in using
#  string.format(username, password)
REMEDY_LOGIN_XML = """\
<?xml version="1.0" encoding="utf-8" ?>
<env:Envelope xmlns:xsd="http://www.w3.org/2001/XMLSchema"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xmlns:env="http://schemas.xmlsoap.org/soap/envelope/">
  <env:Body>
    <n1:login xmlns:n1="urn:partner.soap.sforce.com">
      <n1:username>{}</n1:username>
      <n1:password>{}</n1:password>
    </n1:login>
  </env:Body>
</env:Envelope>"""
