#include "mbed.h"
#include "bbcar.h"
#include "bbcar_rpc.h"


Ticker servo_ticker;
PwmOut pin5(D5), pin6(D6);
// DigitalInOut pin11(D11);
BBCar car(pin5, pin6, servo_ticker);
BufferedSerial pc(USBTX,USBRX); //tx,rx
BufferedSerial uart(D1,D0); //tx,rx

BufferedSerial xbee(D10,D9); //tx,rx

void read_data() {
   char buf[256], outbuf[256];
   while(1){
      for (int i=0; ; i++) {
         char *recv = new char[1];
         uart.read(recv, 1);
         buf[i] = *recv;
         if (*recv == '\n') {
            buf[i] = '\0';
            break;
         }
      }
      // printf("%s", buf);
      if (!strcmp(buf,"Done")) {
            break;         
      }
      else 
         RPC::call(buf, outbuf);        
   }    
   // printf("BYE\n"); 
}

int main() {
   uart.set_baud(9600);

   char tmp[30];
   FILE *devin = fdopen(&xbee, "r");
   FILE *devout = fdopen(&xbee, "w");
   while(1) {
      memset(tmp, 0, 30);
      for( int i = 0; ; i++ ) {
         char recv = fgetc(devin);
         if(recv == '\n') {
            printf("\r\n");
            recv = '\0';
            break;
         }
         tmp[i] = fputc(recv, devout);
      } 
      // printf("got it\n");
      if(!strcmp(tmp,"all")) {
         // printf("%s", tmp);
         uart.write("all\n", 6); 
         read_data();
      }
      else if(!strcmp(tmp,"following")) {
         // printf("%s", tmp);
         uart.write("following\n", 12); 
         read_data();
      }
      else if(!strcmp(tmp,"classification")) {
         // printf("%s", tmp);
         uart.write("classification\n", 17); 
         read_data();
      }
      else if(!strcmp(tmp,"parking")) {
         // printf("%s", tmp);
         uart.write("parking\n", 10); 
         read_data();
      }
      else if(!strcmp(tmp,"finish")) {
         // printf("%s", tmp);
         uart.write("finish\n", 9); 
         break;
      }
      else{
         // printf("byebye\n");
         // printf("error: %s", tmp);
         uart.write("xbee error\n", 13);
      }
         
      }
}

