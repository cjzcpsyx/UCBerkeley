#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>
#include <errno.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>

#define FALSE 0
#define TRUE 1
#include "io.h"
#include "parse.h"

char *path = ".";

int cmd_quit(tok_t arg[]) {
  printf("Bye\n");
  exit(0);
  return 1;
}

int cmd_help(tok_t arg[]);

int cmd_cd(tok_t arg[]);

/* Command Lookup table */
typedef int cmd_fun_t (tok_t args[]); /* cmd functions take token arra and rtn int */
typedef struct fun_desc {
  cmd_fun_t *fun;
  char *cmd;
  char *doc;
} fun_desc_t;

fun_desc_t cmd_table[] = {
  {cmd_help, "?", "show this help menu"},
  {cmd_quit, "quit", "quit the command shell"},
  {cmd_cd, "cd", "change directory"}
};

char * concat(char *s1, char *s2) {
  char *new_str = malloc(strlen(s1)+strlen(s2)+1);
  strcpy(new_str, s1);
  strcat(new_str, s2);
  return new_str;
}

char * last(tok_t arg[]) {
  int i;
  for (i=0; arg[i] != '\0'; i++)
  ;
  return arg[--i];
}

int cmd_help(tok_t arg[]) {
  int i;
  for (i=0; i < (sizeof(cmd_table)/sizeof(fun_desc_t)); i++) {
    printf("%s - %s\n",cmd_table[i].cmd, cmd_table[i].doc);
  }
  return 1;
}

int cmd_cd(tok_t arg[]) {
  int result;
  result = chdir(arg[0]);
  if (result == -1) {
    fprintf(stdout,"%s\n", strerror(errno));
  }
  else {
    path = arg[0];
  }
  return result;
}
int cmd_exec(tok_t arg[]) {
  pid_t cpid;
  int cstatus;
  cpid = fork();
  if(cpid < 0 ) {
    perror("fork failure");
    exit(1);
  }
  if (cpid == 0) {
    int result;
    char * env_path = strtok(getenv("PATH"), ":");
    while (env_path != NULL) {
      result = execv(concat(concat(env_path, "/"), arg[0]), arg);
      env_path = strtok(NULL, ":");
      if (result != -1) {
        break;
      }
    }
    if (result == -1) {
      result = execv(arg[0], arg);
      if (result == -1) {
        fprintf(stdout,"%s\n", "command not found");
      }
    }
    exit(1);
    return result;
  }
  else {
    wait(&cstatus);
    return 1;
  }
}

char * cmd_pwd() {
  long size;
  char *buf;
  char *ptr;
  size = pathconf(path, _PC_PATH_MAX);
  if ((buf = (char *)malloc((size_t)size)) != NULL)
      ptr = getcwd(buf, (size_t)size);
  return ptr;
}

int lookup(char cmd[]) {
  int i;
  for (i=0; i < (sizeof(cmd_table)/sizeof(fun_desc_t)); i++) {
    if (strcmp(cmd_table[i].cmd, cmd) == 0) return i;
  }
  return -1;
}

int shell (int argc, char *argv[]) {
  char *s;      /* user input string */
  tok_t *t;     /* tokens parsed from input */
  int lineNum = 0;
  int fundex = -1;
  pid_t pid = getpid();   /* get current processes PID */
  pid_t ppid = getppid(); /* get parents PID */

  printf("%s running as PID %d under %d\n",argv[0],pid,ppid);  

  lineNum=0;
  fprintf(stdout,"%d %s: ", ++lineNum, cmd_pwd());
  while ((s = freadln(stdin))) {
    t = getToks(s);   /* Break the line into tokens */
    fundex = lookup(t[0]);  /* Is first token a shell literal */
    if (strcmp(last(t), "&") == 0) {
      tok_t *new_tok = malloc(strlen(s)+1);
      int i;
      for (i=0; strcmp(t[i], "&") != 0; i++) {
        new_tok[i] = t[i];
      }
      pid_t cpid;
      int cstatus;
      cpid = fork();
      if(cpid < 0 ) {
        perror("fork failure");
        exit(1);
      }
      if (cpid == 0) {
        if (fundex >= 0) cmd_table[fundex].fun(&new_tok[1]);
        else {      /* Treat it as a file to exec */
          cmd_exec(&new_tok[0]);
        }
      }
      else {
        waitpid(cpid, &cstatus, 0);
        fprintf(stdout,"%d %s: ", ++lineNum, cmd_pwd());
      }
    }
    else {
      if (fundex >= 0) cmd_table[fundex].fun(&t[1]);
      else {      /* Treat it as a file to exec */
        cmd_exec(&t[0]);
      }
      fprintf(stdout,"%d %s: ", ++lineNum, cmd_pwd());
    }
  }
  return 0;
}

int main (int argc, char *argv[]) {
  return shell(argc, argv);
}
