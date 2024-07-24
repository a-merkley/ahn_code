// BART trigger setup
// Define Natus-Arduino pin mapping
int natus_pin9_latch = 51;
int natus_pin1 = 35;  // NOTE: YOU MAY NEED TO CHANGE THIS
int natus_pin2 = 51;  // Backup in case pin1 doesn't work
// Define width parameter (in ms)
int width = 20;
int width2 = 20;
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
  // Start balloon run
  else if (data == 5)
  {
    // Pulse 1
    digitalWrite(natus_pin1, HIGH);
    delay(width);
    digitalWrite(natus_pin1, LOW);
    delay(width2);
    // Pulse 2
    digitalWrite(natus_pin1, HIGH);
    delay(width);
    digitalWrite(natus_pin1, LOW);
  }
  // Space/Enter key
  else if (data == 6)
  {
    digitalWrite(natus_pin1, HIGH);
    delay(width);
    digitalWrite(natus_pin1, LOW);
  }
  // End experiment
  else if (data == 7)
  {
    digitalWrite(natus_pin9_latch, LOW);
  }
  //Start control experiment
  else if (data == 9) {
    digitalWrite(natus_pin9_latch, HIGH);
    delay(width);
    digitalWrite(natus_pin9_latch, LOW);
    delay(width2);
    digitalWrite(natus_pin9_latch, HIGH);
  }
}
