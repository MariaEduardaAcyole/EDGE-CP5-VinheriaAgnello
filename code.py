// =====================================================
// Projeto: Vinheria Agnello - Monitoramento IoT (ESP32)
// Autor base: Fábio Henrique Cabrini
// Revisões e atualização: Ivru
// Descrição: Envia temperatura, umidade e luminosidade via MQTT
// =====================================================
 
#include <WiFi.h>
#include <PubSubClient.h>
#include <DHT.h>  // Biblioteca para o DHT22
 
// ----------------------------
// CONFIGURAÇÕES DE HARDWARE
// ----------------------------
#define DHTPIN   4        // Pino de dados do DHT22
#define DHTTYPE  DHT11    // Tipo de sensor DHT (DHT11 ou DHT22)
#define LDR_PIN  34       // Pino analógico do LDR
#define LED_PIN  2        // LED onboard do ESP32
 
DHT dht(DHTPIN, DHTTYPE); // Instância do sensor DHT
 
// ----------------------------
// CONFIGURAÇÕES DE REDE E MQTT
// ----------------------------
const char* SSID          = "FIAP-IOT";     // Nome da rede Wi-Fi
const char* PASSWORD      = "F!@p25.IOT";   // Senha da rede
const char* BROKER_MQTT   = "54.227.182.115";
const int   BROKER_PORT   = 1883;
 
// Tópicos MQTT (padronizados para device011)
const char* TOPICO_SUBSCRIBE     = "/TEF/device011/cmd";
const char* TOPICO_PUBLISH_MAIN  = "/TEF/device011/attrs";       // JSON/UL
const char* TOPICO_PUBLISH_TEMP  = "/TEF/device011/attrs/temp";  // Temperatura
const char* TOPICO_PUBLISH_UMI   = "/TEF/device011/attrs/umid";  // Umidade
const char* TOPICO_PUBLISH_LDR   = "/TEF/device011/attrs/luz";   // Luminosidade
 
const char* ID_MQTT              = "fiware_device011";
 
WiFiClient espClient;
PubSubClient MQTT(espClient);
 
// ----------------------------
// VARIÁVEIS GLOBAIS
// ----------------------------
char EstadoSaida = '0'; // '1' = on, '0' = off
 
// ----------------------------
// FUNÇÕES AUXILIARES
// ----------------------------
void initSerial() {
  Serial.begin(115200);
  delay(100);
  Serial.println("Inicializando monitor serial...");
}
 
void initWiFi() {
  Serial.println("\nConectando ao Wi-Fi...");
  WiFi.mode(WIFI_STA);
  WiFi.begin(SSID, PASSWORD);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWi-Fi conectado!");
  Serial.print("IP: ");
  Serial.println(WiFi.localIP());
}
 
void reconnectWiFi() {
  if (WiFi.status() == WL_CONNECTED) return;
  Serial.println("Reconectando Wi-Fi...");
  WiFi.begin(SSID, PASSWORD);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWi-Fi reconectado!");
}
 
void callbackMQTT(char* topic, byte* payload, unsigned int length) {
  String msg;
  msg.reserve(length + 1);
  for (unsigned int i = 0; i < length; i++) {
    msg += (char)payload[i];
  }
 
  Serial.print("\nMensagem recebida [");
  Serial.print(topic);
  Serial.print("]: ");
  Serial.println(msg);
 
  // Aceita formatos simples contendo "on"/"off"
  // (ajuste aqui se o seu backend enviar outro padrão, ex.: "led|on")
  if (msg.indexOf("on") != -1) {
    digitalWrite(LED_PIN, HIGH);
    EstadoSaida = '1';
  } else if (msg.indexOf("off") != -1) {
    digitalWrite(LED_PIN, LOW);
    EstadoSaida = '0';
  }
}
 
void initMQTT() {
  MQTT.setServer(BROKER_MQTT, BROKER_PORT);
  MQTT.setCallback(callbackMQTT);
  // Buffer maior para publicar JSON com tranquilidade
  MQTT.setBufferSize(256);
}
 
void reconnectMQTT() {
  while (!MQTT.connected()) {
    Serial.print("Conectando ao Broker MQTT...");
    // (opcional) Last Will: avisa se dispositivo cair
    if (MQTT.connect(ID_MQTT, TOPICO_PUBLISH_MAIN, 0, true, "{\"status\":\"offline\"}")) {
      Serial.println("Conectado!");
      MQTT.subscribe(TOPICO_SUBSCRIBE);
      // (opcional) status online
      MQTT.publish(TOPICO_PUBLISH_MAIN, "{\"status\":\"online\"}", true);
    } else {
      Serial.print("Falha, rc=");
      Serial.print(MQTT.state());
      Serial.println(" | Tentando novamente em 2s...");
      delay(2000);
    }
  }
}
 
// ----------------------------
// FUNÇÕES DE LEITURA/PUBLICAÇÃO
// ----------------------------
void readAndPublishSensors() {
  float temperatura = dht.readTemperature(); // °C
  float umidade     = dht.readHumidity();    // %
  int   ldrValue    = analogRead(LDR_PIN);   // 0..4095
  int   luminosidade= map(ldrValue, 0, 4095, 0, 100); // 0..100%
 
  if (!isnan(temperatura) && !isnan(umidade)) {
    // Publica JSON no tópico principal
    char payload[160];
    snprintf(payload, sizeof(payload),
             "{\"temp\":%.2f,\"umid\":%.2f,\"luz\":%d,\"led\":\"%s\"}",
             temperatura, umidade, luminosidade, (EstadoSaida == '1' ? "on" : "off"));
    Serial.println(payload);
    MQTT.publish(TOPICO_PUBLISH_MAIN, payload, true); // retain = true
 
    // Publica nos tópicos por atributo (muitos apps escutam assim)
    char buf[32];
    dtostrf(temperatura, 0, 2, buf);  MQTT.publish(TOPICO_PUBLISH_TEMP, buf, true);
    dtostrf(umidade,     0, 2, buf);  MQTT.publish(TOPICO_PUBLISH_UMI,  buf, true);
    snprintf(buf, sizeof(buf), "%d", luminosidade);
    MQTT.publish(TOPICO_PUBLISH_LDR,  buf, true);
 
    Serial.println("----- Dados enviados ao broker -----");
    Serial.println(payload);
    Serial.println("-----------------------------------");
  } else {
    Serial.println("Falha na leitura do DHT22!");
  }
}
 

 
// ----------------------------
// SETUP E LOOP PRINCIPAL
// ----------------------------
void setup() {
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, LOW);
 
  initSerial();
  initWiFi();
  initMQTT();
  dht.begin();
 
  Serial.println("Sistema iniciado com sucesso!");
}
 
void loop() {
  reconnectWiFi();
  if (!MQTT.connected()) reconnectMQTT();
  MQTT.loop();
 
  readAndPublishSensors();   // envia sensores + LED
  delay(5000);               // a cada 5 segundos
}
