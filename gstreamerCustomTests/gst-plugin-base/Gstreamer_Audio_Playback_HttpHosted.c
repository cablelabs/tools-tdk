/* GStreamer
 *
 * unit test for Audio playback

Testcase for media playback using different audio streams
  audio streams-mp3,flac,ac3,wav,wma,aac,mka,ogg
*/

#ifdef HAVE_CONFIG_H
# include <config.h>
#endif
#include <gst/check/gstcheck.h>
#include <unistd.h>
#include <sys/wait.h>
#include <stdio.h>
#include "common/networkInfo.h"
#include "common/gstplayback.h"

#define SZ_TCNAME 50
#define SZ_RESOURCE_PATH 200
#define SZ_PATH 200
#define BILLION  1000000000L
#define MAX_CMD_LEN 1024
typedef enum {
  GST_PLAY_FLAG_VIDEO                = 0x1,
  GST_PLAY_FLAG_AUDIO                = 0x2,
  GST_PLAY_FLAG_NATIVE_VIDEO         = 0x20,
  GST_PLAY_FLAG_NATIVE_AUDIO         = 0x40,
  GST_PLAY_FLAG_BUFFER_AFTER_DEMUX   = 0x100        
} GstPlayFlags;

static char tcname[SZ_TCNAME] ;

static gboolean got_eos = FALSE;
GstElement *pipeline = NULL;
GstElement *src = NULL;
double gTotalDuration = 0.0;
GstBus *bus = NULL;
GstFormat format = GST_FORMAT_TIME;
gint64 position=0;
static guint bus_watch = 0;
GstEvent *seek_event = NULL;
GstElement *audio_sink = NULL;
static double sleep_time = 5.0;

struct timespec start_duration, end_duration;
double total_duration_nanosec = 0, total_time_taken = 0, remaining_playback_time = 0,  total_time_paused = 0;
double total_time_seeked = 0, time_taken_to_play_in_seconds = 0;

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
            g_error_free (err);
            g_main_loop_quit (loop);
        break;
        default:
            GST_DEBUG ("message_handler. default: %d \n", GST_MESSAGE_TYPE (msg));
        break;
    }

    GST_DEBUG ("message_handler(). EXIT \n");
    return TRUE;
}



static void load_url (GstElement *src, char *path) {
    /*Set the input filename to the source element */
    g_object_set (G_OBJECT (src), "uri", path, NULL);
    GST_DEBUG ("g_object_set done for location\n");
}

