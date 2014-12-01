/* GStreamer
 *
 * Functional test for Gstreamer Recording Feature
 *
 * 
*/

#ifdef HAVE_CONFIG_H
# include <config.h>
#endif
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
static char tcname[SZ_TCNAME] ;

static gboolean got_eos = FALSE;
GstElement *pipeline = NULL;
GstElement *src = NULL;
GstElement *sink = NULL;
static gulong gCurrentPosition = 0;
GstBus *bus = NULL;
static guint bus_watch = 0;
GstFormat format = GST_FORMAT_TIME;
gint64 position = 0;
GstEvent *seek_event = NULL;
GstElement *video_sink = NULL;

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
      DESCRIPTION(ERROR, "Error: %s",err->message);
      MESSAGE_END();	
      INCIDENT_TYPE(ERROR);	 	 
            g_error_free (err);

            g_main_loop_quit (loop);
        break;
        default:
            GST_DEBUG ("message_handler. default: %d \n", GST_MESSAGE_TYPE (msg));
            //g_print ("message_handler. default: %d \n", GST_MESSAGE_TYPE (msg));
        break;
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

static void load_playbin_url (GstElement *src, char *record_path)
{
   /*Set the input filename to the source element */
   g_object_set (G_OBJECT (src), "uri", record_path, NULL);
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
	}
	fail_unless (pipeline != NULL, "failed to create pipeline");

    src = gst_element_factory_make ("souphttpsrc", "filesrc"); 
    if (!src)
    {
        GST_DEBUG ("Element source not created\n");
        MESSAGE_START();
        DESCRIPTION(ERROR, "Element source not created");
		MESSAGE_END();
		return ERROR;
    }
    fail_unless (src != NULL, "Failed to create filesrc element");

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

