
    //*********************************************************************************************************
    // Initialize Timer 2 - IR light
    //*********************************************************************************************************
    T2CON = 0x0020;                    // Stop 16-bit Timer2, 1:64(40MhzFosc) Prescale, Internal clock (Fosc/2)
    TMR2 = 0x00;                    // Clear timer register
    PR2 = 1250;                        // Load the period value, OCxRS <= PRx, 4ms period = (1/(Fosc/2))*1000*64*PR2 = (1/(40000000/2))*1000*64*1250
    IPC1bits.T2IP = 2;                // Set Timer2 Interrupt Priority Level
    IFS0bits.T2IF = 0;                // Clear Timer2 Interrupt Flag
    IEC0bits.T2IE = 1;                // Enable Timer2 Interrupt
 
    //*********************************************************************************************************
    // Initialize Timer 3 - Red light
    //*********************************************************************************************************
    T3CON = 0x0020;                    // Stop 16-bit Timer3, 1:64(40MhzFosc) Prescale, Internal clock (Fosc/2)
    TMR3 = 0x00;                    // Clear timer register
    PR3 = 1250;                        // Load the period value, OCxRS <= PRx, 4ms period = (1/(Fosc/2))*1000*64*PR2 = (1/(40000000/2))*1000*64*1250
    IPC2bits.T3IP = 2;                // Set Timer3 Interrupt Priority Level
    IFS0bits.T3IF = 0;                // Clear Timer3 Interrupt Flag
    IEC0bits.T3IE = 1;                // Enable Timer3 Interrupt
 
    //*********************************************************************************************************
    // Initialize Output Compare 1 module in Continuous Pulse mode, OC1 controls IR LED switch
    //*********************************************************************************************************
    RPOR6bits.RP13R = 0b10010;        // RP13/RB13 tied to OC1 (IR)
    OC1CONbits.OCM = 0b000;         // Disable Output Compare 1 Module
    OC1R = 0;                         // Write the duty cycle for the first PWM pulse, 24=8MHzFosc(50us), 30=40MHzFosc(50us), 600=40MHzFosc(1ms)
    OC1RS = duty_cycle;             // Write the duty cycle for the second PWM pulse, OCxRS <= PRx, 499=8MHzFosc(1ms), 623=40MHzFosc(1ms), 1246=40MHzFoc,2msPeriod, 4984=40MHzFoc,8msPeriod, 280=450us D/C@40MHzFoc,2msPeriod,switch
    OC1CONbits.OCTSEL = 0;             // Select Timer 2 as output compare time base
 
    //*********************************************************************************************************
    // Initialize Output Compare 2 module in Continuous Pulse mode, OC2 controls Red LED switch
    //*********************************************************************************************************
    RPOR6bits.RP12R = 0b10011;        // RP12/RB12 tied to OC2 (Red)
    OC2CONbits.OCM = 0b000;         // Disable Output Compare 2 Module
    OC2R = 0;                         // Write the duty cycle for the first PWM pulse, 24=8MHzFosc, 30=40MHzFosc, 600=40MHzFosc(1ms)
    OC2RS = duty_cycle;             // Write the duty cycle for the second PWM pulse, OCxRS <= PRx, 499=8MHzFosc(1ms), 623=40MHzFosc(1ms), 1246=40MHzFoc,2msPeriod, 4984=40MHzFoc,8msPeriod, 280=450us D/C@40MHzFoc,2msPeriod,switch
    OC2CONbits.OCTSEL = 1;             // Select Timer 3 as output compare time base

    
