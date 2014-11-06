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
<%@ page import="com.comcast.rdk.ScriptGroup"%>
<%@ page import="com.comcast.rdk.Device"%>
<%@ page import="com.comcast.rdk.ScriptService"%>
<%@ page import="java.util.Date"%>

<g:if test="${jobDetailList.size() > 0}" > 
<table id="scheduletable" >
   <thead>	
   		<tr>
     		<th colspan="8" align="center" style="background-color: white">Scheduled Jobs</th>            
        </tr>   		
        <tr>
     		<th width="2%"></th>
     		<th width="12%">Job Name</th>    
            <th width="13%">StartDate</th>                             
            <th width="35%">Script/ScriptGroup</th>
            <th width="8%">Device</th>
            <th width="15%">Details</th>
            <th width="13%">EndDate</th>
            <th width="2%">Delete</th>
        </tr>              
	</thead>
	<tbody>
		<% int count = 0; %> 
		<g:each in="${jobDetailList}" status="i" var="jobDetailsInstance">
			<g:hiddenField id="listCount" name="listCount" value="${count}"/>
		    <% count++ %>
			<tr class="${(i % 2) == 0 ? 'even' : 'odd'}">
				<% 
		            def deviceInstance = Device.findById(jobDetailsInstance?.device) 
                    def scriptList = jobDetailsInstance.script 
                    def scrLst = ""
                    if(!(scriptList?.isEmpty())){  	
	                    def scripts	                   
	                    scriptList?.each{ scr ->
	                      //  scripts = Script.findById(scr)
	                        scrLst = scrLst + scr + ","
	                    }	
                    }
                    else{
                        def scptGrp = ScriptGroup.findById(jobDetailsInstance?.scriptGroup)
                        scrLst = scptGrp
                    }                    	        
				%>			
				<td align="center"><g:checkBox name="chkbox${count}" value="${false}"  /></td>
				<td align="center">${fieldValue(bean: jobDetailsInstance, field: "jobName")}</td>	
				<td align="center">${fieldValue(bean: jobDetailsInstance, field: "startDate")}</td>							
			
				<td align="center">${scrLst }</td>
			
				<td align="center">${deviceInstance?.stbName} </td>
				
				<td align="center">${fieldValue(bean: jobDetailsInstance, field: "queryString")}
				<g:hiddenField id="id" name="id${count}" value="${jobDetailsInstance?.id}" /></td>	
				<td align="center">${jobDetailsInstance?.endDate}</td>
								
				<%				
					def date = new Date()
					def endDate = jobDetailsInstance?.endDate
					def time
					if(endDate){
						time = date.getTime() - endDate.getTime()
					}
					else{
						time = date.getTime() - jobDetailsInstance?.startDate?.getTime()
					}
				 %>
				 <td>
					 <g:if test="${time > 0 }">
						<g:remoteLink class="delete" 
							action="deleteJob" controller="execution" update="newScheduleTable"
							onSuccess="baseScheduleTableRemove();"
							params="[jobId : "${jobDetailsInstance?.id}"]"><img alt="Delete" style="vertical-align: middle;" src="../images/remove.gif" />
						</g:remoteLink>	
					 </g:if>
				</td>			
			</tr>
		</g:each>
	</tbody>		
</table>
<span class="buttons">
	<g:submitToRemote class="delete" 
		action="unScheduleJob" controller="execution" value="UnSchedule" update="newScheduleTable"
		onSuccess="baseScheduleTableRemove();" >
	</g:submitToRemote>	
</span>
</g:if>