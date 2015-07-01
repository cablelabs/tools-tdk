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
		<g:each in="${stbLogFiles}" var="stbLogFilesNames">
		<tr>	
			<td>
				<g:textField name="stbLogFiles" value="${stbLogFilesNames}" type="text" />
			</td>			
		</tr>	
		</g:each>
	</table>
	