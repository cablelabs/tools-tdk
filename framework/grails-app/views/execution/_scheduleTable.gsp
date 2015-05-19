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

<script>
$(document).ready(function(){
$('#scheduletable').dataTable({
	"sPaginationType": "full_numbers",
	"bRetrieve": true	
});
});
</script>
<g:if test="${jobDetailList.size() > 0}" > 
<table id="scheduletable" style="table-layout:fixed; " >
   <thead>	
   		<tr>
     		<th colspan="9" align="center" style="background-color: white">Scheduled Jobs</th>            
        </tr>   
         <col width="4%">
        <col width= "20%">
        <col width ="13%">
        <col width ="30%">
        <col width ="20%">
        <col width ="20%">
        <col width ="15%">
        <col width ="15%">
        <col width ="4%">			
        <tr>
     		<th ></th>
     		<th >Job Name</th>    
            <th >StartDate</th>                             
            <th >Script/ScriptGroup</th>
            <th >Device</th>
            <th >Details</th>
            <th >EndDate</th>
			<th	>Status</th>
            <th >Delete</th>
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
					int count1 =0
					String  str =" Multiple Scripts "
                    if(!(scriptList?.isEmpty())){  	
	                    def scripts	                   
	                    scriptList?.each{ scr ->
	                      //  scripts = Script.findById(scr) 
							//scrLst = scrLst + scr + ","
						if(count1 > 0){
							scrLst = str
						}
						else{
							scrLst = scrLst + scr + ","
						}
						count1++
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
			
				<td align="center" style ="width :40% ; word-wrap: break-word;">${scrLst }</td>
			
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
				<td align= "center">
				 	<g:if test="${time > 0 }"> EXECUTED</g:if>
				 	<g:else>PENDING</g:else>
				
				 </td>
				 <td align="center">
					 <g:if test="${time > 0 }">
						<g:remoteLink class="delete" 
							action="deleteJob" controller="execution" update="newScheduleTable"
							onSuccess="baseScheduleTableDelete();"
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