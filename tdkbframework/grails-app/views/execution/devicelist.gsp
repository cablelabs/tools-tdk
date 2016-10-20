<!--
 If not stated otherwise in this file or this component's Licenses.txt file the
 following copyright and licenses apply:

 Copyright 2016 RDK Management

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

 http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
-->
<%@ page import="org.codehaus.groovy.grails.validation.routines.InetAddressValidator"%>

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





<%--<div id="root_menu" class="" style="width: 100%; height: 400px; overflow: auto;">
						<div id="device_statusTotal">
						<ul id="browser" class="filetree">
							<li class="" id="root"><span class="folder" id="addconfId">Device</span>
								
								<ul>
										<li><span class="folder" id="">RDK-V</span>
											<ul>
											 <span id="device_statusV">
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
															<li id="deviceExecutionList_${deviceStatusCount}"><g:if
																	test="${device.deviceStatus.toString()=="NOT_FOUND" }">
																	<span class="filedevicenotfound" id="${device.id}">
																		<a href="#"
																		onclick="showScript('${device.id}', '${device.category}' );  highlightTreeElement('deviceExecutionList_', '${deviceStatusCount}', '${deviceInstanceTotal}'); return false;">
																			${device.stbName}
																	</a>
																	</span>
																</g:if> <g:if test="${device.deviceStatus.toString()=="FREE" }">
																	<span class="filedevicefree" id="${device.id}">
																		<a href="#"
																		onclick="showScript('${device.id}','${device.category}');  highlightTreeElement('deviceExecutionList_', '${deviceStatusCount}', '${deviceInstanceTotal}'); return false;">
																			${device.stbName}
																	</a>
																	</span>
																</g:if> <g:if test="${device.deviceStatus.toString()=="BUSY" }">
																	<span class="filedevicebusy" id="${device.id}">
																		<a href="#"
																		onclick="showScript('${device.id}','${device.category}');  highlightTreeElement('deviceExecutionList_', '${deviceStatusCount}', '${deviceInstanceTotal}'); return false;">
																			${device.stbName}
																	</a>
																	</span>
																</g:if> <g:if test="${device.deviceStatus.toString()=="HANG" }">
																	<span class="filedevicehang" id="${device.id}">
																		<a href="#"
																		onclick="showScript('${device.id}', '${device.category}');  highlightTreeElement('deviceExecutionList_', '${deviceStatusCount}', '${deviceInstanceTotal}'); return false;">
																			${device.stbName}
																	</a>
																	</span>
																</g:if> <g:if
																	test="${device.deviceStatus.toString()=="TDK_DISABLED" }">
																	<span class="filedevicetdkenabled" id="${device.id}">
																		<a href="#"
																		onclick="showScript('${device.id}', '${device.category}'); highlightTreeElement('deviceExecutionList_', '${deviceStatusCount}', '${deviceInstanceTotal}'); return false;">
																			${device.stbName}
																	</a>
																	</span>
																</g:if> <g:if
																	test="${device.deviceStatus.toString()=="ALLOCATED" }">
																	<span class="filedevicebusy"><a href="#"
																		onclick="showScript('${device.id}', '${device.category}'); highlightTreeElement('deviceExecutionList_', '${deviceStatusCount}', '${deviceInstanceTotal}'); return false;">
																			${device.stbName}
																	</a></span>
																</g:if></li>
														</div>
													</g:each>
													</span>
											</ul>
										</li>

										<li><span class="folder" id="">RDK-B</span>
											<ul>
												 <span id="device_statusB">
												<% int deviceStatusCount2 = 0; %>
												<g:each in="${deviceListB}" var="device">
														<% def isNameIp = InetAddressValidator.getInstance().isValidInet4Address(device.stbName)
										def name = device.stbName	
										if(isNameIp) {
											name = name.replace(".", "_")
										}
									 %>
														<% deviceStatusCount2++; %>
														<div id="tooltip_${name}" class="tooltip"
															title="Device : ${device.stbName}  &#013;IP : ${device.stbIp}    &#013;BoxType : ${device.boxType}    &#013;Status : ${device.deviceStatus}">
															<li id="deviceExecutionList_${deviceStatusCount2}">
															<g:if test="${device.deviceStatus.toString()=="NOT_FOUND" }">
																	<span class="filedevicenotfound" id="${device.id}">
																		<a href="#"
																		onclick="showScript('${device.id}', '${device.category}' );  highlightTreeElement('deviceExecutionList_', '${deviceStatusCount2}', '${deviceInstanceTotal}'); return false;">
																			${device.stbName}
																	</a>
																	</span>
																</g:if> <g:if test="${device.deviceStatus.toString()=="FREE" }">
																	<span class="filedevicefree" id="${device.id}">
																		<a href="#"
																		onclick="showScript('${device.id}','${device.category}');  highlightTreeElement('deviceExecutionList_', '${deviceStatusCount2}', '${deviceInstanceTotal}'); return false;">
																			${device.stbName}
																	</a>
																	</span>
																</g:if> <g:if test="${device.deviceStatus.toString()=="BUSY" }">
																	<span class="filedevicebusy" id="${device.id}">
																		<a href="#"
																		onclick="showScript('${device.id}','${device.category}');  highlightTreeElement('deviceExecutionList_', '${deviceStatusCount2}', '${deviceInstanceTotal}'); return false;">
																			${device.stbName}
																	</a>
																	</span>
																</g:if> <g:if test="${device.deviceStatus.toString()=="HANG" }">
																	<span class="filedevicehang" id="${device.id}">
																		<a href="#"
																		onclick="showScript('${device.id}', '${device.category}');  highlightTreeElement('deviceExecutionList_', '${deviceStatusCount2}', '${deviceInstanceTotal}'); return false;">
																			${device.stbName}
																	</a>
																	</span>
																</g:if> <g:if
																	test="${device.deviceStatus.toString()=="TDK_DISABLED" }">
																	<span class="filedevicetdkenabled" id="${device.id}">
																		<a href="#"
																		onclick="showScript('${device.id}', '${device.category}'); highlightTreeElement('deviceExecutionList_', '${deviceStatusCount2}', '${deviceInstanceTotal}'); return false;">
																			${device.stbName}
																	</a>
																	</span>
																</g:if> <g:if
																	test="${device.deviceStatus.toString()=="ALLOCATED" }">
																	<span class="filedevicebusy"><a href="#"
																		onclick="showScript('${device.id}', '${device.category}'); highlightTreeElement('deviceExecutionList_', '${deviceStatusCount2}', '${deviceInstanceTotal}'); return false;">
																			${device.stbName}
																	</a></span>
																</g:if></li>
														</div>
													</g:each>
													</span>
													</ul>
											</li>
											</ul>
										
								</li>
							</ul>
							</div>
							</div>
					</div>






--%>
