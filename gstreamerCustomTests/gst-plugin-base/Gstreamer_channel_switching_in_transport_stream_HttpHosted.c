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
/* GStreamer
 *
 * Functional and Performance tests for Switching Between Channels in a Transport Stream
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
#include <sys/wait.h>
#include <sys/param.h>
#include <stdio.h>
#include "common/gstplayback.h"

#define BILLION  1E9
#define NUMBER_OF_CHANNEL 5
#define SZ_TCNAME 50
#define MSEC 1000
#define SZ_RESOURCE_PATH 200
#define SZ_PATH 200

static char tcname[SZ_TCNAME];

guint program = 0, es_type = 0;
guint a[20], b[20];
int program_number=0;
static int flag = 0;

GMainLoop *loop; 
GstElement *pipeline, *filesrc, *demuxer, *video_queue, *videodec, *videosink, *audio_queue, *audiodec, *audiosink;
GstBus *bus; 
GstStateChangeReturn ret;
struct timespec channelStart, channelEnd;

struct timespec clock_before_pipeline_creation, clock_after_pipeline_creation, clock_at_play_event, clock_at_play_command;
static double pipeline_creation_time = 0.0, channel_start_delay=0.0;
static double sumof_pipeline_creation_time = 0, sumof_channel_start_delay = 0;

static gboolean
bus_call (GstBus * bus, GstMessage * msg, gpointer data) {
    GMainLoop *loop = (GMainLoop *) data;
    gchar *debug;
    GError *err;

    GST_DEBUG ("message_handler(). ENTRY \n");

    switch (GST_MESSAGE_TYPE (msg)) {
        case GST_MESSAGE_EOS:
            GST_DEBUG ("message_handler. GST_MESSAGE_EOS: %d \n", GST_MESSAGE_TYPE (msg) );
            GST_DEBUG ("Playback successful \n");
            g_print ("End of stream\n");
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

        case GST_MESSAGE_STATE_CHANGED: {
            GstState old_state, new_state, pending_state,temp_state;
            gst_message_parse_state_changed (msg, &old_state, &new_state, &pending_state);
            GST_DEBUG ("Pipeline state changed from %s to %s:\n",
         gst_element_state_get_name (old_state), gst_element_state_get_name (new_state));
         if (new_state == GST_STATE_PLAYING ) {
             /* We just moved to PLAYING. Check if seeking is possible */
             GST_DEBUG ("Video starts playing \n");
             if( clock_gettime( CLOCK_REALTIME, &clock_at_play_event) == -1 ) {
                    perror( "clock gettime" );
              }
              GST_DEBUG (" *** clock_at_play_event = %lf seconds\n", ((clock_at_play_event.tv_sec * (double)BILLION) + clock_at_play_event.tv_nsec)/(double)BILLION);
          }
      }
      break;

        default:
            GST_DEBUG ("message_handler. default: %d \n", GST_MESSAGE_TYPE (msg));
        break;
    }

    GST_DEBUG ("message_handler(). EXIT \n");
    return TRUE;
}

static void
on_pad_added (GstElement *element,
              GstPad     *pad,
              gpointer    data)
{
  GstPad *sinkpad;
  GstElement *queue = (GstElement *) data;

  /* We can now link this pad with the capsfilter sink pad */
  g_print ("Dynamic pad created, linking demuxer/queue\n");

  sinkpad = gst_element_get_static_pad (queue, "sink");

 
  gst_pad_link (pad, sinkpad);

  gst_object_unref (sinkpad);
}

static void
dump_descriptors (GValueArray *descriptors)
{
  GValue * value;
  gint i;
  for (i = 0 ; i < descriptors->n_values; i++) {
    GString *string;
    value = g_value_array_get_nth (descriptors, i);
    string = (GString *) g_value_get_boxed (value);
    
    if (string->len > 2) {
     g_print ("    descriptor # %d tag %02x len %d\n",
         i + 1, (guint8)string->str[0], (guint8)string->str[1]);
     gst_util_dump_mem ((guint8*)string->str + 2, string->len - 2);    
    }
  }  
  g_print ("\n");
}

