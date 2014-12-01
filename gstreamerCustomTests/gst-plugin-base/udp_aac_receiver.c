
//gst-launch udpsrc port=6969 caps = "application/x-rtp" ! rtppcmadepay ! filesink location=udp_aac.aac


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

  /* We can now link this pad with the decoder sink pad */ 
  g_print ("Dynamic pad created, linking demuxer/decoder\n"); 
  sinkpad = gst_element_get_static_pad (decoder, "sink"); 
  /* Link pad */
  gst_pad_link (pad, sinkpad); 
  gst_object_unref (sinkpad);  
} 


int main (int argc, char *argv[])
{
  GMainLoop *loop;
  GstElement *pipeline, *udpsrc, *rtpdepay, *filesink;
  GstCaps *filtercaps;
  GstBus *bus;

  /* Initialisation */
  gst_init (&argc, &argv);

  loop = g_main_loop_new (NULL, FALSE);

/* Check input arguments */
  if (argc != 3) {
    		g_printerr ("Usage: %s \"filename_path\" \"port_number\"\n", argv[0]);
		MESSAGE_START();
    		DESCRIPTION(ERROR, "Usage: %s \"file_path\" \"port_number\"\n", argv[0]);
		MESSAGE_END();
		INCIDENT_TYPE(ERROR);    
	return -1;
  }

  /* Create gstreamer elements */
  pipeline = gst_pipeline_new ("video-player");
  udpsrc = gst_element_factory_make ("udpsrc", "udpsrc");
  rtpdepay= gst_element_factory_make ("rtppcmadepay", "rtpdepay");
  filesink = gst_element_factory_make ("filesink", "filesink");
  


  if (!pipeline || !udpsrc ||  !rtpdepay || !filesink)
{
    //g_printerr ("One element could not be created. Exiting.\n");
		MESSAGE_START();
		DESCRIPTION(ERROR, "%s : Pipeline creation Failed \n", argv[0]);
		MESSAGE_END();
		INCIDENT_TYPE(ERROR);		
    return -1;
  }

  /* Set up the pipeline */
  g_print ("Elements are created\n");
  filtercaps = gst_caps_new_simple ("application/x-rtp", NULL);

  /* set the properties of other elements */
  g_object_set (G_OBJECT (filesink), "location", argv[1], NULL);
  g_object_set (G_OBJECT (udpsrc),  "port", atoi(argv[2]), "caps", filtercaps, NULL);


  /* we add a message handler */
  bus = gst_pipeline_get_bus (GST_PIPELINE (pipeline));
  gst_bus_add_watch (bus, evtHandler, loop);
  gst_object_unref (bus);


 /* we add all elements into the pipeline */
  gst_bin_add_many (GST_BIN (pipeline), udpsrc, rtpdepay, filesink, NULL);
  g_print ("Added all the Elements into the pipeline\n");


  /* we link the elements together */
  gst_element_link_many (udpsrc, rtpdepay, filesink, NULL);
   
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
  gst_caps_unref (filtercaps);
	MESSAGE_START();
    DESCRIPTION(PASS, "");
    MESSAGE_END(); 
	INCIDENT_TYPE(PASS);  
  return 0;
}

