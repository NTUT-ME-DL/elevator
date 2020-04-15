void setup() {
  for (int thisPin = 2; thisPin <= 12; thisPin++) {
      if (thisPin == 7) {continue;}
      pinMode(thisPin, OUTPUT);
  }
}

void loop() {
  int randomNumber = random(0, 10);
  while(randomNumber > 0) {
    int randomLedPin = random(2, 12 + 1);
    digitalWrite(randomLedPin, HIGH);
    randomNumber -= 1;
  }
  delay(500);

  for(int thisPin = 2; thisPin <= 12; thisPin++) {
      if (thisPin == 7) {continue;}
      digitalWrite(thisPin, LOW);
  } 
}