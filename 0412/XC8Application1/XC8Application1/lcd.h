// LCD 사용 포트
#define LCD_DATA_DIR  DDRE
#define LCD_DATA_PORT PORTE
#define LCD_CTRL_DIR  DDRB
#define LCD_CTRL_PORT PORTB
#define RIGHT         1
#define LEFT          2
#define ON            1
#define OFF           2
#define NO            0

#define LCD_E_HIGH  (LCD_CTRL_PORT |= 0x02)
#define LCD_E_LOW   (LCD_CTRL_PORT &= 0xfd)
#define LCD_RS_HIGH (LCD_CTRL_PORT |= 0x01)
#define LCD_RS_LOW  (LCD_CTRL_PORT &= 0xfe)


void E_pulse(void) {
	LCD_E_HIGH;
	_delay_ms(5);
	LCD_E_LOW;
}

void Command_set(char s) {
	LCD_RS_LOW;
	LCD_DATA_PORT = s;
	E_pulse();
}

void Data_set(char s) {
	LCD_RS_HIGH;
	LCD_DATA_PORT = s;
	E_pulse();
}

void init_lcd(void) {
	Command_set(0x38);
	Command_set(0x0f);
	Command_set(0x06);
}

void cursor_at(char x, char y) {
	switch (y) {
		case 0: y = 0x80; break;
		case 1: y = 0xc0; break;
		case 2: y = 0x94; break;
		case 3: y = 0xd4; break;
	}
	y = y+x;
	Command_set(y);
}

void writeString_lcd(char x, char y, const char *str) {
	cursor_at(x, y);
	while (*str) Data_set(*str++);
}

void cirscr(void) {
	Command_set(0x01);
	_delay_ms(5);
}

void cursor_home(void) {
	Command_set(0x02);
	_delay_ms(5);
}

void move_display(char p) {
	if (p==LEFT) Command_set(0x18);
	else if (p==RIGHT) Command_set(0x1c);
}

void move_cursor(char p) {
	if (p==RIGHT) Command_set(0x14);
	else if (p==LEFT) Command_set(0x10);
}

void Entry_shift(char p) {
	if (p==RIGHT) Command_set(0x05);
	else if (p==LEFT) Command_set(0x07);
	else if (p==NO) Command_set(0x06);
}

void display_onoff(unsigned char d, unsigned char c, unsigned char b) {
	unsigned char display = 0x08;
	if (d==ON) d = 0x04;
	else d = 0x00;
	if (c==ON) c = 0x02;
	else c = 0x00;
	if (b==ON) b = 0x01;
	else b = 0x00;

	display = display | d | c | b;
	Command_set(display);
}