static void
dump_languages (GValueArray *languages)
{
  GValue * value;
  gint i;
  if (!languages->n_values)
    return;
 
 g_print ("    languages: ");
  for (i = 0 ; i < languages->n_values; i++) {
    const gchar *string;
    value = g_value_array_get_nth (languages, i);
    string = g_value_get_string (value);    
   g_print ("%s", string);
  }  
  g_print ("\n");
}

static void
demuxer_notify_pat_info (GObject *obj, GParamSpec *pspec, gpointer user_data)
{
  GValueArray *patinfo = NULL;
  GValue * value = NULL;
  GObject *entry = NULL;
  guint program, pid;
  gint i;

  g_object_get (obj, "pat-info", &patinfo, NULL);
  
  g_print ("PAT: entries: %d\n", patinfo->n_values);  
  for (i = 0; i < patinfo->n_values; i++) {
    value = g_value_array_get_nth (patinfo, i);
    entry = (GObject*) g_value_get_object (value);
    g_object_get (entry, "program-number", &program, NULL);
    g_object_get (entry, "pid", &pid, NULL);
    a[i] = program;
    g_print ("    program: %u pid: %04x\n", program, pid);
  }
    g_print("\n");
}


static void
demuxer_notify_pmt_info (GObject *obj, GParamSpec *pspec, gpointer user_data)
{
  GObject *pmtinfo = NULL, *streaminfo = NULL;
  GValueArray *streaminfos = NULL;
  GValueArray *descriptors = NULL;
  GValueArray *languages = NULL;
  gint i;
  GValue * value;
  guint version, pcr_pid, es_pid;
   
  g_object_get (obj, "pmt-info", &pmtinfo, NULL);
  g_object_get (pmtinfo, "program-number", &program, NULL);
  g_object_get (pmtinfo, "version-number", &version, NULL);
  g_object_get (pmtinfo, "pcr-pid", &pcr_pid, NULL);
  g_object_get (pmtinfo, "stream-info", &streaminfos, NULL);
  g_object_get (pmtinfo, "descriptors", &descriptors, NULL);

  g_print ("PMT: program: %u version: %d pcr: %04x streams: %d descriptors: %d\n",
     (guint16)program, version, (guint16)pcr_pid, streaminfos->n_values,
     descriptors->n_values);

  //dump_descriptors (descriptors);
  for (i = 0 ; i < streaminfos->n_values; i++) {
    value = g_value_array_get_nth (streaminfos, i);
    streaminfo = (GObject*) g_value_get_object (value);
    g_object_get (streaminfo, "pid", &es_pid, NULL);
    g_object_get (streaminfo, "stream-type", &es_type, NULL);
    b[i] = es_type;
    g_object_get (streaminfo, "languages", &languages, NULL);
    g_object_get (streaminfo, "descriptors", &descriptors, NULL);
    g_print ("    pid: %04x type: %x languages: %d descriptors: %d\n",
       (guint16)es_pid, (guint8) es_type, languages->n_values, descriptors->n_values);
    dump_languages (languages);
    dump_descriptors (descriptors);
  }
  g_print("\n");
}

