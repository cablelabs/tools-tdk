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

static char tcname[SZ_TCNAME];
struct timespec clock_before_pipeline_creation, clock_after_pipeline_creation, clock_at_play_event, clock_at_play_command;

GstElement *pipeline, *playbin;
GstBus *bus;

typedef enum {
  GST_PLAY_FLAG_VIDEO                = 0x1,
  GST_PLAY_FLAG_AUDIO                = 0x2,
  GST_PLAY_FLAG_NATIVE_VIDEO         = 0x20,
  GST_PLAY_FLAG_NATIVE_AUDIO         = 0x40,
  GST_PLAY_FLAG_BUFFER_AFTER_DEMUX   = 0x100        
} GstPlayFlags;

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
                    perror( "clock gettime" );
              }
                 sleep(1);
                 g_main_loop_quit (loop);
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
  pipeline = gst_pipeline_new ("audio-player");
  playbin = gst_element_factory_make ("playbin2", "playbin");

  if (!pipeline || !playbin)
  {
	    MESSAGE_START();
        DESCRIPTION(ERROR, "Error: One element could not be created. Exiting");
		MESSAGE_END();
        return ERROR;
  }

  /* Set up the pipeline */
  g_print ("Elements are created\n");
  
  /* set the properties of other elements */
  g_object_set (G_OBJECT (playbin), "uri",  path, NULL);
 
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

  return PASS;

}

STATUS perf_time_taken_pipe_creatn(char *path)
{
   g_print ("ENTRY : %s function\n", __func__);

   GMainLoop *loop = NULL;
   double pipeline_creation_time = 0.0;
   STATUS testresult;   

  /*Measuring time before creating pipeline */
  if( clock_gettime( CLOCK_REALTIME, &clock_before_pipeline_creation) == -1 ) {
 		MESSAGE_START();
        DESCRIPTION(ERROR, "Error: clock gettime");
	   	MESSAGE_END();
        return ERROR;
  }

  testresult = create_pipeline (path, loop);
    if(testresult == ERROR)
        return ERROR;
    else if (testresult == FAIL)
        return FAIL;
		
  /*Measuring time after creating pipeline */
  if( clock_gettime( CLOCK_REALTIME, &clock_after_pipeline_creation) == -1 ) {
 		MESSAGE_START();
        DESCRIPTION(ERROR, "Error: clock gettime");
	   	MESSAGE_END();
        return ERROR;
  }

  /* time measurements */
  pipeline_creation_time = ( clock_after_pipeline_creation.tv_sec - clock_before_pipeline_creation.tv_sec )
                           + (double)( clock_after_pipeline_creation.tv_nsec - clock_before_pipeline_creation.tv_nsec ) / (double)BILLION;

 	MESSAGE_START();
	DESCRIPTION(CHECKS, "First time -Time Taken for creation of pipeline :: %lf ms\n", pipeline_creation_time * MSEC);
	MESSAGE_END();


    /*destroy pipeline*/
    testresult = destroy_pipeline ();
    if(testresult == ERROR)
        return ERROR;
    else if (testresult == FAIL)
        return FAIL;
    g_print ("EXIT : %s function\n", __func__);

    return PASS;
}

