#include <stdio.h>
#include <ctype.h>

void wc(FILE *ofile, FILE *infile, char *inname) {
	int line_count = 0;
	int word_count = 0;
	int char_count = 0;
	int status = 0;
	char c;
	while ((c=fgetc(infile)) != EOF) {
		if (c == '\n') {
			line_count++;
		}
		if (!isspace(c)) {
			if (status == 0) {
				word_count++;
				char_count++;
				status = 1;
			}
			else {
				char_count++;
			}
		}
		else {
			char_count++;
			status = 0;
		}
	}
	fclose(infile);
	int n, count;
	n = char_count;
	while (n != 0) {
		n /= 10;
		count++;
	}
	if (inname == NULL) {
		printf(" %*d %*d %*d\n", count, line_count, count, word_count, count, char_count);
	}
	else if (ofile == NULL) {
		printf("%*d %*d %*d %s\n", count, line_count, count, word_count, count, char_count, inname);
	}
	else {
		fprintf(ofile, "%*d %*d %*d %s\n", count, line_count, count, word_count, count, char_count, inname);
		fclose(ofile);
	}
}

int main (int argc, char *argv[]) {
	if (argc == 1) {
		wc(stdout, stdin, NULL);
	}
	else if (argc == 2) {
		wc(NULL, fopen(argv[1], "r"), argv[1]);
	}
	else if (argc == 3) {
		wc(fopen(argv[2], "w"), fopen(argv[1], "r"), argv[1]);
	}
	else {
		printf("%s\n", "Please Follow the Usage: wc input (output)");
	}
  return 0;
}
