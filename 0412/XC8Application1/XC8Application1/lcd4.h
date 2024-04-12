#define LCD_DATA_DIR  DDRF
#define LCD_DATA_PORT PORTF
#define LCD_CTRL_DIR  DDRF
#define LCD_CTRL_DATA PORTF

#define RIGHT 1
#define LEFT  2
#define ON    1
#define OFF   2
#define NO    0

#define LCD_E_HIGH  (LCD_CTRL_DATA |= 0x02)
#define LCD_E_LOW   (LCD_CTRL_DATA &= 0xfd)
#define LCD_RS_HIGH (LCD_CTRL_DATA |= 0x01)
#define LCD_RS_LOW  (LCD_CTRL_DATA &= 0xfe)

void delay(int d) {
	int i;
	for (i=0; i<d; i++) _delay_ms(1);
}

void E_pulse(void) {
	LCD_E_HIGH;
	delay(5);
	LCD_E_LOW;
}

void Command_set4(char s) {
	LCD_RS_LOW;
	LCD_DATA_PORT = (s&0xf0);
	E_pulse();
	LCD_DATA_PORT = (s<<4);
	E_pulse();
}

void cirscr4(void) {
	Command_set4(0x01);
	delay(5);
}

void Data_set4(char s) {
	LCD_RS_HIGH;
	LCD_DATA_PORT = (s&0xf0) | 0x01;
	E_pulse();
	LCD_DATA_PORT = (s<<4) | 0x01;
	E_pulse();
}

void init_lcd4(void) {
	LCD_DATA_PORT = 0xff;
	Command_set4(0x28);
	Command_set4(0x06);
	Command_set4(0x0c);
	cirscr4();
}

void cursor_at4(char x, char y) {
	switch (y) {
		case 0: y = 0x80; break;
		case 1: y = 0xc0; break;
		case 2: y = 0x94; break;
		case 3: y = 0xd4; break;
	}
	y = y+x;
	Command_set4(y);
}

void writeString_lcd4(char x, char y, const char *str) {
	cursor_at4(x, y);
	while (*str) Data_set4(*str++);
}

void cursor_home4(void) {
	Command_set4(0x02);
	delay(5);
}

void move_display4(char p) {
	if (p==LEFT) Command_set4(0x18);
	else if (p==RIGHT) Command_set4(0x1c);
}

void move_cursor4(char p) {
	if (p==RIGHT) Command_set4(0x14);
	else if (p==LEFT) Command_set4(0x10);
}

void Entry_shift4(char p) {
	if (p==RIGHT) Command_set4(0x05);
	else if (p==LEFT) Command_set4(0x07);
	else if (p==NO) Command_set4(0x06);
}

void display_onoff4(unsigned char d, unsigned char c, unsigned char b) {
	unsigned char display = 0x08;
	if (d==ON) d = 0x04;
	else d = 0x00;
	if (c==ON) c = 0x02;
	else c = 0x00;
	if (b==ON) b = 0x01;
	else b = 0x00;

	display = display | d | c | b;
	Command_set4(display);
}