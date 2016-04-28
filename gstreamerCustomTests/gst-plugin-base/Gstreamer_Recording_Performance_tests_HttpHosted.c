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
#ifdef HAVE_CONFIG_H
# include <config.h>
#endif
#include <gst/check/gstcheck.h>
#include <unistd.h>
#include <dirent.h>
#include <sys/types.h>
#include <sys/dir.h>
#include <sys/wait.h>
#include <sys/param.h>
#include <stdio.h>
#include "common/gstplayback.h"


#define BILLION  1000000000L
#define SZ_TCNAME 50
#define SZ_RESOURCE_PATH 200
#define SZ_PATH 200
#define MSEC 1000

static char tcname[SZ_TCNAME] ;
static int local_recording = 0;
static int http_recording = 0;
static gboolean got_eos = FALSE;
GstElement *pipeline = NULL;
GstElement *src = NULL;
GstElement *sink = NULL;
GstBus *bus = NULL;
static guint bus_watch = 0;

//void mplayer_play (void);
//void mplayer_stop (void);

struct timespec start_video_play, end_video_play;
double record_time = 0;


static gboolean
message_handler (GstBus * bus, GstMessage * msg, gpointer data) {
    GMainLoop *loop = (GMainLoop *) data;
    gchar *debug;
    GError *err;
    GstState old_state, new_state, pending_state;
    int i = 0;
    GST_DEBUG ("message_handler(). ENTRY \n");
    GST_DEBUG("INSIDE MESSAGE HANDLER \n");

    switch (GST_MESSAGE_TYPE (msg)) {
        case GST_MESSAGE_EOS:
            GST_DEBUG ("message_handler. GST_MESSAGE_EOS: %d \n", GST_MESSAGE_TYPE (msg) );
            GST_DEBUG ("Playback successful \n");
            g_print ("End of stream\n");
            got_eos = TRUE;
            
            if( clock_gettime( CLOCK_REALTIME, &end_video_play) == -1 ) {
                    //perror( "clock gettime" );
					DESCRIPTION(ERROR, "Error: clock gettime");
					INCIDENT_TYPE(ERROR);
            }
            record_time = (end_video_play.tv_sec - start_video_play.tv_sec ) + (double)( end_video_play.tv_nsec - start_video_play.tv_nsec ) / (double)BILLION;            
            //g_print( "[   Checks: Recording Time %lf seconds  ]\n", record_time );
			MESSAGE_START();
			DESCRIPTION(CHECKS, "Recording Time :: %lf ms  ]\n", record_time * MSEC );
			MESSAGE_END();
            g_main_loop_quit (loop);
        break;
        case GST_MESSAGE_ERROR:
            GST_DEBUG ("message_handler. GST_MESSAGE_ERROR: %d \n", GST_MESSAGE_TYPE (msg));
            gst_message_parse_error (msg, &err, &debug);
            g_free (debug);

            /* Will abort the check */
            g_warning ("Error: %s\n", err->message);
			      MESSAGE_START();	
      DESCRIPTION(ERROR, "Error: %s",err->message);
      MESSAGE_END();	
      INCIDENT_TYPE(ERROR);	 	 
            g_error_free (err);

            g_main_loop_quit (loop);
        break;
        case GST_MESSAGE_STATE_CHANGED:{
            GST_DEBUG("STATE CHANGED \n");
            GstState old_state, new_state, pending_state;
            gst_message_parse_state_changed (msg, &old_state, &new_state, &pending_state);
            g_print ("Pipeline state changed from %s to %s:\n",
            gst_element_state_get_name (old_state), gst_element_state_get_name (new_state));
            
                           
            if(new_state == GST_STATE_PLAYING)                
            {
               GST_DEBUG ("Playing starts \n");
               if( clock_gettime( CLOCK_REALTIME, &start_video_play) == -1 ) {
                    //perror( "clock gettime" );
					DESCRIPTION(ERROR, "Error: clock gettime");
					INCIDENT_TYPE(ERROR);
               }
               
            }
            
        }
        break;
          
        default:
            GST_DEBUG ("message_handler. default: %d \n", GST_MESSAGE_TYPE (msg));
    }

    GST_DEBUG ("message_handler(). EXIT \n");
   
    return TRUE;
}