STATUS perf_time_taken_pipe_creatn_iter(char *path)
{
   GMainLoop *loop = NULL;
   double pipeline_creation_time = 0.0;
   //struct timespec clock_before_pipeline_creation, clock_after_pipeline_creation;
   int count = 0;
   double sumof_pipeline_creation_time = 0.0;
    STATUS testresult;   

   g_print ("ENTRY : %s function\n", __func__);

   while(count <= NUMBER_OF_ITERATION) {
   pipeline_creation_time = 0.0;
   loop = NULL;

  /*Measuring time before creating pipeline */
  if( clock_gettime( CLOCK_REALTIME, &clock_before_pipeline_creation) == -1 ) {
            MESSAGE_START();
            DESCRIPTION(ERROR, "Error: clock gettime");
	   		MESSAGE_END();
            return ERROR;
  }

  testresult = create_pipeline (path, loop);

  /*Measuring time after creating pipeline */
  if( clock_gettime( CLOCK_REALTIME, &clock_after_pipeline_creation) == -1 ) {
            MESSAGE_START();
            DESCRIPTION(ERROR, "Error: clock gettime");
	   		MESSAGE_END();
            return ERROR;
  }

  /* time measurements */
  pipeline_creation_time = ( clock_after_pipeline_creation.tv_sec - clock_before_pipeline_creation.tv_sec )
                           + (double)( clock_after_pipeline_creation.tv_nsec - clock_before_pipeline_creation.tv_nsec ) / (double)BILLION;


  if (count != 0) {
     sumof_pipeline_creation_time += pipeline_creation_time;
     g_print (" Time Taken for creation of pipeline = %lf seconds\n", pipeline_creation_time);
     g_print (" Sum of Time Taken for creation of pipeline = %lf seconds\n", sumof_pipeline_creation_time);
  } else {
     g_print (" First time -Time Taken for creation of pipeline = %lf seconds\n", pipeline_creation_time);
     }

        /*destroy pipeline*/
        testresult = destroy_pipeline ();
        if(testresult == ERROR)
            return ERROR;
        else if (testresult == FAIL)
            return FAIL;

  count++;
  g_print("Count = %d\n",count);
  if (count > NUMBER_OF_ITERATION)
             break;
   }
    MESSAGE_START();   
    DESCRIPTION(CHECKS, "Average over %d times - Time Taken for creation of pipeline :: %lf ms\n", NUMBER_OF_ITERATION, (sumof_pipeline_creation_time/NUMBER_OF_ITERATION) * MSEC);
    MESSAGE_END();
    g_print ("EXIT : %s function\n", __func__);

    return PASS;
}


STATUS perf_time_taken_audio_play (char *path)
{
  g_print ("ENTRY : %s function\n", __func__);

  GMainLoop *loop;
  double audio_start_delay=0.0;
  STATUS testresult;
  
  loop = g_main_loop_new (NULL, FALSE);

  testresult = create_pipeline (path, loop);
    if(testresult == ERROR)
        return ERROR;
    else if (testresult == FAIL)
        return FAIL;  

  /* Set the pipeline to "playing" state*/
  g_print ("Playing the audio\n");
	if (GST_STATE_CHANGE_FAILURE == gst_element_set_state(GST_ELEMENT(pipeline), GST_STATE_PLAYING))
	{
        GST_DEBUG ("Failed to PLAY\n");
        MESSAGE_START();
        DESCRIPTION(FAIL, "Fail: Pipeline not set to PLAYING. Exiting.");
        MESSAGE_END();
        return FAIL;
	}

  if( clock_gettime( CLOCK_REALTIME, &clock_at_play_command) == -1 ) {
        MESSAGE_START();
        DESCRIPTION(ERROR, "Error: clock gettime");
	   	MESSAGE_END();
        return ERROR;
  }

  /* Iterate */
  g_print ("Running...\n");
  g_main_loop_run (loop);

  audio_start_delay = ( clock_at_play_event.tv_sec - clock_at_play_command.tv_sec )
                                                + (double)( clock_at_play_event.tv_nsec - clock_at_play_command.tv_nsec ) / (double)BILLION;

	MESSAGE_START();
    DESCRIPTION(CHECKS, "First time - Time Taken for audio playing :: %lf ms\n", audio_start_delay * MSEC);
    MESSAGE_END();

	/*destroy pipeline*/
    testresult = destroy_pipeline ();
    if(testresult == ERROR)
        return ERROR;
    else if (testresult == FAIL)
        return FAIL;
    g_print ("EXIT : %s function\n", __func__);

    return PASS;
}

