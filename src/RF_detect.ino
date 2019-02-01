//
// Read and process pin A0.
//
// Notes:
// 	Connect RF detector voltage output to pin A0.
// 	Serial data is being sent back.
//


int voltagePin = A0;

void setup()
{
  pinMode(voltagePin, OUTPUT);
  Serial.begin(9600);
}

float V;
float P;

void loop(){}

void sample()
{
  V = analogRead(A0)/1024.00 * 5.00;
  P = 24 - 40 * V - 5;  
  Serial.println( String(V) + " V\t" + String(P) + " dBm") ;
  delay(100);
}

void serialEvent() {
  while (Serial.available()) {
    // get the new byte:
    char inChar = (char)Serial.read();
    // add it to the inputString:
    inputString += inChar;
    if (inChar == '\n') {
      stringComplete = true;
    }
  }
  
  if (inputString == "SAMPLE\n") sample();
}
