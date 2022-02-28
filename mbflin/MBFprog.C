#include <stdio.h>
#include "mbf.h"
#include "i2m.h"
main(void)
{
FILE *fd;
float f,f1;
	printf("inserisci un float\n");
	scanf("%f",&f);
	f1=m2i(f);
	printf("%f\n",f1);
	if (!(fd=fopen("e:\\F1.dat","rb"))) printf("impossibile aprire il file");
	fseek(fd,32,SEEK_SET);
	int i;
	for (i=0;i<20;i++)
		{
	fread(&f,4,1,fd);
	printf("float letto da file: %f  ",f);
	f1=m2i(f);
	printf("dopo: %f\n",f1);
		}
	fclose(fd);
}