STATUS perf_time_taken_audio_play_iter (char *path)
{
  GMainLoop *loop;
  double audio_start_delay=0.0;
  //struct timespec clock_at_play_command;
  double sumof_audio_start_delay = 0.0;
  int count = 0;
    STATUS testresult;  

  g_print ("ENTRY : %s function\n", __func__);

  while(count <= NUMBER_OF_ITERATION) {
  audio_start_delay=0.0;
  loop = g_main_loop_new (NULL, FALSE);

  testresult = create_pipeline (path, loop);
        if(testresult == ERROR)
            return ERROR;
        else if (testresult == FAIL)
            return FAIL;  

  /* Set the pipeline to "playing" state*/
  g_print ("Playing the audio\n");
	if (GST_STATE_CHANGE_FAILURE == gst_element_set_state(GST_ELEMENT(pipeline), GST_STATE_PLAYING))
	{
        GST_DEBUG ("Failed to PLAY\n");
        MESSAGE_START();
        DESCRIPTION(FAIL, "Fail: Pipeline not set to PLAYING. Exiting.");
        MESSAGE_END();
        return FAIL;
	}

  if( clock_gettime( CLOCK_REALTIME, &clock_at_play_command) == -1 ) {
            MESSAGE_START();
            DESCRIPTION(ERROR, "Error: clock gettime");
            MESSAGE_END();
            return ERROR;
  }

  /* Iterate */
  g_print ("Running...\n");
  g_main_loop_run (loop);

  audio_start_delay = ( clock_at_play_event.tv_sec - clock_at_play_command.tv_sec )
                                                + (double)( clock_at_play_event.tv_nsec - clock_at_play_command.tv_nsec ) / (double)BILLION;

  if (count != 0) {
        sumof_audio_start_delay += audio_start_delay;
        g_print (" Time Taken for audio playing = %lf seconds\n", audio_start_delay);
        g_print (" Sum of Time Taken for audio playing = %lf seconds\n", sumof_audio_start_delay);
  } else {
        g_print (" First time - Time Taken for audio playing = %lf seconds\n", audio_start_delay);
  }

        /*destroy pipeline*/
        testresult = destroy_pipeline ();
        if(testresult == ERROR)
            return ERROR;
        else if (testresult == FAIL)
            return FAIL;

  count++;
  g_print("Count = %d\n",count);
  if (count > NUMBER_OF_ITERATION)
             break;
  }
    MESSAGE_START();
    DESCRIPTION(CHECKS, "Average over %d times - Time Taken for audio playing :: %lf ms\n", NUMBER_OF_ITERATION, (sumof_audio_start_delay/NUMBER_OF_ITERATION) * MSEC);
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

GST_START_TEST (gstAudioPerfMp3CreatingPipelineHttpHosted)
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
    g_print ("GST_START_TEST: ENTRY. gstAudioPerfMp3CreatingPipelineHttpHosted()\n");

    strcpy ( path, (char *)getenv ("RESRC_PUBLISHER_LINK") );strcat ( path, "/" );strcat ( path, "Test.mp3" );
    g_print ("\n\n **** resources path = %s ***** \n", path);

    res = url_check(path);
    if (res == FAIL || res == ERROR)
	{
		INCIDENT_TYPE(res);
		return;
	}
	
    res = perf_time_taken_pipe_creatn(path);
	INCIDENT_TYPE(res);

    g_print ("GST_START_TEST: EXIT. %s\n", __func__);
	TESTFUNCTION_END();

}
GST_END_TEST;

GST_START_TEST (gstAudioPerfMp3PlayHttpHosted)
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
    g_print ("GST_START_TEST: ENTRY. gstAudioPerfMp3PlayHttpHosted()\n");

    strcpy ( path, (char *)getenv ("RESRC_PUBLISHER_LINK") );strcat ( path, "/" );strcat ( path, "Test.mp3" );
    g_print ("\n\n **** resources path = %s ***** \n", path);

    res = url_check(path);
    if (res == FAIL || res == ERROR)
	{
		INCIDENT_TYPE(res);
		return;
	}

    res = perf_time_taken_audio_play(path);

	INCIDENT_TYPE(res);

    g_print ("GST_START_TEST: EXIT. %s\n", __func__);
	TESTFUNCTION_END();

}
GST_END_TEST;

GST_START_TEST (gstAudioPerfAc3CreatingPipelineHttpHosted)
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
    g_print ("GST_START_TEST: ENTRY. gstAudioPerfAc3CreatingPipelineHttpHosted()\n");

    strcpy ( path, (char *)getenv ("RESRC_PUBLISHER_LINK") );strcat ( path, "/" );strcat ( path, "Test.ac3" );
    g_print ("\n\n **** resources path = %s ***** \n", path);

    res = url_check(path);
    if (res == FAIL || res == ERROR)
	{
		INCIDENT_TYPE(res);
		return;
	}

    res = perf_time_taken_pipe_creatn(path);
	INCIDENT_TYPE(res);

    g_print ("GST_START_TEST: EXIT. %s\n", __func__);
	TESTFUNCTION_END();

}
GST_END_TEST;

