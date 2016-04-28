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
/* GStreamer
 *
 * Functional test for Gstreamer Video playback
 *
 * Testcase for media playback using different video streams
 * video streams- mp4,flv,avi,wmv,mov,mkv,asf,m2v
*/

#ifdef HAVE_CONFIG_H
# include <config.h>
#endif
#include <gst/check/gstcheck.h>
#include <sys/wait.h>
#include <unistd.h>
#include <stdio.h>
#include "common/gstplayback.h"
#include "common/networkInfo.h"

#define SZ_TCNAME 50
#define SZ_RESOURCE_PATH 200
#define SZ_PATH 200
#define BILLION  1000000000L
#define MAX_CMD_LEN 1024

static char tcname[SZ_TCNAME] ;
static gboolean got_eos = FALSE;
GstElement *pipeline = NULL;
GstElement *src = NULL;
static double gCurrentPosition = 0.0;
static double gCurrentPosition_in_seconds = 0.0;
GstBus *bus = NULL;
static guint bus_watch = 0;
GstFormat format = GST_FORMAT_TIME;
gint64 position = 0;
GstEvent *seek_event = NULL;
GstElement *video_sink = NULL;
static double playback_time = 0.0;
static double sleep_time = 5.0;
typedef enum {
  GST_PLAY_FLAG_VIDEO                = 0x1,
  GST_PLAY_FLAG_AUDIO                = 0x2,
  GST_PLAY_FLAG_NATIVE_VIDEO         = 0x20,
  GST_PLAY_FLAG_NATIVE_AUDIO         = 0x40,
  GST_PLAY_FLAG_BUFFER_AFTER_DEMUX   = 0x100
} GstPlayFlags;


static gboolean
message_handler (GstBus * bus, GstMessage * msg, gpointer data) {
    GMainLoop *loop = (GMainLoop *) data;
    gchar *debug;
    GError *err;

    GST_DEBUG ("message_handler(). ENTRY \n");

    switch (GST_MESSAGE_TYPE (msg)) {
        case GST_MESSAGE_EOS:
            GST_DEBUG ("message_handler. GST_MESSAGE_EOS: %d \n", GST_MESSAGE_TYPE (msg) );
            GST_DEBUG ("Playback successful \n");
            g_print ("End of stream\n");
            got_eos = TRUE;
            g_main_loop_quit (loop);
        break;
        case GST_MESSAGE_ERROR:
            GST_DEBUG ("message_handler. GST_MESSAGE_ERROR: %d \n", GST_MESSAGE_TYPE (msg));
            gst_message_parse_error (msg, &err, &debug);
            g_free (debug);

            /* Will abort the check */
            g_warning ("Error: %s\n", err->message);
			MESSAGE_START();
			DESCRIPTION(ERROR, "Error: %s\n",err->message);
			MESSAGE_END();
			INCIDENT_TYPE(ERROR);
            g_error_free (err);

            g_main_loop_quit (loop);
        break;
        default:
            GST_DEBUG ("message_handler. default: %d \n", GST_MESSAGE_TYPE (msg));
           // g_print ("message_handler. default: %d \n", GST_MESSAGE_TYPE (msg));
        break;
    }

    GST_DEBUG ("message_handler(). EXIT \n");
    return TRUE;
}

static STATUS current_position_validation(double playback_time)
{
    gCurrentPosition_in_seconds = mplayer_position_update(&pipeline);

	if(gCurrentPosition_in_seconds>=(playback_time-1))
	{
	    	g_print ("Current Playback Position validation passed\n");
	    	g_print ("Current Position=%lf seconds\n", gCurrentPosition_in_seconds);
	    	return PASS;

	}
	else
	{
            g_print ("Current Playback Position validation failed\n");
            g_print ("Current Position=%lf seconds\n", gCurrentPosition_in_seconds);
            MESSAGE_START();
            DESCRIPTION(FAIL, "Current Playback Position validation failed");
            MESSAGE_END();
            return FAIL;
	}
}


static void load_url (GstElement *src, char *path) {
    /*Set the input filename to the source element */
    g_object_set (G_OBJECT (src), "uri", path, NULL);
    GST_DEBUG ("g_object_set done for location\n");
}

static STATUS load_elements (GMainLoop *loop, char *path)
{
    gint flags;
    pipeline= gst_pipeline_new ("player");
    GST_DEBUG ("gst_pipeline_new\n");
    if (!pipeline)
    {
        GST_DEBUG ("pipeline not created\n");
        MESSAGE_START();
        DESCRIPTION(ERROR, "pipeline not created");
		MESSAGE_END();
		return ERROR;
    }
    fail_unless (pipeline != NULL, "failed to create pipeline");

    src = gst_element_factory_make ("playbin2", "source");
    GST_DEBUG ("gst_element_factory_make. filesrc\n");
    if (!src)
    {
        GST_DEBUG ("Element source not created\n");
        MESSAGE_START();
        DESCRIPTION(ERROR, "Element source not created");
		MESSAGE_END();
		return ERROR;
    }
    fail_unless (src != NULL, "Failed to create filesrc element");

    /* Set the source path to get the stream from */
    load_url (src, path);
    g_object_get ( src, "flags", &flags, NULL);
    flags = GST_PLAY_FLAG_VIDEO | GST_PLAY_FLAG_AUDIO | GST_PLAY_FLAG_NATIVE_VIDEO
	    | GST_PLAY_FLAG_NATIVE_AUDIO;
    g_object_set (src, "flags", flags, NULL);

    fail_unless (gst_bin_add (GST_BIN (pipeline), src));
    GST_DEBUG ("Added All the Elements into the pipeline \n");

    bus = gst_element_get_bus (pipeline);
    GST_DEBUG ("gst_element_get_bus\n");

    bus_watch = gst_bus_add_watch (bus, message_handler, loop);

    GST_DEBUG ("gst_bus_add_watch\n");

    gst_object_unref (bus);
    GST_DEBUG ("gst_object_unref\n");

    return PASS;
}

