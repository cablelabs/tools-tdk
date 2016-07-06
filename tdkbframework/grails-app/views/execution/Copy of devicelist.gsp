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
<%@ page import="org.codehaus.groovy.grails.validation.routines.InetAddressValidator"%>
	<%--<ul id="browser" class="filetree">
		<li class="" id="root"><span class="folder" id="addconfId">Device</span>
			<ul>
				<li><span class="folder" id="">RDK-V</span>
					<ul>
						<% int deviceStatusCount = 0; %>
						<g:each in="${deviceListV}" var="device">
							<% def isNameIp = InetAddressValidator.getInstance().isValidInet4Address(device.stbName)
										def name = device.stbName	
										if(isNameIp) {
											name = name.replace(".", "_")
										}
									 %>
							<% deviceStatusCount++; %>
							<div id="tooltip_${name}" class="tooltip"
								title="Device : ${device.stbName}  &#013;IP : ${device.stbIp}    &#013;BoxType : ${device.boxType}    &#013;Status : ${device.deviceStatus}">
								<li id="deviceExecutionList_${deviceStatusCount}">
								<g:if test="${device.deviceStatus.toString()=="NOT_FOUND" }">
										<span class="filedevicenotfound" id="${device.id}"> <a
											href="#"
											onclick="showScript('${device.id}', '${device.category}' );  highlightTreeElement('deviceExecutionList_', '${deviceStatusCount}', '${deviceInstanceTotalV}'); return false;">
												${device.stbName}
										</a>
										</span>
									</g:if> <g:if test="${device.deviceStatus.toString()=="FREE" }">
										<span class="filedevicefree" id="${device.id}"> <a
											href="#"
											onclick="showScript('${device.id}','${device.category}');  highlightTreeElement('deviceExecutionList_', '${deviceStatusCount}', '${deviceInstanceTotalV}'); return false;">
												${device.stbName}
										</a>
										</span>
									</g:if> <g:if test="${device.deviceStatus.toString()=="BUSY" }">
										<span class="filedevicebusy" id="${device.id}"> <a
											href="#"
											onclick="showScript('${device.id}','${device.category}');  highlightTreeElement('deviceExecutionList_', '${deviceStatusCount}', '${deviceInstanceTotalV}'); return false;">
												${device.stbName}
										</a>
										</span>
									</g:if> <g:if test="${device.deviceStatus.toString()=="HANG" }">
										<span class="filedevicehang" id="${device.id}"> <a
											href="#"
											onclick="showScript('${device.id}', '${device.category}');  highlightTreeElement('deviceExecutionList_', '${deviceStatusCount}', '${deviceInstanceTotalV}'); return false;">
												${device.stbName}
										</a>
										</span>
									</g:if> <g:if
										test="${device.deviceStatus.toString()=="TDK_DISABLED" }">
										<span class="filedevicetdkenabled" id="${device.id}"> <a
											href="#"
											onclick="showScript('${device.id}', '${device.category}'); highlightTreeElement('deviceExecutionList_', '${deviceStatusCount}', '${deviceInstanceTotalV}'); return false;">
												${device.stbName}
										</a>
										</span>
									</g:if> <g:if test="${device.deviceStatus.toString()=="ALLOCATED" }">
										<span class="filedevicebusy"><a href="#"
											onclick="showScript('${device.id}', '${device.category}'); highlightTreeElement('deviceExecutionList_', '${deviceStatusCount}', '${deviceInstanceTotalV}'); return false;">
												${device.stbName}
										</a></span>
									</g:if>
								</li>
							</div>
						</g:each>
					</ul>
				</li>

				<li><span class="folder" id="">RDK-B</span>
					<ul>
						<% int deviceStatusCount2 = 0; %>
						<g:each in="${deviceListB}" var="device">
							<% def isNameIp = InetAddressValidator.getInstance().isValidInet4Address(device.stbName)
										def name = device.stbName	
										if(isNameIp) {
											name = name.replace(".", "_")
										}
									 %>
							<% deviceStatusCount2++; %>
							<div id="tooltip_${name}" class="tooltip" title="Device : ${device.stbName}  &#013;IP : ${device.stbIp}    &#013;BoxType : ${device.boxType}    &#013;Status : ${device.deviceStatus}">
								<li id="deviceExecutionList_${deviceStatusCount2}"><g:if
										test="${device.deviceStatus.toString()=="NOT_FOUND" }">
										<span class="filedevicenotfound" id="${device.id}"> <a
											href="#"
											onclick="showScript('${device.id}', '${device.category}' );  highlightTreeElement('deviceExecutionList_', '${deviceStatusCount2}', '${deviceInstanceTotalB}'); return false;">
												${device.stbName}
										</a>
										</span>
									</g:if> <g:if test="${device.deviceStatus.toString()=="FREE" }">
										<span class="filedevicefree" id="${device.id}"> <a
											href="#"
											onclick="showScript('${device.id}','${device.category}');  highlightTreeElement('deviceExecutionList_', '${deviceStatusCount2}', '${deviceInstanceTotalB}'); return false;">
												${device.stbName}
										</a>
										</span>
									</g:if> <g:if test="${device.deviceStatus.toString()=="BUSY" }">
										<span class="filedevicebusy" id="${device.id}"> <a
											href="#"
											onclick="showScript('${device.id}','${device.category}');  highlightTreeElement('deviceExecutionList_', '${deviceStatusCount2}', '${deviceInstanceTotalB}'); return false;">
												${device.stbName}
										</a>
										</span>
									</g:if> <g:if test="${device.deviceStatus.toString()=="HANG" }">
										<span class="filedevicehang" id="${device.id}"> <a
											href="#"
											onclick="showScript('${device.id}', '${device.category}');  highlightTreeElement('deviceExecutionList_', '${deviceStatusCount2}', '${deviceInstanceTotalB}'); return false;">
												${device.stbName}
										</a>
										</span>
									</g:if> <g:if
										test="${device.deviceStatus.toString()=="TDK_DISABLED" }">
										<span class="filedevicetdkenabled" id="${device.id}"> <a
											href="#"
											onclick="showScript('${device.id}', '${device.category}'); highlightTreeElement('deviceExecutionList_', '${deviceStatusCount2}', '${deviceInstanceTotalB}'); return false;">
												${device.stbName}
										</a>
										</span>
									</g:if> <g:if test="${device.deviceStatus.toString()=="ALLOCATED" }">
										<span class="filedevicebusy"><a href="#"
											onclick="showScript('${device.id}', '${device.category}'); highlightTreeElement('deviceExecutionList_', '${deviceStatusCount2}', '${deviceInstanceTotalB}'); return false;">
												${device.stbName}
										</a></span>
									</g:if></li>
							</div>
						</g:each>
					</ul>
				</li>
			</ul>
		</li>
	</ul>
