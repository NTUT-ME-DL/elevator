void setup() {
  Serial.begin(9600);

  for (int thisPin = 2; thisPin <= 12; thisPin++) {
      pinMode(thisPin, OUTPUT);
  }      
}

void loop() {  
  // 檢查是否有資料可供讀取
  if (Serial.available() > 0) {
    int inByte = Serial.read();
    switch (inByte) {
      case '1':
        digitalWrite(2, HIGH);
        delay(1000);
        break;
      case '2':
        digitalWrite(3, HIGH);
        delay(1000);
        break;
      case '3':
        digitalWrite(4, HIGH);
        delay(1000);
        break;
      case '4':   
        digitalWrite(5, HIGH);
        delay(1000);
        break;
      case '5':   
        digitalWrite(6, HIGH);
        delay(1000);
        break;
      case '6':   
        digitalWrite(8, HIGH);
        delay(1000);
        break;
      case '7':   
        digitalWrite(9, HIGH);
        delay(1000);
        break;
      case '8':   
        digitalWrite(10, HIGH);
        delay(1000);
        break;
      case '9':   
        digitalWrite(11, HIGH);
        delay(1000);
        break;
      case '10':   
        digitalWrite(12, HIGH);
        delay(1000);
        break;
      default:
        for (int thisPin = 2; thisPin <= 12; thisPin++) {
          digitalWrite(thisPin, LOW);
        }
    }
  }
}