GST_START_TEST (gstAudioPerfAc3PlayHttpHosted)
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
    g_print ("GST_START_TEST: ENTRY. gstAudioPerfAc3PlayHttpHosted()\n");

    strcpy ( path, (char *)getenv ("RESRC_PUBLISHER_LINK") );strcat ( path, "/" );strcat ( path, "Test.ac3" );
    g_print ("\n\n **** resources path = %s ***** \n", path);

    res = url_check(path);
    if (res == FAIL || res == ERROR)
	{
		INCIDENT_TYPE(res);
		return;
	}

    res = perf_time_taken_audio_play(path);
	INCIDENT_TYPE(res);

    g_print ("GST_START_TEST: EXIT. %s\n", __func__);
	TESTFUNCTION_END();

}
GST_END_TEST;

GST_START_TEST (gstAudioPerf3GPCreatingPipelineHttpHosted)
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
    g_print ("GST_START_TEST: ENTRY. gstAudioPerf3GPCreatingPipelineHttpHosted()\n");

    strcpy ( path, (char *)getenv ("RESRC_PUBLISHER_LINK") );strcat ( path, "/" );strcat ( path, "Test.3GP" );
    g_print ("\n\n **** resources path = %s ***** \n", path);

    res = url_check(path);
    if (res == FAIL || res == ERROR)
	{
		INCIDENT_TYPE(res);
		return;
	}

    res = perf_time_taken_pipe_creatn(path);
	INCIDENT_TYPE(res);

    g_print ("GST_START_TEST: EXIT. %s\n", __func__);
	TESTFUNCTION_END();
}
GST_END_TEST;

GST_START_TEST (gstAudioPerf3GPPlayHttpHosted)
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
    g_print ("GST_START_TEST: ENTRY. gstAudioPerf3GPPlayHttpHosted()\n");

   strcpy ( path, (char *)getenv ("RESRC_PUBLISHER_LINK") );strcat ( path, "/" );strcat ( path, "Test.3GP" );
    g_print ("\n\n **** resources path = %s ***** \n", path);

    res = url_check(path);
    if (res == FAIL || res == ERROR)
	{
		INCIDENT_TYPE(res);
		return;
	}

    res = perf_time_taken_audio_play(path);
	INCIDENT_TYPE(res);

    g_print ("GST_START_TEST: EXIT. %s\n", __func__);
	TESTFUNCTION_END();

}
GST_END_TEST;

GST_START_TEST (gstAudioPerfAacCreatingPipelineHttpHosted)
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
    g_print ("GST_START_TEST: ENTRY. gstAudioPerfAacCreatingPipelineHttpHosted()\n");

   strcpy ( path, (char *)getenv ("RESRC_PUBLISHER_LINK") );strcat ( path, "/" );strcat ( path, "Test.aac" );
    g_print ("\n\n **** resources path = %s ***** \n", path);

    res = url_check(path);
    if (res == FAIL || res == ERROR)
	{
		INCIDENT_TYPE(res);
		return;
	}

    res = perf_time_taken_pipe_creatn(path);
	INCIDENT_TYPE(res);

    g_print ("GST_START_TEST: EXIT. %s\n", __func__);
	TESTFUNCTION_END();
}
GST_END_TEST;

GST_START_TEST (gstAudioPerfAacPlayHttpHosted)
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
    g_print ("GST_START_TEST: ENTRY. gstAudioPerfAacPlayHttpHosted()\n");

    strcpy ( path, (char *)getenv ("RESRC_PUBLISHER_LINK") );strcat ( path, "/" );strcat ( path, "Test.aac" );
    g_print ("\n\n **** resources path = %s ***** \n", path);

    res = url_check(path);
    if (res == FAIL || res == ERROR)
	{
		INCIDENT_TYPE(res);
		return;
	}

    res = perf_time_taken_audio_play(path);
	INCIDENT_TYPE(res);

    g_print ("GST_START_TEST: EXIT. %s\n", __func__);
	TESTFUNCTION_END();
}
GST_END_TEST;

