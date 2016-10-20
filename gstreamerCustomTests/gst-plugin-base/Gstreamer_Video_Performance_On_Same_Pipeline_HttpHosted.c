/*
 * If not stated otherwise in this file or this component's Licenses.txt file the
 * following copyright and licenses apply:
 *
 * Copyright 2016 RDK Management
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
*/
#include <gst/gst.h>
#include <glib.h>
#include <time.h>
#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <sys/wait.h>
#include <gst/check/gstcheck.h>
#include "common/gstplayback.h"

#define BILLION  1000000000L
#define SZ_TCNAME 50
#define SZ_RESOURCE_PATH 200
#define SZ_PATH 200
#define NUMBER_OF_ITERATION 50 
#define MSEC 1000
typedef enum {
  GST_PLAY_FLAG_VIDEO                = 0x1,
  GST_PLAY_FLAG_AUDIO                = 0x2,
  GST_PLAY_FLAG_NATIVE_VIDEO         = 0x20,
  GST_PLAY_FLAG_NATIVE_AUDIO         = 0x40,
  GST_PLAY_FLAG_BUFFER_AFTER_DEMUX   = 0x100
} GstPlayFlags;

static char tcname[SZ_TCNAME];
struct timespec clock_before_pipeline_creation, clock_after_pipeline_creation, clock_at_play_event, clock_at_play_command;

GstElement *pipeline, *playbin;
GstBus *bus;

static gboolean bus_call (GstBus *bus, GstMessage *msg, gpointer data)
{
  GMainLoop *loop = (GMainLoop *) data;

  switch (GST_MESSAGE_TYPE (msg)) {

    case GST_MESSAGE_EOS:
      g_print ("End of stream\n");
      g_main_loop_quit (loop);
      break;

    case GST_MESSAGE_ERROR: {
      gchar  *debug;
      GError *error;

      gst_message_parse_error (msg, &error, &debug);
      g_free (debug);

      g_warning ("Error: %s\n", error->message);
      MESSAGE_START();	
      DESCRIPTION(ERROR, "Error: %s",error->message);
      MESSAGE_END();	
      INCIDENT_TYPE(ERROR);	 	 
      g_error_free (error);

      g_main_loop_quit (loop);
      break;
    }

   case GST_MESSAGE_STATE_CHANGED: {
     GstState old_state, new_state, pending_state,temp_state;
     gst_message_parse_state_changed (msg, &old_state, &new_state, &pending_state);
     if (new_state == GST_STATE_READY && old_state == GST_STATE_NULL)
         temp_state = GST_STATE_NULL;
         if (new_state == GST_STATE_PLAYING ) {
             if( clock_gettime( CLOCK_REALTIME, &clock_at_play_event) == -1 ) {
                    //perror( "clock gettime" );
					DESCRIPTION(ERROR, "Error: clock gettime");
					INCIDENT_TYPE(ERROR);
              }
                 sleep(1);
                 g_main_loop_quit (loop);
                 gst_element_set_state (pipeline, GST_STATE_NULL);
                 
          }
      }
      break;  

    default:
      break;
  }

  return TRUE;
}

STATUS create_pipeline (char *path, GMainLoop *loop)
{
  gint flags;
  /* Create gstreamer elements */
  pipeline = gst_pipeline_new ("video-player");
  playbin = gst_element_factory_make ("playbin2", "playbin");

  if (!pipeline || !playbin)
  {
    g_printerr ("One element could not be created. Exiting.\n");
	MESSAGE_START();
	DESCRIPTION(ERROR, "Element source not created");
	MESSAGE_END();
	return ERROR;
  }

  /* Set up the pipeline */
  g_print ("Elements are created\n");

  /* set the properties of other elements */
  g_object_set (G_OBJECT (playbin), "uri", path, NULL);

  g_object_get (playbin, "flags", &flags, NULL);
  flags = GST_PLAY_FLAG_VIDEO | GST_PLAY_FLAG_AUDIO | GST_PLAY_FLAG_NATIVE_VIDEO
                | GST_PLAY_FLAG_NATIVE_AUDIO;
  g_object_set (playbin, "flags", flags, NULL);

  /* we add a message handler */
  bus = gst_pipeline_get_bus (GST_PIPELINE (pipeline));
  gst_bus_add_watch (bus, bus_call, loop);
  gst_object_unref (bus);

  /* we add all elements into the pipeline */
  gst_bin_add_many (GST_BIN (pipeline), playbin, NULL);
  g_print ("Added all the Elements into the pipeline\n");
  return PASS;

}

