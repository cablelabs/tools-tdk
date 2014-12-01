/* GStreamer
 *
 * unit test for Audio playback

/*Testcase for media playback using different audio streams
  audio streams-mp3,flac,ac3,wav,wma,aac,mka,ogg
*/

#ifdef HAVE_CONFIG_H
# include <config.h>
#endif
#include <gst/check/gstcheck.h>
#include <unistd.h>
#include <stdio.h>
#include <sys/wait.h>
#include "common/gstplayback.h"

#define SZ_RESOURCE_PATH 200
#define SZ_PATH 200
#define SZ_TCNAME 50
static char tcname[SZ_TCNAME] ;

//static gboolean got_eos = FALSE;
GstElement *pipeline;
GstElement *src;
static gulong gCurrentPosition = 0;
GstBus *bus;
GstFormat format = GST_FORMAT_TIME;
gint64 position;
static guint bus_watch = 0;
GstEvent *seek_event;
GstElement *audio_sink;
typedef enum {
  GST_PLAY_FLAG_VIDEO                = 0x1,
  GST_PLAY_FLAG_AUDIO                = 0x2,
  GST_PLAY_FLAG_NATIVE_VIDEO         = 0x20,
  GST_PLAY_FLAG_NATIVE_AUDIO         = 0x40,
  GST_PLAY_FLAG_BUFFER_AFTER_DEMUX   = 0x100
} GstPlayFlags;

static gboolean
message_handler (GstBus * bus, GstMessage * msg, gpointer data)
{
	GMainLoop *loop = (GMainLoop *) data;
	gchar *debug;
	GError *err;

	GST_DEBUG ("message_handler(). ENTRY \n");

	switch (GST_MESSAGE_TYPE (msg)) {
		case GST_MESSAGE_EOS:
			GST_DEBUG ("message_handler. GST_MESSAGE_EOS: %d \n", GST_MESSAGE_TYPE (msg) );
			GST_DEBUG ("Playback successful \n");
			g_print ("End of stream\n");
			//got_eos = TRUE;
			g_main_loop_quit (loop);
		break;
	  
		case GST_MESSAGE_ERROR:   {
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
		}
		default:
			GST_DEBUG ("message_handler. default: %d \n", GST_MESSAGE_TYPE (msg));
		break;
	}


	GST_DEBUG ("message_handler(). EXIT \n");

	return TRUE;
}

