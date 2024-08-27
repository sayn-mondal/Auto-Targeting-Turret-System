#include <AccelStepper.h> // Library for stepper motor control
#include <Servo.h>

AccelStepper stepperX(1, 2, 5); // Define X-axis stepper motor pins (Step, Dir)
AccelStepper stepperY(1, 3, 6); // Define Y-axis stepper motor pins (Step, Dir)
Servo servoTrigger; // Servo for toy gun trigger

int x;
int y;
int prevX = -1; // Initialize previous coordinates to invalid values
int prevY = -1; 

void setup()
{
  Serial.begin(9600);
  stepperX.setMaxSpeed(20); // Set X-axis stepper motor max speed
  stepperX.setAcceleration(5); // Set X-axis stepper motor acceleration
  
  stepperY.setMaxSpeed(20); // Set Y-axis stepper motor max speed
  stepperY.setAcceleration(5); // Set Y-axis stepper motor acceleration
  
}

void Pos()
{
  if (prevX != x || prevY != y)
  {
    // Vertical movement (Y-axis) stepper control
    int stepsY = map(y, 450, 0, 0, 100); // Map Y coordinate to stepper steps (adjust as needed)
    stepperY.moveTo(stepsY);
  
    // Horizontal movement (X-axis) stepper control
    int stepsX = map(x, 0, 640, 0, 100); // Map X coordinate to stepper steps (adjust as needed)
    stepperX.moveTo(stepsX);
    
    // Update previous coordinates
    prevX = x; 
    prevY = y; 
  }
}

void loop()
{
  if (Serial.available() > 0)
  {
    if (Serial.read() == 'X')
    {
      x = Serial.parseInt();
      if (Serial.read() == 'Y')
      {
        y = Serial.parseInt();
        Pos();
      }
    }
    // Check for trigger command
    // else if (Serial.read() == 'T')
    // {
    //   triggerFlag = true; // Set trigger flag
    // }
    while (Serial.available() > 0)
    {
      Serial.read(); // Clear remaining characters from serial buffer
    }
  }
  
  // Continuously run both stepper motors
  stepperX.run(); 
  stepperY.run(); 
  
  // Trigger toy gun if flag is set
}
