# Wedit Makefile for project mbfprog
SRCDIR=c:\surfer\c++\compilat\lcc\prog\mbflin
CFLAGS=-Ie:\lcc\include  -O  -g2  -ansic
CC=$(LCCROOT)\bin\lcc.exe
LINKER=$(LCCROOT)\bin\lcclnk.exe
OBJS=\
	mbfprog.obj \

LIBS= tcconio.lib
EXE=mbfprog.exe

$(EXE):	$(OBJS) Makefile
	$(LINKER)  -subsystem console -o $(SRCDIR)\lcc\mbfprog.exe $(OBJS) $(LIBS)

# Build MBFPROG.C
MBFPROG_C=\
	$(SRCDIR)\mbf.h\

mbfprog.obj: $(MBFPROG_C) $(SRCDIR)\mbfprog.c
	$(CC) -c $(CFLAGS) $(SRCDIR)\mbfprog.c

link:
	$(LINKER)  -subsystem console -o $(SRCDIR)\lcc\mbfprog.exe $(OBJS) $(LIBS)

clean:
	del $(OBJS) c:\surfer\c++\compilat\lcc\prog\mbflin\lcc\mbfprog.exe
