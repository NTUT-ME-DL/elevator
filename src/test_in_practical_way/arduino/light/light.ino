int floor_pin[10] = {11, 2, 3, 4, 5, 6, 8, 9, 10, 12};

void setup() {
  for (int pin = 2; pin <= 12; pin++) {
      if (pin == 7) { continue; }
      pinMode(pin, OUTPUT);
  }
  
  pinMode(LED_BUILTIN, OUTPUT);

  Serial.begin(9600);
}

void loop() {  
  if (Serial.available() > 0) {
    String incoming = Serial.readString();

    if(not incoming.startsWith("close")) {
      digitalWrite(floor_pin[incoming.toInt()], HIGH);
    } else {
      incoming.replace("close-", "");
      digitalWrite(floor_pin[incoming.toInt()], LOW);
    }
  }
}