static STATUS
create_pipeline(char *resources_path, int Tflag) {

  loop = g_main_loop_new (NULL, FALSE); 
  
  if(Tflag==2){ 
	if( clock_gettime(CLOCK_REALTIME, &channelStart) == -1)
	{	
            MESSAGE_START();
            DESCRIPTION(ERROR, "Error: clock gettime\n");
            MESSAGE_END();
			return ERROR;
	}
	printf("Start time for the channel: %lfsecs %lfnanosecs\n",(double)channelStart.tv_sec,(double)channelStart.tv_nsec);
  }

  /*Measuring time before creating pipeline */
  if( clock_gettime( CLOCK_REALTIME, &clock_before_pipeline_creation) == -1 ) {
            MESSAGE_START();
            DESCRIPTION(ERROR, "Error: clock gettime\n");
            MESSAGE_END();			
			return ERROR;
  }

  /* Create gstreamer elements */ 
  pipeline = gst_pipeline_new ("ts-player"); 
  filesrc = gst_element_factory_make ("souphttpsrc", "src"); 
  demuxer = gst_element_factory_make ("flutsdemux", "demux");
  video_queue =  gst_element_factory_make ("queue", "queue for video");
  videodec = gst_element_factory_make ("omx_videodec", "videodec"); 
  videosink = gst_element_factory_make ("omx_videosink", "videosink");
  audio_queue =  gst_element_factory_make ("queue", "queue for audio");
  audiodec = gst_element_factory_make ("omx_audiodec", "audiodec"); 
  audiosink = gst_element_factory_make ("omx_audiosink", "audiosink"); 
  
  if (!pipeline || !filesrc || !demuxer || !videodec || !videosink || !video_queue || !audio_queue || !audiodec || !audiosink) 
  { 
   // g_printerr ("One element could not be created. Exiting.\n"); 
            MESSAGE_START();
            DESCRIPTION(ERROR, "One element could not be created. Exiting.\n");
            MESSAGE_END();
			return ERROR;
  } 

  /* Set up the pipeline */ 
  g_print ("Elements are created\n"); 

  /* set the properties of other elements */ 
  g_object_set (G_OBJECT (filesrc), "location", resources_path, NULL); 
  
  /* we add a message handler */ 
  bus = gst_pipeline_get_bus (GST_PIPELINE (pipeline)); 
  gst_bus_add_watch (bus, bus_call, loop); 
  gst_object_unref (bus); 


 /* we add all elements into the pipeline */ 
  gst_bin_add_many (GST_BIN (pipeline),filesrc, demuxer, video_queue, videodec, videosink, audio_queue, audiodec, audiosink, NULL); 

  g_print ("Added all the Elements into the pipeline\n"); 

  /* we link the elements together */ 
  gst_element_link (filesrc, demuxer);
  g_signal_connect (demuxer, "pad-added", G_CALLBACK (on_pad_added), video_queue); 
  gst_element_link_many (video_queue, videodec, videosink, NULL); 
  
  g_signal_connect (demuxer, "pad-added", G_CALLBACK (on_pad_added), audio_queue);
  gst_element_link_many (audio_queue, audiodec, audiosink, NULL); 

  if(Tflag == 1)
  {
  g_signal_connect(G_OBJECT(demuxer), "notify::pat-info", (GCallback)demuxer_notify_pat_info, NULL);
  g_signal_connect(G_OBJECT(demuxer), "notify::pmt-info", (GCallback)demuxer_notify_pmt_info, NULL);
  }
  g_print ("Linked all the Elements together\n"); 

  /*Measuring time after creating pipeline */
  if( clock_gettime( CLOCK_REALTIME, &clock_after_pipeline_creation) == -1 ) {
            MESSAGE_START();
            DESCRIPTION(ERROR, "Error: clock gettime\n");
            MESSAGE_END();			
			return ERROR;
  }
  pipeline_creation_time = ( clock_after_pipeline_creation.tv_sec - clock_before_pipeline_creation.tv_sec )
                                                + (double)( clock_after_pipeline_creation.tv_nsec - clock_before_pipeline_creation.tv_nsec ) / (double)BILLION;
  g_print (" Time Taken for creation of pipeline = %lf seconds\n", pipeline_creation_time);

  return PASS;
}