static void load_url (GstElement *src, GstElement *sink, char *resources_path, char *record_path) {
    /*Set the input filename to the source element */
    g_object_set (G_OBJECT (src), "location", resources_path, NULL);
    g_object_set (G_OBJECT (sink), "location", record_path, NULL);
    GST_DEBUG ("g_object_set done for location\n");
}

static STATUS load_elements (GMainLoop *loop, char *resources_path, char *record_path)
{
    pipeline= gst_pipeline_new ("player");
    if (!pipeline)
     {
        GST_DEBUG ("pipeline not created\n");
        MESSAGE_START();
        DESCRIPTION(ERROR, "pipeline not created");
		MESSAGE_END();
		return ERROR;
    }
    fail_unless (pipeline != NULL, "failed to create pipeline");
    /*if(local_recording == 1)
    {
        src = gst_element_factory_make ("filesrc", "filesrc"); 
        if (!src)
        {
			GST_DEBUG ("Element source not created\n");
			MESSAGE_START();
			DESCRIPTION(ERROR, "Element source not created");
			MESSAGE_END();
			return ERROR;
		}
        fail_unless (src != NULL, "Failed to create filesrc element");
    }
    else if(http_recording == 1)
    {*/
        src = gst_element_factory_make ("souphttpsrc", "filesrc"); 
        if (!src)
        {
			GST_DEBUG ("Element source not created\n");
			MESSAGE_START();
			DESCRIPTION(ERROR, "Element source not created");
			MESSAGE_END();
			return ERROR;
		}
        fail_unless (src != NULL, "Failed to create souphttpsrc element");
    /*}
    else
    if (!src)
    {
        GST_DEBUG("No source element found. Please define the source element\n");
		MESSAGE_START();
		DESCRIPTION(ERROR, "Element source not created");
		MESSAGE_END();
		return ERROR;
    }*/

    sink = gst_element_factory_make ("filesink", "filesink"); 
    if (!sink)
    {
		GST_DEBUG ("Element sink not created\n");
		MESSAGE_START();
		DESCRIPTION(ERROR, "Element sink not created");
		MESSAGE_END();
		return ERROR;
	}
    fail_unless (sink != NULL, "Failed to create filesink element");

    /* Set the source path to get the stream from */
    load_url (src, sink, resources_path, record_path);

    fail_unless (gst_bin_add (GST_BIN (pipeline), src)); 
    fail_unless (gst_bin_add (GST_BIN (pipeline), sink));
    GST_DEBUG ("Added All the Elements into the pipeline \n");

    fail_unless (gst_element_link (src, sink)); 
    g_print ("Linked all the Elements together\n");

    bus = gst_element_get_bus (pipeline);
    GST_DEBUG ("gst_element_get_bus\n");

    bus_watch = gst_bus_add_watch (bus, message_handler, loop);

    GST_DEBUG ("gst_bus_add_watch\n");

    gst_object_unref (bus);
    GST_DEBUG ("gst_object_unref\n");

    return PASS;
}

static STATUS media_state(char *resources_path, char *record_path) {
    GMainLoop *loop;

    got_eos = FALSE;
	STATUS res;
    loop = g_main_loop_new (NULL, FALSE);

    
    res = load_elements(loop, resources_path, record_path);
	if(res == ERROR)
		return ERROR;
    
	res = mplayer_play(&pipeline);
	if (res == FAIL)
		return FAIL;
		
    g_main_loop_run (loop);
    GST_DEBUG ("gst_element_set_state. g_main_loop_run\n");

    res = mplayer_stop(&pipeline);
	if (res == FAIL)
		return FAIL;
		
    g_main_loop_unref (loop);
    GST_DEBUG (" g_main_loop_unref.\n");

    g_source_remove (bus_watch);
    GST_DEBUG (" g_source_remove.\n");
	return PASS;
}

