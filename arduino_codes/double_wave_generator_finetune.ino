int half_period = 100;
int phase_diff_time = 0;
int SIG_IN = 13;
int COMP_IN = 12;
long runtime = 3000;
long runmode = -1;
long offset_1 = 10;
long offset_2 = 10;
long offset_3 = 10;
long offset_4 = 10;

void setup() {
  Serial.begin(9600);
  DDRB=B110000;
}

void loop() {
  // put your main code here, to run repeatedly:
  //if serial available
  //readline and parse "runtime (ms),runmode,offset_1(millis),offset_2,offset_3,offset_4,offset5"


  while (Serial.read() != 0x28) {
  }
  runtime = Serial.parseInt();
  Serial.read();
  runmode = Serial.parseInt();
  Serial.read();
  offset_1 = Serial.parseInt();
  Serial.read();
  offset_2 = Serial.parseInt();
  Serial.read();
  offset_3 = Serial.parseInt();
  Serial.read();
  offset_4 = Serial.parseInt();
  Serial.read();
  Serial.println(offset_1);
  Serial.println(offset_2);
  Serial.flush();
  
  if (offset_2 == 0){
    runmode == -1;
    long e_loop_count = runtime*2000/(offset_1 + offset_2);
    Serial.println(e_loop_count);
    cli();
    for (long i = 0; i <= e_loop_count; i++){
      PORTB=B100000;
      delayMicroseconds(offset_1);
      PORTB=B010000;
      delayMicroseconds(offset_1 - 1);
    }
    sei();

  }
  if (runmode == 0) {
    long e_loop_count = runtime*1000/(offset_1 + offset_2);
    Serial.println(e_loop_count);
    Serial.flush();
//    Serial.println(e_loop_count);
    cli();
    for (long i = 0; i <= e_loop_count; i++){
      PORTB=B110000;
      delayMicroseconds(offset_1);
      PORTB=B000000;
      delayMicroseconds(offset_2);
    }
    sei();
  }
  //determine runmode sinlge
    //apply offsets 
    //turn of interrupts
    //record start time
    //calculate end time using runtime
    //while time still left
      //do very clean register loops
    //turn interrupts on

  //loop end of phase_diff = 0
  if (runmode == 1) {
    long e_loop_count = runtime*1000/(offset_1 + offset_2 + offset_3 + offset_4);
//    Serial.println(e_loop_count);
    cli();
    for (long i = 0; i <= e_loop_count; i++){
      PORTB=B100000;
      delayMicroseconds(offset_1);
      PORTB=B110000;
      delayMicroseconds(offset_2);
      PORTB=B010000;
      delayMicroseconds(offset_3);
      PORTB=B000000;
      delayMicroseconds(offset_4);
    }
    sei();
  }

  //loop start for SIG_IN ahead runmode front

    //turn of interrupts
    //determine steps by pre-calculating offset times
    //record start time
    //calculate end time
    //while time still left
      //do very clean register loops
    //turn interrupts on

  //loop end for SIG_IN case
    if (runmode == 2) {
    long e_loop_count = runtime*1000/(offset_1 + offset_2 + offset_3 + offset_4);
//    Serial.println(e_loop_count);
    cli();
    for (long i = 0; i <= e_loop_count; i++){
      PORTB=B010000;
      delayMicroseconds(offset_1);
      PORTB=B110000;
      delayMicroseconds(offset_2);
      PORTB=B100000;
      delayMicroseconds(offset_3);
      PORTB=B000000;
      delayMicroseconds(offset_4);
    }
    sei();
    delay(1000);
  }


  //loop start for COMP_IN ahead runmode back

    //turn off interrupts
    //determine steps by pre-calculating offset times
    //record start time
    //calculate end time
    //while time still left
      //do very clean register loops
    //turn interrupts on

  //loop end for COMP_IN case
}
