/*
 This file contains platform dependent APIs
*/

#include <stdio.h>      
#include <sys/types.h>
#include <ifaddrs.h>
#include <netinet/in.h> 
#include <string.h> 
#include <arpa/inet.h>

int GetIpAddrDetails(char * portName, char * ipAddr) 
{
    struct ifaddrs * ipAddrStruct = NULL, * ifa = NULL;
    void * tempAddrPtr = NULL;

    /* Get ip address structure */
    getifaddrs(&ipAddrStruct);

    for (ifa = ipAddrStruct; ifa != NULL; ifa = ifa->ifa_next) {
	/* IPv4 */
        if (ifa ->ifa_addr->sa_family == AF_INET) { 
            char mask[INET_ADDRSTRLEN];
            void* mask_ptr = &((struct sockaddr_in*) ifa->ifa_netmask)->sin_addr;
            inet_ntop(AF_INET, mask_ptr, mask, INET_ADDRSTRLEN);
            if (strcmp(mask, "255.0.0.0") != 0) {
                // valid IPv4 Address
                tempAddrPtr = &((struct sockaddr_in *) ifa->ifa_addr)->sin_addr;
                char addressBuffr[INET_ADDRSTRLEN];
                inet_ntop(AF_INET, tempAddrPtr, addressBuffr, INET_ADDRSTRLEN);
                printf("\n%s IP Address %s\n", ifa->ifa_name, addressBuffr);
		/*Return the adrress and port name */
		strcpy(portName, ifa->ifa_name);
		strcpy(ipAddr, addressBuffr);
        }
    }
    }
    if (ipAddrStruct != NULL) freeifaddrs(ipAddrStruct);
    return 0;
}
