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
<%@ page import="com.comcast.rdk.PrimitiveTest" %>
<%@ page import="com.comcast.rdk.Module" %>
<%@ page import="com.comcast.rdk.User" %>
<%@ page import="com.comcast.rdk.Groups" %>
<%@ page import="org.apache.shiro.SecurityUtils" %>

<table>
  <tr>
    <th>Select Module</th>
  </tr>
  <tr>
    <td>
    <%
		def user = User.findByUsername(SecurityUtils.subject.principal)
		def group = Groups.findById(user.groupName?.id)
	%>
    	<g:select from="${Module.findAllByGroupsOrGroupsIsNull(group, [order: 'asc', sort: 'name'])}" var="module" noSelection="['' : 'Please Select']" id="module" name="module"/>
    </td>
  </tr>
</table>