STATUS url_check(char *path){
    char resources_path[SZ_RESOURCE_PATH];
    int ret, i;
    char command[SZ_PATH+SZ_RESOURCE_PATH];
    strcpy ( resources_path, (char *)getenv ("OPENSOURCETEST_PATH") );
    strcat ( resources_path, "resources/");
    strcat (resources_path, "urlCheck.sh");
    g_print ("\n\n **** validate url path = %s ***** \n", resources_path);
    sprintf(command, "%s %s",resources_path, path);
    ret = system(command);
    i=WEXITSTATUS(ret);
    g_print("ret = %d", i);
    if ( i != 0 ) {
    	g_warning ( "Error: Resource Not Found\n" );
		MESSAGE_START();
        DESCRIPTION(ERROR, "Resource Not Found");
		MESSAGE_END();
		INCIDENT_TYPE(ERROR);
		TESTFUNCTION_END();
    	return ERROR;
    }
    return PASS;
}

GST_START_TEST (gstVideoRecPerfMp4HttpHosted) {
    char resources_path[SZ_RESOURCE_PATH];
    char path[SZ_PATH] ;
    int ret, i;
    char command[SZ_PATH+SZ_RESOURCE_PATH];
    char record_path[SZ_PATH];
	STATUS res;
	TESTFUNCTION_START();
    g_print ("\n=========================\n");
    g_sprintf(tcname, __func__);
    g_print ("TestCase: %s\n", tcname) ;
    g_print ("GST_START_TEST: ENTRY. %s\n", __func__);
    g_print( "[   Checks: MP4 video ] \n");
    strcpy ( path, (char *)getenv ("RESRC_PUBLISHER_LINK") );strcat ( path, "/" );strcat ( path, "Test.mp4" );
    g_print ("\n\n **** resources path = %s ***** \n", path);

    res = url_check(path);
    if (res == FAIL || res == ERROR)
	{
		INCIDENT_TYPE(res);
		return;
	}

    strcpy ( record_path, (char *)getenv ("OPENSOURCETEST_PATH") );
    strcat ( record_path, "recordings/");
    strcat (record_path, "record.mp4");
    //local_recording = 1;
    res = media_state(path, record_path);
	if (res == FAIL || res == ERROR)
	{
		INCIDENT_TYPE(res);
	}
	else 
	{
		MESSAGE_START();
		DESCRIPTION(PASS, "");
		MESSAGE_END();
		INCIDENT_TYPE(PASS);
	}
    g_print ("GST_START_TEST: EXIT. %s\n", __func__);
	TESTFUNCTION_END();
}
GST_END_TEST;
GST_START_TEST (gstVideoRecPerfAviHttpHosted) {
    char resources_path[SZ_RESOURCE_PATH];
    char path[SZ_PATH] ;
    int ret, i;
    char command[SZ_PATH+SZ_RESOURCE_PATH];
    char record_path[SZ_PATH];
	STATUS res;
	TESTFUNCTION_START();
	
    g_print ("\n [   Checks: ========================================  ]\n");
    g_sprintf(tcname, __func__);
    g_print ("TestCase: %s\n", tcname) ;
    g_print ("GST_START_TEST: ENTRY. %s\n", __func__);
    g_print( "[   Checks: AVI video ] \n");
    strcpy ( path, (char *)getenv ("RESRC_PUBLISHER_LINK") );strcat ( path, "/" );strcat ( path, "Test.avi" );
    g_print ("\n\n **** resources path = %s ***** \n", path);

    res = url_check(path);
    if (res == FAIL || res == ERROR)
	{
		INCIDENT_TYPE(res);
		return;
	}

    strcpy ( record_path, (char *)getenv ("OPENSOURCETEST_PATH") );
    strcat ( record_path, "recordings/");
    strcat (record_path, "record.avi");
    //local_recording = 1;
    res = media_state(path, record_path);
	if (res == FAIL || res == ERROR)
	{
		INCIDENT_TYPE(res);
	}
	else 
	{
		MESSAGE_START();
		DESCRIPTION(PASS, "");
		MESSAGE_END();
		INCIDENT_TYPE(PASS);
	}
    g_print ("GST_START_TEST: EXIT. %s\n", __func__);
	TESTFUNCTION_END();
}
GST_END_TEST;

