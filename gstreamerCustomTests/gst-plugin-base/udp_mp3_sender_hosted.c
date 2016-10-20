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

#include "common/gstplayback.h"


static gboolean evtHandler (GstBus *bus, GstMessage *msg, gpointer data)
{
  GMainLoop *loop = (GMainLoop *) data;

  switch (GST_MESSAGE_TYPE (msg)) {

    case GST_MESSAGE_EOS:
      g_print ("EOS : End of stream\n");
      g_main_loop_quit (loop);
      break;

    case GST_MESSAGE_ERROR: {
      gchar  *debug;
      GError *error;

      /* Parse the error message*/
      gst_message_parse_error (msg, &error, &debug);
      g_free (debug);
      /* Print error message */
      g_printerr ("Error: %s\n", error->message);
      g_error_free (error);

      /*Quit main loop on error */
      g_main_loop_quit (loop);
      break;
    }
    default:
      break;
  }

  return TRUE;
}

static void on_pad_added_evtHandler (GstElement *element, 
              GstPad     *pad, 
              gpointer    data) 
{ 
  GstPad *sinkpad; 
  GstElement *decoder = (GstElement *) data; 

  /* We can now link this pad with the vorbis-decoder sink pad */ 
  g_print ("Dynamic pad created, linking demuxer/decoder\n"); 
  sinkpad = gst_element_get_static_pad (decoder, "sink"); 
  /* Link pad */
  gst_pad_link (pad, sinkpad); 
  gst_object_unref (sinkpad); 
} 

int main (int argc, char *argv[])
{
  
  GMainLoop *loop;
  GstElement *pipeline, *filesrc, *demuxer, *audioqueue, *rtppay, *udpsink;
  GstBus *bus;

  /* Initialisation */
  gst_init (&argc, &argv);

  loop = g_main_loop_new (NULL, FALSE);

	/* Check input arguments */
	if (argc != 4) {
		g_printerr ("Usage: %s \"filename_path\" \"port_number\" \"host_ip_address\"\n", argv[0]);
		MESSAGE_START();
		DESCRIPTION(ERROR, "Usage: %s \"filename_path\" \"port_number\" \"host_ip_address\"\n", argv[0]);
		MESSAGE_END();
		INCIDENT_TYPE(ERROR);		
		return -1;    	
	}

	/* Create gstreamer elements */
	pipeline = gst_pipeline_new ("video-player");
	filesrc = gst_element_factory_make ("souphttpsrc", "filesrc");
	demuxer = gst_element_factory_make ("id3demux", "demuxer");
	audioqueue = gst_element_factory_make ("queue", "audioqueue");
	rtppay= gst_element_factory_make ("rtpmpapay", "rtppay");
	udpsink = gst_element_factory_make ("udpsink", "udpsink");
  


	if (!pipeline || !filesrc || !demuxer || !audioqueue || !rtppay || !udpsink)
	{
		//g_printerr ("One element could not be created. Exiting.\n");
		MESSAGE_START();
		DESCRIPTION(ERROR, "%s: Pipeline creation FAILED\n", argv[0]);
		MESSAGE_END();
		INCIDENT_TYPE(ERROR);		
		return -1;    	
	}

  /* Set up the pipeline */
  g_print ("Elements are created\n");
  

  /* set the properties of other elements */
  g_object_set (G_OBJECT (filesrc), "location", argv[1], NULL);
  g_object_set (G_OBJECT (udpsink), "port", atoi(argv[2]), NULL);
  g_object_set (G_OBJECT (udpsink), "host", argv[3], NULL);

  /* we add a message handler */
  bus = gst_pipeline_get_bus (GST_PIPELINE (pipeline));
  gst_bus_add_watch (bus, evtHandler, loop);
  gst_object_unref (bus);


	/* we add all elements into the pipeline */
	gst_bin_add_many (GST_BIN (pipeline), filesrc, demuxer, audioqueue, rtppay, udpsink, NULL);
	g_print ("Added all the Elements into the pipeline\n");


	/* we link the elements together */
	gst_element_link (filesrc, demuxer);
	g_signal_connect (demuxer, "pad-added", G_CALLBACK (on_pad_added_evtHandler), audioqueue);
	gst_element_link_many (audioqueue, rtppay, udpsink, NULL);
   
	g_print ("Linked all the Elements together\n");


	/* Set the pipeline to "playing" state*/
	g_print ("Streaming to port: %s\n", argv[2]);
	if (GST_STATE_CHANGE_FAILURE == gst_element_set_state(GST_ELEMENT(pipeline), GST_STATE_PLAYING))
	{
        GST_DEBUG ("Failed to PLAY\n");
        MESSAGE_START();
        DESCRIPTION(FAIL, "Fail: Pipeline not set to PLAYING. Exiting.");
        MESSAGE_END();
		INCIDENT_TYPE(FAIL);
        return -1;
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
		INCIDENT_TYPE(FAIL);		
        return -1;
	}

	g_print ("Deleting pipeline\n");
	gst_object_unref (GST_OBJECT (pipeline));
	MESSAGE_START();
    DESCRIPTION(PASS, "");
    MESSAGE_END(); 
	INCIDENT_TYPE(PASS);	
    return 0;
}