STATUS destroy_pipeline ()
{
  /* Out of the main loop, clean up nicely */
  g_print ("Returned, stopping playback\n");
  //gst_element_set_state (pipeline, GST_STATE_NULL);
  if (GST_STATE_CHANGE_FAILURE == gst_element_set_state(GST_ELEMENT(pipeline), GST_STATE_NULL))
  {
    GST_DEBUG ("Failed to destroy_pipeline\n");
    MESSAGE_START();
    DESCRIPTION(FAIL, "Fail: Pipeline not set to STOP. Exiting.");
    MESSAGE_END();		
	return FAIL;
  }	
  g_print ("Deleting pipeline\n");
  gst_object_unref (GST_OBJECT (pipeline));
  
  return PASS;

}

STATUS perf_time_taken_video_play_iter (char *path)
{
  GMainLoop *loop;
  double video_start_delay=0.0;
  //struct timespec clock_at_play_command;
  double sumof_video_start_delay = 0.0;
  int count = 0;
  STATUS testresult;
  GstStateChangeReturn ret;
  g_print ("ENTRY : %s function\n", __func__);
  
  loop = g_main_loop_new (NULL, FALSE);
  
  testresult = create_pipeline (path, loop);
  if(testresult == ERROR)
    return ERROR;
  else if (testresult == FAIL)
    return FAIL;
	
  while(count <= NUMBER_OF_ITERATION) {
  video_start_delay=0.0;

  /* Set the pipeline to "playing" state*/
  g_print ("Playing the video\n");
  if (GST_STATE_CHANGE_FAILURE == gst_element_set_state(GST_ELEMENT(pipeline), GST_STATE_PLAYING))
	{
        GST_DEBUG ("Failed to PLAY\n");
        MESSAGE_START();
        DESCRIPTION(FAIL, "Fail: Pipeline not set to PLAYING. Exiting.");
        MESSAGE_END();
        return FAIL;
	}

  if( clock_gettime( CLOCK_REALTIME, &clock_at_play_command) == -1 ) {
      //perror( "clock gettime" );
      MESSAGE_START();
      DESCRIPTION(ERROR, "Error: clock gettime");
      MESSAGE_END();
      return ERROR;
  }

  /* Iterate */
  g_print ("Running...");
  g_main_loop_run (loop);

  video_start_delay = ( clock_at_play_event.tv_sec - clock_at_play_command.tv_sec )
                                                + (double)( clock_at_play_event.tv_nsec - clock_at_play_command.tv_nsec ) / (double)BILLION;

  if (count != 0) {
        sumof_video_start_delay += video_start_delay;
        g_print (" Time Taken for video playing = %lf seconds\n", video_start_delay * MSEC);
        g_print (" Sum of Time Taken for video playing = %lf seconds\n", sumof_video_start_delay * MSEC);
  } else {
        g_print (" Checks: First time - Time Taken for video playing = %lf seconds\n", video_start_delay * MSEC);
  }
     count++;
     g_print("Count = %d\n",count);
     if (count > NUMBER_OF_ITERATION)
             break;
  }
  /*Destroy pipeline*/
  testresult = destroy_pipeline ();
  if(testresult == ERROR)
	return ERROR;
  else if (testresult == FAIL)
    return FAIL;
	
  MESSAGE_START();
  //g_print (" Checks: Average over %d times - Time Taken for video playing = %lf seconds\n", NUMBER_OF_ITERATION, (sumof_video_start_delay/NUMBER_OF_ITERATION));
  DESCRIPTION(CHECKS, "Average over %d times - Time Taken for video playing :: %lf ms\n", NUMBER_OF_ITERATION, (sumof_video_start_delay/NUMBER_OF_ITERATION) * MSEC);
  MESSAGE_END();
  g_print ("EXIT : %s function\n", __func__);
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

GST_START_TEST (gstVideoPerfMp4PlaySamePipeIterHttpHosted) 
{
    char resources_path[SZ_RESOURCE_PATH];
    char path[SZ_PATH] ;
    int ret, i;
    char command[SZ_PATH+SZ_RESOURCE_PATH];
	STATUS res;
	TESTFUNCTION_START();
    g_print ("\n[   Checks: ============================================   ]\n");
    g_sprintf (tcname, __func__);
    g_print ("\n[   Checks: TestCase: %s   ]\n\r", tcname);
    g_print ("GST_START_TEST: ENTRY. %s\n", __func__);

    strcpy ( path, (char *)getenv ("RESRC_PUBLISHER_LINK") );strcat ( path, "/" );strcat ( path, "Test.mp4" );
    g_print ("\n\n **** resources path = %s ***** \n", path);

    res = url_check(path);
    if (res == FAIL || res == ERROR)
	{
		INCIDENT_TYPE(res);
		return;
	}
    
    res = perf_time_taken_video_play_iter(path);
	INCIDENT_TYPE(res);
    g_print ("GST_START_TEST: EXIT. %s\n", __func__);
	TESTFUNCTION_END();
}
GST_END_TEST;


GST_START_TEST (gstVideoPerfAviPlaySamePipeIterHttpHosted) 
{
    char resources_path[SZ_RESOURCE_PATH];
    char path[SZ_PATH] ;
    int ret, i;
    char command[SZ_PATH+SZ_RESOURCE_PATH];
	STATUS res;
	TESTFUNCTION_START();
    g_print ("\n[   Checks: ============================================   ]\n");
    g_sprintf (tcname, __func__);
    g_print ("\n[   Checks: TestCase: %s   ]\n\r", tcname);
    g_print ("GST_START_TEST: ENTRY. %s\n", __func__);

    strcpy ( path, (char *)getenv ("RESRC_PUBLISHER_LINK") );strcat ( path, "/" );strcat ( path, "Test.avi" );
    g_print ("\n\n **** resources path = %s ***** \n", path);

    res = url_check(path);
    if (res == FAIL || res == ERROR)
	{
		INCIDENT_TYPE(res);
		return;
	}

    res = perf_time_taken_video_play_iter(path);
	INCIDENT_TYPE(res);
    g_print ("GST_START_TEST: EXIT. %s\n", __func__);
	TESTFUNCTION_END();

}
GST_END_TEST;

GST_START_TEST (gstVideoPerfM2vPlaySamePipeIterHttpHosted) 
{
    char resources_path[SZ_RESOURCE_PATH];
    char path[SZ_PATH] ;
    int ret, i;
    char command[SZ_PATH+SZ_RESOURCE_PATH];
	STATUS res;
	TESTFUNCTION_START();
    g_print ("\n[   Checks: ============================================   ]\n");
    g_sprintf (tcname, __func__);
    g_print ("\n[   Checks: TestCase: %s   ]\n\r", tcname);
    g_print ("GST_START_TEST: ENTRY. %s\n", __func__);

   strcpy ( path, (char *)getenv ("RESRC_PUBLISHER_LINK") );strcat ( path, "/" );strcat ( path, "Test.m2v" );
    g_print ("\n\n **** resources path = %s ***** \n", path);

    res = url_check(path);
    if (res == FAIL || res == ERROR)
	{
		INCIDENT_TYPE(res);
		return;
	}

    res = perf_time_taken_video_play_iter(path);
	INCIDENT_TYPE(res);
    g_print ("GST_START_TEST: EXIT. %s\n", __func__);
	TESTFUNCTION_END();
}
GST_END_TEST;



GST_START_TEST (gstVideoPerfFlvPlaySamePipeIterHttpHosted) 
{
    char resources_path[SZ_RESOURCE_PATH];
    char path[SZ_PATH] ;
    int ret, i;
    char command[SZ_PATH+SZ_RESOURCE_PATH];
	STATUS res;
	TESTFUNCTION_START();
    g_print ("\n[   Checks: ============================================   ]\n");
    g_sprintf (tcname, __func__);
    g_print ("\n[   Checks: TestCase: %s   ]\n\r", tcname);
    g_print ("GST_START_TEST: ENTRY. %s\n", __func__);

    strcpy ( path, (char *)getenv ("RESRC_PUBLISHER_LINK") );strcat ( path, "/" );strcat ( path, "Test.flv" );
    g_print ("\n\n **** resources path = %s ***** \n", path);

    res = url_check(path);
    if (res == FAIL || res == ERROR)
	{
		INCIDENT_TYPE(res);
		return;
	}

    res = perf_time_taken_video_play_iter(path);
	INCIDENT_TYPE(res);
    g_print ("GST_START_TEST: EXIT. %s\n", __func__);
	TESTFUNCTION_END();
}
GST_END_TEST;



GST_START_TEST (gstVideoPerfMpgPlaySamePipeIterHttpHosted) 
{
    char resources_path[SZ_RESOURCE_PATH];
    char path[SZ_PATH] ;
    int ret, i;
    char command[SZ_PATH+SZ_RESOURCE_PATH];
	STATUS res;
	TESTFUNCTION_START();
    g_print ("\n[   Checks: ============================================   ]\n");
    g_sprintf (tcname, __func__);
    g_print ("\n[   Checks: TestCase: %s   ]\n\r", tcname);
    g_print ("GST_START_TEST: ENTRY. %s\n", __func__);

    strcpy ( path, (char *)getenv ("RESRC_PUBLISHER_LINK") );strcat ( path, "/" );strcat ( path, "Test.mpg" );
    g_print ("\n\n **** resources path = %s ***** \n", path);

    res = url_check(path);
    if (res == FAIL || res == ERROR)
	{
		INCIDENT_TYPE(res);
		return;
	}

    res = perf_time_taken_video_play_iter(path);
	INCIDENT_TYPE(res);
    g_print ("GST_START_TEST: EXIT. %s\n", __func__);
	TESTFUNCTION_END();
}
GST_END_TEST;

static Suite *
performance_video_testsuite (void) {
    Suite *s ;
    TCase *tc_chain ;
    int timeoutvalue = 100;

    GST_DEBUG ("performance_video_testsuite(): ENTRY.()\n");

    s = suite_create ("performance_video_testsuite");
    tc_chain = tcase_create ("performance_video_testsuite");

    tcase_set_timeout (tc_chain, timeoutvalue);
    GST_DEBUG ("performance_video_testsuite():timeoutvalue = %d\n", timeoutvalue);

    suite_add_tcase (s, tc_chain);

    
    tcase_add_test (tc_chain, gstVideoPerfMp4PlaySamePipeIterHttpHosted);
    tcase_add_test (tc_chain, gstVideoPerfAviPlaySamePipeIterHttpHosted);
    tcase_add_test (tc_chain, gstVideoPerfM2vPlaySamePipeIterHttpHosted);
    tcase_add_test (tc_chain, gstVideoPerfFlvPlaySamePipeIterHttpHosted);
    tcase_add_test (tc_chain, gstVideoPerfMpgPlaySamePipeIterHttpHosted);
      
    GST_DEBUG ("performance_video_testsuite(): EXIT.()\n");
    return s;
}

int
main (int argc, char **argv)
{
    int nf;
    Suite *s;
    SRunner *sr;

	g_print ("Gstreamer_Video_Performance_On_Same_Pipeline_HttpHosted()\n");
    XML_START();
	TESTCASE_START("Gstreamer_Video_Performance_On_Same_Pipeline_HttpHosted");
	GST_ENV();
	
    GST_DEBUG ("main(): ENTRY.()\n");

    s = performance_video_testsuite ();
    sr = srunner_create (s);

    gst_check_init (&argc, &argv);

    srunner_run_all (sr, CK_NORMAL);
    nf = srunner_ntests_failed (sr);
    srunner_free (sr);

    GST_DEBUG ("main(): EXIT.()\n");
	TESTCASE_END();
    return nf;
}

