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

