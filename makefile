CC = clang
CFLAGS = -Wall -pedantic -std=c99
PYTHON_INCLUDE = /usr/include/python3.11

all: _phylib.so

clean:
	rm -f *.o *.so _phylib.so

A2Test1.py: A2Test1.py Physics.py 
	$(CC) $(CFLAGS) -o A2Test1 A2Test.py -lm

libphylib.so: phylib.o
	$(CC) -shared -o libphylib.so phylib.o -lm

phylib.o: phylib.c phylib.h
	$(CC) $(CFLAGS) -fPIC -c phylib.c -o phylib.o

phylib_wrap.c: phylib.i 
	swig -python phylib.i

phylib.py: phylib.i
	swig -python phylib.i 

phylib_wrap.o: phylib_wrap.c
	$(CC) $(CFLAGS) -c phylib_wrap.c -I$(PYTHON_INCLUDE) -fPIC -o phylib_wrap.o

_phylib.so: phylib_wrap.o libphylib.so
	$(CC) $(CFLAGS) -shared phylib_wrap.o -L. -L/usr/lib/python3.11 -lpython3.11 -lphylib -o _phylib.so



