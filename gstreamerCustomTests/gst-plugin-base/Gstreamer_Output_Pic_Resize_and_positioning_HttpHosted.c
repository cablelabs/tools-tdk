/* GStreamer
 *
 * Functional test for Output Picture Resizing and Positioning Feature
 *
 * 
*/

#include <gst/gst.h> 
#include <glib.h> 
#include <gst/check/gstcheck.h>
#include <unistd.h>

#include <dirent.h>
#include <sys/types.h>
#include <sys/dir.h>
#include <sys/param.h>
#include <sys/wait.h>
#include <stdio.h>
#include "common/gstplayback.h"
#define SZ_TCNAME 50
#define SZ_RESOURCE_PATH 200
#define SZ_PATH 200
static char tcname[SZ_TCNAME];
static int flag = 0;
bus_call (GstBus *bus, GstMessage *msg, gpointer data) 
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
      DESCRIPTION(ERROR, "Error: %s", error->message);
      MESSAGE_END();	
	  INCIDENT_TYPE(ERROR);
      g_error_free (error); 

      g_main_loop_quit (loop); 
      break; 
    } 
    default: 
      break; 
  } 

  return TRUE; 
} 


static void
on_pad_added (GstElement *element,
              GstPad     *pad,
              gpointer    data)
{
  GstPad *sinkpad;
  GstElement *capsfilter = (GstElement *) data;

  /* We can now link this pad with the capsfilter sink pad */
  g_print ("Dynamic pad created, linking demuxer/capsfilter\n");

  sinkpad = gst_element_get_static_pad (capsfilter, "sink");

 
  gst_pad_link (pad, sinkpad);

  gst_object_unref (sinkpad);
}