GST_START_TEST (gstAudioPerfMkaCreatingPipelineHttpHosted)
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
    g_print ("GST_START_TEST: ENTRY. gstAudioPerfMkaCreatingPipelineHttpHosted()\n");

    strcpy ( path, (char *)getenv ("RESRC_PUBLISHER_LINK") );strcat ( path, "/" );strcat ( path, "Test.mka" );
    g_print ("\n\n **** resources path = %s ***** \n", path);

    res = url_check(path);
    if (res == FAIL || res == ERROR)
	{
		INCIDENT_TYPE(res);
		return;
	}

    res = perf_time_taken_pipe_creatn(path);
	INCIDENT_TYPE(res);

    g_print ("GST_START_TEST: EXIT. %s\n", __func__);
	TESTFUNCTION_END();
}
GST_END_TEST;

GST_START_TEST (gstAudioPerfMkaPlayHttpHosted)
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
    g_print ("GST_START_TEST: ENTRY. gstAudioPerfMkaPlayHttpHosted()\n");

    strcpy ( path, (char *)getenv ("RESRC_PUBLISHER_LINK") );strcat ( path, "/" );strcat ( path, "Test.mka" );
    g_print ("\n\n **** resources path = %s ***** \n", path);

    res = url_check(path);
    if (res == FAIL || res == ERROR)
	{
		INCIDENT_TYPE(res);
		return;
	}

    res = perf_time_taken_audio_play(path);
	INCIDENT_TYPE(res);

    g_print ("GST_START_TEST: EXIT. %s\n", __func__);
	TESTFUNCTION_END();
}
GST_END_TEST;

GST_START_TEST (gstAudioPerfMp3CreatingPipelineIterHttpHosted)
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
    g_print ("GST_START_TEST: ENTRY. gstAudioPerfMp3CreatingPipelineIterHttpHosted()\n");

   strcpy ( path, (char *)getenv ("RESRC_PUBLISHER_LINK") );strcat ( path, "/" );strcat ( path, "Test.mp3" );
    g_print ("\n\n **** resources path = %s ***** \n", path);

    res = url_check(path);
    if (res == FAIL || res == ERROR)
	{
		INCIDENT_TYPE(res);
		return;
	}

    res = perf_time_taken_pipe_creatn_iter(path);
	INCIDENT_TYPE(res);

    g_print ("GST_START_TEST: EXIT. %s\n", __func__);
	TESTFUNCTION_END();
}
GST_END_TEST;

GST_START_TEST (gstAudioPerfMp3PlayIterHttpHosted)
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
    g_print ("GST_START_TEST: ENTRY. gstAudioPerfMp3PlayIterHttpHosted()\n");

   strcpy ( path, (char *)getenv ("RESRC_PUBLISHER_LINK") );strcat ( path, "/" );strcat ( path, "Test.mp3" );
    g_print ("\n\n **** resources path = %s ***** \n", path);

    res = url_check(path);
    if (res == FAIL || res == ERROR)
	{
		INCIDENT_TYPE(res);
		return;
	}

    res = perf_time_taken_audio_play_iter(path);
	INCIDENT_TYPE(res);

    g_print ("GST_START_TEST: EXIT. %s\n", __func__);
	TESTFUNCTION_END();
}
GST_END_TEST;

GST_START_TEST (gstAudioPerfAc3CreatingPipelineIterHttpHosted)
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
    g_print ("GST_START_TEST: ENTRY. gstAudioPerfAc3CreatingPipelineIterHttpHosted()\n");

    strcpy ( path, (char *)getenv ("RESRC_PUBLISHER_LINK") );strcat ( path, "/" );strcat ( path, "Test.ac3" );
    g_print ("\n\n **** resources path = %s ***** \n", path);

    res = url_check(path);
    if (res == FAIL || res == ERROR)
	{
		INCIDENT_TYPE(res);
		return;
	}

    res = perf_time_taken_pipe_creatn_iter(path);
	INCIDENT_TYPE(res);

    g_print ("GST_START_TEST: EXIT. %s\n", __func__);
	TESTFUNCTION_END();
}
GST_END_TEST;

GST_START_TEST (gstAudioPerfAc3PlayIterHttpHosted)
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
    g_print ("GST_START_TEST: ENTRY. gstAudioPerfAc3PlayIterHttpHosted()\n");

    strcpy ( path, (char *)getenv ("RESRC_PUBLISHER_LINK") );strcat ( path, "/" );strcat ( path, "Test.ac3" );
    g_print ("\n\n **** resources path = %s ***** \n", path);

    res = url_check(path);
    if (res == FAIL || res == ERROR)
	{
		INCIDENT_TYPE(res);
		return;
	}

    res = perf_time_taken_audio_play_iter(path);
	INCIDENT_TYPE(res);

    g_print ("GST_START_TEST: EXIT. %s\n", __func__);
	TESTFUNCTION_END();
}
GST_END_TEST;

