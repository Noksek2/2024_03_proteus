/*
 * main.c
 *
 * Created: 3/20/2024 4:23:26 PM
 *  Author: DatNgo
 */ 
#define F_CPU 16000000
#include <xc.h>
#include <util/delay.h>
#include <avr/io.h>
#include "lcd4.h"

int main(void)
{
	DDRF = 0xff;
	init_lcd4();
	writeString_lcd4(0, 0, "AMSD KFMA SKFM KASK");
	writeString_lcd4(0, 1, "Have a nice day");
    while(1)
    {
         
    }
}