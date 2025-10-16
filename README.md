# 🍷 Vinheria Agnello - Monitoramento de Temperatura, Umidade e Luminosidade (ESP32 + IoT)

## Descrição
Este projeto faz parte do Checkpoint 05 da disciplina de Edge Computing, com o objetivo de implementar uma solução IoT para a Vinheria Agnello, permitindo o monitoramento do ambiente da adega em tempo real.

O sistema utiliza um ESP32 com os sensores DHT22 (temperatura e umidade) e LDR (luminosidade), publicando os dados via protocolo MQTT para o aplicativo MyMQTT, permitindo leitura e escrita bidirecional.


## 🎯 Objetivo

Monitorar variáveis ambientais críticas para a conservação dos vinhos:

- Temperatura: deve permanecer próxima a 13 °C
- Umidade: ideal entre 60% e 80%
- Luminosidade: ambientes escuros preservam a qualidade do vinho
- 
Essas informações são enviadas ao broker MQTT e podem ser visualizadas ou controladas via aplicativo MyMQTT, promovendo uma comunicação em tempo real entre hardware e aplicação.

## Materiais necessarios
- ESP32
- Sensor DHT11
- LDR + resistor de 10kΩ
- Protoboard e jumpers
- Cabo USB

## 🧑‍💻 Equipe
👤 Autor | RM |
Arthur Marcio - 563359
Gabriela Abdelnor Tavares - 562291
Maria Eduarda Sousa Acyole de Oliveira – 566337
Mayke Santos - 562680
Matheus Goes - 566407


## Diagrama esquemático
[PRINT DO DIAGRAMA]

## Configuração do MyMQTT
o Broker MQTT usado: IP local

1️⃣ Preparar o hardware

- Conecte o ESP32 ao computador via USB.
- Conecte os sensores ao ESP32:
  - DHT22 → Pino de dados no GPIO 4
  - LDR → Pino analógico GPIO 34
  - LED → LED onboard ou externo no GPIO 2
 
2️⃣ Configurar a rede Wi-Fi

3️⃣ Configurar o broker MQTT

4️⃣ Integrar sensores e LED no JSON

5️⃣ Publicação MQTT

