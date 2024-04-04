/*
 * main.c
 *
 * Created: 3/7/2024 10:28:26 AM
 *  Author: USER
 */ 
#define F_CPU 16000000UL
#include <xc.h>
#include <avr/io.h>
#include <util/delay.h>
#include <time.h>
#include <stdlib.h>
int printLedX(void) {
	unsigned short led1=0x0000;
	unsigned short led2=0x0000;
	unsigned short led;
	DDRB=0xff;
	DDRE=0xff;
    while(1) {
		led=led1|led2;
		if(led1==0)led1=0x0001; else led1<<=1;
		if(led2==0)led2=0x8000; else led2>>=1;
		if(led1==256)continue;
		_delay_ms(20);
		PORTB=led%256;
		PORTE=led/256;
        //TODO:: Please write your application code 
    }
}
int printButton(void){
	DDRB=0xff;
	DDRE=0xff;
	DDRC=0x00;
	PORTC=0xff;
	unsigned char btn;
	while(1){
		btn=PINC;
		PORTB=~btn;
		_delay_ms(20);
	}
}

//MATRIX LED
inline unsigned char GetLedBit(unsigned char lednum){
	unsigned char innum,outnum;
	innum=1<<(lednum%4);
	outnum=~(1<<(lednum/4));
	return (outnum<<4)+innum;
}
void printMatrixLed(){
	DDRB=0xff;
	PORTB=0;
	unsigned char lednum=0;
	while(1){
		PORTB=GetLedBit(lednum);
		lednum=(lednum+1)%16;
		_delay_ms(20);
	}
}
unsigned char getBtn(unsigned char btnout){
	unsigned char a,b;
	unsigned char btnin;
	btnin=PINE;
	btnin^=btnout;
	btnin>>=4;
	if(btnin){
		a=btnin/2;
		if(a==4)a--;
		b=btnout/2;
		if(a==4)btnout--;
		return b*4+a;
	}
	return 0;
}

int main(){
	DDRB=0xff;
	PORTB=0;
	
	DDRE=0x0f;
	PORTE=0x01;
	unsigned char btnout=0x01;
	
	unsigned char lednum=0;
	while(1){
		lednum=getBtn(btnout);
		PORTB=GetLedBit(lednum);
		btnout=(btnout<<1)%256;
		PORTE=btnout;
		_delay_ms(20);
	}
}//in:0001 out:0000