--%>

<%@ page import="org.codehaus.groovy.grails.validation.routines.InetAddressValidator" %>
<% int deviceStatusCount = 0; %>

<g:each in="${deviceList}" var="device">
	<% deviceStatusCount++; %>
	<% def isNameIp = InetAddressValidator.getInstance().isValidInet4Address(device.stbName)
										def name = device.stbName	
										if(isNameIp) {
											name = name.replace(".", "_")
										}
									 %>
	
	
<div id="tooltip_${name}" title="Device : ${device.stbName}  &#013;IP : ${device.stbIp}   &#013;BoxType : ${device.boxType}   &#013;Status : ${device.deviceStatus}">
	<li id="deviceExecutionList_${deviceStatusCount}">
	<g:if test="${device.deviceStatus.toString()=="NOT_FOUND" }">
		<span class="filedevicenotfound" id="${device.id}"><a href="#" oncontextmenu="callFunc(${device.id})"
				    onclick="showScript('${device.id}','${device.category}'); highlightTreeElement('deviceExecutionList_', '${deviceStatusCount}', '${deviceInstanceTotal}'); return false;">
					${device.stbName}
			</a></span>
		</g:if> <g:if test="${device.deviceStatus.toString()=="FREE" }">
			<span class="filedevicefree" id="${device.id}"><a href="#" oncontextmenu="callFunc(${device.id})"
				onclick="showScript('${device.id}','${device.category}'); highlightTreeElement('deviceExecutionList_', '${deviceStatusCount}', '${deviceInstanceTotal}'); return false;">
					${device.stbName}
			</a></span>
		</g:if> <g:if test="${device.deviceStatus.toString()=="BUSY" }">
			<span class="filedevicebusy" id="${device.id}"><a href="#" oncontextmenu="callFunc(${device.id})"
				onclick="showScript('${device.id}','${device.category}'); highlightTreeElement('deviceExecutionList_', '${deviceStatusCount}', '${deviceInstanceTotal}'); return false;">
					${device.stbName}
			</a></span>
		</g:if> <g:if test="${device.deviceStatus.toString()=="HANG" }">
			<span class="filedevicehang" id="${device.id}"><a href="#" oncontextmenu="callFunc(${device.id})"
				onclick="showScript('${device.id}','${device.category}'); highlightTreeElement('deviceExecutionList_', '${deviceStatusCount}', '${deviceInstanceTotal}'); return false;">
					${device.stbName}
			</a></span>
		</g:if>		
		 <g:if test="${device.deviceStatus.toString()=="TDK_DISABLED" }">
			<span class="filedevicetdkdisabled" id="${device.id}"><a href="#" oncontextmenu="callFunc(${device.id})"
				onclick="showScript('${device.id}','${device.category}'); highlightTreeElement('deviceExecutionList_', '${deviceStatusCount}', '${deviceInstanceTotal}'); return false;">
					${device.stbName}
			</a></span>
		</g:if>		
		<g:if test="${device.deviceStatus.toString()=="ALLOCATED" }">
			<span class="filedevicebusy" id="${device.id}"><a href="#" oncontextmenu="callFunc(${device.id})"
				onclick="showScript('${device.id}','${device.category}'); highlightTreeElement('deviceExecutionList_', '${deviceStatusCount}', '${deviceInstanceTotal}'); return false;">
					${device.stbName}
			</a></span>
		</g:if>
	</li>
	</div>
</g:each>