GST_START_TEST (gstAudioPerf3GPCreatingPipelineIterHttpHosted)
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
    g_print ("GST_START_TEST: ENTRY. gstAudioPerf3GPCreatingPipelineIterHttpHosted()\n");

    strcpy ( path, (char *)getenv ("RESRC_PUBLISHER_LINK") );strcat ( path, "/" );strcat ( path, "Test.3GP" );
    g_print ("\n\n **** resources path = %s ***** \n", path);

    res = url_check(path);
    if (res == FAIL || res == ERROR)
	{
		INCIDENT_TYPE(res);
		return;
	}

    res = perf_time_taken_pipe_creatn_iter(path);
	INCIDENT_TYPE(res);

    g_print ("GST_START_TEST: EXIT. %s\n", __func__);
	TESTFUNCTION_END();
}
GST_END_TEST;

GST_START_TEST (gstAudioPerf3GPPlayIterHttpHosted)
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
    g_print ("GST_START_TEST: ENTRY. gstAudioPerf3GPPlayIterHttpHosted()\n");

    strcpy ( path, (char *)getenv ("RESRC_PUBLISHER_LINK") );strcat ( path, "/" );strcat ( path, "Test.3GP" );
    g_print ("\n\n **** resources path = %s ***** \n", path);

    res = url_check(path);
    if (res == FAIL || res == ERROR)
	{
		INCIDENT_TYPE(res);
		return;
	}

    res = perf_time_taken_audio_play_iter(path);
	INCIDENT_TYPE(res);

    g_print ("GST_START_TEST: EXIT. %s\n", __func__);
	TESTFUNCTION_END();
}
GST_END_TEST;

GST_START_TEST (gstAudioPerfAacCreatingPipelineIterHttpHosted)
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
    g_print ("GST_START_TEST: ENTRY. gstAudioPerfAacCreatingPipelineIterHttpHosted()\n");

    strcpy ( path, (char *)getenv ("RESRC_PUBLISHER_LINK") );strcat ( path, "/" );strcat ( path, "Test.aac" );
    g_print ("\n\n **** resources path = %s ***** \n", path);

    res = url_check(path);
    if (res == FAIL || res == ERROR)
	{
		INCIDENT_TYPE(res);
		return;
	}

    res = perf_time_taken_pipe_creatn_iter(path);
	INCIDENT_TYPE(res);

    g_print ("GST_START_TEST: EXIT. %s\n", __func__);
	TESTFUNCTION_END();
}
GST_END_TEST;

GST_START_TEST (gstAudioPerfAacPlayIterHttpHosted)
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
    g_print ("GST_START_TEST: ENTRY. gstAudioPerfAacPlayIterHttpHosted()\n");

    strcpy ( path, (char *)getenv ("RESRC_PUBLISHER_LINK") );strcat ( path, "/" );strcat ( path, "Test.aac" );
    g_print ("\n\n **** resources path = %s ***** \n", path);

    res = url_check(path);
    if (res == FAIL || res == ERROR)
	{
		INCIDENT_TYPE(res);
		return;
	}

    res = perf_time_taken_audio_play_iter(path);
	INCIDENT_TYPE(res);

    g_print ("GST_START_TEST: EXIT. %s\n", __func__);
	TESTFUNCTION_END();
}
GST_END_TEST;

GST_START_TEST (gstAudioPerfMkaCreatingPipelineIterHttpHosted)
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
    g_print ("GST_START_TEST: ENTRY. gstAudioPerfMkaCreatingPipelineIterHttpHosted()\n");

    strcpy ( path, (char *)getenv ("RESRC_PUBLISHER_LINK") );strcat ( path, "/" );strcat ( path, "Test.mka" );
    g_print ("\n\n **** resources path = %s ***** \n", path);

    res = url_check(path);
    if (res == FAIL || res == ERROR)
	{
		INCIDENT_TYPE(res);
		return;
	}

    res = perf_time_taken_pipe_creatn_iter(path);
	INCIDENT_TYPE(res);

    g_print ("GST_START_TEST: EXIT. %s\n", __func__);
	TESTFUNCTION_END();
}
GST_END_TEST;