static STATUS load_elements (GMainLoop *loop, char *path) {
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

    fail_unless (got_eos);
    GST_DEBUG ("got_eos. %d\n", got_eos);

    got_eos = FALSE;
    GST_DEBUG ("got_eos. %d\n", got_eos);

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

GST_START_TEST (gstAudioFuncMp3HttpHosted) {
    char path[SZ_PATH] ;
	STATUS res;
	TESTFUNCTION_START();
    g_print ("\n=========================\n");
    g_sprintf(tcname, __func__);
    g_print ("TestCase: %s\n", tcname) ;
    g_print ("GST_START_TEST: ENTRY. gstAudioFuncMp3HttpHosted()\n");

    strcpy ( path, (char *)getenv ("RESRC_PUBLISHER_LINK") );strcat ( path, "/" );strcat ( path, "Test.mp3" );
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

GST_START_TEST (gstAudioFuncAc3HttpHosted) {
    char path[SZ_PATH] ;
	STATUS res;
	TESTFUNCTION_START();
    g_print ("\n=========================\n");
    g_sprintf (tcname, __func__);
    g_print ("TestCase: %s\n", tcname) ;
    g_print ("GST_START_TEST: ENTRY. gstAudioFuncAc3HttpHosted()\n");

    strcpy ( path, (char *)getenv ("RESRC_PUBLISHER_LINK") );strcat ( path, "/" );strcat ( path, "Test.ac3" );
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

GST_START_TEST (gstAudioFuncAacHttpHosted) {
    char path[SZ_PATH] ;
	STATUS res;
	TESTFUNCTION_START();
    g_print ("\n=========================\n");
    g_sprintf(tcname, __func__);
    g_print("TestCase: %s\n", tcname) ;
    g_print ("GST_START_TEST: ENTRY. gstAudioFuncAacHttpHosted()\n");

    strcpy ( path, (char *)getenv ("RESRC_PUBLISHER_LINK") );strcat ( path, "/" );strcat ( path, "Test.aac" );
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

GST_START_TEST (gstAudioFuncMkaHttpHosted) { 
    char path[SZ_PATH] ;
    STATUS res;
	TESTFUNCTION_START();
    g_print ("\n=========================\n");
    g_sprintf(tcname, __func__);
    g_print("TestCase: %s\n", tcname) ;
    g_print ("GST_START_TEST: ENTRY. gstAudioFuncMkaHttpHosted()\n");

    strcpy ( path, (char *)getenv ("RESRC_PUBLISHER_LINK") );strcat ( path, "/" );strcat ( path, "Test.mka" );
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

GST_START_TEST (gstAudioFunc3GPHttpHosted) {
    char path[SZ_PATH] ;
    STATUS res;
	TESTFUNCTION_START();
    g_print ("\n=========================\n");
    g_sprintf (tcname, __func__);
    g_print ("TestCase: %s\n", tcname) ;
    g_print ("GST_START_TEST: ENTRY. gstAudioFunc3GPHttpHosted()\n");

    strcpy ( path, (char *)getenv ("RESRC_PUBLISHER_LINK") );strcat ( path, "/" );strcat ( path, "Test.3GP" );
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

GST_START_TEST (gstAudioFuncPauseHttpHosted) {
    char path[SZ_PATH] ;
    GMainLoop *loop = NULL;
    STATUS res;
	TESTFUNCTION_START();
    g_print ("\n=========================\n");
    g_sprintf(tcname, __func__);
    g_print ("TestCase: %s\n", tcname) ;
    g_print ("GST_START_TEST: ENTRY. gstAudioFuncPauseHttpHosted()\n");

    strcpy ( path, (char *)getenv ("RESRC_PUBLISHER_LINK") );strcat ( path, "/" );strcat ( path, "Test.mp3" );
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
	g_print("Gstreamer audio playback 'pause_audio' functionality testing \n");

    res = mplayer_play(&pipeline);
	if (res == FAIL)
	{
        INCIDENT_TYPE(res);
        TESTFUNCTION_END();
        return;
    }

    if( clock_gettime( CLOCK_REALTIME, &start_duration) == -1 ) {
			MESSAGE_START();
            DESCRIPTION(ERROR, "Error: clock gettime");
			MESSAGE_END();
			INCIDENT_TYPE(ERROR);
            return;
        }

        sleep(sleep_time);

	if( gst_element_query_duration (pipeline, &format, &position) &&
       format == GST_FORMAT_TIME && position != GST_CLOCK_TIME_NONE ) {

       printf("Stream Duration (in ms) : %lld\n", (position/1000000));
       gTotalDuration = (position/1000000000);
       	g_print ("Total Stream Duration=%lf seconds\n", gTotalDuration);
       }


    res = mplayer_pause(&pipeline);
	if (res == FAIL)
	{
        INCIDENT_TYPE(res);
        TESTFUNCTION_END();
        return;
    }
	sleep(3);
    res = mplayer_play(&pipeline);
	if (res == FAIL)
	{
        INCIDENT_TYPE(res);
        TESTFUNCTION_END();
        return;
    }
    sleep(gTotalDuration - sleep_time);

    if( clock_gettime( CLOCK_REALTIME, &end_duration) == -1 ) {
			MESSAGE_START();
            DESCRIPTION(ERROR, "Error: clock gettime");
			MESSAGE_END();
			INCIDENT_TYPE(ERROR);
            return;
    }

    res = mplayer_stop(&pipeline);
	if (res == FAIL)
	{
        INCIDENT_TYPE(res);
        TESTFUNCTION_END();
        return;
    }
    total_duration_nanosec = (end_duration.tv_sec - start_duration.tv_sec ) * (double) BILLION;
    total_time_taken = total_duration_nanosec + (double)(end_duration.tv_nsec - start_duration.tv_nsec);
    time_taken_to_play_in_seconds = total_time_taken/(double) BILLION;
    total_time_paused = time_taken_to_play_in_seconds - gTotalDuration;
    g_print ("total_time_paused=%lf seconds\n\n", total_time_paused);
    if (total_time_paused>=3)
	{
		g_print ("Pause validation success\n");
	}
    else
	{
        g_print ("Pause validation failed\n");
		MESSAGE_START();
        DESCRIPTION(FAIL, "Pause validation failed");
		MESSAGE_END();
        INCIDENT_TYPE(FAIL);
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

GST_START_TEST (gstAudioFuncStopHttpHosted)
{
	GMainLoop *loop = NULL;
    char path[SZ_PATH] ;
    STATUS res;
	TESTFUNCTION_START();
    g_print ("\n=========================\n");
    g_sprintf (tcname, __func__);
    g_print ("TestCase: %s\n", tcname) ;
    g_print ("GST_START_TEST: ENTRY. gstAudioFuncStopHttpHosted()\n");

    strcpy ( path, (char *)getenv ("RESRC_PUBLISHER_LINK") );strcat ( path, "/" );strcat ( path, "Test.mp3" );
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
        return;
    }
	g_print("Gstreamer audio playback 'stop_audio' functionality testing \n");
	res = mplayer_play(&pipeline);
	if (res == FAIL)
	{
        INCIDENT_TYPE(res);
        TESTFUNCTION_END();
        return;
    }
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

GST_START_TEST (gstAudioFuncSeekForwardHttpHosted)
{
	GMainLoop *loop = NULL;
    char path[SZ_PATH] ;
    STATUS res;
	TESTFUNCTION_START();
    g_print ("\n=========================\n");
    g_sprintf(tcname, __func__);
    g_print ("TestCase: %s\n", tcname) ;
    g_print ("GST_START_TEST: ENTRY. gstAudioFuncSeekForwardHttpHosted()\n");

    strcpy ( path, (char *)getenv ("RESRC_PUBLISHER_LINK") );strcat ( path, "/" );strcat ( path, "Test.mp3" );
    g_print ("\n\n **** resource path = %s ***** \n", path);

    res = url_check(path);
    if (res == FAIL || res == ERROR)
	{
		INCIDENT_TYPE(res);
		return;
	}


    loop = g_main_loop_new (NULL, FALSE);
	res = load_elements (loop, path);
    if(res == ERROR)
    {
        INCIDENT_TYPE(res);
        TESTFUNCTION_END();
        return;
    }
	g_print ("Gstreamer audio playback 'seek_forward' functionality testing \n");

	res = mplayer_play(&pipeline);
    if(res == FAIL)
    {
        INCIDENT_TYPE(res);
        TESTFUNCTION_END();
        return;
    }

	sleep(sleep_time);

    gst_element_seek(src,
                         1.0 /*rate*/, /* Currently support only 1x speed during seek */
                         GST_FORMAT_TIME, GST_SEEK_FLAG_FLUSH | GST_SEEK_FLAG_KEY_UNIT,GST_SEEK_TYPE_SET,
                         10000000000,
                         GST_SEEK_TYPE_NONE, 0);


	g_print ("seeking forward from current position to 10 seconds\n");

	time_t start_time = time(NULL);
        printf("Current Time after seeking is %s\n", ctime(&start_time));

        gst_element_query_duration (pipeline, &format, &position);
	gTotalDuration = GST_TIME_AS_SECONDS(position);
	g_print ("Total Stream Duration=%lf seconds\n", gTotalDuration);

	g_main_loop_run(loop);

	time_t end_time = time(NULL);
    printf("Current Time after getting EOS is %s\n", ctime(&end_time));

    res = mplayer_stop(&pipeline);
    if(res == FAIL)
    {
        INCIDENT_TYPE(res);
        TESTFUNCTION_END();
        return;
    }
    g_main_loop_unref (loop);
    GST_DEBUG ("g_main_loop_unref.\n");

    g_source_remove (bus_watch);
    GST_DEBUG ("g_source_remove.\n");

    remaining_playback_time = difftime(end_time,start_time);
    total_time_taken = sleep_time + remaining_playback_time;
    total_time_seeked = (gTotalDuration - total_time_taken) + sleep_time;

        g_print ("seeked forward to %lf seconds\n\n", total_time_seeked);
        if (total_time_seeked>=9 && total_time_seeked<=11)
	{
		g_print ("Seek validation success\n");
	}
    else
	{
        g_print ("Seek validation failed\n");
		MESSAGE_START();
        DESCRIPTION(FAIL, "Seek validation failed");
		MESSAGE_END();
        INCIDENT_TYPE(FAIL);
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

GST_START_TEST (gstAudioFuncSeekBackwardHttpHosted) {
    GMainLoop *loop = NULL;
    char path[SZ_PATH] ;
    STATUS res;
	TESTFUNCTION_START();
    g_print ("\n=========================\n");
    g_sprintf(tcname, __func__);
    g_print ("TestCase: %s\n", tcname) ;
    g_print ("GST_START_TEST: ENTRY. gstAudioFuncSeekBackwardHttpHosted()\n");

    strcpy ( path, (char *)getenv ("RESRC_PUBLISHER_LINK") );strcat ( path, "/" );strcat ( path, "Test.mp3" );
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
    g_print("Gstreamer audio playback 'seek_backward' functionality testing \n");

    mplayer_play(&pipeline);
    if(res == FAIL)
    {
        INCIDENT_TYPE(res);
        TESTFUNCTION_END();
        return;
    }

    if( clock_gettime( CLOCK_REALTIME, &start_duration) == -1 ) {
			MESSAGE_START();
            DESCRIPTION(ERROR, "Error: clock gettime");
			MESSAGE_END();
			INCIDENT_TYPE(ERROR);
            return;
        }
	sleep(10);

    gst_element_seek(src,
                         1.0 /*rate*/, /* Currently support only 1x speed during seek */
                         GST_FORMAT_TIME, GST_SEEK_FLAG_FLUSH | GST_SEEK_FLAG_KEY_UNIT,GST_SEEK_TYPE_SET,
                         5000000000,
                         GST_SEEK_TYPE_NONE, 0);


	g_print ("seeking backward from current position to 5 seconds\n");

        gst_element_query_duration (pipeline, &format, &position);
	gTotalDuration = GST_TIME_AS_SECONDS(position);
	g_print ("Total Stream Duration=%lf seconds\n", gTotalDuration);

	sleep(gTotalDuration - 5.0);

	if( clock_gettime( CLOCK_REALTIME, &end_duration) == -1 ) {
            perror( "clock gettime" );
            return;
            }
        res = mplayer_stop(&pipeline);
	if(res == FAIL)
    {
        INCIDENT_TYPE(res);
        TESTFUNCTION_END();
        return;
    }

        total_duration_nanosec = (end_duration.tv_sec - start_duration.tv_sec ) * (double) BILLION;
        total_time_taken = total_duration_nanosec + (double)(end_duration.tv_nsec - start_duration.tv_nsec);
        time_taken_to_play_in_seconds = total_time_taken/(double) BILLION;
        total_time_seeked = time_taken_to_play_in_seconds - gTotalDuration;
        g_print ("seeked backward to =%lf seconds\n\n", total_time_seeked);
        if (total_time_seeked>=4.5 && total_time_seeked<=6)
	{
		g_print ("Seek validation success\n");
	}
    else
	{
        g_print ("Seek validation failed\n");
		MESSAGE_START();
        DESCRIPTION(FAIL, "Seek validation failed");
		MESSAGE_END();
        INCIDENT_TYPE(FAIL);
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

GST_START_TEST (gstAudioFuncRewindHttpHosted) {
    GMainLoop *loop = NULL;
    char path[SZ_PATH] ;
	STATUS res;
	TESTFUNCTION_START();
    g_print ("\n=========================\n");
    g_sprintf (tcname, __func__);
    g_print ("TestCase: %s\n", tcname) ;
    g_print ("GST_START_TEST: ENTRY. gstAudioFuncRewindHttpHosted()\n");

    strcpy ( path, (char *)getenv ("RESRC_PUBLISHER_LINK") );strcat ( path, "/" );strcat ( path, "Test.mp3" );
    g_print ("\n **** resource path = %s ***** \n", path);

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
	g_print("Gstreamer audio playback 'rewind' functionality testing \n");

	res = mplayer_play(&pipeline);
    if(res == FAIL)
    {
        INCIDENT_TYPE(res);
        TESTFUNCTION_END();
        return;
    }
	sleep(sleep_time);
    
    gst_element_seek(src,
                         1.0 /*rate*/, /* Currently support only 1x speed during seek */
                         GST_FORMAT_TIME, GST_SEEK_FLAG_FLUSH | GST_SEEK_FLAG_KEY_UNIT,GST_SEEK_TYPE_SET,
                         0,
                         GST_SEEK_TYPE_NONE, 0);

    g_print("Rewinded to start position\n");
    res = mplayer_play(&pipeline);
    if(res == FAIL)
    {
        INCIDENT_TYPE(res);
        TESTFUNCTION_END();
        return;
    }
	mplayer_position_update(&pipeline);
	sleep(5);
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

GST_START_TEST (gstAudioFuncUdpStreamingMp3HttpHosted) {
    int script_path_res = 0;
    char script_path[SZ_PATH];
    char path[SZ_PATH] ;
    char command[SZ_PATH+SZ_RESOURCE_PATH];
	STATUS res;
	TESTFUNCTION_START();
    g_print ("\n=========================\n");
    g_sprintf (tcname, __func__);
    g_print ("TestCase: %s\n", tcname) ;
    g_print ("GST_START_TEST: ENTRY. gstVideoFuncUdpStreamingMp3HttpHosted()\n");
    
    strcpy ( path, (char *)getenv ("RESRC_PUBLISHER_LINK") );strcat ( path, "/" );strcat ( path, "Test.mp3" );
    g_print ("\n **** resource path = %s ***** \n", path);
    
    res = url_check(path);
    if (res == FAIL || res == ERROR)
	{
		INCIDENT_TYPE(res);
		return;
	}
	
 
    strcpy ( script_path, (char *)getenv ("OPENSOURCETEST_PATH") );
    strcat ( script_path, "/gst-plugin-base/udp_mp3_receiver");

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
    strcat ( script_path, "/gst-plugin-base/udp_mp3_sender_hosted");

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
    g_print("STB BOX - portName : %s, ipAddr :%s \n", portName, ipAddr); 

    pid_t RXidChild = vfork();

    if(RXidChild == 0)
    {
	   sprintf( AppName,"%s" , "udp_mp3_receiver");
	   sprintf ( AppPath,"%s", (char *)getenv ("OPENSOURCETEST_PATH") );
	   strcat ( AppPath, "/gst-plugin-base/");
	   strcat ( AppPath, AppName );
	   sprintf ( RsrcPath,"%s",  (char *)getenv ("TDKOUTPUT_PATH"));
	   strcat ( RsrcPath, "/resources/udp.mp3");
	   sprintf ( udpPort,"%s", "8888");

	   g_print ("\n RX - AppPath::%s AppName::%s RsrcPath::%s udpPort::%s \n", AppPath,AppName,RsrcPath,udpPort);

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
		   sprintf( AppName,"%s" , "udp_mp3_sender_hosted");
		   sprintf ( AppPath,"%s", (char *)getenv ("OPENSOURCETEST_PATH") );
		   strcat ( AppPath, "/gst-plugin-base/");
		   strcat ( AppPath, AppName );
		   sprintf ( RsrcPath, "%s",  path);
   		   sprintf ( ipAddr, "%s", ipAddr);

		   g_print ("\n TX - AppPath::%s AppName::%s RsrcPath::%s udpPort::%s ipAddr::%s \n", AppPath,AppName,RsrcPath,udpPort, ipAddr);

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

GST_START_TEST (gstAudioFuncUdpStreamingAacHttpHosted) {
    int script_path_res = 0;
    char script_path[SZ_PATH];
    char path[SZ_PATH] ;
    char command[SZ_PATH+SZ_RESOURCE_PATH];
	STATUS res;
	TESTFUNCTION_START();
    g_print ("\n=========================\n");
    g_sprintf (tcname, __func__);
    g_print ("TestCase: %s\n", tcname) ;
    g_print ("GST_START_TEST: ENTRY. gstVideoFuncUdpStreamingAacHttpHosted()\n");
    
    strcpy ( path, (char *)getenv ("RESRC_PUBLISHER_LINK") );strcat ( path, "/" );strcat ( path, "Test.aac" );
    g_print ("\n **** resource path = %s ***** \n", path);
    
    res = url_check(path);
    if (res == FAIL || res == ERROR)
	{
		INCIDENT_TYPE(res);
		return;
	}


    strcpy ( script_path, (char *)getenv ("OPENSOURCETEST_PATH") );
    strcat ( script_path, "/gst-plugin-base/udp_aac_receiver");

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
    strcat ( script_path, "/gst-plugin-base/udp_aac_sender_hosted");

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
    g_print("STB BOX - portName : %s, ipAddr :%s \n", portName, ipAddr); 

    pid_t RXidChild = vfork();

    if(RXidChild == 0)
    {
	   sprintf( AppName,"%s" , "udp_aac_receiver");
	   sprintf ( AppPath,"%s", (char *)getenv ("OPENSOURCETEST_PATH") );
	   strcat ( AppPath, "/gst-plugin-base/");
	   strcat ( AppPath, AppName );
	   sprintf ( RsrcPath,"%s",  (char *)getenv ("TDKOUTPUT_PATH"));
	   strcat ( RsrcPath, "/resources/udp.aac");
	   sprintf ( udpPort,"%s", "8888");

	   g_print ("\n RX - AppPath::%s AppName::%s RsrcPath::%s udpPort::%s \n", AppPath,AppName,RsrcPath,udpPort);

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
		   sprintf( AppName,"%s" , "udp_aac_sender_hosted");
		   sprintf ( AppPath,"%s", (char *)getenv ("OPENSOURCETEST_PATH") );
		   strcat ( AppPath, "/gst-plugin-base/");
		   strcat ( AppPath, AppName );
		   sprintf ( RsrcPath, "%s",  path);
   		   sprintf ( ipAddr, "%s", ipAddr);

		   g_print ("\n TX - AppPath::%s AppName::%s RsrcPath::%s udpPort::%s ipAddr::%s \n", AppPath,AppName,RsrcPath,udpPort, ipAddr);

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

GST_START_TEST (gstAudioFuncUdpStreamingAc3HttpHosted) {
    int script_path_res = 0; 
    char script_path[SZ_PATH];
    char path[SZ_PATH] ;
    char command[SZ_PATH+SZ_RESOURCE_PATH];
	STATUS res;
	TESTFUNCTION_START();
    g_print ("\n=========================\n");
    g_sprintf (tcname, __func__);
    g_print ("TestCase: %s\n", tcname) ;
    g_print ("GST_START_TEST: ENTRY. gstVideoFuncUdpStreamingAc3HttpHosted()\n");
    
    strcpy ( path, (char *)getenv ("RESRC_PUBLISHER_LINK") );strcat ( path, "/" );strcat ( path, "Test.ac3" );
    g_print ("\n **** resource path = %s ***** \n", path);
    
    res = url_check(path);
    if (res == FAIL || res == ERROR)
	{
		INCIDENT_TYPE(res);
		return;
	}


    strcpy ( script_path, (char *)getenv ("OPENSOURCETEST_PATH") );
    strcat ( script_path, "/gst-plugin-base/udp_ac3_receiver");

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
    strcat ( script_path, "/gst-plugin-base/udp_ac3_sender_hosted");

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
    g_print("STB BOX - portName : %s, ipAddr :%s \n", portName, ipAddr); 

    pid_t RXidChild = vfork();

    if(RXidChild == 0)
    {
	   sprintf( AppName,"%s" , "udp_ac3_receiver");
	   sprintf ( AppPath,"%s", (char *)getenv ("OPENSOURCETEST_PATH") );
	   strcat ( AppPath, "/gst-plugin-base/");
	   strcat ( AppPath, AppName );
	   sprintf ( RsrcPath,"%s",  (char *)getenv ("TDKOUTPUT_PATH"));
	   strcat ( RsrcPath, "/resources/udp.ac3");
	   sprintf ( udpPort,"%s", "8888");

	   g_print ("\n RX - AppPath::%s AppName::%s RsrcPath::%s udpPort::%s \n", AppPath,AppName,RsrcPath,udpPort);

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
		   sprintf( AppName,"%s" , "udp_ac3_sender_hosted");
		   sprintf ( AppPath,"%s", (char *)getenv ("OPENSOURCETEST_PATH") );
		   strcat ( AppPath, "/gst-plugin-base/");
		   strcat ( AppPath, AppName );
		   sprintf ( RsrcPath, "%s",  path);
   		   sprintf ( ipAddr, "%s", ipAddr);

		   g_print ("\n TX - AppPath::%s AppName::%s RsrcPath::%s udpPort::%s ipAddr::%s \n", AppPath,AppName,RsrcPath,udpPort, ipAddr);

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

static Suite *
media_testsuite (void) {
    Suite *s ;
    TCase *tc_chain ;
    int timeoutvalue = 300;

    GST_DEBUG ("Gstreamer_Audio_Playback_HttpHosted_testsuite(): ENTRY.()\n");

    s = suite_create ("mediasuite");
    tc_chain = tcase_create ("mediachain");

    tcase_set_timeout (tc_chain, timeoutvalue);
    GST_DEBUG ("media_suite():timeoutvalue = %d\n", timeoutvalue);

    suite_add_tcase (s, tc_chain);

//    tcase_add_test (tc_chain, gstAudioFuncMp3HttpHosted);
    tcase_add_test (tc_chain, gstAudioFuncAc3HttpHosted);
    tcase_add_test (tc_chain, gstAudioFuncAacHttpHosted);
    tcase_add_test (tc_chain, gstAudioFuncMkaHttpHosted);
    tcase_add_test (tc_chain, gstAudioFunc3GPHttpHosted);
    tcase_add_test (tc_chain, gstAudioFuncPauseHttpHosted);
    tcase_add_test (tc_chain, gstAudioFuncStopHttpHosted);
    tcase_add_test (tc_chain, gstAudioFuncSeekForwardHttpHosted);
    tcase_add_test (tc_chain, gstAudioFuncSeekBackwardHttpHosted);
    tcase_add_test (tc_chain, gstAudioFuncRewindHttpHosted);
    tcase_add_test (tc_chain, gstAudioFuncUdpStreamingMp3HttpHosted);
    tcase_add_test (tc_chain, gstAudioFuncUdpStreamingAacHttpHosted);
    tcase_add_test (tc_chain, gstAudioFuncUdpStreamingAc3HttpHosted);

    GST_DEBUG ("Gstreamer_Audio_Playback_HttpHosted_testsuite(): EXIT.()\n");

    return s;
}

int
main (int argc, char **argv) {
    int nf;
    Suite *s;
    SRunner *sr;

    g_print("Gstreamer_Audio_Playback_HttpHosted\n");
    GST_DEBUG ("main(): ENTRY.()\n");
    XML_START();
	TESTCASE_START("Gstreamer_Audio_Playback_HttpHosted");
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
