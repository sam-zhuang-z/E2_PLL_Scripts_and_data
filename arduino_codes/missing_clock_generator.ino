// generation of missing clock signals 
unsigned long hp = 10; //default 10 microsecond per pulse
bool instructions[1000];
long runtime = 10000;
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  DDRB=B110000;
}

void loop() {
  // put your main code here, to run repeatedly:

  // recieve instructions
  unsigned long task_filler = 0;
  while (true){
    char receive_char = Serial.read();
    if (receive_char == '('){
      //parseint
      int iterator = Serial.parseInt();
      // add to string
      if (iterator > 0) {
        for (int i = 1; i <= iterator; i++) {
          instructions[task_filler] = true;
          task_filler++;
        }
      }
      if (iterator < 0 ) {
        for (int i = 1; i <= -iterator; i++){
          instructions[task_filler] = false;
          task_filler++;
        }
      }
    }
    else if (receive_char == ','){
      //parseint 
      // add to string
      int iterator = Serial.parseInt();
      // add to string
      if (iterator > 0) {
        for (int i = 1; i <= iterator; i++) {
          instructions[task_filler] = true;
          task_filler++;
        }
      }
      if (iterator < 0 ) {
        for (int i = 1; i <= -iterator; i++){
          instructions[task_filler] = false;
          task_filler++;
        }
      }
    }
    else if (receive_char == '+') {
      hp = Serial.parseInt();
    }
    else if (receive_char == ')') {
      break;
    }
  }
  //out of while loop
  Serial.println("proceed");
  Serial.flush();
  // wait for char
    //start on start char
    //break on end char
    // parseInt 
    // append to string
  //

  //looping of built string
  //calculate operation time
  long e_loop_count = runtime*1000/(2*hp*task_filler);
  
  // disable interrupts
  cli();
  // looping through profile for a few seconds
  for (long i = 0; i <= e_loop_count; i++){
    //start of small batch here
    delayMicroseconds(hp-2);
    PORTB=B000000; // filling in the gap between repetitions
    delayMicroseconds(hp);
    PORTB=B110000;// indication of start of loop 
    //maybe send a pulse on second pin here
    for (long profile_i = 0; profile_i < task_filler; profile_i++){
      //go through every element in instructions array
      //decide if active
      delayMicroseconds(hp-1);
      PORTB=B000000;
      if (instructions[profile_i]){
        delayMicroseconds(hp-1);
        PORTB=B100000;
      }
      else{
        delayMicroseconds(hp-1);
        PORTB=B000000;
      }
    }
  }
  sei();
  PORTB=B000000;
  // reenable interrupts
}