void __attribute__((__interrupt__, no_auto_psv)) _T3Interrupt(void)        //Read Red DC & AC signals from AN0 & AN1
{
    int delay;
    unsigned char i;
 
    Read_ADC_Red = 1;
    CH0_ADRES_Red_sum = 0;
    CH1_ADRES_Red_sum = 0;
 
    for (delay=0; delay<200; delay++);    //2000=delayed 256us before read ADC
 
//    LATBbits.LATB14 = 1;            // for debugging
 
    for (i=0; i<oversampling_number; i++)
    {
        //Acquires Red-DC from Channel0 (AN0)
        AD1CHS0bits.CH0SA = 0x00;        // Select AN0
        AD1CON1bits.SAMP = 1;            // Begin sampling
        while(!AD1CON1bits.DONE);        // Waiting for ADC completed
        AD1CON1bits.DONE = 0;            // Clear conversion done status bit
        CH0_ADRES_Red_sum = CH0_ADRES_Red_sum + ADC1BUF0;    // Read ADC result
 
        //Acquires Red-AC from Channel1 (AN1)
        AD1CHS0bits.CH0SA = 0x01;        // Select AN1
        AD1CON1bits.SAMP = 1;            // Begin sampling
        while(!AD1CON1bits.DONE);        // Waiting for ADC completed
        AD1CON1bits.DONE = 0;            // Clear conversion done status bit
        CH1_ADRES_Red_sum = CH1_ADRES_Red_sum + ADC1BUF0;    // Read ADC result
    }
 
    CH0_ADRES_Red = CH0_ADRES_Red_sum / oversampling_number;
    FIR_input_Red[0] = CH1_ADRES_Red_sum / oversampling_number;
 
#ifdef Sleep_Enabled
    if (CH0_ADRES_Red<=74 && CH1_ADRES_Red>=4000)    //if spo2 probe is not connected, 74=60mV, 4000=3.2V
    {
        goto_sleep = 1;
    }
    else if (CH0_ADRES_Red > Finger_Present_Threshold)    //if no finger present then goto sleep
    {
        goto_sleep = 1;
    }
    else
#endif
    {
//        LATBbits.LATB14 = 0;            // for debugging
        for (delay=0; delay<500; delay++);    //1000=delayed 256us before read ADC
//        LATBbits.LATB14 = 1;            // for debugging
 
        //Acquires Red-DC baseline from Channel0 (AN0)
        AD1CHS0bits.CH0SA = 0x00;        // Select AN0
        AD1CON1bits.SAMP = 1;            // Begin sampling
        while(!AD1CON1bits.DONE);        // Waiting for ADC completed
        AD1CON1bits.DONE = 0;            // Clear conversion done status bit
        Baseline_ambient = ADC1BUF0;
 
        Baseline_Upper_Limit = Baseline_ambient + DCVppHigh;
        Baseline_Lower_Limit = Baseline_ambient + DCVppLow;
 
        Meter_State = Calibrate_Red();
    }
 
//    LATBbits.LATB14 = 0;            // for debugging
 
    OC2RS = duty_cycle;                // Write Duty Cycle value for next PWM cycle
    IFS0bits.T3IF = 0;                // Clear Timer3 Interrupt Flag
}


    //********** Enable OC1 & OC2 ouputs for IR & Red LED's on/off switch **********
    OC2CONbits.OCM = 0b101;                // Select the Output Compare 2 mode, Turn on Red LED
    T3CONbits.TON = 1;                    // Start Timer3
 
    for (delay=0; delay<2200; delay++);
 
    OC1CONbits.OCM = 0b101;                // Select the Output Compare 1 mode, Turn on IR LED
    T2CONbits.TON = 1;                    // Start Timer2
 
    goto_sleep = 0;
    first_reading = 0;
    
 
    while (1)
    {
        if (goto_sleep)
        {
 
[lines clipped]
 
                Sleep();                    // Put MCU into sleep
                Nop();
            }
        }
 
        //--------- Main State Machine starts here ---------
        if (RedReady && IRReady)
        {
            RedReady = 0;
            IRReady = 0;
 
//            LATBbits.LATB14 = 1;            //for debugging
 
            FIR(1, &FIR_output_IR[0], &FIR_input_IR[0], &BandpassIRFilter);
            FIR(1, &FIR_output_Red[0], &FIR_input_Red[0], &BandpassRedFilter);
 
            CH1_ADRES_IR = FIR_output_IR[0];
            CH1_ADRES_Red = FIR_output_Red[0];
 
[lines clipped]
 
            if (Detection_Done)
            {
                //Max & Min are all found. Calculate SpO2 & Pulse Rate
                SpO2_Calculation();                //calculate SpO2
                Pulse_Rate_Calculation();        //calculate pulse rate
 
[lines clipped]
 
    }
/*****************************************************************************
 * Function Name: SpO2_Calculation()
 * Specification: Calculate the %SpO2
 *****************************************************************************/
void SpO2_Calculation (void)
{
    double Ratio_temp;
 
    IR_Vpp1 = fabs(IR_Max - IR_Min);
    Red_Vpp1 = fabs(Red_Max - Red_Min);
    IR_Vpp2 = fabs(IR_Max2 - IR_Min2);
    Red_Vpp2 = fabs(Red_Max2 - Red_Min2);
 
    IR_Vpp = (IR_Vpp1 + IR_Vpp2) / 2;
    Red_Vpp = (Red_Vpp1 + Red_Vpp2) / 2;
 
    IR_Vrms = IR_Vpp / sqrt(8);
    Red_Vrms = Red_Vpp / sqrt(8);
 
//    SpO2 = log10(Red_Vrms) / log10(IR_Vrms) * 100;
//    if (SpO2 > 100)
//    {
//        SpO2 = 100;
//    }
 
    // Using lookup table to calculate SpO2
    Ratio = (Red_Vrms/CH0_ADRES_Red) / (IR_Vrms/CH0_ADRES_IR);