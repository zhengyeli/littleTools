import base64
import hmac
import time
import urllib.parse

import paho.mqtt.client as mqtt

hubAddress = 'a3d1vz6v56pkuw-ats.iot.us-east-1.amazonaws.com'
deviceId = 'pycharm_00d6f8fd'

ca_cert = 'D:\\智岩科技有限公司\\公司工具及文件\\IOT TEST\\rootCA.pem'
keyfile = 'D:\\智岩科技有限公司\\公司工具及文件\\IOT TEST\\b2f000de59-private.pem.key'
certPath = 'D:\\智岩科技有限公司\\公司工具及文件\\IOT TEST\\b2f000de59-certificate.pem.crt'

hubTopicPublish = 'GD/bb88a07bdd61754adbb03b5d6c564f67'
hubTopicSubscribe = 'GD/bb88a07bdd61754adbb03b5d6c564f67'


class govee_mqtt_client:
    def __init__(self):
        self.client = mqtt.Client(client_id=deviceId, protocol=mqtt.MQTTv311)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.tls_set(ca_certs=ca_cert, certfile=certPath, keyfile=keyfile)
        self.client.connect(hubAddress, port=8883, keepalive=60)
        # self.client.loop_forever()
        self.client.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        self.client.subscribe(hubTopicSubscribe)

    def on_message(self, client, userdata, msg):
        pass
        # print("{0} - {1} ".format(msg.topic, str(msg.payload)))

    def generate_sas_token(self, uri, key, expiry=3600):
        ttl = int(time.time()) + expiry
        urlToSign = urllib.parse.quote(uri, safe='')
        print(urlToSign)
        sign_key = "%s\n%d" % (urlToSign, int(ttl))
        h = hmac.new(base64.b64decode(key), msg="{0}\n{1}".format(urlToSign, ttl).encode('utf-8'), digestmod='sha256')
        signature = urllib.parse.quote(base64.b64encode(h.digest()), safe='')
        return "SharedAccessSignature sr={0}&sig={1}&se={2}".format(urlToSign,
                                                                    urllib.parse.quote(base64.b64encode(h.digest()),
                                                                                       safe=''), ttl)

    def disconnect(self):
        self.client.disconnect()

    def send(self, string):
        self.client.publish(hubTopicPublish, string)
