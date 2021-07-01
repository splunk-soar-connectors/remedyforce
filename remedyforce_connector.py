# --
# File: remedyforce_connector.py
#
# Copyright (c) 2016-2021 Splunk Inc.
#
# SPLUNK CONFIDENTIAL - Use or disclosure of this material in whole or in part
# without a valid written license from Splunk Inc. is PROHIBITED.

# Phantom imports
import phantom.app as phantom
from phantom.base_connector import BaseConnector
from phantom.action_result import ActionResult

# Local imports
from remedyforce_consts import *

import requests
import simplejson as json
import re
from datetime import datetime


class RemedyForceConnector(BaseConnector):

    ACTION_ID_CREATE_TICKET = "create_ticket"
    ACTION_ID_UPDATE_TICKET = "update_ticket"

    def __init__(self):

        self._headers = {}  # Used to store auth

        super(RemedyForceConnector, self).__init__()
        return

    def _make_rest_call(self, endpoint, action_result, headers={}, params=None, body=None, method="get"):
        """ Function that makes the REST call to the device,
            generic function that can be called from various action handlers
        """
        # Create the headers
        headers.update(self._headers)
        base_url = "https://na30.salesforce.com/services/apexrest/BMCServiceDesk/1.0/"

        resp_json = None

        # get or post or put, whatever the caller asked us to use, if not specified the default will be 'get'
        request_func = getattr(requests, method)

        # handle the error in case the caller specified a non-existant method
        if (not request_func):
            action_result.set_status(
                phantom.APP_ERROR, REMEDY_ERR_API_UNSUPPORTED_METHOD, method=method)

        # Make the call
        try:
            r = request_func(base_url + endpoint,
                             json=body,
                             headers=headers,
                             # auth=(self._username, self._key), # Don't need to authenticate in this manner
                             # verify=config[phantom.APP_JSON_VERIFY],
                             params=params)  # uri parameters if any
        except Exception as e:
            return (action_result.set_status(phantom.APP_ERROR, REMEDY_ERR_SERVER_CONNECTION, e), resp_json)

        # self.debug_print('REST url: {0}'.format(r.url))

        # Try a json parse, since most REST API's give back the data in json,
        # if the device does not return JSONs, then need to implement parsing them some other manner
        try:
            resp_json = r.json()
        except Exception as e:
            # r.text is guaranteed to be NON None, it will be empty, but not None
            msg_string = REMEDY_ERR_JSON_PARSE.format(raw_text=r.text)
            return (action_result.set_status(phantom.APP_ERROR, msg_string, e), resp_json)

        # Handle any special HTTP error codes here, many devices return an HTTP error code like 204.
        # The requests module treats these as error,
        # so handle them here before anything else, uncomment the following lines in such cases
        # if (r.status_code == 201):
        #     return (phantom.APP_SUCCESS, resp_json)

        # Handle/process any errors that we get back from the device
        if (200 <= r.status_code <= 399):
            # Success
            return (phantom.APP_SUCCESS, resp_json)

        # Failure
        action_result.add_data(resp_json)

        details = json.dumps(resp_json).replace('{', '').replace('}', '')

        return (action_result.set_status(phantom.APP_ERROR,
                                         REMEDY_ERR_FROM_SERVER.format(status=r.status_code, detail=details)),
                resp_json)

    def _get_session_id(self):
        """ This needs to be done with a SOAP request
            The SessiondID is the only kind of auth we need for
            future requests
        """

        config = self.get_config()
        username = config[REMEDY_JSON_USERNAME]
        password = config[REMEDY_JSON_PASSWORD]
        body = REMEDY_LOGIN_XML.format(username, password)

        # headers and url needed for login request
        if config.get('sandbox', False):
            url = "https://login.salesforce.com/services/Soap/u/35.0"
        else:
            url = "https://test.salesforce.com/services/Soap/u/35.0"

        headers = {'Content-Type': 'text/xml;charset=UTF-8',
                   'SOAPAction': 'Login'}

        self.save_progress("Retrieving SessionID")

        # Thankfully this is the only SOAP request we need to make
        try:
            r = requests.post(url, data=body, headers=headers)
        except Exception as e:
            return self.set_status_save_progress(phantom.APP_ERROR, e)

        try:
            session_id = re.search(
                '<sessionId>(.*)</sessionId>', r.text).groups()[0]
            self._headers['Authorization'] = 'Bearer {}'.format(session_id)
            return self.set_status_save_progress(phantom.APP_SUCCESS, "Retrieved SessionID")
        except:
            try:  # Invalid Credentials
                fs = re.search('<faultstring>(.*)</faultstring>',
                               r.text).groups()[0]
                return self.set_status_save_progress(phantom.APP_ERROR, fs)
            except Exception as e:  # Something else went wrong
                return self.set_status_save_progress(phantom.APP_ERROR, e)

    def _validate_connection(self, action_result):
        """ See if connection is valid and save SessionID """

        ret_val = self._get_session_id()

        if (phantom.is_fail(ret_val)):
            return self.set_status(phantom.APP_ERROR)

        # Get version to confirm that connections works
        ret_val, json_resp = self._make_rest_call(
            ENDPOINT_VERSION, action_result)
        if (not phantom.is_fail(ret_val) and json_resp[RESP_SUCCESS]):
            # We need to conver the result string to proper json
            result = json.loads(json_resp[RESP_RESULT])
            self.save_progress("RemedyForce version {}", result[RESP_VERSION])
            return ret_val

        return self.set_status(phantom.APP_ERROR)

    def _test_connectivity(self, param):

        action_result = ActionResult()
        self.save_progress("Testing connectivity")

        ret_val = self._validate_connection(action_result)
        if (phantom.is_fail(ret_val)):
            return self.set_status_save_progress(phantom.APP_ERROR, "Connectivity test failed")

        return self.set_status_save_progress(phantom.APP_SUCCESS, "Connectivity test succeeded")

    def _create_ticket(self, param):

        action_result = self.add_action_result(ActionResult(dict(param)))
        ret_val = self._validate_connection(action_result)
        if (phantom.is_fail(ret_val)):
            return ret_val

        body = {'Description': param[REMEDY_JSON_DESCRIPTION],
                'OpenDateTime': datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
                'DueDateTime': '',
                'ClientId': '',
                'IncidentSource': 'Source'}

        ret_val, json_resp = self._make_rest_call(ENDPOINT_INCIDENT, action_result,
                                                  body=body, method="post")
        # Something went wrong with the request
        if phantom.is_fail(ret_val):
            self.set_status(phantom.APP_ERROR)
            return action_result.get_status()

        # Some failure is indicated in the response
        if (not json_resp[RESP_SUCCESS]):
            self.set_status(phantom.APP_ERROR)
            return action_result.set_status(phantom.APP_ERROR, json_resp[RESP_MESSAGE])

        result = self._lowercase_keys(json_resp[RESP_RESULT])
        action_result.add_data(result)

        return action_result.set_status(phantom.APP_SUCCESS, "Successfully created ticket (incident)")

    def _update_ticket(self, param):

        action_result = self.add_action_result(ActionResult(dict(param)))
        ret_val = self._validate_connection(action_result)
        if (phantom.is_fail(ret_val)):
            return ret_val

        ActivityLog = {'Summary': param[REMEDY_JSON_SUMMARY],
                       'Notes': param.get(REMEDY_JSON_NOTES, "")}

        body = {'ActivityLog': [ActivityLog]}

        endpoint_note = ENDPOINT_SERVICE + \
            "/{}/clientnote".format(param[REMEDY_JSON_ID])

        ret_val, json_resp = self._make_rest_call(endpoint_note, action_result,
                                                  body=body, method="post")

        # Something went wrong with the request
        if phantom.is_fail(ret_val):
            self.set_status(phantom.APP_ERROR)
            return action_result.get_status()

        # Some failure is indicated in the response
        if (not json_resp[RESP_SUCCESS]):
            self.set_status(phantom.APP_ERROR)
            return action_result.set_status(phantom.APP_ERROR, json_resp[RESP_MESSAGE])

        result = self._lowercase_keys(json_resp[RESP_RESULT])
        action_result.add_data(result)

        return action_result.set_status(phantom.APP_SUCCESS, "Successfully added note to ticket (incident)")

    def _lowercase_keys(self, x):
        """ Convert from CamelCase to snake_case """
        if isinstance(x, list):
            return [self._lowercase_keys(v) for v in x]
        elif isinstance(x, dict):
            return dict((re.sub('(?!^)([A-Z]+)', r'_\1', k).lower(), self._lowercase_keys(v)) for k, v in x.items())
        else:
            return x

    def handle_action(self, param):

        action = self.get_action_identifier()
        ret_val = phantom.APP_SUCCESS

        if (action == phantom.ACTION_ID_TEST_ASSET_CONNECTIVITY):
            ret_val = self._test_connectivity(param)
        elif (action == self.ACTION_ID_CREATE_TICKET):
            ret_val = self._create_ticket(param)
        elif (action == self.ACTION_ID_UPDATE_TICKET):
            ret_val = self._update_ticket(param)

        return ret_val


if __name__ == '__main__':
    # Imports
    import sys
    import pudb

    # Breakpoint at runtime
    pudb.set_trace()

    # The first param is the input json file
    with open(sys.argv[1]) as f:

        # Load the input json file
        in_json = f.read()
        in_json = json.loads(in_json)
        print(json.dumps(in_json, indent=' ' * 4))

        # Create the connector class object
        connector = RemedyForceConnector()

        # Se the member vars
        connector.print_progress_message = True

        # Call BaseConnector::_handle_action(...) to kickoff action handling.
        ret_val = connector._handle_action(json.dumps(in_json), None)

        # Dump the return value
        print(ret_val)

    exit(0)