GST_START_TEST (gstVideoRecPerfFlvHttpHosted) {
    char resources_path[SZ_RESOURCE_PATH];
    char path[SZ_PATH] ;
    int ret, i;
    char command[SZ_PATH+SZ_RESOURCE_PATH];
    char record_path[SZ_PATH];
	STATUS res;
	TESTFUNCTION_START();
    g_print ("\n [   Checks: ========================================  ]\n");
    g_sprintf(tcname, __func__);
    g_print ("TestCase: %s\n", tcname) ;
    g_print ("GST_START_TEST: ENTRY. %s\n", __func__);
    g_print( "[   Checks: FLV video ] \n");
    strcpy ( path, (char *)getenv ("RESRC_PUBLISHER_LINK") );strcat ( path, "/" );strcat ( path, "Test.flv" );
    g_print ("\n\n **** resources path = %s ***** \n", path);

    res = url_check(path);
    if (res == FAIL || res == ERROR)
	{
		INCIDENT_TYPE(res);
		return;
	}

    strcpy ( record_path, (char *)getenv ("OPENSOURCETEST_PATH") );
    strcat ( record_path, "recordings/");
    strcat (record_path, "record.flv");
    //local_recording = 1;
    res = media_state(path, record_path);
	if (res == FAIL || res == ERROR)
	{
		INCIDENT_TYPE(res);
	}
	else 
	{
		MESSAGE_START();
		DESCRIPTION(PASS, "");
		MESSAGE_END();
		INCIDENT_TYPE(PASS);
	}
    g_print ("GST_START_TEST: EXIT. %s\n", __func__);
	TESTFUNCTION_END();
}
GST_END_TEST;

GST_START_TEST (gstVideoRecPerfM2vHttpHosted) {
    char resources_path[SZ_RESOURCE_PATH];
    char path[SZ_PATH] ;
    int ret, i;
    char command[SZ_PATH+SZ_RESOURCE_PATH];
    char record_path[SZ_PATH];
	STATUS res;
	TESTFUNCTION_START();
    g_print ("\n [   Checks: ========================================  ]\n");
    g_sprintf(tcname, __func__);
    g_print ("TestCase: %s\n", tcname) ;
    g_print ("GST_START_TEST: ENTRY. %s\n", __func__);
    g_print( "[   Checks: M2V video ] \n");
    strcpy ( path, (char *)getenv ("RESRC_PUBLISHER_LINK") );strcat ( path, "/" );strcat ( path, "Test.m2v" );
    g_print ("\n\n **** resources path = %s ***** \n", path);

    res = url_check(path);
    if (res == FAIL || res == ERROR)
	{
		INCIDENT_TYPE(res);
		return;
	}

    strcpy ( record_path, (char *)getenv ("OPENSOURCETEST_PATH") );
    strcat ( record_path, "recordings/");
    strcat (record_path, "record.m2v");
    //local_recording = 1;
    res = media_state(path, record_path);
	if (res == FAIL || res == ERROR)
	{
		INCIDENT_TYPE(res);
	}
	else 
	{
		MESSAGE_START();
		DESCRIPTION(PASS, "");
		MESSAGE_END();
		INCIDENT_TYPE(PASS);
	}
    g_print ("GST_START_TEST: EXIT. %s\n", __func__);
	TESTFUNCTION_END();
}
GST_END_TEST;
GST_START_TEST (gstVideoRecPerfMpgHttpHosted) {
    char resources_path[SZ_RESOURCE_PATH];
    char path[SZ_PATH] ;
    int ret, i;
    char command[SZ_PATH+SZ_RESOURCE_PATH];
    char record_path[SZ_PATH];
	STATUS res;
	TESTFUNCTION_START();
    g_print ("\n [   Checks: ========================================  ]\n");
    g_sprintf(tcname, __func__);
    g_print ("TestCase: %s\n", tcname) ;
    g_print ("GST_START_TEST: ENTRY. %s\n", __func__);
    g_print( "[   Checks: MPG video ] \n");
    strcpy ( path, (char *)getenv ("RESRC_PUBLISHER_LINK") );strcat ( path, "/" );strcat ( path, "Test.mpg" );
    g_print ("\n\n **** resources path = %s ***** \n", path);

    res = url_check(path);
    if (res == FAIL || res == ERROR)
	{
		INCIDENT_TYPE(res);
		return;
	}

    strcpy ( record_path, (char *)getenv ("OPENSOURCETEST_PATH") );
    strcat ( record_path, "recordings/");
    strcat (record_path, "record.mpg");
    //local_recording = 1;
    res = media_state(path, record_path);
	if (res == FAIL || res == ERROR)
	{
		INCIDENT_TYPE(res);
	}
	else 
	{
		MESSAGE_START();
		DESCRIPTION(PASS, "");
		MESSAGE_END();
		INCIDENT_TYPE(PASS);
	}
    g_print ("GST_START_TEST: EXIT. %s\n", __func__);
	TESTFUNCTION_END();
}
GST_END_TEST;
GST_START_TEST (gstAudioRecPerfMp3HttpHosted) {
    char resources_path[SZ_RESOURCE_PATH];
    char path[SZ_PATH] ;
    int ret, i;
    char command[SZ_PATH+SZ_RESOURCE_PATH];
    char record_path[SZ_PATH];
	STATUS res;
	TESTFUNCTION_START();
    g_print ("\n [   Checks: ========================================  ]\n");
    g_sprintf(tcname, __func__);
    g_print ("TestCase: %s\n", tcname) ;
    g_print ("GST_START_TEST: ENTRY. %s\n", __func__);
    g_print( "[   Checks: MP3 video ] \n");
    strcpy ( path, (char *)getenv ("RESRC_PUBLISHER_LINK") );strcat ( path, "/" );strcat ( path, "Test.mp3" );
    g_print ("\n\n **** resources path = %s ***** \n", path);

    res = url_check(path);
    if (res == FAIL || res == ERROR)
	{
		INCIDENT_TYPE(res);
		return;
	}

    strcpy ( record_path, (char *)getenv ("OPENSOURCETEST_PATH") );
    strcat ( record_path, "recordings/");
    strcat (record_path, "record.mp3");
    //local_recording = 1;
    res = media_state(path, record_path);
	if (res == FAIL || res == ERROR)
	{
		INCIDENT_TYPE(res);
	}
	else 
	{
		MESSAGE_START();
		DESCRIPTION(PASS, "");
		MESSAGE_END();
		INCIDENT_TYPE(PASS);
	}
    g_print ("GST_START_TEST: EXIT. %s\n", __func__);
	TESTFUNCTION_END();
}
GST_END_TEST;

