double angleClock(int hour, int minutes)
{
    double result = 0.0;
    
    double hour_angle = 30.0 * (minutes / 60.0) + ((hour % 12) * 30.0);
    
    double minute_angle = (minutes * 6) - hour_angle;
    
    if (minute_angle < hour_angle)
        minute_angle += 360;
    
    result = minute_angle > 180 ? 360 - minute_angle : minute_angle;
    
    return result < 0 ? -result : result;
}
