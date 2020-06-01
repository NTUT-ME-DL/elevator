void setup() {
  // change X => for(int ...; thisPin <= X; ...)
  for (int thisPin = 2; thisPin <= 12; thisPin++) {
      if (thisPin == 7) {continue;}
      pinMode(thisPin, OUTPUT);
  }
}

void loop() {
  int randomNumber = random(0, 10);
  bool isOpenOrClose = false;
  
  while(randomNumber > 0) {
    // change X => random(2, X)
    int randomLedPin = random(2, 10);

    if(randomLedPin == 11 || randomLedPin == 12) {
      if(isOpenOrClose) {
        continue;
      } else {
        isOpenOrClose = true;
        
        digitalWrite(randomLedPin, HIGH);
        randomNumber -= 1;
      }
    } else {
      digitalWrite(randomLedPin, HIGH);
      randomNumber -= 1;
    }
  }
  
  digitalWrite(11, HIGH);
  digitalWrite(12, HIGH);
  delay(300);

  // change X => for(int ...; thisPin <= X; ...)
  for(int thisPin = 2; thisPin <= 12; thisPin++) {
      if (thisPin == 7) {continue;}
      digitalWrite(thisPin, LOW);
  } 
}