static STATUS media_state(char *resources_path, int flag) {

  GMainLoop *loop; 

  GstElement *pipeline, *filesrc, *demuxer, *capsfilter, *decoder, *queue, *sink;

  GstBus *bus;

  GstCaps *filtercaps;

  gboolean ret1,ret2;

  loop = g_main_loop_new (NULL, FALSE); 

    /* Create gstreamer elements */ 
  pipeline = gst_pipeline_new ("player"); 
  filesrc = gst_element_factory_make ("souphttpsrc", "filesrc"); 
  demuxer = gst_element_factory_make ("qtdemux", "demuxer"); 
  capsfilter = gst_element_factory_make ("capsfilter", "capsfilter");
  queue = gst_element_factory_make ("queue", "queue for video");
  decoder= gst_element_factory_make ("omx_videodec", "decoder");
  sink = gst_element_factory_make ("omx_videosink", "sink");
  

  if (!pipeline || !filesrc ||  !demuxer  || !capsfilter || !queue || !decoder || !sink ) 
  { 
    g_printerr ("One element could not be created. Exiting.\n"); 
    MESSAGE_START();
    DESCRIPTION(ERROR, "Error: One element could not be created. Exiting.");
    MESSAGE_END();	
    return ERROR;   
} 

  /* Set up the pipeline */ 
  g_print ("Elements are created\n"); 


  filtercaps = gst_caps_new_simple ("video/x-h264", NULL);

   g_print("resource path=%s \n", resources_path);

  /* set the properties of other elements */ 
  g_object_set (G_OBJECT (filesrc), "location", resources_path, NULL); 
  g_object_set (G_OBJECT (capsfilter), "caps", filtercaps, NULL);

  if (flag == 1)
{
  g_print("flag=%d \n",flag);
  g_object_set (G_OBJECT (sink), "rectangle", "0,0,320,240", NULL);
}
  else if (flag == 2)
{
  g_print("flag=%d \n",flag);
  g_object_set (G_OBJECT (sink), "rectangle", "0,0,640,480", NULL);
}
  else if (flag == 3)
{
  g_print("flag=%d \n",flag);
  g_object_set (G_OBJECT (sink), "rectangle", "0,0,150,50", NULL);
}
  else if (flag == 4)
{
  g_print("flag=%d \n",flag);
  g_object_set (G_OBJECT (sink), "rectangle", "0,15,320,240", NULL);
}
  else if (flag == 5)
{
  g_print("flag=%d \n",flag);
  g_object_set (G_OBJECT (sink), "rectangle", "0,15,320,240", NULL);
}
  else if (flag == 6)
{
  g_print("flag=%d \n",flag);
  g_object_set (G_OBJECT (sink), "rectangle", "15,15,320,240", NULL);
}
 
  /* we add a message handler */ 
  bus = gst_pipeline_get_bus (GST_PIPELINE (pipeline)); 
  gst_bus_add_watch (bus, bus_call, loop); 
  gst_object_unref (bus); 


 /* we add all elements into the pipeline */ 
  gst_bin_add_many (GST_BIN (pipeline), filesrc, demuxer, capsfilter, queue, decoder, sink, NULL); 
  g_print ("Added all the Elements into the pipeline\n"); 

  

  /* we link the elements together */ 
  ret1 = gst_element_link (filesrc, demuxer);
  if(ret1){
  g_print("first linking returns %d \n", ret1);
  g_signal_connect (demuxer, "pad-added", G_CALLBACK (on_pad_added), capsfilter);
}else
{
MESSAGE_START();
DESCRIPTION(ERROR,"Error: Linking of elements hindered");
MESSAGE_END();
} 

  ret2 = gst_element_link_many (capsfilter, queue, decoder, sink, NULL);
 if(ret2){
  g_print("second linking returns %d \n", ret2);
  g_print ("Linked all the Elements together\n");
}else
{
MESSAGE_START();
DESCRIPTION(ERROR,"Error: Linking of elements hindered");
MESSAGE_END();
}

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


  /* Iterate */ 
  g_print ("Running...\n"); 
  g_main_loop_run (loop); 

  
  /* Out of the main loop, clean up nicely */ 
  g_print ("Returned, stopping playback\n"); 
 if (GST_STATE_CHANGE_FAILURE == gst_element_set_state(GST_ELEMENT(pipeline), GST_STATE_NULL))
	{
        GST_DEBUG ("Failed to NULL\n");
        MESSAGE_START();
        DESCRIPTION(FAIL, "Fail: Pipeline not set to NULL. Exiting.");
        MESSAGE_END();
		return FAIL;
	}

  g_print ("Deleting pipeline\n"); 
  gst_object_unref (GST_OBJECT (pipeline)); 
  gst_caps_unref (filtercaps);
MESSAGE_START();
    DESCRIPTION(PASS,"");
    MESSAGE_END();
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

GST_START_TEST (gstOutputPicResize0x0x320x240HttpHosted) {    
    char path[SZ_PATH] ;
    STATUS res;
    TESTFUNCTION_START();
    g_print ("\n=========================\n");
    g_sprintf(tcname, __func__);
    g_print ("TestCase: %s\n", tcname) ;
    g_print ("GST_START_TEST: ENTRY. gstOutputPicResize0x0x320x240HttpHosted()\n");

    strcpy ( path, (char *)getenv ("RESRC_PUBLISHER_LINK") );strcat ( path, "/" );strcat ( path, "Test.mp4" );
    g_print ("\n\n **** resource path = %s ***** \n\n", path);

    res = url_check(path);
    if (res == FAIL || res == ERROR)
	{
		INCIDENT_TYPE(res);
		return;
	}

    flag = 1;
    res = media_state(path,flag);
    INCIDENT_TYPE(res);
    g_print ("GST_START_TEST: EXIT. gstOutputPicResize0x0x320x240HttpHosted()\n");
TESTFUNCTION_END();
}
GST_END_TEST;

GST_START_TEST (gstOutputPicResize0x0x640x480HttpHosted) {
    char path[SZ_PATH] ;
    STATUS res;
    TESTFUNCTION_START();
    g_print ("\n=========================\n");
    g_sprintf(tcname, __func__);
    g_print ("TestCase: %s\n", tcname) ;
    g_print ("GST_START_TEST: ENTRY. gstOutputPicResize0x0x640x480HttpHosted()\n");

    strcpy ( path, (char *)getenv ("RESRC_PUBLISHER_LINK") );strcat ( path, "/" );strcat ( path, "Test.mp4" );
    g_print ("\n\n **** resource path = %s ***** \n\n", path);

    res = url_check(path);
    if (res == FAIL || res == ERROR)
	{
		INCIDENT_TYPE(res);
		return;
	}

    flag = 2;
    res = media_state(path,flag);
    INCIDENT_TYPE(res);
    g_print ("GST_START_TEST: EXIT. gstOutputPicResize0x0x640x480HttpHosted()\n");
TESTFUNCTION_END();
}
GST_END_TEST;

GST_START_TEST (gstOutputPicResize0x0x150x50HttpHosted) {
    char path[SZ_PATH] ;
    STATUS res;
    TESTFUNCTION_START();
    g_print ("\n=========================\n");
    g_sprintf(tcname, __func__);
    g_print ("TestCase: %s\n", tcname) ;
    g_print ("GST_START_TEST: ENTRY. gstOutputPicResize0x0x150x50HttpHosted()\n");

    strcpy ( path, (char *)getenv ("RESRC_PUBLISHER_LINK") );strcat ( path, "/" );strcat ( path, "Test.mp4" );
    g_print ("\n\n **** resource path = %s ***** \n\n", path);

    res = url_check(path);
    if (res == FAIL || res == ERROR)
	{
		INCIDENT_TYPE(res);
		return;
	}

    flag = 3;
    res = media_state(path,flag);
    INCIDENT_TYPE(res);
    g_print ("GST_START_TEST: EXIT. gstOutputPicResize0x0x150x50HttpHosted()\n");
TESTFUNCTION_END();
}
GST_END_TEST;

GST_START_TEST (gstOutputPicPositioning0x15x320x240HttpHosted) {
    char path[SZ_PATH] ;
    STATUS res;
    TESTFUNCTION_START();	
    g_print ("\n=========================\n");
    g_sprintf(tcname, __func__);
    g_print ("TestCase: %s\n", tcname) ;
    g_print ("GST_START_TEST: ENTRY. gstOutputPicPositioning0x15x320x240HttpHosted()\n");

    strcpy ( path, (char *)getenv ("RESRC_PUBLISHER_LINK") );strcat ( path, "/" );strcat ( path, "Test.mp4" );
    g_print ("\n\n **** resource path = %s ***** \n\n", path);

    res = url_check(path);
    if (res == FAIL || res == ERROR)
	{
		INCIDENT_TYPE(res);
		return;
	}

    flag = 4;
    res = media_state(path,flag);
    INCIDENT_TYPE(res);
    g_print ("GST_START_TEST: EXIT. gstOutputPicPositioning0x15x320x240HttpHosted()\n");
TESTFUNCTION_END();
}
GST_END_TEST;

GST_START_TEST (gstOutputPicPositioning15x0x320x240HttpHosted) {
    char path[SZ_PATH] ;
    STATUS res;
    TESTFUNCTION_START();
    g_print ("\n=========================\n");
    g_sprintf(tcname, __func__);
    g_print ("TestCase: %s\n", tcname) ;
    g_print ("GST_START_TEST: ENTRY. gstOutputPicPositioning15x0x320x240HttpHosted()\n");

    strcpy ( path, (char *)getenv ("RESRC_PUBLISHER_LINK") );strcat ( path, "/" );strcat ( path, "Test.mp4" );
    g_print ("\n\n **** resource path = %s ***** \n\n", path);

    res = url_check(path);
    if (res == FAIL || res == ERROR)
	{
		INCIDENT_TYPE(res);
		return;
	}

    flag = 5;
    res = media_state(path,flag);
    INCIDENT_TYPE(res);
    g_print ("GST_START_TEST: EXIT. gstOutputPicPositioning15x0x320x240HttpHosted()\n");
TESTFUNCTION_END();
}
GST_END_TEST;

GST_START_TEST (gstOutputPicPositioning15x15x320x240HttpHosted) {
    char path[SZ_PATH] ;
    STATUS res;
    TESTFUNCTION_START();
    g_print ("\n=========================\n");
    g_sprintf(tcname, __func__);
    g_print ("TestCase: %s\n", tcname) ;
    g_print ("GST_START_TEST: ENTRY. gstOutputPicPositioning15x15x320x240HttpHosted()\n");

    strcpy ( path, (char *)getenv ("RESRC_PUBLISHER_LINK") );strcat ( path, "/" );strcat ( path, "Test.mp4" );
    g_print ("\n\n **** resource path = %s ***** \n\n", path);

    res = url_check(path);
    if (res == FAIL || res == ERROR)
	{
		INCIDENT_TYPE(res);
		return;
	}

    flag = 6;
    res = media_state(path,flag);
    INCIDENT_TYPE(res);
    g_print ("GST_START_TEST: EXIT. gstOutputPicPositioning15x15x320x240HttpHosted()\n");
TESTFUNCTION_END();
}
GST_END_TEST;


static Suite *
media_testsuite (void) {
    Suite *s ;
    TCase *tc_chain ;
    int timeoutvalue = 300;

    GST_DEBUG ("Gstreamer_Resizing and_Positioning_Feature_testsuite(): ENTRY.()\n");

    s = suite_create ("mediasuite");
    tc_chain = tcase_create ("mediachain");

    tcase_set_timeout (tc_chain, timeoutvalue);

    GST_DEBUG ("media_suite():timeoutvalue = %d\n", timeoutvalue);
    suite_add_tcase (s, tc_chain);

    tcase_add_test (tc_chain, gstOutputPicResize0x0x320x240HttpHosted);
    tcase_add_test (tc_chain, gstOutputPicResize0x0x640x480HttpHosted);
    tcase_add_test (tc_chain, gstOutputPicResize0x0x150x50HttpHosted);
    tcase_add_test (tc_chain, gstOutputPicPositioning0x15x320x240HttpHosted);
    tcase_add_test (tc_chain, gstOutputPicPositioning15x0x320x240HttpHosted);
    tcase_add_test (tc_chain, gstOutputPicPositioning15x15x320x240HttpHosted);
    

    GST_DEBUG ("Gstreamer_Resizing and_Positioning_Feature_testsuite(): EXIT.()\n");

    return s;
}


int
main (int argc, char **argv) {
    int nf;
    Suite *s;
    SRunner *sr;
    
   g_print ("Gstreamer_Output_Pic_Resize_and_positioning_HttpHosted()\n");

    XML_START();
	TESTCASE_START("Gstreamer_Output_Pic_Resize_and_positioning_HttpHosted");
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
