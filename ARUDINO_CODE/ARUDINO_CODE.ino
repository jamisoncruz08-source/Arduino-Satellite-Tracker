#include <Wire.h>
#include <LiquidCrystal.h>
LiquidCrystal lcd(12, 11, 5, 4, 3, 2);
String incoming = "";

String displayType = "";
String displayText = "";

unsigned long lastScroll = 0;
int scrollIndex = 0;

const int buttonPin = 22;
const int clkPin = 40;
const int dtPin = 42;
int lastCLK = HIGH;
void setDisplay(String type, String text)
{
    if (displayType == type && displayText == text)
        return;

    displayType = type;
    displayText = text;

    scrollIndex = 0;
    lastScroll = millis();

    //lcd.clear();

    if (displayType == "GROUP")
    {
        lcd.setCursor(0,0);
        lcd.print("> Groups");
    }
    else if (displayType == "MENU")
    {
        lcd.setCursor(0,0);
        lcd.print("> Select");
    }
}
void drawDisplay()
{
    if (displayType == "GROUP")
    {
        lcd.setCursor(0,0);
        lcd.print("> Groups");

        scrollText(displayText, 1);
    }

    else if (displayType == "MENU")
    {
        lcd.setCursor(0,0);
        lcd.print("> Select       ");

        scrollText(displayText, 1);
    }

    else if (displayType == "TRACK")
{
    int first = displayText.indexOf(',');
    int second = displayText.indexOf(',', first + 1);
    int third = displayText.indexOf(',', second + 1);

    String name = displayText.substring(0, first);
    String lat  = displayText.substring(first + 1, second);
    String lon  = displayText.substring(second + 1, third);
    String alt  = displayText.substring(third + 1);

    lcd.setCursor(0,0);
    lcd.setCursor(0,0);
    lcd.print(name);

    String info = "LAT:" + lat +
     " | LON:" + lon + 
    " | ALT:" + alt + "km";

    scrollText(info, 1);
}
}
void scrollText(String text, int row)
{
if (text.length() <= 16)
{
    static String lastShortText = "";

    if (text != lastShortText)
    {
        lcd.setCursor(0,row);
        lcd.print("                ");
        lcd.setCursor(0,row);
        lcd.print(text);

        lastShortText = text;
    }

    return;
}
    if (millis() - lastScroll < 900)
        return;

    lastScroll = millis();

    String scroll = text + "    ";

    String window = "";

    for (int i = 0; i < 16; i++)
    {
        window += scroll[(scrollIndex + i) % scroll.length()];
    }

    lcd.setCursor(0,row);
    lcd.print("                ");
    lcd.setCursor(0,row);
    lcd.print(window);

    scrollIndex++;

    if (scrollIndex >= scroll.length())
        scrollIndex = 0;
}
void updateDisplay()
{
    if (displayType == "GROUP" || displayType == "MENU")
    {
        scrollText(displayText,1);
    }
}
void setup()
{
    Serial.begin(9600);
    pinMode(buttonPin, INPUT_PULLUP);
    pinMode(clkPin, INPUT_PULLUP);
    pinMode(dtPin, INPUT_PULLUP);
    lastCLK = digitalRead(clkPin);
    lcd.begin(16,2);

   
}
void readEncoder()
{
    int currentCLK = digitalRead(clkPin);

    if (currentCLK != lastCLK && currentCLK == LOW)
    {
        if (digitalRead(dtPin) != currentCLK)
        {
            Serial.println("RIGHT");
        }
        else
        {
            Serial.println("LEFT");
        }
    }

    lastCLK = currentCLK;

    if (digitalRead(buttonPin) == LOW)
    {
        Serial.println("SELECT");

        while (digitalRead(buttonPin) == LOW);

        delay(100);
    }
}
void loop()
{
//------- Encoder
    readEncoder();
    //---------------
    // gets python message 
    //---------------
while (Serial.available())
{
    char c = Serial.read();

    if (c == '\n')
    {
        int first = incoming.indexOf(',');

        String type = incoming.substring(0, first);

        if (type == "GROUP")
        {
            setDisplay("GROUP", incoming.substring(first + 1));
        }
        else if (type == "MENU")
        {
            setDisplay("MENU", incoming.substring(first + 1));
        }
        else
        {
            setDisplay("TRACK", incoming);
        }

        incoming = "";
    }
    else
    {
        incoming += c;
    }
}
updateDisplay();
drawDisplay();
}