GST_START_TEST (gstAudioRecPerfAc3HttpHosted) {
    char resources_path[SZ_RESOURCE_PATH];
    char path[SZ_PATH] ;
    int ret, i;
    char command[SZ_PATH+SZ_RESOURCE_PATH];
    char record_path[SZ_PATH];
	STATUS res;
	TESTFUNCTION_START();
    g_print ("\n [   Checks: ========================================  ]\n");
    g_sprintf(tcname, __func__);
    g_print ("TestCase: %s\n", tcname) ;
    g_print ("GST_START_TEST: ENTRY. %s\n", __func__);
    g_print( "[   Checks: AC3 video ] \n");
    strcpy ( path, (char *)getenv ("RESRC_PUBLISHER_LINK") );strcat ( path, "/" );strcat ( path, "Test.ac3" );
    g_print ("\n\n **** resources path = %s ***** \n", path);

    res = url_check(path);
    if (res == FAIL || res == ERROR)
	{
		INCIDENT_TYPE(res);
		return;
	}

    strcpy ( record_path, (char *)getenv ("OPENSOURCETEST_PATH") );
    strcat ( record_path, "recordings/");
    strcat (record_path, "record.ac3");
    //local_recording = 1;
    res = media_state(path, record_path);
	if (res == FAIL || res == ERROR)
	{
		INCIDENT_TYPE(res);
	}
	else 
	{
		MESSAGE_START();
		DESCRIPTION(PASS, "");
		MESSAGE_END();
		INCIDENT_TYPE(PASS);
	}
    g_print ("GST_START_TEST: EXIT. %s\n", __func__);
	TESTFUNCTION_END();
}
GST_END_TEST;

