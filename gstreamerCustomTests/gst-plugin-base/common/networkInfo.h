/*
 This file contains platform dependent APIs
*/

#include <stdio.h>      
#include <sys/types.h>
#include <ifaddrs.h>
#include <netinet/in.h> 
#include <string.h> 
#include <arpa/inet.h>

int GetIpAddrDetails(char * portName, char * ipAddr);
