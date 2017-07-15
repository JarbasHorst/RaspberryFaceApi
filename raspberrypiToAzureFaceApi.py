# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
# Jarbas Horst wrote this file. As long as you retain this notice you
# can do whatever you want with this stuff. If we meet some day, and you think
# this stuff is worth it, you can buy me a beer in return.
# ----------------------------------------------------------------------------

# ----------------------------------------------------------------------------
# This code shows how to interact with the Azure Cognitive Service "Face Api"
# to recognize the age of a person in a picture. The picture is taken using
# the Raspberry camera module after pressing a push button.
# ----------------------------------------------------------------------------

# Imports modules.
import RPi.GPIO as GPIO, picamera, random, httplib, urllib, base64, json
# BCM: Describes numbers of GPIO pins.
GPIO.setmode(GPIO.BCM)
# GPIO.PUD_UP: Defines button event which will be handled.
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# Initializes PI camera.
camera = picamera.PiCamera()
# Replace the subscription_key string value with your valid subscription key.
subscription_key = '13hc77781f7e4b19b5fcdd72a8df7156'
# Replace or verify the region.
#
# You must use the same region in your REST API call as you used to obtain your subscription keys.
# For example, if you obtained your subscription keys from the westus region, replace 
# "westcentralus" in the URI below with "westus".
#
# NOTE: Free trial subscription keys are generated in the westcentralus region, so if you are using
# a free trial subscription key, you should not need to change this region.
uri_base = 'westcentralus.api.cognitive.microsoft.com'
# Request headers.
headers = {
    'Content-Type': 'application/octet-stream',
    'Ocp-Apim-Subscription-Key': subscription_key,
}
# Request parameters.
params = urllib.urlencode({
    'returnFaceId': 'true',
    'returnFaceLandmarks': 'false',
    'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise',
})

try:    
    while True:
        if (GPIO.input(23) == 0):
            # Creates random name for picture file.
            fileName = str(random.randint(1000,9999)) + '.jpg'
            # Sets file path.
            filePath = '/home/pi/Desktop/pictures/' + fileName
            # Takes picture.
            camera.capture(filePath)
            print('The picture has been stored in ' + filePath)
            # Streams JPG image to analyze.
            fileStream = open(filePath, "rb")
            body = fileStream.read()
            fileStream.close
            # Execute the REST API call and get the response.
            conn = httplib.HTTPSConnection(uri_base)
            conn.request("POST", "/face/v1.0/detect?%s" % params, body, headers)
            response = conn.getresponse()
            data = response.read()
            # 'data' contains the JSON data. The following formats the JSON data for display.
            parsed = json.loads(data)
            
            if not parsed:
                print('Picture could not be detected. Try taking another picture.')
            else:
                print('\033[92m')
                print('Response:')
                print(json.dumps(parsed, sort_keys=True, indent=2))
                # Gets age from face attributes.
                age = parsed[0]['faceAttributes']['age']
                # Rounds and print age.
                print('\nI think your age is: ' + str(round(age)))
                print('\033[0m')
                conn.close()
                
except Exception as e:
    GPIO.cleanup()
    print('\033[91m')
    print(text)
    print('\033[0m')
