#include <WiFi.h>
#include <PubSubClient.h>

#define BLDC 0
#define BLDC_PIN 15
#define BONK 1
#define BONK_PIN 2
#define RELAY_1 4
#define RELAY_2 13

const char* ssid = "fy1928";
const char* password = "r11271688";

const char* mqtt_server = "192.168.43.76";
const char* topic = "sleep";

WiFiClient espClient;
PubSubClient client(espClient);

unsigned long lastMsg = 0;
#define MSG_BUFFER_SIZE  (50)
char msg[MSG_BUFFER_SIZE];

int state = 0;

void higher() {
  digitalWrite(RELAY_1, HIGH);
  digitalWrite(RELAY_2, HIGH);
}

void lower() {
  digitalWrite(RELAY_1, LOW);
  digitalWrite(RELAY_2, LOW);
}

void hold() {
  digitalWrite(RELAY_1, HIGH);
  digitalWrite(RELAY_2, LOW);
}

void stage1() {
  ledcWrite(BLDC, 13);
}

void stage2() {
  ledcWrite(BLDC, 10);

  for (int i = 0; i < 51; ++i) {
    ledcWrite(BONK, i);
    delay(10);
  }
  delay(100);
  for (int i = 51; i > 0; --i) {
    ledcWrite(BONK, i);
    delay(10);
  }
  delay(3000);
}

void servoDown() {
  for (int i = 0; i < 51; ++i) {
    ledcWrite(BONK, i);
    delay(10);
  }
}

void servoUp() {
  for (int i = 51; i > 0; --i) {
    ledcWrite(BONK, i);
    delay(10);
  }
}
void stage3() {
  lower();
  delay(8000);
  hold();
}


void setup_wifi() {

  delay(10);
  // We start by connecting to a WiFi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  randomSeed(micros());

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");
  for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
  }
  Serial.println();

  state = (char)payload[0] - '0';
  
}

void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Create a random client ID
    String clientId = "ESP8266Client-";
    clientId += String(random(0xffff), HEX);
    // Attempt to connect
    if (client.connect(clientId.c_str())) {
      Serial.println("connected");
      // ... and resubscribe
      client.subscribe(topic);
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}

void setup() {
    
  ledcSetup(BLDC, 50, 8);
  ledcAttachPin(BLDC_PIN, BLDC);
  ledcSetup(BONK, 50, 8);
  ledcAttachPin(BONK_PIN, BONK);
  pinMode(RELAY_1, OUTPUT);
  pinMode(RELAY_2, OUTPUT);

  hold();
  ledcWrite(BLDC, 10);
  
  Serial.begin(115200);
  lower();
  delay(10000);
  higher();
  delay(5200);
  hold();
  
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
  
}

void loop() {
  
  if (!client.connected()) {
    reconnect();
  }
  client.loop();
  
  
  if (Serial.available()) {
    state = Serial.parseInt();
  }
  Serial.println(state);
  switch (state) {
    case 0: // idle
      ledcWrite(BLDC, 10);
      hold();
      break;
    case 1:
      ledcWrite(BLDC, 13);
      break;
    case 2:
      ledcWrite(BLDC, 10);
      servoDown();
      delay(100);
      servoUp();
      delay(500);
      break;
    case 3:
      servoUp();
      lower();
      delay(6000);
      break;
    case 4: // reset
      ledcWrite(BLDC, 10);
      servoUp();
      lower();
      delay(6000);
      higher();
      delay(5200);
      hold();
      state = 0;
      break;
    default:
      Serial.println("Error in state");
  }
  /*
  if (Serial.available()) {
    int cmd = Serial.parseInt();
    if (cmd == 1) {
      lower();
      delay(10000);
    }
    if (cmd ==0) {    
      lower();
      delay(6000);
      hold();
      delay(1000);
      higher();
      delay(5300);
      hold();
      delay(3000);   
    }
  }*/
}
