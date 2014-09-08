CC = gcc -g
all:
	$(CC) main.c -o main
	$(CC) map.c -o map
	$(CC) wc.c -o wc
clean:
	rm -rf main map wc
check:
	$(CC) wc.c -o wc
	wc main.c
	./wc main.c