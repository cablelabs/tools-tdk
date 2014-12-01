
#ifdef HAVE_CONFIG_H
# include <config.h>
#endif
#include <gst/check/gstcheck.h>
#include <unistd.h>
#include "gstplayback.h"


static gulong gCurrentPosition = 0;
static float gCurrentPosition_in_seconds = 0.0f;

float mplayer_position_update(GstElement **pipeline) {
    GST_DEBUG ("%s : Entry \n", __func__);
    GstFormat fmt = GST_FORMAT_TIME;
    gint64 pos = 0;

    if (!gst_element_query_position (GST_ELEMENT(*pipeline), &fmt, &pos)) {
    g_printerr ("Unable to retrieve current position.\n");
    return 1.0;
  }
	gCurrentPosition = GST_TIME_AS_MSECONDS(pos);
	gCurrentPosition_in_seconds = gCurrentPosition/1000;
	//g_print ("Current Position=%f in seconds\n", gCurrentPosition_in_seconds);
   GST_DEBUG ("%s : Exit \n", __func__);
	return gCurrentPosition_in_seconds;
}

STATUS mplayer_null (GstElement **pipeline) {

    GST_DEBUG("%s : Entry 2DO \n", __func__);

    if (!*pipeline) 
	{
	    MESSAGE_START();
        DESCRIPTION(FAIL, "Fail: Pipeline creation Failed");
        MESSAGE_END();	
		return FAIL;		
	}
    if (GST_STATE_CHANGE_FAILURE == gst_element_set_state(GST_ELEMENT(*pipeline), GST_STATE_NULL))
	{
        g_print ("Failed to NULL\n");
        MESSAGE_START();
        DESCRIPTION(FAIL, "Fail: Pipeline not set to NULL. Exiting.");
        MESSAGE_END();
		return FAIL;
	}
   GST_DEBUG("%s : Exit \n", __func__);
return PASS;
}

STATUS mplayer_play (GstElement **pipeline) {
    GST_DEBUG ("%s : Entry \n", __func__);
    if (!*pipeline) 
	{
	    MESSAGE_START();
        DESCRIPTION(FAIL, "Fail: Pipeline creation Failed");
        MESSAGE_END();
		return FAIL;
	}	

	if (GST_STATE_CHANGE_FAILURE == gst_element_set_state(GST_ELEMENT(*pipeline), GST_STATE_PLAYING))
	{
        g_print ("Failed to PLAY\n");
        MESSAGE_START();
        DESCRIPTION(FAIL, "Fail: Pipeline not set to PLAYING. Exiting.");
        MESSAGE_END();
        return FAIL;
	}
	g_print ("PLAYING\n");
   GST_DEBUG("%s : Exit \n", __func__);
return PASS;
}

STATUS mplayer_ready (GstElement **pipeline) {
    GST_DEBUG("%s : Entry \n", __func__);
    if (!*pipeline) 
	{
	    MESSAGE_START();
        DESCRIPTION(FAIL, "Fail: Pipeline creation Failed");
        MESSAGE_END();
		return FAIL;
	}
    //mplayer_position_update(mplayer_position_update(mplayer_position_update(pipeline)pipeline)pipeline);

    if (GST_STATE_CHANGE_FAILURE == gst_element_set_state(GST_ELEMENT(*pipeline), GST_STATE_READY))
	{
        g_print ("Failed to Ready\n");
        MESSAGE_START();
        DESCRIPTION(FAIL, "Fail: Pipeline not set to READY. Exiting.");
        MESSAGE_END();		
		return FAIL;
	}
   GST_DEBUG("%s : Exit \n", __func__);
	return PASS;
}

STATUS mplayer_pause (GstElement **pipeline) {
    GST_DEBUG("%s : Entry \n", __func__);
    if (!*pipeline) 
	{
	    MESSAGE_START();
        DESCRIPTION(FAIL, "Fail: Pipeline creation Failed");
        MESSAGE_END();
		return FAIL;
	}

	//mplayer_position_update(mplayer_position_update(mplayer_position_update(pipeline)pipeline)pipeline);

    if (GST_STATE_CHANGE_FAILURE == gst_element_set_state(GST_ELEMENT(*pipeline), GST_STATE_PAUSED))
	{
        g_print ("Failed to PAUSE\n");
        MESSAGE_START();
        DESCRIPTION(FAIL, "Fail: Pipeline not set to PAUSED. Exiting.");
        MESSAGE_END();		
		return FAIL;
	}
	g_print ("PAUSED\n");
   GST_DEBUG("%s : Exit \n", __func__);

	return PASS;
}

STATUS mplayer_stop(GstElement **pipeline) {
    GST_DEBUG("%s : Entry \n", __func__);
	if (!*pipeline) 
	{
	    MESSAGE_START();
        DESCRIPTION(FAIL, "Fail: Pipeline creation Failed");
        MESSAGE_END();
		return FAIL;
	}
    //mplayer_position_update(mplayer_position_update(mplayer_position_update(pipeline)pipeline)pipeline);

    if (GST_STATE_CHANGE_FAILURE == gst_element_set_state(GST_ELEMENT(*pipeline), GST_STATE_NULL))
	{
        g_print ("Failed to STOP\n");
        MESSAGE_START();
        DESCRIPTION(FAIL, "Fail: Pipeline not set to STOP. Exiting.");
        MESSAGE_END();		
		return FAIL;
	}
    gst_object_unref(*pipeline);
	*pipeline = NULL;
	g_print ("STOPPED\n");

   GST_DEBUG("%s : Exit \n", __func__);
	return PASS;
}
