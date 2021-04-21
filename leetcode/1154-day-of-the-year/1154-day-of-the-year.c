const int num_days[] = {
    31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31
};

int dayOfYear(char *date)
{
    int year =  (date[0] - '0') * 1000  +
                (date[1] - '0') * 100   +
                (date[2] - '0') * 10    +
                (date[3] - '0') * 1     ;
    
    int month = 0;
    if (date[5] == '1') {
        month = 10;
    }
    month += date[6] - '0';
    
    int days = 0;
    
    for (int i = 0; i < month - 1; i++) {
        days += num_days[i];
    }
    
    int day = (date[8] - '0') * 10 + (date[9] - '0');
    
    return days + day +
        ( (month >= 3 ) ?
            ( (year % 4) ? 0 : (year % 100) ? 1 : (year % 400) ? 0 : 1 ) : 0 );
}

