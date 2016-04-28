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
	<table style="width:15%;">	
		<g:each in="${crashfiles}" var="crashfilename">
		<tr>	
			<td>
				<g:textField name="logFileNames" value="${crashfilename}" type="text" />
			</td>			
		</tr>	
		</g:each>
	</table>
	
		
	