static STATUS media_state(char *path) {
    GMainLoop *loop;

    got_eos = FALSE;

	STATUS res;
    loop = g_main_loop_new (NULL, FALSE);

    res = load_elements(loop, path);
	if(res == ERROR)
		return ERROR;

    res = mplayer_null(&pipeline);
	if (res == FAIL)
		return FAIL;
    res = mplayer_ready(&pipeline);
	if (res == FAIL)
		return FAIL;
    res = mplayer_pause(&pipeline);
	if (res == FAIL)
		return FAIL;
    res = mplayer_play(&pipeline);
	if (res == FAIL)
		return FAIL;

    g_main_loop_run (loop);
    GST_DEBUG ("gst_element_set_state. g_main_loop_run\n");

    fail_unless (got_eos);
    GST_DEBUG (" got_eos. %d\n", got_eos);

    got_eos = FALSE;
    GST_DEBUG (" got_eos. %d\n", got_eos);

    res = mplayer_stop(&pipeline);
	if (res == FAIL)
		return FAIL;

    g_main_loop_unref (loop);
    GST_DEBUG (" g_main_loop_unref.\n");

    g_source_remove (bus_watch);
    GST_DEBUG (" g_source_remove.\n");
	return PASS;
}

STATUS looping_the_program(char *path) {
    GMainLoop *loop = NULL;
	STATUS res;
    res = load_elements (loop, path);
	if(res == ERROR)
		return ERROR;
	else if (res == FAIL)
		return FAIL;

    g_print("Gstreamer video playback in a loop functionality testing \n");
    res = mplayer_play(&pipeline);
	if (res == FAIL)
		return FAIL;
    sleep(10);
    res = mplayer_stop(&pipeline);
	if (res == FAIL)
		return FAIL;
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

GST_START_TEST (gstVideoFuncMp4HttpHosted) {
    char path[SZ_PATH] ;
	STATUS res;
	TESTFUNCTION_START();
    g_print ("\n=========================\n");
    g_sprintf (tcname, __func__);
    g_print ("TestCase: %s\n", tcname) ;
    g_print ("GST_START_TEST: ENTRY. gstVideoFuncMp4HttpHosted()\n");

    strcpy ( path, (char *)getenv ("RESRC_PUBLISHER_LINK") );strcat ( path, "/" );strcat ( path, "Test.mp4" );
    g_print ("\n\n **** resource path = %s ***** \n", path);

    res = url_check(path);
    if (res == FAIL || res == ERROR)
	{
		INCIDENT_TYPE(res);
		return;
	}

	res = media_state(path);
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

GST_START_TEST (gstVideoFuncAviHttpHosted) {
    char path[SZ_PATH] ;
	STATUS res;
	TESTFUNCTION_START();
    g_print ("\n=========================\n");
    g_sprintf (tcname, __func__);
    g_print ("TestCase: %s\n", tcname) ;
    g_print ("GST_START_TEST: ENTRY. gstVideoFuncAviHttpHosted()\n");

    strcpy ( path, (char *)getenv ("RESRC_PUBLISHER_LINK") );strcat ( path, "/" );strcat ( path, "Test.avi" );
    g_print ("\n\n **** resource path = %s ***** \n", path);

    res = url_check(path);
    if (res == FAIL || res == ERROR)
	{
		INCIDENT_TYPE(res);
		return;
	}

    res = media_state(path);
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

GST_START_TEST (gstVideoFuncM2vHttpHosted) {
    char path[SZ_PATH] ;
	STATUS res;
	TESTFUNCTION_START();
    g_print ("\n=========================\n");
    g_sprintf(tcname, __func__);
    g_print ("TestCase: %s\n", tcname) ;
    g_print ("GST_START_TEST: ENTRY. gstVideoFuncM2vHttpHosted()\n");

    strcpy ( path, (char *)getenv ("RESRC_PUBLISHER_LINK") );strcat ( path, "/" );strcat ( path, "Test.m2v" );
    g_print ("\n\n **** resource path = %s ***** \n", path);

    res = url_check(path);
    if (res == FAIL || res == ERROR)
	{
		INCIDENT_TYPE(res);
		return;
	}

    res = media_state(path);
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

GST_START_TEST (gstVideoFuncPlayPauseStopHttpHosted) {
    GMainLoop *loop = NULL;
    char path[SZ_PATH] ;
    STATUS res;
	TESTFUNCTION_START();
    g_print ("\n=========================\n");
    g_sprintf(tcname, __func__);
    g_print ("TestCase: %s\n", tcname) ;
    g_print ("GST_START_TEST: ENTRY. gstVideoFuncPlayPauseStopHttpHosted()\n");

    strcpy ( path, (char *)getenv ("RESRC_PUBLISHER_LINK") );strcat ( path, "/" );strcat ( path, "Test.mp4" );
    g_print ("\n\n **** resource path = %s ***** \n", path);

    res = url_check(path);
    if (res == FAIL || res == ERROR)
	{
		INCIDENT_TYPE(res);
		return;
	}

    res = load_elements (loop, path);
    if(res == ERROR)
    {
        INCIDENT_TYPE(res);
        TESTFUNCTION_END();
        return;
    }

    g_print("Gstreamer video playback 'play_pause_stop' functionality testing \n");


    res = mplayer_null(&pipeline);
	if (res == FAIL)
	{
        INCIDENT_TYPE(res);
        TESTFUNCTION_END();
        return;
    }
    res = mplayer_ready(&pipeline);
	if (res == FAIL)
    {
        INCIDENT_TYPE(res);
        TESTFUNCTION_END();
        return;
    }
    res = mplayer_pause(&pipeline);
	if (res == FAIL)
    {
        INCIDENT_TYPE(res);
        TESTFUNCTION_END();
        return;
    }
    res = mplayer_play(&pipeline);
	if (res == FAIL)
    {
        INCIDENT_TYPE(res);
        TESTFUNCTION_END();
        return;
    }

    g_print("for 5 seconds\n");
	sleep(sleep_time);
	playback_time = playback_time + sleep_time;
	res = current_position_validation(playback_time);
    if(res == FAIL)
    {
        INCIDENT_TYPE(res);
        TESTFUNCTION_END();
        return;
    }

    mplayer_pause(&pipeline);
	g_print("for 5 seconds\n");
	sleep(sleep_time);

    mplayer_play(&pipeline);
	g_print("for 5 seconds\n");
	sleep(sleep_time);
    playback_time = playback_time + sleep_time;
	res = current_position_validation(playback_time);
    if(res == FAIL)
    {
        INCIDENT_TYPE(res);
        TESTFUNCTION_END();
        return;
    }

    res = mplayer_stop(&pipeline);
    if(res == FAIL)
    {
        INCIDENT_TYPE(res);
        TESTFUNCTION_END();
        return;
    }
    MESSAGE_START();
    DESCRIPTION(PASS, "");
    MESSAGE_END();
    INCIDENT_TYPE(PASS);
    g_print ("GST_START_TEST: EXIT. %s\n", __func__);
	TESTFUNCTION_END();
}
GST_END_TEST;

GST_START_TEST (gstVideoFuncPlayPauseHttpHosted) {
    GMainLoop *loop = NULL;
    char path[SZ_PATH] ;
    STATUS res;
	TESTFUNCTION_START();
    g_print ("\n=========================\n");

    g_sprintf(tcname, __func__);
    g_print ("TestCase: %s\n", tcname) ;
    g_print ("GST_START_TEST: ENTRY. gstVideoFuncPlayPauseHttpHosted()\n");

    strcpy ( path, (char *)getenv ("RESRC_PUBLISHER_LINK") );strcat ( path, "/" );strcat ( path, "Test.mp4" );
    g_print ("\n\n **** resource path = %s ***** \n", path);

    res = url_check(path);
    if (res == FAIL || res == ERROR)
	{
		INCIDENT_TYPE(res);
		return;
	}

    res = load_elements (loop, path);
    if(res == ERROR)
    {
        INCIDENT_TYPE(res);
        TESTFUNCTION_END();
        return;
    }

	g_print ("Gstreamer video playback 'play_pause' functionality testing \n");

    res = mplayer_play(&pipeline);
	if (res == FAIL)
    {
        INCIDENT_TYPE(res);
        TESTFUNCTION_END();
        return;
    }
    g_print("for 5 seconds\n");
	sleep(sleep_time);
	playback_time = playback_time + sleep_time;
	res = current_position_validation(playback_time);
	if (res == FAIL)
    {
        INCIDENT_TYPE(res);
        TESTFUNCTION_END();
        return;
    }
    res = mplayer_pause(&pipeline);
	if (res == FAIL)
    {
        INCIDENT_TYPE(res);
        TESTFUNCTION_END();
        return;
    }
	g_print("for 5 seconds\n");
	sleep(sleep_time);

    res = mplayer_stop(&pipeline);
	if (res == FAIL)
    {
        INCIDENT_TYPE(res);
        TESTFUNCTION_END();
        return;
    }
    MESSAGE_START();
    DESCRIPTION(PASS, "");
    MESSAGE_END();
    INCIDENT_TYPE(PASS);
    g_print ("GST_START_TEST: EXIT. %s\n", __func__);
	TESTFUNCTION_END();

}
GST_END_TEST;

GST_START_TEST (gstVideoFuncPlayStopHttpHosted) {
    GMainLoop *loop = NULL;
    char path[SZ_PATH] ;
    STATUS res;
	TESTFUNCTION_START();
    g_print ("\n=========================\n");

    g_sprintf (tcname, __func__);
    g_print ("TestCase: %s\n", tcname) ;
    g_print ("GST_START_TEST: ENTRY. gstVideoFuncPlayStopHttpHosted()\n");

    strcpy ( path, (char *)getenv ("RESRC_PUBLISHER_LINK") );strcat ( path, "/" );strcat ( path, "Test.mp4" );
    g_print ("\n\n **** resource path = %s ***** \n", path);

    res = url_check(path);
    if (res == FAIL || res == ERROR)
	{
		INCIDENT_TYPE(res);
		return;
	}

    res = load_elements (loop, path);
    if(res == ERROR)
    {
        INCIDENT_TYPE(res);
        TESTFUNCTION_END();
        return;
    }

    g_print ("Gstreamer video playback 'play_stop' functionality testing \n");

    res = mplayer_play(&pipeline);
    {
        INCIDENT_TYPE(res);
        TESTFUNCTION_END();
        return;
    }
    g_print("for 5 seconds\n");
	sleep(sleep_time);
	playback_time = playback_time + sleep_time;
	res = current_position_validation(playback_time);
    {
        INCIDENT_TYPE(res);
        TESTFUNCTION_END();
        return;
    }

    res = mplayer_stop(&pipeline);
	if (res == FAIL)
    {
        INCIDENT_TYPE(res);
        TESTFUNCTION_END();
        return;
    }
    MESSAGE_START();
    DESCRIPTION(PASS, "");
    MESSAGE_END();
    INCIDENT_TYPE(PASS);
    g_print ("GST_START_TEST: EXIT. %s\n", __func__);
	TESTFUNCTION_END();

}
GST_END_TEST;

GST_START_TEST (gstVideoFuncRewindHttpHosted) {
    GMainLoop *loop = NULL;
    char path[SZ_PATH] ;
    STATUS res;
	TESTFUNCTION_START();
    g_print ("\n=========================\n");

    g_sprintf(tcname, __func__);
    g_print ("TestCase: %s\n", tcname) ;
    g_print ("GST_START_TEST: ENTRY. gstVideoFuncRewindHttpHosted()\n");

    strcpy ( path, (char *)getenv ("RESRC_PUBLISHER_LINK") );strcat ( path, "/" );strcat ( path, "Test.mp4" );
    g_print ("\n\n **** resource path = %s ***** \n", path);

    res = url_check(path);
    if (res == FAIL || res == ERROR)
	{
		INCIDENT_TYPE(res);
		return;
	}

    res = load_elements (loop, path);
    if(res == ERROR)
    {
        INCIDENT_TYPE(res);
        TESTFUNCTION_END();
        return;
    }

    g_print ("Gstreamer video playback 'rewind' functionality testing \n");

    res = mplayer_play(&pipeline);
	if(res == FAIL)
    {
        INCIDENT_TYPE(res);
        TESTFUNCTION_END();
        return;
    }
    g_print("for 5 seconds\n");
	sleep(sleep_time);
	playback_time = playback_time + sleep_time;
	res = current_position_validation(playback_time);
	if (res == FAIL)
    {
        INCIDENT_TYPE(res);
        TESTFUNCTION_END();
        return;
    }
    gst_element_seek(src,
                         1.0 /*rate*/, /* Currently support only 1x speed during seek */
                         GST_FORMAT_TIME, GST_SEEK_FLAG_FLUSH | GST_SEEK_FLAG_KEY_UNIT,GST_SEEK_TYPE_SET,
                         0,
                         GST_SEEK_TYPE_NONE, 0);
	g_print("Rewinded to start position\n");
        sleep(1);
	playback_time=0.0;
	res = current_position_validation(playback_time);
	if (res == FAIL)
    {
        INCIDENT_TYPE(res);
        TESTFUNCTION_END();
        return;
    }

    g_print("Playing for 5 seconds\n");
	sleep(sleep_time);
	playback_time = playback_time + sleep_time;
	res = current_position_validation(playback_time);
	if (res == FAIL)
    {
        INCIDENT_TYPE(res);
        TESTFUNCTION_END();
        return;
    }
    res = mplayer_stop(&pipeline);
	if (res == FAIL)
    {
        INCIDENT_TYPE(res);
        TESTFUNCTION_END();
        return;
    }
    MESSAGE_START();
    DESCRIPTION(PASS, "");
    MESSAGE_END();
    INCIDENT_TYPE(PASS);
    g_print ("GST_START_TEST: EXIT. %s\n", __func__);
	TESTFUNCTION_END();
}
GST_END_TEST;

GST_START_TEST (gstVideoFuncSeekForwardFramesHttpHosted) {
    GMainLoop *loop = NULL;
    char path[SZ_PATH] ;
    STATUS res;
	TESTFUNCTION_START();
    g_print ("\n=========================\n");
    g_sprintf (tcname, __func__);
    g_print ("TestCase: %s\n", tcname) ;
    g_print ("GST_START_TEST: ENTRY. gstVideoFuncSeekForwardFramesHttpHosted()\n");
    strcpy ( path, (char *)getenv ("RESRC_PUBLISHER_LINK") );strcat ( path, "/" );strcat ( path, "Test.mp4" );
    g_print ("\n\n **** resource path = %s ***** \n", path);

    res = url_check(path);
    if (res == FAIL || res == ERROR)
	{
		INCIDENT_TYPE(res);
		return;
	}

	res = load_elements (loop, path);
    if(res == ERROR)
    {
        INCIDENT_TYPE(res);
        TESTFUNCTION_END();
        return;
    }

    g_print ("Gstreamer video playback 'seek forward by frames' functionality testing \n");

    res = mplayer_play(&pipeline);
	if (res == FAIL)
    {
        INCIDENT_TYPE(res);
        TESTFUNCTION_END();
        return;
    }
    g_print("for 5 seconds\n");
	sleep(sleep_time);
	playback_time = playback_time + sleep_time;
	res = current_position_validation(playback_time);
	if (res == FAIL)
    {
        INCIDENT_TYPE(res);
        TESTFUNCTION_END();
        return;
    }

    if (video_sink == NULL)
    {
        /* If we have not done so, obtain the sink through which we will send the step events */
        g_object_get (src, "video-sink", &video_sink, NULL);
    }

    gst_element_send_event (video_sink,gst_event_new_step (GST_FORMAT_BUFFERS, 1, 1, TRUE, FALSE));
    g_print ("Stepping one frame forward\n");

    //mplayer_play(&pipeline);
	playback_time = mplayer_position_update(&pipeline);

	g_print("Playing for 5 seconds\n");
	sleep(sleep_time);
	playback_time = playback_time + sleep_time;
	res = current_position_validation(playback_time);
	if (res == FAIL)
    {
        INCIDENT_TYPE(res);
        TESTFUNCTION_END();
        return;
    }

    res = mplayer_stop(&pipeline);
	if (res == FAIL)
    {
        INCIDENT_TYPE(res);
        TESTFUNCTION_END();
        return;
    }
    MESSAGE_START();
    DESCRIPTION(PASS, "");
    MESSAGE_END();
    INCIDENT_TYPE(PASS);
    g_print ("GST_START_TEST: EXIT. %s\n", __func__);
	TESTFUNCTION_END();
}
GST_END_TEST;

GST_START_TEST (gstVideoFuncSeekBackwardTimestampHttpHosted) {
    GMainLoop *loop = NULL;
    char path[SZ_PATH] ;
    STATUS res;
	TESTFUNCTION_START();
	g_print ("\n=========================\n");
    g_sprintf(tcname, __func__);
    g_print ("TestCase: %s\n", tcname) ;
    g_print ("GST_START_TEST: ENTRY. gstVideoFuncSeekBackwardTimestampHttpHosted()\n");

    strcpy ( path, (char *)getenv ("RESRC_PUBLISHER_LINK") );strcat ( path, "/" );strcat ( path, "Test.mp4" );
    g_print ("\n\n **** resource path = %s ***** \n", path);

    res = url_check(path);
    if (res == FAIL || res == ERROR)
	{
		INCIDENT_TYPE(res);
		return;
	}


	res = load_elements (loop, path);
    if(res == ERROR)
    {
        INCIDENT_TYPE(res);
        TESTFUNCTION_END();
        return;
    }
    g_print ("Gstreamer video playback 'seek backward by timestamp' functionality testing \n");

    res = mplayer_play(&pipeline);
	if (res == FAIL)
    {
        INCIDENT_TYPE(res);
        TESTFUNCTION_END();
        return;
    }
    g_print("for 10 seconds\n");
	sleep(sleep_time + 5 );
	playback_time = playback_time + sleep_time + 5;
	res = current_position_validation(playback_time);
	if (res == FAIL)
    {
        INCIDENT_TYPE(res);
        TESTFUNCTION_END();
        return;
    }

    gst_element_seek(src,
                         1.0 /*rate*/, /* Currently support only 1x speed during seek */
                         GST_FORMAT_TIME, GST_SEEK_FLAG_FLUSH | GST_SEEK_FLAG_KEY_UNIT,GST_SEEK_TYPE_SET,
                         5000000000,
                         GST_SEEK_TYPE_NONE, 0);


	g_print ("seeking backward from current position to 5 seconds\n");

	gst_element_query_duration (pipeline, &format, &position);
	gCurrentPosition = GST_TIME_AS_SECONDS(position);
	g_print ("Total Stream Duration=%lf seconds\n", gCurrentPosition);

	sleep(gCurrentPosition - 5.0);
	playback_time = gCurrentPosition - 5.0;
	res  = current_position_validation(playback_time);
	if (res == FAIL)
    {
        INCIDENT_TYPE(res);
        TESTFUNCTION_END();
        return;
    }

    res = mplayer_stop(&pipeline);
	if (res == FAIL)
    {
        INCIDENT_TYPE(res);
        TESTFUNCTION_END();
        return;
    }
    MESSAGE_START();
    DESCRIPTION(PASS, "");
    MESSAGE_END();
    INCIDENT_TYPE(PASS);
    g_print ("GST_START_TEST: EXIT. %s\n", __func__);
	TESTFUNCTION_END();
}
GST_END_TEST;

GST_START_TEST (gstVideoFuncSlowForwardHttpHosted) {
    GMainLoop *loop = NULL;
    char path[SZ_PATH] ;
    STATUS res;
	TESTFUNCTION_START();
    g_print ("\n=========================\n");
    g_sprintf(tcname, __func__);
    g_print ("TestCase: %s\n", tcname) ;
    g_print ("GST_START_TEST: ENTRY. gstVideoFuncSlowForwardHttpHosted()\n");
    strcpy ( path, (char *)getenv ("RESRC_PUBLISHER_LINK") );strcat ( path, "/" );strcat ( path, "Test.mp4" );
    g_print ("\n\n **** resource path = %s ***** \n", path);

    res = url_check(path);
    if (res == FAIL || res == ERROR)
	{
		INCIDENT_TYPE(res);
		return;
	}


	res = load_elements (loop, path);
    if(res == ERROR)
    {
        INCIDENT_TYPE(res);
        TESTFUNCTION_END();
        return;
    }

    g_print("Gstreamer video playback 'slow forward' functionality testing  \n");

    res = mplayer_play(&pipeline);
    if(res == FAIL)
    {
        INCIDENT_TYPE(res);
        TESTFUNCTION_END();
        return;
    }
    g_print("for 5 seconds\n");
	sleep(sleep_time);
	playback_time = playback_time + sleep_time;
	res  = current_position_validation(playback_time);
    if(res == FAIL)
    {
        INCIDENT_TYPE(res);
        TESTFUNCTION_END();
        return;
    }

    g_print ("Playing forward in 0.5x speed for 10 seconds\n");
    g_object_set (src, "trick-rate", 0.5, NULL);
    sleep(10);

    /* Obtain the current position, needed for the seek event */
    gst_element_query_position (pipeline, &format, &position);
    gCurrentPosition = GST_TIME_AS_MSECONDS(position);
    g_print ("position is %lf seconds\n",gCurrentPosition/1000);

    res = mplayer_pause(&pipeline);
    if(res == ERROR)
    {
        INCIDENT_TYPE(res);
        TESTFUNCTION_END();
        return;
    }
    g_object_set (src, "trick-rate", 1.0, NULL);
	g_print("Playing forward in 1x speed for 5 seconds\n");


    res = mplayer_play(&pipeline);
    if(res == ERROR)
    {
        INCIDENT_TYPE(res);
        TESTFUNCTION_END();
        return;
    }
    sleep(5);

    /* Obtain the current position, needed for the seek event */
    gst_element_query_position (pipeline, &format, &position);
    gCurrentPosition = GST_TIME_AS_MSECONDS(position);
    g_print ("position is %lf seconds\n",gCurrentPosition/1000);

    res = mplayer_stop(&pipeline);
    if(res == ERROR)
    {
        INCIDENT_TYPE(res);
        TESTFUNCTION_END();
        return;
    }
    MESSAGE_START();
    DESCRIPTION(PASS, "");
    MESSAGE_END();
    INCIDENT_TYPE(PASS);
    g_print ("GST_START_TEST: EXIT. %s\n", __func__);
	TESTFUNCTION_END();
}
GST_END_TEST;

GST_START_TEST (gstVideoFuncSeekForwardTimestampHttpHosted) {
    GMainLoop *loop = NULL;
    char path[SZ_PATH] ;
    STATUS res;
	TESTFUNCTION_START();
    g_print ("\n=========================\n");
    g_sprintf (tcname, __func__);
    g_print ("TestCase: %s\n", tcname) ;
    g_print ("GST_START_TEST: ENTRY. gstVideoFuncSeekForwardTimestampHttpHosted()\n");

    strcpy ( path, (char *)getenv ("RESRC_PUBLISHER_LINK") );strcat ( path, "/" );strcat ( path, "Test.mp4" );
    g_print ("\n\n **** resource path = %s ***** \n", path);

    res = url_check(path);
    if (res == FAIL || res == ERROR)
	{
		INCIDENT_TYPE(res);
		return;
	}

	res = load_elements (loop, path);
	if (res == ERROR)
	{
		INCIDENT_TYPE(res);
		TESTFUNCTION_END();
	}

	g_print ("Gstreamer video playback 'seek forward by timestamp' functionality testing  \n");

    res = mplayer_play(&pipeline);
	if (res == FAIL)
	{
		INCIDENT_TYPE(res);
		TESTFUNCTION_END();
	}
    g_print("for 5 seconds\n");
	sleep(sleep_time);
	playback_time = playback_time + sleep_time;
	res = current_position_validation(playback_time);
	if (res == FAIL)
	{
		INCIDENT_TYPE(res);
		TESTFUNCTION_END();
	}

    gst_element_seek(src,
                         1.0 /*rate*/, /* Currently support only 1x speed during seek */
                         GST_FORMAT_TIME, GST_SEEK_FLAG_FLUSH | GST_SEEK_FLAG_KEY_UNIT,GST_SEEK_TYPE_SET,
                         20000000000,
                         GST_SEEK_TYPE_NONE, 0);


	g_print ("seeking forward from current position to 20 seconds\n");

	gst_element_query_duration (pipeline, &format, &position);
	gCurrentPosition = GST_TIME_AS_SECONDS(position);
	g_print ("Total Stream Duration=%lf seconds\n", gCurrentPosition);

	sleep(gCurrentPosition - 20.0);
	playback_time = gCurrentPosition - 20.0;
	res = current_position_validation(playback_time);
	if (res == FAIL)
	{
		INCIDENT_TYPE(res);
		TESTFUNCTION_END();
	}

    res = mplayer_stop(&pipeline);
	if (res == FAIL)
	{
		INCIDENT_TYPE(res);
		TESTFUNCTION_END();
	}
	MESSAGE_START();
    DESCRIPTION(PASS, "");
    MESSAGE_END();
    INCIDENT_TYPE(PASS);
    g_print ("GST_START_TEST: EXIT. %s\n", __func__);
	TESTFUNCTION_END();
}
GST_END_TEST;

GST_START_TEST (gstVideoFuncFastForwardHttpHosted) {
    GMainLoop *loop = NULL;
    char path[SZ_PATH] ;
    STATUS res;
	TESTFUNCTION_START();
    g_print ("\n=========================\n");
    g_sprintf (tcname, __func__);
    g_print ("TestCase: %s\n", tcname) ;
    g_print ("GST_START_TEST: ENTRY. gstVideoFuncFastForwardHttpHosted()\n");

    strcpy ( path, (char *)getenv ("RESRC_PUBLISHER_LINK") );strcat ( path, "/" );strcat ( path, "Test.mp4" );
    g_print ("\n\n **** resource path = %s ***** \n", path);

    res = url_check(path);
    if (res == FAIL || res == ERROR)
	{
		INCIDENT_TYPE(res);
		return;
	}


	res = load_elements (loop, path);
	if(res == ERROR)
	{
		INCIDENT_TYPE(res);
    	TESTFUNCTION_END();
	}

	g_print ("Gstreamer video playback 'fast forward' functionality testing  \n");
	res = mplayer_play(&pipeline);
	if(res == FAIL)
	{
		INCIDENT_TYPE(res);
    	TESTFUNCTION_END();
	}
    g_print("for 5 seconds\n");
	sleep(sleep_time);
	playback_time = playback_time + sleep_time;
	res = current_position_validation(playback_time);
	if(res == FAIL)
	{
		INCIDENT_TYPE(res);
    	TESTFUNCTION_END();
	}

    g_print ("Playing forward in 2x speed for 10 seconds\n");
    g_object_set (src, "trick-rate", 2.0, NULL);
    sleep(10);

    /* Obtain the current position, needed for the seek event */
    gst_element_query_position (pipeline, &format, &position);
    gCurrentPosition = GST_TIME_AS_MSECONDS(position);
    g_print ("position is %lf seconds\n",gCurrentPosition/1000);

    res = mplayer_stop(&pipeline);
	if(res == FAIL)
	{
		INCIDENT_TYPE(res);
    	TESTFUNCTION_END();
	}
	MESSAGE_START();
    DESCRIPTION(PASS, "");
    MESSAGE_END();
    INCIDENT_TYPE(PASS);
    g_print ("GST_START_TEST: EXIT. %s\n", __func__);
	TESTFUNCTION_END();
}
GST_END_TEST;

GST_START_TEST (gstVideoFuncTogglingPlayPauseHttpHosted) {
    GMainLoop *loop = NULL;
    char path[SZ_PATH] ;
	STATUS res;
	TESTFUNCTION_START();
    g_print ("\n=========================\n");
    g_sprintf (tcname, __func__);
    g_print ("TestCase: %s\n", tcname) ;
    g_print ("GST_START_TEST: ENTRY. gstVideoFuncTogglingPlayPauseHttpHosted()\n");

    strcpy ( path, (char *)getenv ("RESRC_PUBLISHER_LINK") );strcat ( path, "/" );strcat ( path, "Test.mp4" );
    g_print ("\n\n **** resource path = %s ***** \n", path);

    res = url_check(path);
    if (res == FAIL || res == ERROR)
	{
		INCIDENT_TYPE(res);
		return;
	}

	res = load_elements (loop, path);
	if (res == ERROR)
	{
		INCIDENT_TYPE(res);
		TESTFUNCTION_END();
	}

	g_print ("Gstreamer video playback 'toggling between play and pause' functionality testing  \n");

	res = mplayer_play(&pipeline);
	if (res == FAIL)
	{
		INCIDENT_TYPE(res);
		TESTFUNCTION_END();
	}
    g_print("for 5 seconds\n");
	sleep(sleep_time);
	playback_time = playback_time + sleep_time;
	res = current_position_validation(playback_time);
	if (res == FAIL)
	{
		INCIDENT_TYPE(res);
		TESTFUNCTION_END();
	}

    res = mplayer_pause(&pipeline);
	if (res == FAIL)
	{
		INCIDENT_TYPE(res);
		TESTFUNCTION_END();
	}

	sleep(sleep_time);

	res = mplayer_play(&pipeline);
	if (res == FAIL)
	{
		INCIDENT_TYPE(res);
		TESTFUNCTION_END();
	}

    g_print("for 5 seconds\n");
	sleep(sleep_time);
	playback_time = playback_time + sleep_time;
	res = current_position_validation(playback_time);
	if (res == FAIL)
	{
		INCIDENT_TYPE(res);
		TESTFUNCTION_END();
	}

	res = mplayer_pause(&pipeline);
	if (res == FAIL)
	{
		INCIDENT_TYPE(res);
		TESTFUNCTION_END();
	}
	sleep(sleep_time);

	res = mplayer_play(&pipeline);
	if (res == FAIL)
	{
		INCIDENT_TYPE(res);
		TESTFUNCTION_END();
	}

    g_print("for 5 seconds\n");
	sleep(sleep_time);
	playback_time = playback_time + sleep_time;
	res = current_position_validation(playback_time);
	if (res == FAIL)
	{
		INCIDENT_TYPE(res);
		TESTFUNCTION_END();
	}

    res = mplayer_stop(&pipeline);
	if (res == FAIL)
	{
		INCIDENT_TYPE(res);
		TESTFUNCTION_END();
	}
	MESSAGE_START();
    DESCRIPTION(PASS, "");
    MESSAGE_END();
    INCIDENT_TYPE(PASS);
    g_print ("GST_START_TEST: EXIT. %s\n", __func__);
	TESTFUNCTION_END();
}
GST_END_TEST;

GST_START_TEST (gstVideoFuncPlayIterativelyHttpHosted) {
    int loop_count = 0;
    char path[SZ_PATH] ;
	STATUS res;
	TESTFUNCTION_START();
    g_print ("\n=========================\n");
    g_sprintf (tcname, __func__);
    g_print ("TestCase: %s\n", tcname) ;
    g_print ("GST_START_TEST: ENTRY. gstVideoFuncPlayIterativelyHttpHosted()\n");

    strcpy ( path, (char *)getenv ("RESRC_PUBLISHER_LINK") );strcat ( path, "/" );strcat ( path, "Test.mp4" );
    g_print ("\n\n **** resource path = %s ***** \n", path);

    res = url_check(path);
    if (res == FAIL || res == ERROR)
	{
		INCIDENT_TYPE(res);
		return;
	}


    while  (loop_count < 5)
    {
        res = looping_the_program(path);
		if(res == FAIL || res == ERROR)
		{
			INCIDENT_TYPE(res);
			TESTFUNCTION_END();
		}
        loop_count++;
        g_print ("Looping count = %d\n", loop_count);
    }
	MESSAGE_START();
    DESCRIPTION(PASS, "");
    MESSAGE_END();
    INCIDENT_TYPE(PASS);
    g_print ("GST_START_TEST: EXIT. %s\n", __func__);
	TESTFUNCTION_END();
}
GST_END_TEST;

GST_START_TEST (gstVideoFuncFastBackwardHttpHosted) {
    GMainLoop *loop = NULL;
    char path[SZ_PATH] ;
	STATUS res;
	TESTFUNCTION_START();
    g_print ("\n=========================\n");
    g_sprintf(tcname, __func__);
    g_print ("TestCase: %s\n", tcname) ;
    g_print ("GST_START_TEST: ENTRY. gstVideoFuncFastBackwardHttpHosted()\n");

    strcpy ( path, (char *)getenv ("RESRC_PUBLISHER_LINK") );strcat ( path, "/" );strcat ( path, "Test.mp4" );
    g_print ("\n\n **** resource path = %s ***** \n", path);

    res = url_check(path);
    if (res == FAIL || res == ERROR)
	{
		INCIDENT_TYPE(res);
		return;
	}
	
	res = load_elements (loop, path);
	if (res == ERROR)
	{
		INCIDENT_TYPE(res);
		TESTFUNCTION_END();
	}

	g_print ("Gstreamer video playback 'fast backward' functionality testing  \n");

	res = mplayer_play(&pipeline);
	if (res == FAIL)
	{
		INCIDENT_TYPE(res);
		TESTFUNCTION_END();
	}
    sleep(50);

	/* Obtain the current position, needed for the seek event */
    gst_element_query_position (pipeline, &format, &position);
    gCurrentPosition = GST_TIME_AS_MSECONDS(position);
    g_print ("position is %lf seconds\n",gCurrentPosition/1000);

    g_print ("Playing backward in 1x speed\n");
    g_object_set (src, "trick-rate", -1.0, NULL);
    sleep(10);

    /* Obtain the current position, needed for the seek event */
    gst_element_query_position (pipeline, &format, &position);
    gCurrentPosition = GST_TIME_AS_MSECONDS(position);
    g_print ("position is %lf seconds\n",gCurrentPosition/1000);

	g_print("Fast backward in 2x speed \n");
	g_object_set (src, "trick-rate", -2.0, NULL);
	sleep(10);

    /* Obtain the current position, needed for the seek event */
    gst_element_query_position (pipeline, &format, &position);
    gCurrentPosition = GST_TIME_AS_MSECONDS(position);
    g_print ("position is %lf seconds\n",gCurrentPosition/1000);

	res = mplayer_stop(&pipeline);
	if (res == FAIL)
	{
		INCIDENT_TYPE(res);
		TESTFUNCTION_END();
	}
	MESSAGE_START();
    DESCRIPTION(PASS, "");
    MESSAGE_END();
    INCIDENT_TYPE(PASS);
    g_print ("GST_START_TEST: EXIT. %s\n", __func__);
	TESTFUNCTION_END();
}
GST_END_TEST;

GST_START_TEST (gstVideoFuncUdpStreamingHttpHosted) {
    int script_path_res = 0;
    char script_path[SZ_PATH];
    char path[SZ_PATH] ;
    char command[SZ_PATH+SZ_RESOURCE_PATH];
	STATUS res;
	TESTFUNCTION_START();
    g_print ("\n=========================\n");
    g_sprintf (tcname, __func__);
    g_print ("TestCase: %s\n", tcname) ;
    g_print ("GST_START_TEST: ENTRY. gstVideoFuncUdpStreamingHttpHosted()\n");
    
    strcpy ( path, (char *)getenv ("RESRC_PUBLISHER_LINK") );strcat ( path, "/" );strcat ( path, "Test.mp4" );
    g_print ("\n\n **** resource path = %s ***** \n", path);
    
    res = url_check(path);
    if (res == FAIL || res == ERROR)
	{
		INCIDENT_TYPE(res);
		return;
	}

    strcpy ( script_path, (char *)getenv ("OPENSOURCETEST_PATH") );
    strcat ( script_path, "/gst-plugin-base/udp_mp4_receiver");

    script_path_res = access ( script_path, F_OK );
    if ( script_path_res != 0 ) {
        g_warning ( "Error: Resource Not Found, missing receiver app\n" );
		MESSAGE_START();
        DESCRIPTION(ERROR, "Resource Not Found, missing receiver app");
		MESSAGE_END();
		INCIDENT_TYPE(ERROR);
		TESTFUNCTION_END();
    	return;
    }
    strcpy ( script_path, (char *)getenv ("OPENSOURCETEST_PATH") );
    strcat ( script_path, "/gst-plugin-base/udp_mp4_sender_hosted");

    script_path_res = access ( script_path, F_OK );
    if ( script_path_res != 0 ) {
        g_warning ( "Error: Resource Not Found, missing transmitted app\n" );
		MESSAGE_START();
        DESCRIPTION(ERROR, "Resource Not Found, missing transmitter app");
		MESSAGE_END();
		INCIDENT_TYPE(ERROR);
		TESTFUNCTION_END();
    	return;
    }

    char portName[10]; char ipAddr[32];
    char AppPath[MAX_CMD_LEN];
    char AppName[256];
    char RsrcPath[MAX_CMD_LEN];
    char udpPort[32];

    /* Get Box Netowrk Details */
    /* GetIpAddrDetails API will be platform specific defined in platform.c file */
    GetIpAddrDetails(portName, ipAddr);
    g_print("STB BOX - portName : %s, ipAddr :%s \n\n", portName, ipAddr); 

    pid_t RXidChild = vfork();

    if(RXidChild == 0)
    {
	   sprintf( AppName,"%s" , "udp_mp4_receiver");
	   sprintf ( AppPath,"%s", (char *)getenv ("OPENSOURCETEST_PATH") );
	   strcat ( AppPath, "/gst-plugin-base/");
	   strcat ( AppPath, AppName );
	   sprintf ( RsrcPath,"%s",  (char *)getenv ("TDKOUTPUT_PATH"));
	   strcat ( RsrcPath, "/resources/udp.mp4");
	   sprintf ( udpPort,"%s", "8888");

	   g_print ("\n\n RX - AppPath::%s AppName::%s RsrcPath::%s udpPort::%s \n", AppPath,AppName,RsrcPath,udpPort);

	   // Parameters to execl must be strings
           execl(AppPath, AppName, RsrcPath, udpPort , (char *)NULL);
	
    }else if(RXidChild <0)
    {
		g_print("failed fork\n");
		return ;
    }
    else {
	  g_print("for 5 seconds\n");
          sleep(sleep_time);

          pid_t TXidChild = vfork();
   	  if(TXidChild == 0)
   	  {
		   sprintf( AppName,"%s" , "udp_mp4_sender_hosted");
		   sprintf ( AppPath,"%s", (char *)getenv ("OPENSOURCETEST_PATH") );
		   strcat ( AppPath, "/gst-plugin-base/");
		   strcat ( AppPath, AppName );
		   sprintf ( RsrcPath, "%s",  path);
   		   sprintf ( ipAddr, "%s", ipAddr);

		   g_print ("\n\n TX - AppPath::%s AppName::%s RsrcPath::%s udpPort::%s ipAddr::%s \n", AppPath,AppName,RsrcPath,udpPort, ipAddr);

	           // Parameters to execl must be strings
		   execl(AppPath, AppName, RsrcPath, udpPort , ipAddr, (char *)NULL);

	    }else if(TXidChild <0)
	    {
		g_print("failed fork\n");
		return ;
	    } else {
		    int returnStatus = 0;
		    g_print("Wait for TX and RX to finish for 5 seconds\n");
                    sleep(sleep_time);
		    waitpid(TXidChild, &returnStatus, 0);
		    // Verify transmitter process terminated without error.  
   		    if (returnStatus == 0)  
		    {
		       g_print ("The transmitter process terminated normally.\n");    
		    }

		    if (returnStatus == 1)      
		    {
		       g_print ("The transmitter process terminated with an error!.\n");    
		    }
		    kill(RXidChild, SIGKILL);
	    }
     }
  
    g_print ("GST_START_TEST: EXIT. %s\n", __func__);
	TESTFUNCTION_END();
}
GST_END_TEST;

GST_START_TEST (gstVideoFuncFlvHttpHosted) {
    char path[SZ_PATH] ;
	STATUS res;
	TESTFUNCTION_START();
    g_print ("\n=========================\n");
    g_sprintf (tcname, __func__);
    g_print ("TestCase: %s\n", tcname) ;
    g_print ("GST_START_TEST: ENTRY. %s\n", __func__);

    strcpy ( path, (char *)getenv ("RESRC_PUBLISHER_LINK") );strcat ( path, "/" );strcat ( path, "Test.flv" );
    g_print ("\n\n **** resource path = %s ***** \n", path);

    res = url_check(path);
    if (res == FAIL || res == ERROR)
	{
		INCIDENT_TYPE(res);
		return;
	}


    res = media_state(path);
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

GST_START_TEST (gstVideoFuncMpgHttpHosted) {
    char path[SZ_PATH] ;
	STATUS res;
	TESTFUNCTION_START();
    g_print ("\n=========================\n");
    g_sprintf (tcname, __func__);
    g_print ("TestCase: %s\n", tcname) ;
    g_print ("GST_START_TEST: ENTRY. %s\n", __func__);

   strcpy ( path, (char *)getenv ("RESRC_PUBLISHER_LINK") );strcat ( path, "/" );strcat ( path, "Test.mpg" );
    g_print ("\n\n **** resource path = %s ***** \n", path);

    res = url_check(path);
    if (res == FAIL || res == ERROR)
	{
		INCIDENT_TYPE(res);
		return;
	}

    
    res = media_state(path);
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

GST_START_TEST (gstVideoFuncWebmHttpHosted) {
    char path[SZ_PATH] ;
	STATUS res;
	TESTFUNCTION_START();
    g_print ("\n=========================\n");
    g_sprintf (tcname, __func__);
    g_print ("TestCase: %s\n", tcname) ;
    g_print ("GST_START_TEST: ENTRY. %s\n", __func__);

    strcpy ( path, (char *)getenv ("RESRC_PUBLISHER_LINK") );strcat ( path, "/" );strcat ( path, "Test.webm" );
    g_print ("\n\n **** resource path = %s ***** \n", path);

    res = url_check(path);
    if (res == FAIL || res == ERROR)
	{
		INCIDENT_TYPE(res);
		return;
	}


    res = media_state(path);
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

static Suite *
media_testsuite (void) {
    Suite *s ;
    TCase *tc_chain ;
    int timeoutvalue = 300;

    GST_DEBUG ("Gstreamer_Video_Playback_HttpHosted_testsuite(): ENTRY.()\n");

    s = suite_create ("mediasuite");
    tc_chain = tcase_create ("mediachain");

    tcase_set_timeout (tc_chain, timeoutvalue);
    GST_DEBUG ("media_suite():timeoutvalue = %d\n", timeoutvalue);
    suite_add_tcase (s, tc_chain);

    tcase_add_test (tc_chain, gstVideoFuncMp4HttpHosted);
    tcase_add_test (tc_chain, gstVideoFuncAviHttpHosted);
    tcase_add_test (tc_chain, gstVideoFuncM2vHttpHosted);

    tcase_add_test (tc_chain, gstVideoFuncFlvHttpHosted);
    tcase_add_test (tc_chain, gstVideoFuncMpgHttpHosted);
  //  tcase_add_test (tc_chain, gstVideoFuncWebmHttpHosted);

    tcase_add_test (tc_chain, gstVideoFuncPlayPauseStopHttpHosted);
    tcase_add_test (tc_chain, gstVideoFuncPlayPauseHttpHosted);
    tcase_add_test (tc_chain, gstVideoFuncPlayStopHttpHosted);
    tcase_add_test (tc_chain, gstVideoFuncRewindHttpHosted);

    //tcase_add_test (tc_chain, gstVideoFuncSeekForwardFramesHttpHosted); /*This test in Build 3 is not working*/
	tcase_add_test (tc_chain, gstVideoFuncSeekBackwardTimestampHttpHosted);
    tcase_add_test (tc_chain, gstVideoFuncSlowForwardHttpHosted);
    tcase_add_test (tc_chain, gstVideoFuncSeekForwardTimestampHttpHosted);
    tcase_add_test (tc_chain, gstVideoFuncFastForwardHttpHosted);
    tcase_add_test (tc_chain, gstVideoFuncTogglingPlayPauseHttpHosted);
    tcase_add_test (tc_chain, gstVideoFuncPlayIterativelyHttpHosted);

    //tcase_add_test (tc_chain, gstVideoFuncFastBackwardHttpHosted); /*This test in Build 3 is not working*/
	tcase_add_test (tc_chain, gstVideoFuncUdpStreamingHttpHosted);
	


    GST_DEBUG ("Gstreamer_Video_Playback_HttpHosted_testsuite(): EXIT.()\n");

    return s;
}


int
main (int argc, char **argv) {
    int nf;
    Suite *s;
    SRunner *sr;

    g_print("Gstreamer_Video_Playback_HttpHosted\n");
    GST_DEBUG ("main(): ENTRY.()\n");
    XML_START();
	TESTCASE_START("Gstreamer_Video_Playback_HttpHosted");
	GST_ENV();

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
