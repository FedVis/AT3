#include <stdio.h>
float m2i(float f)
{
union{
	float f;
	unsigned long l;}um;
unsigned long l1,l2;
um.f=f;
l1=um.l;
l2=um.l;
um.l= (um.l<<8)&0x80000000;
l1=((((l1>>24)&0xff)-2)<<23)&0x7F800000;
l2=l2&0x7FFFFF;
um.l=(um.l|l1)|l2;
return(um.f);
}