GST_START_TEST (gstAudioPerfMkaPlayIterHttpHosted)
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
    g_print ("GST_START_TEST: ENTRY. gstAudioPerfMkaPlayIterHttpHosted()\n");

    strcpy ( path, (char *)getenv ("RESRC_PUBLISHER_LINK") );strcat ( path, "/" );strcat ( path, "Test.mka" );
    g_print ("\n\n **** resources path = %s ***** \n", path);

    res = url_check(path);
    if (res == FAIL || res == ERROR)
	{
		INCIDENT_TYPE(res);
		return;
	}

    res = perf_time_taken_audio_play_iter(path);
	INCIDENT_TYPE(res);

    g_print ("GST_START_TEST: EXIT. %s\n", __func__);
	TESTFUNCTION_END();
}
GST_END_TEST;

static Suite *
performance_audio_testsuite (void) {
    Suite *s ;
    TCase *tc_chain ;
    int timeoutvalue = 200;

    GST_DEBUG ("performance_audio_testsuite(): ENTRY.()\n");

    s = suite_create ("performance_audio_testsuite");
    tc_chain = tcase_create ("performance_audio_testsuite");

    tcase_set_timeout (tc_chain, timeoutvalue);
    GST_DEBUG ("performance_audio_testsuite():timeoutvalue = %d\n", timeoutvalue);

    suite_add_tcase (s, tc_chain);

    tcase_add_test (tc_chain, gstAudioPerfMp3CreatingPipelineHttpHosted);
    tcase_add_test (tc_chain, gstAudioPerfMp3PlayHttpHosted);

    tcase_add_test (tc_chain, gstAudioPerfAc3CreatingPipelineHttpHosted);
    tcase_add_test (tc_chain, gstAudioPerfAc3PlayHttpHosted);
    tcase_add_test (tc_chain, gstAudioPerf3GPCreatingPipelineHttpHosted);
    tcase_add_test (tc_chain, gstAudioPerf3GPPlayHttpHosted);
    tcase_add_test (tc_chain, gstAudioPerfAacCreatingPipelineHttpHosted);
    tcase_add_test (tc_chain, gstAudioPerfAacPlayHttpHosted);
    tcase_add_test (tc_chain, gstAudioPerfMkaCreatingPipelineHttpHosted);
    tcase_add_test (tc_chain, gstAudioPerfMkaPlayHttpHosted);
    tcase_add_test (tc_chain, gstAudioPerfMp3CreatingPipelineIterHttpHosted);
    tcase_add_test (tc_chain, gstAudioPerfMp3PlayIterHttpHosted);
	
    tcase_add_test (tc_chain, gstAudioPerfAc3CreatingPipelineIterHttpHosted);
    tcase_add_test (tc_chain, gstAudioPerfAc3PlayIterHttpHosted);
/*
    tcase_add_test (tc_chain, gstAudioPerf3GPCreatingPipelineIterHttpHosted);
    tcase_add_test (tc_chain, gstAudioPerf3GPPlayIterHttpHosted);
    tcase_add_test (tc_chain, gstAudioPerfAacCreatingPipelineIterHttpHosted);
    tcase_add_test (tc_chain, gstAudioPerfAacPlayIterHttpHosted);
    tcase_add_test (tc_chain, gstAudioPerfMkaCreatingPipelineIterHttpHosted);
    tcase_add_test (tc_chain, gstAudioPerfMkaPlayIterHttpHosted);
*/
    GST_DEBUG ("performance_audio_testsuite(): EXIT.()\n");
    return s;
}

int
main (int argc, char **argv)
{
    int nf;
    Suite *s;
    SRunner *sr;
    g_print ("Gstreamer_Audio_Performance_On_New_Pipeline_HttpHosted()\n");

    XML_START();
	TESTCASE_START("Gstreamer_Audio_Performance_On_New_Pipeline_HttpHosted");
	GST_ENV();
    GST_DEBUG ("main(): ENTRY.()\n");

    s = performance_audio_testsuite ();
    sr = srunner_create (s);

    gst_check_init (&argc, &argv);

    srunner_run_all (sr, CK_NORMAL);
    nf = srunner_ntests_failed (sr);
    srunner_free (sr);

    GST_DEBUG ("main(): EXIT.()\n");
	TESTCASE_END();
    return nf;
}

