#include <WProgram.h>


#define INTERRUPT_GRACE 300ul

// Ignore triggers that last too short a time (typical car passes are on the
// order of 300-600 (measured in i/o read cycles)
#define MIN_PASS_DURATION 50

#define PIN_LED_0 5
#define PIN_LED_1 6

#define PIN_TRACK_0 2
#define PIN_TRACK_1 3

#define INVERT_TRACK 1

#define INTERRUPT_TRACK_0 0
#define INTERRUPT_TRACK_1 1


typedef struct {
	// Flag indicating the lane was interrupted
	bool flag;
	
	// Is the ISR enabled for this lane
	bool isr_disabled;
	
	// The ISR
	void (*isr)();
	
	// Milis when the interrupt was last triggered
	unsigned long last_trigger;
	
	// Cycles during which the sensor was triggered
	int pass_duration;
	
	// Pin the track sensor is on
	int track_pin;
	
	// Pin the debug LED is on
	int led_pin;
	
	// The interrupt number
	int interrupt;
} lane_t;


lane_t lanes[2];


#define DEF_ISR(name, lane) \
	void name() {\
		if (lanes[lane].isr_disabled)\
			return; \
		int count = 0;\
		while (digitalRead(lanes[lane].track_pin) != INVERT_TRACK) \
			count++;\
		if (count < MIN_PASS_DURATION)\
			return;\
		lanes[lane].pass_duration = count;\
		lanes[lane].flag = true; \
		lanes[lane].isr_disabled = true; \
		lanes[lane].last_trigger = millis(); \
		detachInterrupt(lanes[lane].interrupt);\
	}

// Define ISRs
DEF_ISR(interrupt_track_0, 0)
DEF_ISR(interrupt_track_1, 1)


void
setup()
{
	lanes[0].flag = false;
	lanes[1].flag = false;
	
	lanes[0].isr_disabled = true;
	lanes[1].isr_disabled = true;
	
	lanes[0].isr = interrupt_track_0;
	lanes[1].isr = interrupt_track_1;
	
	lanes[0].last_trigger = 0ul;
	lanes[1].last_trigger = 0ul;
	
	lanes[0].led_pin = PIN_LED_0;
	lanes[1].led_pin = PIN_LED_1;
	
	lanes[0].track_pin = PIN_TRACK_0;
	lanes[1].track_pin = PIN_TRACK_1;
	
	lanes[0].interrupt = INTERRUPT_TRACK_0;
	lanes[1].interrupt = INTERRUPT_TRACK_1;
	
	// Enable the status LEDs
	pinMode(PIN_LED_0, OUTPUT);
	pinMode(PIN_LED_1, OUTPUT);
	digitalWrite(PIN_LED_0, HIGH);
	digitalWrite(PIN_LED_1, HIGH);
	
	// Enable the tracks with pullups
	pinMode(PIN_TRACK_0, INPUT);
	pinMode(PIN_TRACK_1, INPUT);
	digitalWrite(PIN_TRACK_0, HIGH);
	digitalWrite(PIN_TRACK_1, HIGH);
	
	Serial.begin(9600);
}


void
loop()
{
	for (int i = 0; i < 2; i++) {
		if (lanes[i].flag) {
			lanes[i].flag = false;
			digitalWrite(lanes[i].led_pin, HIGH);
			Serial.print(i);
			Serial.print(' ');
			Serial.println(lanes[i].last_trigger);
		}
		
		if (lanes[i].isr_disabled
		    && (lanes[i].last_trigger + INTERRUPT_GRACE) < millis()) {
			attachInterrupt(lanes[i].interrupt, lanes[i].isr, INVERT_TRACK ? FALLING : RISING);
			lanes[i].isr_disabled = false;
			digitalWrite(lanes[i].led_pin, LOW);
		}
	}
}