static void load_url (GstElement *src, char *path)
{
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
	flags = GST_PLAY_FLAG_VIDEO | GST_PLAY_FLAG_AUDIO | GST_PLAY_FLAG_NATIVE_VIDEO | GST_PLAY_FLAG_NATIVE_AUDIO;
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

static STATUS media_state(char *path)
{

	GMainLoop *loop;
	//got_eos = FALSE;
	STATUS res;
	loop = g_main_loop_new (NULL, FALSE);

	res = load_elements(loop, path);
	if(res == ERROR)
		return ERROR;	
   
    res = mplayer_null(&pipeline);
	if(res == FAIL)
		return FAIL;
    res = mplayer_ready(&pipeline);
	if(res == FAIL)
		return FAIL;
    res = mplayer_pause(&pipeline);
	if(res == FAIL)
		return FAIL;	
    res = mplayer_play(&pipeline);
	if(res == FAIL)
		return FAIL;

	g_main_loop_run (loop);
	GST_DEBUG ("gst_element_set_state. g_main_loop_run\n");

	/*fail_unless (got_eos);
	GST_DEBUG ("got_eos. %d\n", got_eos);

	got_eos = FALSE;
	GST_DEBUG ("got_eos. %d\n", got_eos);*/

 	sleep(5);

	res = mplayer_stop(&pipeline);
	if(res == FAIL)
		return FAIL;	

	g_main_loop_unref (loop);
	GST_DEBUG ("g_main_loop_unref.\n");  

	g_source_remove (bus_watch);
	GST_DEBUG ("g_source_remove.\n");  
	
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

GST_START_TEST (gstImageFuncJpegHttpHosted){
    char path[SZ_PATH] ;
	STATUS res;
	TESTFUNCTION_START();	
    g_printf ("\n=========================\n");
    g_sprintf(tcname, __func__);
    g_print ("TestCase: %s\n", tcname) ;
    g_print ("GST_START_TEST: ENTRY. gstImageFuncJpegHttpHosted()\n");

    strcpy ( path, (char *)getenv ("RESRC_PUBLISHER_LINK") );strcat ( path, "/" );strcat ( path, "Test.jpeg" );
    g_print ("\n\n **** resource path = %s ***** \\n", path);

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

GST_START_TEST (gstImageFuncPngHttpHosted){
    char path[SZ_PATH] ;
	STATUS res;
	TESTFUNCTION_START();
    g_printf ("\n=========================\n");
    g_sprintf(tcname, __func__);
    g_print ("TestCase: %s\n", tcname) ;
    g_print ("GST_START_TEST: ENTRY. gstImageFuncPngHttpHosted()\n");
    strcpy ( path, (char *)getenv ("RESRC_PUBLISHER_LINK") );strcat ( path, "/" );strcat ( path, "Test.png" );
    g_print ("\n\n **** resource path = %s ***** \\n", path);

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


GST_START_TEST (gstImageFuncGifHttpHosted)
{	
    char path[SZ_PATH] ;
	STATUS res;
	TESTFUNCTION_START();
    g_printf ("\n=========================\n");
    g_sprintf(tcname, __func__);
    g_print ("TestCase: %s\n", tcname) ;
    g_print ("GST_START_TEST: ENTRY. gstImageFuncGifHttpHosted()\n");
    strcpy ( path, (char *)getenv ("RESRC_PUBLISHER_LINK") );strcat ( path, "/" );strcat ( path, "Test.gif" );
    g_print ("\n\n **** resource path = %s ***** \\n", path);

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

GST_START_TEST (gstImageFuncBmpHttpHosted)
{
    char path[SZ_PATH] ;
	STATUS res;
	TESTFUNCTION_START();	
    g_printf ("\n=========================\n");
    g_sprintf(tcname, __func__);
    g_print ("TestCase: %s\n", tcname) ;
    g_print ("GST_START_TEST: ENTRY. gstImageFuncBmpHttpHosted()\n");
    strcpy ( path, (char *)getenv ("RESRC_PUBLISHER_LINK") );strcat ( path, "/" );strcat ( path, "Test.bmp" );
    g_print ("\n\n **** resource path = %s ***** \\n", path);

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

GST_START_TEST (gstImageFuncTiffHttpHosted)
{	
    char path[SZ_PATH] ;
	STATUS res;
	TESTFUNCTION_START();	
    g_printf ("\n=========================\n");
    g_sprintf(tcname, __func__);
    g_print ("TestCase: %s\n", tcname) ;
    g_print ("GST_START_TEST: ENTRY. gstImageFuncTiffHttpHosted()\n");
    strcpy ( path, (char *)getenv ("RESRC_PUBLISHER_LINK") );strcat ( path, "/" );strcat ( path, "Test.tiff" );
    g_print ("\n\n **** resource path = %s ***** \\n", path);

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

GST_START_TEST (gstImageFuncXcfHttpHosted)
{
    char path[SZ_PATH] ;
	STATUS res;
	TESTFUNCTION_START();	
    g_printf ("\n=========================\n");
    g_sprintf(tcname, __func__);
    g_print ("TestCase: %s\n", tcname) ;
    g_print ("GST_START_TEST: ENTRY. gstImageFuncXcfHttpHosted()\n");
    strcpy ( path, (char *)getenv ("RESRC_PUBLISHER_LINK") );strcat ( path, "/" );strcat ( path, "Test.xcf" );
    g_print ("\n\n **** resource path = %s ***** \\n", path);

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

GST_START_TEST (gstImageFuncMngHttpHosted)
{
    char path[SZ_PATH] ;
	STATUS res;
	TESTFUNCTION_START();	
    g_printf ("\n=========================\n");
    g_sprintf(tcname, __func__);
    g_print ("TestCase: %s\n", tcname) ;
    g_print ("GST_START_TEST: ENTRY. gstImageFuncMngHttpHosted()\n");
    strcpy ( path, (char *)getenv ("RESRC_PUBLISHER_LINK") );strcat ( path, "/" );strcat ( path, "Test.mng" );
    g_print ("\n\n **** resource path = %s ***** \\n", path);

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

GST_START_TEST (gstImageFuncJngHttpHosted)
{
    char path[SZ_PATH] ;
	STATUS res;
	TESTFUNCTION_START();	
    g_printf ("\n=========================\n");
    g_sprintf(tcname, __func__);
    g_print ("TestCase: %s\n", tcname) ;
    g_print ("GST_START_TEST: ENTRY. gstImageFuncJngHttpHosted()\n");
    strcpy ( path, (char *)getenv ("RESRC_PUBLISHER_LINK") );strcat ( path, "/" );strcat ( path, "Test.jng" );
    g_print ("\n\n **** resource path = %s ***** \\n", path);

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

GST_START_TEST (gstImageFuncXpmHttpHosted)
{	
    char path[SZ_PATH] ;
	STATUS res;
	TESTFUNCTION_START();	
    g_printf ("\n=========================\n");
    g_sprintf(tcname, __func__);
    g_print ("TestCase: %s\n", tcname) ;
    g_print ("GST_START_TEST: ENTRY. gstImageFuncXpmHttpHosted()\n");
    strcpy ( path, (char *)getenv ("RESRC_PUBLISHER_LINK") );strcat ( path, "/" );strcat ( path, "Test.xpm" );
    g_print ("\n\n **** resource path = %s ***** \\n", path);

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

GST_START_TEST (gstImageFuncRasHttpHosted)
{	
    char path[SZ_PATH] ;
	STATUS res;
	TESTFUNCTION_START();	
    g_printf ("\n=========================\n");
    g_sprintf(tcname, __func__);
    g_print ("TestCase: %s\n", tcname) ;
    g_print ("GST_START_TEST: ENTRY. gstImageFuncRasHttpHosted()\n");
    strcpy ( path, (char *)getenv ("RESRC_PUBLISHER_LINK") );strcat ( path, "/" );strcat ( path, "Test.ras" );
    g_print ("\n\n **** resource path = %s ***** \\n", path);

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

GST_START_TEST (gstImageFuncPsdHttpHosted)
{
    char path[SZ_PATH] ;
	STATUS res;
	TESTFUNCTION_START();	
    g_printf ("\n=========================\n");
    g_sprintf(tcname, __func__);
    g_print ("TestCase: %s\n", tcname) ;
    g_print ("GST_START_TEST: ENTRY. gstImageFuncPsdHttpHosted()\n");
    strcpy ( path, (char *)getenv ("RESRC_PUBLISHER_LINK") );strcat ( path, "/" );strcat ( path, "Test.psd" );
    g_print ("\n\n **** resource path = %s ***** \\n", path);

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

GST_START_TEST (gstImageFuncPpmHttpHosted)
{	
    char path[SZ_PATH] ;
	STATUS res;
	TESTFUNCTION_START();	
    g_printf ("\n=========================\n");
    g_sprintf(tcname, __func__);
    g_print ("TestCase: %s\n", tcname) ;
    g_print ("GST_START_TEST: ENTRY. gstImageFuncPpmHttpHosted()\n");
    strcpy ( path, (char *)getenv ("RESRC_PUBLISHER_LINK") );strcat ( path, "/" );strcat ( path, "Test.ppm" );
    g_print ("\n\n **** resource path = %s ***** \\n", path);

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

GST_START_TEST (gstImageFuncJp2HttpHosted)
{	
    char path[SZ_PATH] ;
	STATUS res;
	TESTFUNCTION_START();	
    g_printf ("\n=========================\n");
    g_sprintf(tcname, __func__);
    g_print ("TestCase: %s\n", tcname) ;
    g_print ("GST_START_TEST: ENTRY. gstImageFuncJp2HttpHosted()\n");
    strcpy ( path, (char *)getenv ("RESRC_PUBLISHER_LINK") );strcat ( path, "/" );strcat ( path, "Test.jp2" );
    g_print ("\n\n **** resource path = %s ***** \\n", path);

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

GST_START_TEST (gstImageFuncQtifHttpHosted)
{	
    char path[SZ_PATH] ; 
	STATUS res;
	TESTFUNCTION_START();	
    g_printf ("\n=========================\n");
    g_sprintf(tcname, __func__);
    g_print ("TestCase: %s\n", tcname) ;
    g_print ("GST_START_TEST: ENTRY. gstImageFuncQtifHttpHosted()\n");
    strcpy ( path, (char *)getenv ("RESRC_PUBLISHER_LINK") );strcat ( path, "/" );strcat ( path, "Test.qtif" );
    g_print ("\n\n **** resource path = %s ***** \\n", path);

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
media_testsuite (void)
{
	Suite *s ;
	TCase *tc_chain ;   
	int timeoutvalue = 300;

	GST_DEBUG ("Gstreamer_Image_Playback_testsuite(): ENTRY.()\n");

	s = suite_create ("mediasuite");
	tc_chain = tcase_create ("mediachain");
  
	tcase_set_timeout (tc_chain, timeoutvalue);
	GST_DEBUG ("media_suite():timeoutvalue = %d\n", timeoutvalue);

	suite_add_tcase (s, tc_chain);
  
	tcase_add_test (tc_chain, gstImageFuncJpegHttpHosted);
	tcase_add_test (tc_chain, gstImageFuncPngHttpHosted);
	tcase_add_test (tc_chain, gstImageFuncGifHttpHosted);
	tcase_add_test (tc_chain, gstImageFuncBmpHttpHosted);
	tcase_add_test (tc_chain, gstImageFuncTiffHttpHosted);
	tcase_add_test (tc_chain, gstImageFuncXcfHttpHosted);
	tcase_add_test (tc_chain, gstImageFuncMngHttpHosted);
	tcase_add_test (tc_chain, gstImageFuncJngHttpHosted);
	tcase_add_test (tc_chain, gstImageFuncXpmHttpHosted);
	tcase_add_test (tc_chain, gstImageFuncRasHttpHosted);
	tcase_add_test (tc_chain, gstImageFuncPsdHttpHosted);
	tcase_add_test (tc_chain, gstImageFuncPpmHttpHosted);
	tcase_add_test (tc_chain, gstImageFuncJp2HttpHosted);
	tcase_add_test (tc_chain, gstImageFuncQtifHttpHosted);  
  
	GST_DEBUG ("Gstreamer_Image_Playback_testsuite(): EXIT.()\n");
  
	return s;
}

int
main (int argc, char **argv)
{
	int nf;
	Suite *s;
	SRunner *sr;

	g_print("Gstreamer_Image_Playback_HttpHosted\n");
    XML_START();
	TESTCASE_START("Gstreamer_Image_Playback_HttpHosted");
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
