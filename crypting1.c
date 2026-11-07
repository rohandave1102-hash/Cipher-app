#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<time.h>

char* userinput();
char randomgenerator(const char *list);
void encryptdata(const char *data);
char* Deconverterletters(const char *userinput);
void Dencryptdata(const char *data);

char listofallcharacters[18][5]=
{
    {'a','b','c','d','e'},
    {'f','g','h','i','j'},
    {'k','l','m','n','o'},
    {'p','q','r','s','t'},
    {'u','v','w','x','y'},
    {'z','A','B','C','D'},
    {'E','F','G','H','I'},
    {'J','K','L','M','N'},
    {'O','P','Q','R','S'},
    {'T','U','V','W','X'},
    {'Y','Z','0','1','2'},
    {'3','4','5','6','7'},
    {'8','9','!','@','#'},
    {'$','%','^','&','*'},
    {'(',')','-','_','='},
    {'+','/','?','.',','},
    {':',';','[',']','{'},
    {'}','<','>','~',' '}
};

char uniquekeyofcharacter[18][5][4]=
{
    {"22","3","2$","30","6^"},
    {"!0","&7","42","34","8@"},
    {"09","#5","?6","8*","36"},
    {"u8","9)","y!","%4","0-"},
    {"25","%2","0+","56","8#"},
    {"@1","0<","1=","2a","@3"},
    {"4!","5a","22-","l7","8"},
    {"9","!+","@k","#1","Na"},
    {"%5","^0","&s","*}","("},
    {")","-","_","p+","l="},
    {"/","0?","@6", "#2", "$1"},
    {"%6", "^6","&", "*", "!#"},
    {"?", "+","a","A","1"},
    {"!","b","B","2","@"},
    {"c","C","3u","#","d"},
    {"D","4","$","e","E"},
    {"5","%8","f","F","6"},
    {"^|","g","G","7"," "}
};

static char dynamicspacemaker[2]={'\0','\0'};
static char dynamicspacetaker[2]={'\0','\0'};

char* Converterletters(char userinput)
{
    int i;
    int j;
    if(userinput==' ')
    {   
        const char *listofspacecharacter="[]{}";
        dynamicspacemaker[0]=randomgenerator(listofspacecharacter);
        return dynamicspacemaker;
    }
    for(i=0;i<18;i++)
    {
        for(j=0;j<5;j++)
        {
            if (listofallcharacters[i][j] == ' ' && i == 17 && j > 3) {
                continue; 
            }
            if(userinput==listofallcharacters[i][j])
            {
                return uniquekeyofcharacter[i][j];
            }
        }
    }
    return NULL;
}

char randomgenerator(const char *list)
{
    int len=strlen(list);
    int characterrandom=rand()%len;
    return list[characterrandom];
}

char* Deconverterletters(const char *userinput)
{
    int i;
    int j;
    if(strcmp(userinput,"[")==0||strcmp(userinput,"]")==0||strcmp(userinput,"{")==0||strcmp(userinput,"}")==0)
    {   
        dynamicspacetaker[0]=' ';
        return dynamicspacetaker;
    }
    for(i=0;i<18;i++)
    {
        for(j=0;j<5;j++)
        {
            if (strcmp(uniquekeyofcharacter[i][j]," ")==0 && i == 17 && j > 3)
            {
                continue; 
            }
            if(strcmp(userinput,uniquekeyofcharacter[i][j])==0)
            {
                dynamicspacetaker[0]=listofallcharacters[i][j];
                return dynamicspacetaker;
            }
        }
    }
    return NULL;
}
