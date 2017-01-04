import logging
import boto3
import json

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

iotDataPlaneClient = boto3.client('iot-data')
iotClient = boto3.client('iot')

def lambda_handler(event, context):
    logger.info('got event{}'.format(event))
    access_token = event['payload']['accessToken']
    if (event['header']['namespace'] == 'Alexa.ConnectedHome.Discovery' and
        event['header']['name'] == 'DiscoverAppliancesRequest'):
        return handleDiscovery(context, event)
    elif event['header']['namespace'] == 'Alexa.ConnectedHome.Control':
        return handleControl(context, event)

def handleDiscovery(context, event):
    return {
        'header': {
            'messageId': event['header']['messageId'],
            'name': 'DiscoverAppliancesResponse',
            'namespace': 'Alexa.ConnectedHome.Discovery',
            'payloadVersion': '2'
        },
        'payload': {
            'discoveredAppliances': [
                {
                    'applianceId': 'aarav-room-shade',
                    'friendlyName': 'Aarav room shades',
                    'friendlyDescription': 'Shades in Aaravs room controlled by Raspberry Pi',
                    'actions': [
                        'turnOn',
                        'turnOff'
                    ],
                    'additionalApplianceDetails': {},
                    'isReachable': True,
                    'manufacturerName': 'AaravSystems Inc',
                    'modelName': '1',
                    'version': 'Beta'
                },
                {
                    'applianceId': 'study-room-shade',
                    'friendlyName': 'Study room shades',
                    'friendlyDescription': 'Shades in Study room room controlled by Raspberry Pi',
                    'actions': [
                        'turnOn',
                        'turnOff'
                    ],
                    'additionalApplianceDetails': {},
                    'isReachable': True,
                    'manufacturerName': 'AaravSystems Inc',
                    'modelName': '1',
                    'version': 'Beta'
                },                
                {
                    'applianceId': 'bedroom-shades',
                    'friendlyName': 'Bedroom shades',
                    'friendlyDescription': 'Shades in both bedrooms controlled by Raspberry Pi',
                    'actions': [
                        'turnOn',
                        'turnOff'
                    ],
                    'additionalApplianceDetails': {},
                    'isReachable': True,
                    'manufacturerName': 'AaravSystems Inc',
                    'modelName': '1',
                    'version': 'Beta'
                },                
                {
                    'applianceId': 'family-room-shade1',
                    'friendlyName': 'Family room shade 1',
                    'friendlyDescription': 'Shade 1 in family room controlled by Raspberry Pi',
                    'actions': [
                        'turnOn',
                        'turnOff'
                    ],
                    'additionalApplianceDetails': {},
                    'isReachable': True,
                    'manufacturerName': 'AaravSystems Inc',
                    'modelName': '1',
                    'version': 'Beta'
                },                                
                {
                    'applianceId': 'family-room-shade2',
                    'friendlyName': 'Family room shade 2',
                    'friendlyDescription': 'Shade 2 in family room controlled by Raspberry Pi',
                    'actions': [
                        'turnOn',
                        'turnOff'
                    ],
                    'additionalApplianceDetails': {},
                    'isReachable': True,
                    'manufacturerName': 'AaravSystems Inc',
                    'modelName': '1',
                    'version': 'Beta'
                },
                {
                    'applianceId': 'family-room-shade3',
                    'friendlyName': 'Family room shade 3',
                    'friendlyDescription': 'Shade 3 in family room controlled by Raspberry Pi',
                    'actions': [
                        'turnOn',
                        'turnOff'
                    ],
                    'additionalApplianceDetails': {},
                    'isReachable': True,
                    'manufacturerName': 'AaravSystems Inc',
                    'modelName': '1',
                    'version': 'Beta'
                },                                
                {
                    'applianceId': 'family-room-shade4',
                    'friendlyName': 'Family room shade 4',
                    'friendlyDescription': 'Shade 4 in family room controlled by Raspberry Pi',
                    'actions': [
                        'turnOn',
                        'turnOff'
                    ],
                    'additionalApplianceDetails': {},
                    'isReachable': True,
                    'manufacturerName': 'AaravSystems Inc',
                    'modelName': '1',
                    'version': 'Beta'
                },                                
                {
                    'applianceId': 'family-room-shades',
                    'friendlyName': 'Family room shades',
                    'friendlyDescription': 'All Shades in family room controlled by Raspberry Pi',
                    'actions': [
                        'turnOn',
                        'turnOff'
                    ],
                    'additionalApplianceDetails': {},
                    'isReachable': True,
                    'manufacturerName': 'AaravSystems Inc',
                    'modelName': '1',
                    'version': 'Beta'
                }                                                                                                                
            ]
        }
    }

def handleControl(context, event):
    device_id = event['payload']['appliance']['applianceId']
    logger.debug('Executing handle control request: on %s' % (device_id))    
    requestType = event['header']['name']
    if requestType == 'TurnOnRequest':
        name = 'TurnOnConfirmation'
        shade = 'ON'
    elif requestType == 'TurnOffRequest':
        name = 'TurnOffConfirmation'
        shade = 'OFF'
    # we don't support other requestTypes yet

    logger.debug('Executing: %s on %s' % (shade, device_id))

    response = iotDataPlaneClient.update_thing_shadow(
        thingName=device_id,
        payload=json.dumps({
            'state': {
                'desired': {
                    'shade': shade
                }
            }
        })
    )

    logger.debug('received {}'.format(response))

    return {
        'header': {
            "messageId": event['header']['messageId'],
            "name": name,
            "namespace":"Alexa.ConnectedHome.Control",
            "payloadVersion":"2"
        },
        'payload': {}
    }
