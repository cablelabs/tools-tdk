#ifndef gstplayback_h__
#define gstplayback_h__

#include "tdkcommon.h"

extern STATUS mplayer_null (GstElement **pipeline );
extern STATUS mplayer_ready (GstElement **pipeline);
extern STATUS mplayer_pause (GstElement **pipeline);
extern STATUS mplayer_play (GstElement **pipeline);
extern STATUS mplayer_stop (GstElement **pipeline);
extern float mplayer_position_update(GstElement **pipeline);

#endif  // gstplayback_h__

