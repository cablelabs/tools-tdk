/*
 * ============================================================================
 * COMCAST C O N F I D E N T I A L AND PROPRIETARY
 * ============================================================================
 * This file (and its contents) are the intellectual property of Comcast.  It may
 * not be used, copied, distributed or otherwise  disclosed in whole or in part
 * without the express written permission of Comcast.
 * ============================================================================
 * Copyright (c) 2014 Comcast. All rights reserved.
 * ============================================================================
 */

#include <stdio.h>
#include <unistd.h>
#include <gst/gst.h>
#include <string.h>
#include <math.h>

GstElement *pipeline, *plug;
static gulong gCurrentPosition = 0;

#define MPLAYER_PLAYBIN  "playbin2"



static gboolean bus_call(GstBus * bus, GstMessage * msg, gpointer data)
{
	g_print("[MediaPlayer bus_call] msg=%d,%s \n", GST_MESSAGE_TYPE(msg), GST_MESSAGE_TYPE_NAME(msg));

	switch (GST_MESSAGE_TYPE (msg))
	{
		case GST_MESSAGE_EOS:
			g_print ("End of stream\n");
			break;
		case GST_MESSAGE_ERROR:
		case GST_MESSAGE_WARNING:
		case GST_MESSAGE_APPLICATION:
			{
				gchar *debug;
				GError *error;
				gst_message_parse_error (msg, &error, &debug);
				g_free (debug);
				g_printerr ("Error: %s\n", error->message);
				g_error_free (error);
				break;
			}
		case GST_MESSAGE_STATE_CHANGED:
			g_print ("State Change...\n");
		default: 
			break;
	}

	return TRUE;
}

static void mplayer_position_update()
{
	GstFormat fmt = GST_FORMAT_TIME;
	gint64 pos = 0;

	gst_element_query_position (pipeline, &fmt, &pos);
	gCurrentPosition = GST_TIME_AS_MSECONDS(pos);
	g_print ("Current Position=%lu\n", gCurrentPosition);
	return;
}
static void load_url (char* pURL)
{
	if (pURL)
	{
		/*Set the input filename to the source element */
		g_print ("url = %s\n", pURL);
		g_object_set (G_OBJECT (plug), "uri", pURL, NULL);
	}
	else
	{
		g_print ("Invalid URL..\n");
	}
}

/* Wrapper Function for gst_element_factory_make for creating an element*/
static GstElement *gst_element_factory_make_or_warn (const gchar * type, gchar * name)
{
	GstElement *element = gst_element_factory_make (type, name);
	if (!element) {
		g_warning ("Failed to create element %s of type %s", name, type);
	}
	return element;
}

static int load_elements (char* pURL)
{
	g_print("In load element before pipeline\n");
	/* Create gstreamer elements */
	pipeline = gst_pipeline_new ("Mplayer-Standalone");
	plug = gst_element_factory_make(MPLAYER_PLAYBIN, NULL);


	/* Set the source path to get the stream from */
	load_url (pURL);

	/* Add Elements to the pipelines */
	gst_bin_add_many (GST_BIN(pipeline), plug, NULL);
	if(!gst_bin_add_many)
	{
		g_print("add many to bin  failed\n");
	}
        else
        {
         g_print(" add many to bin success\n");
        }

	/*listening for End Of Stream (EOS) events, etc.*/
	GstBus* bin_bus = gst_pipeline_get_bus(GST_PIPELINE(pipeline));
	gst_bus_add_watch(bin_bus, bus_call, NULL);
	gst_object_unref(bin_bus);
	return 0;
	}

void mplayer_play (void)
{
	if (!pipeline) return;

	if (GST_STATE_CHANGE_FAILURE == gst_element_set_state(GST_ELEMENT(pipeline), GST_STATE_PLAYING))
	{
		g_print ("Failed to PLAY\n");
		return;
	}
}

void mplayer_ready (void)
{
	if (!pipeline) return;

	mplayer_position_update();

	if (GST_STATE_CHANGE_FAILURE == gst_element_set_state(GST_ELEMENT(pipeline), GST_STATE_READY))
	{
		g_print ("Failed to PAUSE\n");
		return;
	}
}

void mplayer_pause (void)
{
	if (!pipeline) return;

	mplayer_position_update();

	if (GST_STATE_CHANGE_FAILURE == gst_element_set_state(GST_ELEMENT(pipeline), GST_STATE_PAUSED))
	{
		g_print ("Failed to PAUSE\n");
		return;
	}

}

void mplayer_stop()
{

	if (!pipeline) return;

	mplayer_position_update();

	gst_element_set_state(GST_ELEMENT(pipeline), GST_STATE_NULL);

	gst_object_unref(pipeline);

	pipeline = NULL;
	plug = NULL;
	g_print ("STOPPED\n");
}


int main (int argc, char *argv[])
{
    char *pCurrentURL = NULL;
    char *pPlayURL1 = NULL;
    char *pPlayURL2 = NULL;
    int loopFlag = 1;
    char* inputCommand = 0;
    char arr[1024] = "";
    /* Check input arguments */
    if (argc < 2)
    {
        g_printerr ("Usage: %s <url to play>\n", argv[0]);
        return -1;
    }
    pPlayURL1 = argv[1];
    pPlayURL2 = argv[2];
    /* Initialisation */
    gst_init (&argc, &argv);
    load_elements (pPlayURL1);
    pCurrentURL = pPlayURL1;
    inputCommand=argv[2];
    char mplayerOption = *argv[2];
    if(mplayerOption=='l')
    {
	 g_print("Mediastreamer streaming Interface testing \n");
         mplayer_play();
	 sleep(30);
         mplayer_stop();
    }
    else
    {
         g_print("Invalid option to play the URL \n");
    }    
    return 0;
}



