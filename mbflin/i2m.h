#include <stdio.h>
float i2m(float f)
{
union{
	float f;
	unsigned long l;}um;
unsigned long s,e;
um.f=f;
s=um.l;
e=um.l;
um.l= um.l&0x7FFFFF;
e=((((e>>23)&0xff)+2)<<24)&0xFF000000;
s=(s>>8)&0x800000;
um.l=(um.l|s)|e;
return(um.f);
}
