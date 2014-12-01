/* GStreamer
 *
 * Functional test to get content-frame-rate and interlace property of omx videodecoder
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
#define SZ_PATH 200
#define SZ_RESOURCE_PATH 200
static char tcname[SZ_TCNAME];
static int flag = 0;

static void
on_pad_added (GstElement *element,
              GstPad     *pad,
              gpointer    data)
{
  GstPad *sinkpad;
  GstElement *queue = (GstElement *) data;

  /* We can now link this pad with the queue sink pad */
  g_print ("Dynamic pad created, linking demuxer/queue\n");

  sinkpad = gst_element_get_static_pad (queue, "sink");

 
  gst_pad_link (pad, sinkpad);

  gst_object_unref (sinkpad);
}

static STATUS media_state(char *resources_path, int flag) {

  GMainLoop *loop; 
  GstElement *pipeline, *filesrc, *demuxer, *video_queue, *videodec, *videosink, *audio_queue, *audiodec, *audiosink;
  GstBus *bus;
  double cValue = 0.0;
  gboolean iValue;

  loop = g_main_loop_new (NULL, FALSE); 
 

  /* Create gstreamer elements */ 
  pipeline = gst_pipeline_new ("video-player"); 
  filesrc = gst_element_factory_make ("souphttpsrc", "httpsrc"); 
  demuxer = gst_element_factory_make ("qtdemux", "demuxer"); 
  video_queue =  gst_element_factory_make ("queue", "queue for video");
  videodec = gst_element_factory_make ("omx_videodec", "videodec"); 
  videosink = gst_element_factory_make ("omx_videosink", "videosink");
  audio_queue =  gst_element_factory_make ("queue", "queue for audio");
  audiodec = gst_element_factory_make ("omx_audiodec", "audiodec"); 
  audiosink = gst_element_factory_make ("omx_audiosink", "audiosink"); 
  
  if (!pipeline || !filesrc ||  !demuxer  || !video_queue || !audio_queue || !videodec || !audiodec ||!videosink ||!audiosink ) 
  { 
    g_printerr ("One element could not be created. Exiting.\n"); 
    MESSAGE_START();
    DESCRIPTION(ERROR, "Error: One element could not be created. Exiting.");
    MESSAGE_END();	
    return ERROR; 
  } 

  /* Set up the pipeline */ 
  g_print ("Elements are created\n\n"); 

  /* set the properties of other elements */ 
  g_object_set (G_OBJECT (filesrc), "location", resources_path, NULL); 
  

 /* we add all elements into the pipeline */ 
  gst_bin_add_many (GST_BIN (pipeline), filesrc, demuxer, video_queue, videodec, videosink, audio_queue, audiodec, audiosink, NULL); 
  g_print ("Added all the Elements into the pipeline\n"); 

  /* we link the elements together */ 
  gst_element_link (filesrc, demuxer);
  g_signal_connect (demuxer, "pad-added", G_CALLBACK (on_pad_added), video_queue); 
  gst_element_link_many (video_queue, videodec, videosink, NULL); 
  
  g_signal_connect (demuxer, "pad-added", G_CALLBACK (on_pad_added), audio_queue);
  gst_element_link_many (audio_queue, audiodec, audiosink, NULL); 
  
  g_print ("Linked all the Elements together\n");


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
  g_print ("Running for 10 seconds...\n"); 
  
  sleep(10);
  
   if (flag == 1)
  {
  g_object_get (G_OBJECT(videodec), "contentframerate", &cValue, NULL);
  g_print("content framerate: %lf fps\n",cValue);
  }
  if (flag == 2)
  {
  g_object_get (G_OBJECT(videodec), "interlace", &iValue, NULL);
  g_print("stream interlace value : %d\n",iValue);
  if(iValue == 1)
  g_print("stream is interlaced\n");
  else
  g_print("stream is not interlaced\n");
  }
  
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

GST_START_TEST (gstOmxdecProprtyContentframerate) {
    char path[SZ_PATH] ;
    STATUS res;
    TESTFUNCTION_START();
    g_print ("\n=========================\n");
    g_sprintf(tcname, __func__);
    g_print ("TestCase: %s\n", tcname) ;
    g_print ("GST_START_TEST: ENTRY. gstOmxdecProprtyContentframerate()\n");

    if ( NULL == (char *)getenv ("RESRC_PUBLISHER_LINK") ) {
    	g_warning ( "Error: Env variable RESRC_PUBLISHER_LINK Not Found, Configure /var/tdk/tdk.conf\n" );
		MESSAGE_START();
        DESCRIPTION(ERROR, "Env variable RESRC_PUBLISHER_LINK Not Found, Configure /var/tdk/tdk.conf");
		MESSAGE_END();
		INCIDENT_TYPE(ERROR);
		TESTFUNCTION_END();
    	return ERROR;
    }

    strcpy ( path, (char *)getenv ("RESRC_PUBLISHER_LINK") );strcat ( path, "/" );strcat ( path, "Test.mp4" );
    g_print ("\n\n **** resource path = %s ***** \n", path);

    res = url_check(path);
    if (res == FAIL || res == ERROR)
	{
		INCIDENT_TYPE(res);
		return;
	}
    
    flag = 1;
    res = media_state(path,flag);
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
    g_print ("GST_START_TEST: EXIT. gstOmxdecProprtyContentframerate()\n");
    TESTFUNCTION_END();
}
GST_END_TEST;

GST_START_TEST (gstOmxdecProprtyStreaminterlace) {
    char path[SZ_PATH] ;
    STATUS res;
    TESTFUNCTION_START();
    g_print ("\n=========================\n");
    g_sprintf(tcname, __func__);
    g_print ("TestCase: %s\n", tcname) ;
    g_print ("GST_START_TEST: ENTRY. gstOmxdecProprtyStreaminterlace()\n");

    if ( NULL == (char *)getenv ("RESRC_PUBLISHER_LINK") ) {
    	g_warning ( "Error: Env variable RESRC_PUBLISHER_LINK Not Found, Configure /var/tdk/tdk.conf\n" );
		MESSAGE_START();
        DESCRIPTION(ERROR, "Env variable RESRC_PUBLISHER_LINK Not Found, Configure /var/tdk/tdk.conf");
		MESSAGE_END();
		INCIDENT_TYPE(ERROR);
		TESTFUNCTION_END();
    	return ERROR;
    }

    strcpy ( path, (char *)getenv ("RESRC_PUBLISHER_LINK") );strcat ( path, "/" );strcat ( path, "Test.mp4" );
    g_print ("\n\n **** resource path = %s ***** \n", path);

    res = url_check(path);
    if (res == FAIL || res == ERROR)
	{
		INCIDENT_TYPE(res);
		return;
	}
    
    flag = 2;
    res = media_state(path,flag);
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
    g_print ("GST_START_TEST: EXIT. gstOmxdecProprtyStreaminterlace()\n");
    TESTFUNCTION_END();
}
GST_END_TEST;

static Suite *
media_testsuite (void) {
    Suite *s ;
    TCase *tc_chain ;
    int timeoutvalue = 300;

    GST_DEBUG ("Gstreamer_omxdecoder_Feature_testsuite(): ENTRY.()\n");

    s = suite_create ("mediasuite");
    tc_chain = tcase_create ("mediachain");

    tcase_set_timeout (tc_chain, timeoutvalue);

    GST_DEBUG ("media_suite():timeoutvalue = %d\n", timeoutvalue);
    suite_add_tcase (s, tc_chain);

    tcase_add_test (tc_chain, gstOmxdecProprtyContentframerate);
    tcase_add_test (tc_chain, gstOmxdecProprtyStreaminterlace);
    GST_DEBUG ("Gstreamer_omxdecoder_Feature_testsuite(): EXIT.()\n");

    return s;
}


int
main (int argc, char **argv) {
    int nf;
    Suite *s;
    SRunner *sr;

    g_print("Gstreamer_omxdecoder_Feature_testsuite\n");
    GST_DEBUG ("main(): ENTRY.()\n");
    XML_START();
	TESTCASE_START("Gstreamer_omxdecoder_Feature_testsuite");
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
  