static STATUS load_playbin_elements (GMainLoop *loop, char *record_path)
{

  pipeline= gst_pipeline_new ("player");
  GST_DEBUG ("gst_pipeline_new\n");
  if (!pipeline)
  {
	GST_DEBUG ("pipeline not created\n");
	MESSAGE_START();
    DESCRIPTION(ERROR, "pipeline not created");
	MESSAGE_END();
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
  load_playbin_url (src, record_path);

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

static STATUS playbin_media_state(char *record_path) {
    GMainLoop *loop;

    got_eos = FALSE;
    STATUS res;
    loop = g_main_loop_new (NULL, FALSE);

    load_playbin_elements(loop, record_path);

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

GST_START_TEST (gstVideoRecFuncMp4HttpHosted) {
    char path[SZ_PATH] ;
    char record_path[SZ_PATH];
	STATUS res;
	TESTFUNCTION_START();
    g_print ("\n=========================\n");
    g_sprintf(tcname, __func__);
    g_print ("TestCase: %s\n", tcname) ;
    g_print ("GST_START_TEST: ENTRY. gstVideoRecFuncMp4HttpHosted()\n");

    strcpy ( path, (char *)getenv ("RESRC_PUBLISHER_LINK") );strcat ( path, "/" );strcat ( path, "Test.mp4" );
    g_print ("\n\n **** resource path = %s ***** \n\n", path);

    res = url_check(path);
    if (res == FAIL || res == ERROR)
	{
		INCIDENT_TYPE(res);
		return;
	}

    strcpy ( record_path, (char *)getenv ("OPENSOURCETEST_PATH") );
    strcat ( record_path, "recordings/");
    strcat (record_path, "record.mp4");

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
    g_print ("GST_START_TEST: EXIT. gstVideoRecFuncMp4HttpHosted()\n");
	TESTFUNCTION_END();
}
GST_END_TEST;

GST_START_TEST (gstVideoRecFuncAviHttpHosted) {
    char path[SZ_PATH] ;
    char record_path[SZ_PATH];
	STATUS res;
	TESTFUNCTION_START();
    g_print ("\n=========================\n");
    g_sprintf(tcname, __func__);
    g_print ("TestCase: %s\n", tcname) ;
    g_print ("GST_START_TEST: ENTRY. gstVideoRecFuncAviHttpHosted()\n");

    strcpy ( path, (char *)getenv ("RESRC_PUBLISHER_LINK") );strcat ( path, "/" );strcat ( path, "Test.avi" );
    g_print ("\n\n **** resource path = %s ***** \n\n", path);

    res = url_check(path);
    if (res == FAIL || res == ERROR)
	{
		INCIDENT_TYPE(res);
		return;
	}

    strcpy ( record_path, (char *)getenv ("OPENSOURCETEST_PATH") );
    strcat ( record_path, "recordings/");
    strcat (record_path, "record.avi");

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
    g_print ("GST_START_TEST: EXIT. gstVideoRecFuncAviHttpHosted()\n");
	TESTFUNCTION_END();
}
GST_END_TEST;

GST_START_TEST (gstAudioRecFuncAc3HttpHosted) {
    char path[SZ_PATH] ;
    char record_path[SZ_PATH];
	STATUS res;
	TESTFUNCTION_START();
    g_print ("\n=========================\n");
    g_sprintf(tcname, __func__);
    g_print ("TestCase: %s\n", tcname) ;
    g_print ("GST_START_TEST: ENTRY. gstAudioRecFuncAc3HttpHosted()\n");

    strcpy ( path, (char *)getenv ("RESRC_PUBLISHER_LINK") );strcat ( path, "/" );strcat ( path, "Test.ac3" );
    g_print ("\n\n **** resource path = %s ***** \n\n", path);

    res = url_check(path);
    if (res == FAIL || res == ERROR)
	{
		INCIDENT_TYPE(res);
		return;
	}

    strcpy ( record_path, (char *)getenv ("OPENSOURCETEST_PATH") );
    strcat ( record_path, "recordings/");
    strcat (record_path, "record.ac3");

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
    g_print ("GST_START_TEST: EXIT. gstAudioRecFuncAc3HttpHosted()\n");
	TESTFUNCTION_END();
}
GST_END_TEST;

GST_START_TEST (gstAudioRecFuncAacHttpHosted) {
    char path[SZ_PATH] ;
    char record_path[SZ_PATH];
	STATUS res;
	TESTFUNCTION_START();
    g_print ("\n=========================\n");
    g_sprintf(tcname, __func__);
    g_print ("TestCase: %s\n", tcname) ;
    g_print ("GST_START_TEST: ENTRY. gstAudioRecFuncAacHttpHosted()\n");

    strcpy ( path, (char *)getenv ("RESRC_PUBLISHER_LINK") );strcat ( path, "/" );strcat ( path, "Test.aac" );
    g_print ("\n\n **** resource path = %s ***** \n\n", path);

    res = url_check(path);
    if (res == FAIL || res == ERROR)
	{
		INCIDENT_TYPE(res);
		return;
	}

    strcpy ( record_path, (char *)getenv ("OPENSOURCETEST_PATH") );
    strcat ( record_path, "recordings/");
    strcat (record_path, "record.aac");

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
    g_print ("GST_START_TEST: EXIT. gstAudioRecFuncAacHttpHosted()\n");
	TESTFUNCTION_END();
}
GST_END_TEST;

GST_START_TEST (gstVideoRecFuncM2vHttpHosted) {
    char path[SZ_PATH] ;
    char record_path[SZ_PATH];
	STATUS res;
	TESTFUNCTION_START();
    g_print ("\n=========================\n");
    g_sprintf(tcname, __func__);
    g_print ("TestCase: %s\n", tcname) ;
    g_print ("GST_START_TEST: ENTRY. gstVideoRecFuncM2vHttpHosted()\n");

    strcpy ( path, (char *)getenv ("RESRC_PUBLISHER_LINK") );strcat ( path, "/" );strcat ( path, "Test.m2v" );
    g_print ("\n\n **** resource path = %s ***** \n\n", path);

    res = url_check(path);
    if (res == FAIL || res == ERROR)
	{
		INCIDENT_TYPE(res);
		return;
	}

    strcpy ( record_path, (char *)getenv ("OPENSOURCETEST_PATH") );
    strcat ( record_path, "recordings/");
    strcat (record_path, "record.m2v");

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
    g_print ("GST_START_TEST: EXIT. gstVideoRecFuncM2vHttpHosted()\n");
	TESTFUNCTION_END();
}
GST_END_TEST;

GST_START_TEST (gstAudioRecFuncMp3HttpHosted) {
    char path[SZ_PATH] ;
    char record_path[SZ_PATH];
	STATUS res;
	TESTFUNCTION_START();
    g_print ("\n=========================\n");
    g_sprintf(tcname, __func__);
    g_print ("TestCase: %s\n", tcname) ;
    g_print ("GST_START_TEST: ENTRY. gstAudioRecFuncMp3HttpHosted()\n");

    strcpy ( path, (char *)getenv ("RESRC_PUBLISHER_LINK") );strcat ( path, "/" );strcat ( path, "Test.mp3" );
    g_print ("\n\n **** resource path = %s ***** \n\n", path);

    res = url_check(path);
    if (res == FAIL || res == ERROR)
	{
		INCIDENT_TYPE(res);
		return;
	}

    strcpy ( record_path, (char *)getenv ("OPENSOURCETEST_PATH") );
    strcat ( record_path, "recordings/");
    strcat (record_path, "record.mp3");

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
    g_print ("GST_START_TEST: EXIT. gstAudioRecFuncMp3HttpHosted()\n");
	TESTFUNCTION_END();
}
GST_END_TEST;

GST_START_TEST (gstAudioRecFuncMkaHttpHosted) {
    char path[SZ_PATH] ;
    char record_path[SZ_PATH];
	STATUS res;
	TESTFUNCTION_START();
    g_print ("\n=========================\n");
    g_sprintf(tcname, __func__);
    g_print ("TestCase: %s\n", tcname) ;
    g_print ("GST_START_TEST: ENTRY. gstAudioRecFuncMkaHttpHosted()\n");

    strcpy ( path, (char *)getenv ("RESRC_PUBLISHER_LINK") );strcat ( path, "/" );strcat ( path, "Test.mka" );
    g_print ("\n\n **** resource path = %s ***** \n\n", path);

    res = url_check(path);
    if (res == FAIL || res == ERROR)
	{
		INCIDENT_TYPE(res);
		return;
	}

    strcpy ( record_path, (char *)getenv ("OPENSOURCETEST_PATH") );
    strcat ( record_path, "recordings/");
    strcat (record_path, "record.mka");

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
    g_print ("GST_START_TEST: EXIT. gstAudioRecFuncMkaHttpHosted()\n");
	TESTFUNCTION_END();
}
GST_END_TEST;

GST_START_TEST (gstVideoRecFuncHttpMP4) {
    char resources_path [] = "http://clips.vorwaerts-gmbh.de/big_buck_bunny.mp4";
    char record_path[SZ_PATH];
	STATUS res;
	TESTFUNCTION_START();
    g_print ("\n=========================\n");
    g_sprintf(tcname, __func__);
    g_print ("TestCase: %s\n", tcname) ;
    g_print ("GST_START_TEST: ENTRY. gstVideoRecFuncHttpMP4()\n");

    strcpy ( record_path, (char *)getenv ("OPENSOURCETEST_PATH") );
    strcat ( record_path, "recordings/");
    strcat (record_path, "record_http.mp4");

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
    g_print ("GST_START_TEST: EXIT. gstVideoRecFuncHttpMP4()\n");
	TESTFUNCTION_END();
}
GST_END_TEST;

GST_START_TEST (gstPlayRecStreamsHttpHosted) {
    int file_count = 0;
    int i;
    struct direct **files;
    DIR * dirp;
    struct dirent * entry;
    char path[SZ_PATH];
    char record_path[SZ_PATH];
	STATUS res;
	TESTFUNCTION_START();
    g_print ("\n=========================\n");
    g_sprintf(tcname, __func__);
    g_print ("TestCase: %s\n", tcname) ;
    g_print ("GST_START_TEST: ENTRY. gstPlayRecStreamsHttpHosted()\n");

    strcpy ( path, (char *)getenv ("OPENSOURCETEST_PATH") );
    strcat ( path, "/" );strcat ( path, "recordings/");
    
    dirp = opendir(path);       
    while ((entry = readdir(dirp)) != NULL) {
    if (entry->d_type == DT_REG)       /* If the entry is a regular file */
    { 
         g_print ("File name :%s\n", entry->d_name);

         strcat ( path, entry->d_name);
         strcpy ( record_path, "file://");
         strcat ( record_path, path );
         g_print("Path of the record file is %s \n", record_path);

         res = playbin_media_state(record_path);
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
         file_count++;
    }
         strcpy ( path, (char *)getenv ("OPENSOURCETEST_PATH") );
         strcat ( path, "/" );strcat ( path, "recordings/");
    }

	printf("Number of files played= %d \n",file_count);

	closedir(dirp);
    g_print ("GST_START_TEST: EXIT. gstPlayRecStreamsHttpHosted()\n");
	TESTFUNCTION_END();
}
GST_END_TEST;

static Suite *
media_testsuite (void) {
    Suite *s ;
    TCase *tc_chain ;
    int timeoutvalue = 300;

    GST_DEBUG ("Gstreamer_Recording_Feature_testsuite(): ENTRY.()\n");

    s = suite_create ("mediasuite");
    tc_chain = tcase_create ("mediachain");

    tcase_set_timeout (tc_chain, timeoutvalue);

    GST_DEBUG ("media_suite():timeoutvalue = %d\n", timeoutvalue);
    suite_add_tcase (s, tc_chain);

    tcase_add_test (tc_chain, gstVideoRecFuncMp4HttpHosted);
    tcase_add_test (tc_chain, gstVideoRecFuncAviHttpHosted);
    tcase_add_test (tc_chain, gstAudioRecFuncAc3HttpHosted);
    //tcase_add_test (tc_chain, gstAudioRecFuncAacHttpHosted);
    tcase_add_test (tc_chain, gstVideoRecFuncM2vHttpHosted);
    tcase_add_test (tc_chain, gstAudioRecFuncMp3HttpHosted);
    //tcase_add_test (tc_chain, gstAudioRecFuncMkaHttpHosted);
    tcase_add_test (tc_chain, gstVideoRecFuncHttpMP4);
    tcase_add_test (tc_chain, gstPlayRecStreamsHttpHosted);
    

    GST_DEBUG ("Gstreamer_Recording_Feature_testsuite(): EXIT.()\n");

    return s;
}


int
main (int argc, char **argv) {
    int nf;
    Suite *s;
    SRunner *sr;

    g_print("Gstreamer_Recording_Feature_HttpHosted\n");
    GST_DEBUG ("main(): ENTRY.()\n");
    XML_START();
	TESTCASE_START("Gstreamer_Recording_Feature_HttpHosted");
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
