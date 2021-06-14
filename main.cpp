#include "mbed.h"
#include "bbcar.h"
#include "bbcar_rpc.h"


Ticker servo_ticker;
PwmOut pin5(D5), pin6(D6);

BBCar car(pin5, pin6, servo_ticker);
BufferedSerial pc(USBTX,USBRX); //tx,rx
BufferedSerial uart(D1,D0); //tx,rx

BufferedSerial xbee(D10,D9); //tx,rx



int main() {
   
   char mode[10];
   FILE *devin = fdopen(&xbee, "r");
   FILE *devout = fdopen(&xbee, "w");
   while(1) {
      memset(mode, 0, 10);
      for( int i = 0; ; i++ ) {
         char recv = fgetc(devin);
         if(recv == '\n') {
            printf("\r\n");
            break;
         }
         mode[i] = fputc(recv, devout);
      } 
      break;     
   }

   // printf("receving: %s\n", mode);


   uart.set_baud(9600);
   if(!strcmp(mode,"normal")) 
      // printf("normal\n");
      uart.write("normal\n", 9);
   else if(!strcmp(mode,"sport"))
      // printf("sport\n");
      uart.write("sport\n", 8);
   else
      // printf("error\n");
      uart.write("xbee error\n", 13);

   char buf[256], outbuf[256];
   while(1){
      for (int i=0; ; i++) {
         char *recv = new char[1];
         uart.read(recv, 1);
         buf[i] = *recv;
         if (*recv == '\n') {
         break;
         }
      }
      printf("%s\r\n", buf);
      RPC::call(buf, outbuf);        
   } 
}

