int natus_pin9_latch = 51;
int natus_pin1 = 35;  // NOTE: YOU MAY NEED TO CHANGE THIS
int natus_pin2 = 51;  // Backup in case pin1 doesn't work
// Define width parameter (in ms)
int width = 200;
int width2 = 200;
// Define misc
int data;


void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  pinMode(natus_pin1, OUTPUT);
  pinMode(natus_pin2, OUTPUT);
  pinMode(natus_pin9_latch, OUTPUT);

  digitalWrite(natus_pin9_latch, HIGH);
}


void loop() {
  data = Serial.read();
  // Start experiment
  if (data == 8)
  {
    digitalWrite(natus_pin9_latch, HIGH);
  }
  // stim onset
  else if (data == 5)
  {
    // Pulse 
    digitalWrite(natus_pin1, HIGH);
    delay(width);
    digitalWrite(natus_pin1, LOW);
  }

 // person makes a choice
  else if (data == 6) 
  {
// pulse 
    digitalWrite(natus_pin1, HIGH);
    delay(width);
    digitalWrite(natus_pin1, LOW);
  }
  //showing the answer
  else if (data == 7) {
    digitalWrite(natus_pin1, HIGH);
    delay(width);
    digitalWrite(natus_pin1, LOW);
  }

}