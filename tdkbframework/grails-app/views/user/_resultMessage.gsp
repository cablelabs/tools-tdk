<!-- 
 ============================================================================
  COMCAST CONFIDENTIAL AND PROPRIETARY
 ============================================================================
  This file and its contents are the intellectual property of Comcast.  It may
  not be used, copied, distributed or otherwise  disclosed in whole or in part
  without the express written permission of Comcast.
  ============================================================================
  Copyright (c) 2013 Comcast. All rights reserved.
  ============================================================================
-->
<g:if test="${flash.message}">
	<div class="message" role="status">${flash.message}</div>
</g:if>
<g:if test="${flash.error}">
	<div class="errors" role="status">${flash.error}</div>
</g:if>