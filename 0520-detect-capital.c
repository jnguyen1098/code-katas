bool detectCapitalUse(char *word)
{
    A:
        isupper(*word) ? ({goto B;}) : ({goto D;});
    B:
        !*++word ? ({goto G;}) : isupper(*word) ? ({goto E;}) : ({goto C;});
    C:
        !*++word ? ({goto G;}) : isupper(*word) ? ({goto F;}) : ({goto C;});
    D:
        !*++word ? ({goto G;}) : isupper(*word) ? ({goto F;}) : ({goto D;});
    E:
        !*++word ? ({goto G;}) : isupper(*word) ? ({goto E;}) : ({goto F;});
    F:
        return false;
    G:
        return true;
}
