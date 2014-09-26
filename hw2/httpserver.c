/* A simple HTTP server with port number is passed as an argument */
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <sys/types.h> 
 
#include <sys/socket.h>
#include <netinet/in.h>
#include <fcntl.h>
#include <unistd.h>
#include <signal.h>

#define MAXPATH 1024
#define MAXBUF 10240
#define MAXREQ  8192
#define MAXQUEUE 5

void error(char *msg)
{
    perror(msg);
    exit(1);
}

const char htmlheader[]="HTTP/1.0 200 OK\r\n"
  "Content-Type: text/html\r\n"
  "\r\n";

const char notfoundheader[]="HTTP/1.0 404 Not Found\r\n"
  "Content-Type: text/html\r\n"
  "\r\n";

const char badreaquestheader[]="HTTP/1.0 200 OK\r\n"
  "Content-Type: text/html\r\n"
  "\r\n";

const char textheader[]="HTTP/1.0 200 OK\r\n"
  "Content-Type: text/plain\r\n"
  "\r\n";

char * concat(char *s1, char *s2) {
  char *new_str = malloc(strlen(s1)+strlen(s2)+1);
  strcpy(new_str, s1);
  strcat(new_str, s2);
  return new_str;
}

int process_http_request(int httpsockfd)
{
  char reqbuf[MAXREQ];
  int n=0;
  /* IMPLEMENT ME!
     This services a single http request.  
     In this skeleton it responds to all connections by
     echoing the request to the client with a text/plain content type.
     This is handy for seeing what the requests look like, but is
     non-compliant.  It should do the following.

     Service the GET command.  
       - All other requests should receive a valid error 400 response.
       - A GET specifies a resource as the second token, followed by
       the http version.

     The directory in which the server runs should contain a directory
     ./www.  
     - Resources specified in the GET should be treated as a pathname 
     relative to that directory.
     - If the resource specifies a file, the file is returned to the
     client with  Content-Type set to text/html in the response header.
    - If the path does not resolve to a file an error 404 is returned.
 */
  memset(reqbuf,0, MAXREQ);
  n = read(httpsockfd,reqbuf,MAXREQ-1);
  write(STDOUT_FILENO, reqbuf, n );

  char * method;
  method = strtok(reqbuf," ");
  char * dir;
  dir = strtok(NULL, " ");
  if (strcmp(method, "GET") == 0) {
    char resbuf[MAXBUF];
    FILE *fp = fopen(concat("www", dir), "r");
    if (fp != NULL) {
      size_t newLen = fread(resbuf, sizeof(char), MAXBUF, fp);
      fclose(fp);
      write(httpsockfd,htmlheader,strlen(htmlheader));
      write(httpsockfd, resbuf, newLen);
    }
    else {
      FILE *fp = fopen("404.html", "r");
      size_t newLen = fread(resbuf, sizeof(char), MAXBUF, fp);
      fclose(fp);
      write(httpsockfd,notfoundheader,strlen(htmlheader));
      write(httpsockfd, resbuf, newLen);
    }
  }
  else {
    char resbuf[MAXBUF];
    FILE *fp = fopen("400.html", "r");
    size_t newLen = fread(resbuf, sizeof(char), MAXBUF, fp);
    fclose(fp);
    write(httpsockfd,badreaquestheader,strlen(htmlheader));
    write(httpsockfd, resbuf, newLen);
  }
  return 0;
}

int sockfd, newsockfd;    /* make static so signal handler can close */

void signal_callback_handler(int signum)
{
  printf("Caught signal %d\n",signum);
  printf("Close socket %d\n", sockfd);
  if (close(sockfd) < 0) perror("failed to close sockfd\n");
  exit(signum);
}

int server(int portno)
{
  struct sockaddr_in serv_addr; /* internet style socket address object */
  struct sockaddr_in cli_addr;
  uint clilen = sizeof(cli_addr);

  pid_t cpid;
  int socketOption = 1;

  signal(SIGINT, signal_callback_handler);

  /* Create Socket to receive requests*/
  sockfd = socket(PF_INET, SOCK_STREAM, 0);
  if (sockfd < 0) error("ERROR opening socket");
  printf("Got socket: %d\n", sockfd);

  if (setsockopt(sockfd, SOL_SOCKET, SO_REUSEADDR, &socketOption, sizeof(socketOption)))
    error("ERROR setting reuseadd option");

  /* Bind socket to port */
  memset((char *) &serv_addr,0,sizeof(serv_addr));
  serv_addr.sin_family      = AF_INET;
  serv_addr.sin_addr.s_addr = INADDR_ANY;
  serv_addr.sin_port        = htons(portno);
  if (bind(sockfd, (struct sockaddr *) &serv_addr, sizeof(serv_addr)) < 0) {
    close(sockfd);
    error("ERROR on binding");
  }

  while (1) {
    listen(sockfd,MAXQUEUE);    /* Listen for incoming connections */

    /* Accept incoming connection, obtaining a new socket for it */
    if ((newsockfd = accept(sockfd, (struct sockaddr *) &cli_addr, &clilen)) < 0)
      error("ERROR on accept");
    printf("new socket: %d\n", newsockfd);

    cpid = fork();         /* create new process for connection */
    if (cpid > 0) {     /* parent process */
      close(newsockfd);     /* parent drops refernce on connection socket */
      printf("Ready for next\n");
    } else if (cpid == 0) {   /* child process */
      close(sockfd);      /* clild drops reference on listening socket */
      process_http_request(newsockfd);
      close(newsockfd); /* child drops refernce on connection socket */
      exit(EXIT_SUCCESS); /* exit child normally */
    } else {      /* fork failed */
      error("Fork of child process failed\n");
    }
  }
  printf("Server exiting\n");
  close(sockfd);
  return 0; 
}


int main(int argc, char *argv[])
{
  int portno;
  if (argc < 2) {
    fprintf(stderr,"usage %s portno\n", argv[0]);
    exit(1);
  }
  portno = atoi(argv[1]);
  printf("Opening server on port %d\n",portno);
  return server(portno);
}
