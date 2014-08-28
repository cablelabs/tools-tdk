/*
 * ============================================================================
 * COMCAST C O N F I D E N T I A L AND PROPRIETARY
 * ============================================================================
 * This file (and its contents) are the intellectual property of Comcast.  It may
 * not be used, copied, distributed or otherwise  disclosed in whole or in part
 * without the express written permission of Comcast.
 * ============================================================================
 * Copyright (c) 2014 Comcast. All rights reserved.
 * ============================================================================
 */

#ifndef __RDK_TEST_STUB_INTF__
#define __RDK_TEST_STUB_INTF__

#include <string>

#define IN	
#define OUT

class RDKTestAgent;

/**************************************************************************************
 Description   : This Class provides provides interface for the modules.
 
 **************************************************************************************/
class RDKTestStubInterface
{
    public:

        /* Constructor */
        RDKTestStubInterface(){}

        /* Destructor */
        virtual ~RDKTestStubInterface(){}

        virtual std::string testmodulepre_requisites() = 0;
        virtual bool testmodulepost_requisites() = 0;
        virtual bool initialize(IN const char* szVersion, IN RDKTestAgent *ptrAgentObj) = 0;
        virtual bool cleanup(IN const char* szVersion, IN RDKTestAgent *ptrAgentObj) = 0;
		
}; /* End of RDKTestStubInterface */

#endif //__RDK_TEST_STUB_INTF__