STATUS delete_pipeline(void ) {

  /* Out of the main loop, clean up nicely */ 
  g_print ("Returned, stopping playback\n"); 
  if (GST_STATE_CHANGE_FAILURE == gst_element_set_state (pipeline, GST_STATE_NULL))
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

static double switch_channel(int program_number,int Tflag) {

  double time_taken = 0;
  
  if(Tflag==2){
  if (clock_gettime(CLOCK_REALTIME, &channelStart) == -1)
  {
            MESSAGE_START();
            DESCRIPTION(ERROR, "Error: clock gettime\n");
            MESSAGE_END();			
			return;  
  }
  printf("Start time for the channel: %lfsecs %lfnanosecs\n",(double)channelStart.tv_sec,(double)channelStart.tv_nsec);
  }

  /* to set the properties */ 
  g_object_set (demuxer, "program-number", program_number, NULL); 
  
  /* Set the pipeline to "playing" state*/ 
  g_print ("Playing the video\n"); 
	if (GST_STATE_CHANGE_FAILURE == gst_element_set_state(GST_ELEMENT(pipeline), GST_STATE_PLAYING))
	{
        GST_DEBUG ("Failed to PLAY\n");
        MESSAGE_START();
        DESCRIPTION(FAIL, "Fail: Pipeline not set to PLAYING. Exiting.");
        MESSAGE_END();
        return;
	}
 
  if( clock_gettime( CLOCK_REALTIME, &clock_at_play_command) == -1 ) {
//      perror( "clock gettime" );
            MESSAGE_START();
            DESCRIPTION(ERROR, "Error: clock gettime\n");
            MESSAGE_END();			
			return;  
  }
  GST_DEBUG (" *** clock_at_play_command = %lf seconds\n", ((clock_at_play_command.tv_sec * (double)BILLION) + clock_at_play_command.tv_nsec)/(double)BILLION);
    
 
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
        return;
	}
  
  //Delay in channel switching
  channel_start_delay = ( clock_at_play_event.tv_sec - clock_at_play_command.tv_sec )
                                                + (double)( clock_at_play_event.tv_nsec - clock_at_play_command.tv_nsec ) / (double)BILLION;

  if(Tflag==2){
  if(clock_gettime(CLOCK_REALTIME, &channelEnd) == -1)
  {
              MESSAGE_START();
            DESCRIPTION(ERROR, "Error: clock gettime\n");
            MESSAGE_END();			
			return;  
  }
  printf("End time for the channel: %lf secs %lf nanosecs\n",(double)channelEnd.tv_sec,(double)channelEnd.tv_nsec);
  
  time_taken = ( channelEnd.tv_sec - channelStart.tv_sec )
  + ( channelEnd.tv_nsec - channelStart.tv_nsec )
  / BILLION;
  printf( "Time duration:%lfsecs\n", time_taken );
  }

  if(Tflag==2){
 return time_taken;
 }
 else
 return 0.0;

}