GST_START_TEST (gstAudioRecPerfAacHttpHosted) {
    char resources_path[SZ_RESOURCE_PATH];
    char path[SZ_PATH] ;
    int ret, i;
    char command[SZ_PATH+SZ_RESOURCE_PATH];
    char record_path[SZ_PATH];
	STATUS res;
	TESTFUNCTION_START();
    g_print ("\n [   Checks: ========================================  ]\n");
    g_sprintf(tcname, __func__);
    g_print ("TestCase: %s\n", tcname) ;
    g_print ("GST_START_TEST: ENTRY. %s\n", __func__);
    g_print( "[   Checks: AAC video ] \n");
    strcpy ( path, (char *)getenv ("RESRC_PUBLISHER_LINK") );strcat ( path, "/" );strcat ( path, "Test.aac" );
    g_print ("\n\n **** resources path = %s ***** \n", path);

    res = url_check(path);
    if (res == FAIL || res == ERROR)
	{
		INCIDENT_TYPE(res);
		return;
	}

    strcpy ( record_path, (char *)getenv ("OPENSOURCETEST_PATH") );
    strcat ( record_path, "recordings/");
    strcat (record_path, "record.aac");
    //local_recording = 1;
    res = media_state(path, record_path);
	if (res == FAIL || res == ERROR)
	{
		INCIDENT_TYPE(res);
	}
	else 
	{
		MESSAGE_START();
		DESCRIPTION(PASS, "");
		MESSAGE_END();
		INCIDENT_TYPE(PASS);
	}
    g_print ("GST_START_TEST: EXIT. %s\n", __func__);
	TESTFUNCTION_END();
}
GST_END_TEST;

GST_START_TEST (gstAudioRecPerfMkaHttpHosted) {
    char resources_path[SZ_RESOURCE_PATH];
    char path[SZ_PATH] ;
    int ret, i;
    char command[SZ_PATH+SZ_RESOURCE_PATH];
    char record_path[SZ_PATH];
	STATUS res;
	TESTFUNCTION_START();
    g_print ("\n [   Checks: ========================================  ]\n");
    g_sprintf(tcname, __func__);
    g_print ("TestCase: %s\n", tcname) ;
    g_print ("GST_START_TEST: ENTRY. %s\n", __func__);
    g_print( "[   Checks: MKA video ] \n");
    strcpy ( path, (char *)getenv ("RESRC_PUBLISHER_LINK") );strcat ( path, "/" );strcat ( path, "Test.mka" );
    g_print ("\n\n **** resources path = %s ***** \n", path);

    res = url_check(path);
    if (res == FAIL || res == ERROR)
	{
		INCIDENT_TYPE(res);
		return;
	}

    strcpy ( record_path, (char *)getenv ("OPENSOURCETEST_PATH") );
    strcat ( record_path, "recordings/");
    strcat (record_path, "record.mka");
    //local_recording = 1;
    res = media_state(path, record_path);
	if (res == FAIL || res == ERROR)
	{
		INCIDENT_TYPE(res);
	}
	else 
	{
		MESSAGE_START();
		DESCRIPTION(PASS, "");
		MESSAGE_END();
		INCIDENT_TYPE(PASS);
	}
    g_print ("GST_START_TEST: EXIT. %s\n", __func__);
	TESTFUNCTION_END();
}
GST_END_TEST;

GST_START_TEST (gstAudioRecPerf3GPHttpHosted) {
    char resources_path[SZ_RESOURCE_PATH];
    char path[SZ_PATH] ;
    int ret, i;
    char command[SZ_PATH+SZ_RESOURCE_PATH];
    char record_path[SZ_PATH];
	STATUS res;
	TESTFUNCTION_START();
    g_print ("\n [   Checks: ========================================  ]\n");
    g_sprintf(tcname, __func__);
    g_print ("TestCase: %s\n", tcname) ;
    g_print ("GST_START_TEST: ENTRY. %s\n", __func__);
    g_print( "[   Checks: 3GP video ] \n");
    strcpy ( path, (char *)getenv ("RESRC_PUBLISHER_LINK") );strcat ( path, "/" );strcat ( path, "Test.3GP" );
    g_print ("\n\n **** resources path = %s ***** \n", path);

    res = url_check(path);
    if (res == FAIL || res == ERROR)
	{
		INCIDENT_TYPE(res);
		return;
	}

    strcpy ( record_path, (char *)getenv ("OPENSOURCETEST_PATH") );
    strcat ( record_path, "recordings/");
    strcat (record_path, "record.3GP");
    //local_recording = 1;
    res = media_state(path, record_path);
    if (res == FAIL || res == ERROR)
	{
		INCIDENT_TYPE(res);
	}
	else 
	{
		MESSAGE_START();
		DESCRIPTION(PASS, "");
		MESSAGE_END();
		INCIDENT_TYPE(PASS);
	}
	g_print ("GST_START_TEST: EXIT. %s\n", __func__);
	TESTFUNCTION_END();
}
GST_END_TEST;

