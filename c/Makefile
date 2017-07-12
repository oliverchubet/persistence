all:
	gcc -c -fpic utils.c matrix.c persistence.c
	ld -r utils.o matrix.o persistence.o -o test.o
	gcc -shared test.o -o libtest.so
	gcc -ggdb3 main.c utils.c matrix.c persistence.c -o main.o

clean:
	rm test.o main.o utils.o matrix.o persistence.o libtest.so