static double
media_state(char *resources_path, int program_number,int Tflag) {

  //Create pipeline
  create_pipeline(resources_path, Tflag);

  //Switch to selected channel
  double net_time = switch_channel(program_number,Tflag);
  
  //Delete pipeline
  delete_pipeline( );

  return net_time;
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

GST_START_TEST (gstChannelSwitchingFuncHttpHosted) {

    char resources_path[SZ_RESOURCE_PATH];
    char path[SZ_PATH] ;
    int ret, i;
    char command[SZ_PATH+SZ_RESOURCE_PATH];
    int loop_count = 0;
	STATUS res;
	TESTFUNCTION_START();	
    g_print ("\n=========================\n");
    g_sprintf(tcname, __func__);
    g_print ("TestCase: %s\n", tcname);
    g_print ("GST_START_TEST: ENTRY. gstChannelSwitchingFuncHttpHosted()\n");

    strcpy ( path, (char *)getenv ("RESRC_PUBLISHER_LINK") );strcat ( path, "/" );strcat ( path, "Test.ts" );
    g_print ("\n **** resources path = %s ***** \n", path);

    res = url_check(path);
    if (res == FAIL || res == ERROR)
	{
		INCIDENT_TYPE(res);
		return;
	}

    while (loop_count < 5)
  {      
     if(loop_count==0)
       program_number=257;
     else if(loop_count==1)
       program_number=272;
     else if(loop_count==2)
       program_number=260;
     else if(loop_count==3)
       program_number=262;
     else if(loop_count==4)
       program_number=259;
     
     flag=0;
     double var=media_state(path, program_number,flag);

     g_print ("Played channel %d \n",loop_count+1); 
     g_print ("\n\n\n");
     loop_count++;

  }
		MESSAGE_START();
        DESCRIPTION(PASS, "");
		MESSAGE_END();
		INCIDENT_TYPE(PASS);
		g_print ("GST_START_TEST: EXIT. gstChannelSwitchingFuncHttpHosted()\n");
		TESTFUNCTION_END();  
}
GST_END_TEST;

 GST_START_TEST (gstChannelSwitchingFuncDisplayProgDetailsHttpHosted) {
    char resources_path[SZ_RESOURCE_PATH];
    char path[SZ_PATH] ;
    int ret, i;
    char command[SZ_PATH+SZ_RESOURCE_PATH];
    int loop_count = 0;
    flag = 1;
	STATUS res;
	TESTFUNCTION_START();
    g_print ("\n=========================\n");
    g_sprintf(tcname, __func__);
    g_print ("TestCase: %s\n", tcname);
    g_print ("GST_START_TEST: ENTRY. gstChannelSwitchingFuncDisplayProgDetailsHttpHosted()\n");

    strcpy ( path, (char *)getenv ("RESRC_PUBLISHER_LINK") );strcat ( path, "/" );strcat ( path, "Test.ts" );
    g_print ("\n **** resources path = %s ***** \n", path);

    res = url_check(path);
    if (res == FAIL || res == ERROR)
	{
		INCIDENT_TYPE(res);
		return;
	}

    while (loop_count < 5)
  {      
     if(loop_count==0)
       program_number=257;
     else if(loop_count==1)
       program_number=272;
     else if(loop_count==2)
       program_number=260;
     else if(loop_count==3)
       program_number=262;
     else if(loop_count==4)
       program_number=259;
     
     double var=media_state(path, program_number,flag);

     g_print ("Played channel %d \n",loop_count+1); 
     g_print ("\n\n\n");
     loop_count++;
  }
		MESSAGE_START();
        DESCRIPTION(PASS, "");
		MESSAGE_END();
		INCIDENT_TYPE(PASS);  
    g_print ("GST_START_TEST: EXIT. gstChannelSwitchingFuncDisplayProgDetailsHttpHosted()\n");
	TESTFUNCTION_END();
}
GST_END_TEST;

  GST_START_TEST (gstChannelSwitchingPerfHttpHosted) {
    char resources_path[SZ_RESOURCE_PATH];
    char path[SZ_PATH] ;
    int ret, i;
    char command[SZ_PATH+SZ_RESOURCE_PATH];
    int loop_count = 0;
    
    struct timespec streamStart, streamEnd;    
    double net_time=0, switching_time=0;
	STATUS res;
	TESTFUNCTION_START();
    g_print ("\n=========================\n");
    g_sprintf(tcname, __func__);
    g_print ("TestCase: %s\n", tcname);
    g_print ("GST_START_TEST: ENTRY. gstChannelSwitchingPerfHttpHosted()\n");
    g_print (" [   Checks: Performance measurements for channel switching creating NEW pipeline evertime }\n");

    strcpy ( path, (char *)getenv ("RESRC_PUBLISHER_LINK") );strcat ( path, "/" );strcat ( path, "Test.ts" );
    g_print ("\n **** resources path = %s ***** \n", path);

    res = url_check(path);
    if (res == FAIL || res == ERROR)
	{
		INCIDENT_TYPE(res);
		return;
	}

    while (loop_count < 5)
  {      
     if(loop_count==0){
       program_number=257;
       clock_gettime(CLOCK_REALTIME, &streamStart);
       printf("Start time for all the channels: %lfsecs %lfnanosecs\n",(double)streamStart.tv_sec,(double)streamStart.tv_nsec);	
     }
     else if(loop_count==1)
       program_number=272;
     else if(loop_count==2)
       program_number=260;
     else if(loop_count==3)
       program_number=262;
     else if(loop_count==4)
       program_number=259;
     

     flag=2;
     net_time+=media_state(path, program_number,flag);

     if (loop_count != 0) {
        sumof_channel_start_delay += channel_start_delay;
        sumof_pipeline_creation_time += pipeline_creation_time;
        g_print (" Time Taken for creation of pipeline = %lf seconds\n", pipeline_creation_time);
        g_print (" Time Taken for channel switching = %lf seconds\n", channel_start_delay);
        g_print (" Sum of Time Taken for creation of pipeline = %lf seconds\n", sumof_pipeline_creation_time);
        g_print (" Sum of Time Taken for channel switching = %lf seconds\n", sumof_channel_start_delay);
     } else {
        g_print( "[   Checks: First time -Time Taken for creation of pipeline = %lf seconds]\n", pipeline_creation_time);
        g_print( " [   Checks: First time - Time Taken for channel switching = %lf seconds]\n", channel_start_delay);
        channel_start_delay = 0;
     }

     g_print ("Played channel %d \n",loop_count+1); 
     g_print ("\n\n\n");
     loop_count++;
}
  if( clock_gettime(CLOCK_REALTIME, &streamEnd) == -1)
	{
                MESSAGE_START();
            DESCRIPTION(ERROR, "Error: clock gettime\n");
            MESSAGE_END();	
			INCIDENT_TYPE(ERROR);
			TESTFUNCTION_END();
			return;
	}
    g_print( "[ Checks: Average over %d times - Time Taken for creating of NEW pipeline  = %lf seconds]\n", (NUMBER_OF_CHANNEL-1), (sumof_pipeline_creation_time/(NUMBER_OF_CHANNEL-1)));
	MESSAGE_START();  
    DESCRIPTION(CHECKS, "Average over %d times - Time Taken for channel switching On NEW pipeline :: %lf ms\n", (NUMBER_OF_CHANNEL-1), (sumof_channel_start_delay/(NUMBER_OF_CHANNEL-1)) * MSEC);
	MESSAGE_END();

  g_print("End time for all the channels: %lf secs %lf nanosecs\n",(double)streamEnd.tv_sec,(double)streamEnd.tv_nsec);

  /* Calculate time it took to establish the pipeline connection*/
  double accum = ( streamEnd.tv_sec - streamStart.tv_sec )+( streamEnd.tv_nsec - streamStart.tv_nsec )
  / BILLION;
  printf("Time duration for the entire stream duration:%lf secs\n", accum );
  printf("Net Time taken, channel wise: %lf secs\n",net_time);  

  switching_time=accum-net_time;
  printf("Time elapsed between channel switching :%lf secs\n",switching_time);

                MESSAGE_START();
            DESCRIPTION(PASS, "");
            MESSAGE_END();	
			INCIDENT_TYPE(PASS);
      g_print ("GST_START_TEST: EXIT. gstChannelSwitchingPerfHttpHosted()\n");
			TESTFUNCTION_END();	
}
GST_END_TEST;

GST_START_TEST (gstChannelSwitchingPerfOnsamepipelineHttpHosted) {
    char resources_path[SZ_RESOURCE_PATH];
    char path[SZ_PATH] ;
    int ret, i;
    char command[SZ_PATH+SZ_RESOURCE_PATH];
    int loop_count = 0;
    
    struct timespec streamStart, streamEnd;    
    double net_time=0, switching_time=0;
	
    pipeline_creation_time = 0.0, channel_start_delay=0.0;
    sumof_pipeline_creation_time = 0, sumof_channel_start_delay = 0;
	STATUS res;
	TESTFUNCTION_START();
    g_print ("\n [   Checks: ========================================  ]\n");
    g_sprintf(tcname, __func__);
    GST_DEBUG ("TestCase: %s\n", tcname);
    GST_DEBUG ("GST_START_TEST: ENTRY. gstChannelSwitchingPerfOnsamepipelineHttpHosted()\n");
    g_print (" [   Checks: Performance measurements for channel switching creating SAME pipeline evertime }\n");

    strcpy ( path, (char *)getenv ("RESRC_PUBLISHER_LINK") );strcat ( path, "/" );strcat ( path, "Test.ts" );
    g_print ("\n **** resources path = %s ***** \n", path);

    res = url_check(path);
    if (res == FAIL || res == ERROR)
	{
		INCIDENT_TYPE(res);
		return;
	}

   flag=2;

   create_pipeline(path, flag);


    while (loop_count < NUMBER_OF_CHANNEL)
  {      
     if(loop_count==0){
       program_number=257;
       clock_gettime(CLOCK_REALTIME, &streamStart);
       printf("Start time for all the channels: %lfsecs %lfnanosecs\n",(double)streamStart.tv_sec,(double)streamStart.tv_nsec);	
     }
     else if(loop_count==1)
       program_number=272;
     else if(loop_count==2)
       program_number=260;
     else if(loop_count==3)
       program_number=262;
     else if(loop_count==4)
       program_number=259;
 
     net_time += switch_channel(program_number,flag);

     if (loop_count != 0) {
        sumof_channel_start_delay += channel_start_delay;
        g_print (" Time Taken for channel switching = %lf seconds\n", channel_start_delay);
        g_print (" Sum of Time Taken for channel switching = %lf seconds\n", sumof_channel_start_delay);
     } else {
        g_print (" [   Checks: First time -Time Taken for creation of pipeline = %lf seconds\n", pipeline_creation_time);
        g_print (" [   Checks: First time - Time Taken for channel switching = %lf seconds\n", channel_start_delay);
        channel_start_delay = 0;
     }

     GST_DEBUG ("Played channel %d \n",loop_count+1); 
     GST_DEBUG ("\n\n\n");
     loop_count++;
    GST_DEBUG ("GST_START_TEST: EXIT. test_average_time_taken_for_channel_switching()\n");
}  
  GST_DEBUG ("Deleting pipeline\n"); 
  gst_object_unref (GST_OBJECT (pipeline)); 
		MESSAGE_START();
        DESCRIPTION(CHECKS, "Average over %d times - Time Taken for channel switching On same pipeline :: %lf ms\n", (NUMBER_OF_CHANNEL-1), (sumof_channel_start_delay/(NUMBER_OF_CHANNEL-1)) * MSEC);
	    MESSAGE_END();
  if(clock_gettime(CLOCK_REALTIME, &streamEnd) == -1)
  {
		MESSAGE_START();
        DESCRIPTION(ERROR, "Error: clock gettime");
		MESSAGE_END();
		INCIDENT_TYPE(ERROR);
		TESTFUNCTION_END();  
		return;
  }  
  printf("End time for all the channels: %lf secs %lf nanosecs\n",(double)streamEnd.tv_sec,(double)streamEnd.tv_nsec);

  /* Calculate time it took to establish the pipeline connection*/
  double accum = ( streamEnd.tv_sec - streamStart.tv_sec )+( streamEnd.tv_nsec - streamStart.tv_nsec )
  / BILLION;
  printf("Time duration for the entire stream duration:%lf secs\n", accum );
  printf("Net Time taken, channel wise: %lf secs\n",net_time);  

  switching_time=accum-net_time;
  printf("Time elapsed between channel switching :%lf secs\n",switching_time);

    g_print ("GST_START_TEST: EXIT. gstChannelSwitchingPerfOnsamepipelineHttpHosted()\n");   
        MESSAGE_START();
        DESCRIPTION(PASS, "");
        MESSAGE_END();	
    	INCIDENT_TYPE(PASS);
		TESTFUNCTION_END();	
}
GST_END_TEST;

static Suite * media_testsuite (void) {
    Suite *s ;
    TCase *tc_chain ;
    int timeoutvalue = 300;

    GST_DEBUG ("Gstreamer_channel_switching_in_transport_stream_Feature_testsuite(): ENTRY.()\n");

    s = suite_create ("mediasuite");
    tc_chain = tcase_create ("mediachain");

    tcase_set_timeout (tc_chain, timeoutvalue);

    GST_DEBUG ("media_suite():timeoutvalue = %d\n", timeoutvalue);
    suite_add_tcase (s, tc_chain);

    tcase_add_test (tc_chain, gstChannelSwitchingFuncHttpHosted);
    tcase_add_test (tc_chain, gstChannelSwitchingFuncDisplayProgDetailsHttpHosted);
    tcase_add_test (tc_chain, gstChannelSwitchingPerfHttpHosted);
    tcase_add_test (tc_chain, gstChannelSwitchingPerfOnsamepipelineHttpHosted);

    GST_DEBUG ("Gstreamer_channel_switching_in_transport_stream_Feature_testsuite(): EXIT.()\n");

    return s;
}


int main (int argc, char **argv) {
    int nf;
    Suite *s;
    SRunner *sr;

    g_print ("Gstreamer_channel_switching_in_transport_stream_HttpHosted()\n");

    XML_START();
	TESTCASE_START("Gstreamer_channel_switching_in_transport_stream_HttpHosted");
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