GST_START_TEST (gstVideoRecPerfHttpMp4) {
    char resources_path [SZ_RESOURCE_PATH] = "http://media.w3.org/2010/05/sintel/trailer.mp4";
    char record_path[SZ_PATH];
	STATUS res;
	TESTFUNCTION_START();
    g_print ("\n [   Checks: ========================================  ]\n");
    g_sprintf(tcname, __func__);
    g_print ("TestCase: %s\n", tcname) ;
    g_print ("GST_START_TEST: ENTRY. gstVideoRecPerfHttpMp4()\n");
    g_print( "[   Checks: MP4 video from http source] \n");
    strcpy ( record_path, (char *)getenv ("OPENSOURCETEST_PATH") );
    strcat ( record_path, "recordings/");
    strcat (record_path, "record_http.mp4");
    //http_recording = 1;
    res = media_state(resources_path, record_path);
	if (res == FAIL || res == ERROR)
	{
		INCIDENT_TYPE(res);
	}
	else 
	{
		MESSAGE_START();
		DESCRIPTION(PASS, "");
		MESSAGE_END();
		INCIDENT_TYPE(PASS);
	}
    g_print ("GST_START_TEST: EXIT. gstVideoRecPerfHttpMp4()\n");
	TESTFUNCTION_END();
}
GST_END_TEST;


static Suite *
media_testsuite (void) {
    Suite *s ;
    TCase *tc_chain ;
    int timeoutvalue = 300;

    GST_DEBUG ("Gstreamer_Recording_Performance_testsuite(): ENTRY.()\n");

    s = suite_create ("mediasuite");
    tc_chain = tcase_create ("mediachain");

    tcase_set_timeout (tc_chain, timeoutvalue);

    GST_DEBUG ("media_suite():timeoutvalue = %d\n", timeoutvalue);
    suite_add_tcase (s, tc_chain);

    tcase_add_test (tc_chain, gstVideoRecPerfMp4HttpHosted);
    tcase_add_test (tc_chain, gstVideoRecPerfAviHttpHosted);
    tcase_add_test (tc_chain, gstVideoRecPerfFlvHttpHosted);
    tcase_add_test (tc_chain, gstVideoRecPerfM2vHttpHosted);
    tcase_add_test (tc_chain, gstVideoRecPerfMpgHttpHosted);

    tcase_add_test (tc_chain, gstAudioRecPerfMp3HttpHosted);
    tcase_add_test (tc_chain, gstAudioRecPerfAc3HttpHosted);
    tcase_add_test (tc_chain, gstAudioRecPerfAacHttpHosted);
    tcase_add_test (tc_chain, gstAudioRecPerfMkaHttpHosted);
    tcase_add_test (tc_chain, gstAudioRecPerf3GPHttpHosted);

    tcase_add_test (tc_chain, gstVideoRecPerfHttpMp4);
    GST_DEBUG ("Gstreamer_Recording_Performance_testsuite(): EXIT.()\n");

    return s;
}

int
main (int argc, char **argv) {
    int nf;
    Suite *s;
    SRunner *sr;
	
	g_print ("Gstreamer_Recording_Performance_tests_HttpHosted()\n");
    XML_START();
	TESTCASE_START("Gstreamer_Recording_Performance_tests_HttpHosted");
	GST_ENV();
    
	GST_DEBUG ("main(): ENTRY.()\n");

    s = media_testsuite ();
    sr = srunner_create (s);

    gst_check_init (&argc, &argv);

    srunner_run_all (sr, CK_NORMAL);
    nf = srunner_ntests_failed (sr);
    srunner_free (sr);

    GST_DEBUG ("main(): EXIT.()\n");
	TESTCASE_END();
    return nf;
}
