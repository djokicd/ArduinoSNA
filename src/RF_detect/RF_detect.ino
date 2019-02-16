//
// Read and process pin A0.
//
// Notes:
//   Connect RF detector voltage output to pin A0.
//  Serial data is being sent back.
//


// int voltagePin = A0;
String inputString = "";


void setup()
{
  pinMode(A0, INPUT);
  pinMode(A1, INPUT);
  pinMode(A2, INPUT);

  Serial.begin(9600);
  //Serial.println("Init");
}

float V;
float P;

void loop(){}

void sample(int X)
{
  V = analogRead(X)/1024.00 * 5.00;

  Serial.print( String(V, 10) ) ;
  Serial.print('\n');
  delay(100);
}

void serialFlush(){
  while(Serial.available() > 0) {
    char t = Serial.read();
  }
}

void serialEvent() {


  while (Serial.available()) {
    // get the new byte:
    char inChar = (char) Serial.read();
    // add it to the inputString:
    inputString += inChar;
    if (inChar == '\n') {
      if (inputString == "SAMPLE\n") sample(A0);
      if (inputString == "SAMPLE0\n") sample(A0);
      if (inputString == "SAMPLE1\n") sample(A1);
      if (inputString == "SAMPLE2\n") sample(A2);
      if (inputString == "INIT\n") serialFlush();
      inputString = "";
    }
  }


}
