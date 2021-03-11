//
// Created by ourson on 3/10/21.
//
#include <stdio.h>
#include <string.h>
//Struct for accelerometre and gyrometre
typedef struct  {
    float X;
    float Y;
    float Z;
} D_vect;



/**
 * @brief Function to convert a 3d vector to a string with (x,y,z) value separated with the **separator** char
 * @arg 3dVect: struct who represent the vector
 * @arg separator betwen the (x,y,z) values
 * @args precision : precisions of the float values
 * @return the str of the vector
 */
char * D_vect_to_str( char * str_out, D_vect  dVect, char  separator ) {

    char buffer [16]="";
    char sep [2]={separator,'\0'};
    int res = 0;
    str_out[0]='\0';
    res = snprintf(buffer, sizeof buffer , "%0.3f", dVect.X);
    strcat(str_out,buffer);
    strcat(str_out,sep);
    printf("str out : %s\n",str_out );
    buffer[0]='\0';

    res = snprintf(buffer,  sizeof buffer, "%0.3f", dVect.Y);
    strcat(str_out,buffer);
    strcat(str_out,sep);
    buffer[0]='\0';

    printf("str out : %s\n",str_out );

    res = snprintf(buffer, sizeof buffer, "%0.3f", dVect.Z);
    strcat(str_out,buffer);
    strcat(str_out,"\0");

    printf("str out : %s\n",str_out );


return str_out;


}
