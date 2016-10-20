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

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#include <gst/check/gstcheck.h>
#include <string.h>


/*AESDECRYPT START*/
static void
cleanup_aesdecrypt (GstElement * aesdecrypt)
{
#if 1
  gst_check_teardown_src_pad (aesdecrypt);
  gst_check_teardown_sink_pad (aesdecrypt);
  gst_check_teardown_element (aesdecrypt);
#endif

  GST_INFO ("in plugin clenup \n");

}

char propValue[264]={'\0'};

GST_START_TEST (test_decryption_enable_prop_set)
{
  GstElement *decrypt;
  gint value; 
  int pValue;	

  /* aesdecrypt setup */
  decrypt = gst_check_setup_element ("aesdecrypt");
  GST_INFO ("In setup_aesdecrypt done \n");
 
  pValue = atoi(propValue);
  GST_INFO ("set property value: %d \n",pValue);
  g_object_set (G_OBJECT (decrypt), "decryption-enable",pValue, NULL);
  
  g_object_get(decrypt,"decryption-enable",&value,NULL);
  
  GST_INFO("After get: Value is:%d \n",value);

  fail_unless_equals_int(pValue,value);  
  
  GST_INFO("In test case test_decryption_enable_prop_set \n");
  GST_INFO ("Before cleanup\n"); 

  /* cleanup */
  cleanup_aesdecrypt (decrypt);
}

GST_END_TEST;


GST_START_TEST (test_decryption_enable_prop_get)
{
  GstElement *decrypt;
  gint value; 

  /* aesdecrypt setup */
  decrypt = gst_check_setup_element ("aesdecrypt");
  GST_INFO ("In setup_aesdecrypt done \n");
 
  g_object_get(decrypt,"decryption-enable",&value,NULL);
  
  GST_INFO("After get: Value is:%d \n",value);

  fail_unless_equals_int(1,value);  
  
  GST_INFO("In test case test_decryption_enable_prop_get \n");
  GST_INFO ("Before cleanup\n"); 
  /* cleanup */
  cleanup_aesdecrypt (decrypt);
}

GST_END_TEST;
/*AESDECRYPT END*/


/*AESENCRYPT START*/
static void
cleanup_aesencrypt (GstElement * aesencrypt)
{
#if 1
  gst_check_teardown_src_pad (aesencrypt);
  gst_check_teardown_sink_pad (aesencrypt);
  gst_check_teardown_element (aesencrypt);
#endif

  GST_INFO ("in plugin clenup \n");

}


GST_START_TEST (test_encryption_enable_prop_set)
{
  GstElement *encrypt;
  gint value; 
  int pValue;	

  /* aesencrypt setup */
  encrypt = gst_check_setup_element ("aesencrypt");
  GST_INFO ("In setup_aesencrypt done \n");
 
  pValue = atoi(propValue);
  GST_INFO ("set property value: %d \n",pValue);
  g_object_set (G_OBJECT (encrypt), "encryption-enable",pValue, NULL);
  
  g_object_get(encrypt,"encryption-enable",&value,NULL);
  
  GST_INFO("After get: Value is:%d \n",value);

  fail_unless_equals_int(pValue,value);  
  
  GST_INFO("In test case test_encryption_enable_prop_set \n");
  GST_INFO ("Before cleanup\n"); 

  /* cleanup */
  cleanup_aesencrypt (encrypt);
}

GST_END_TEST;


GST_START_TEST (test_encryption_enable_prop_get)
{
  GstElement *encrypt;
  gint value; 

  /* aesencrypt setup */
  encrypt = gst_check_setup_element ("aesencrypt");
  GST_INFO ("In setup_aesencrypt done \n");
 
  GST_INFO("Before property get \n");
  g_object_get(encrypt,"encryption-enable",&value,NULL);
  
  GST_INFO("After get: Value is:%d \n",value);

  fail_unless_equals_int(1,value);  
  
  GST_INFO("In test case test_encryption_enable_prop_get \n");
  GST_INFO ("Before cleanup\n"); 

  /* cleanup */
  cleanup_aesencrypt (encrypt);
}

GST_END_TEST;
/*AESENCRYPT END*/


/*DVRSRC START*/
#if 1
static void
cleanup_dvrsrc(GstElement * dvrsrc)
{
/*FIXME:*/
#if 0
  gst_check_teardown_src_pad (dvrsrc);
  gst_check_teardown_element (dvrsrc);
#endif

  GST_INFO ("in plugin clenup \n");

}

GST_START_TEST (test_dvrsrc_recordid_prop_set)
{
  GstElement *dvrsrc;
  char value[254] = {'\0'};

  /* dvrsrc setup */
  dvrsrc = gst_check_setup_element ("dvrsrc");
  GST_INFO ("In setup_dvrsrc done \n");

  GST_INFO ("In dvrsrc recordid to be set: %s \n",propValue);
  g_object_set(G_OBJECT(dvrsrc),"recording-id",propValue,NULL);

  g_object_get(dvrsrc,"recording-id",value,NULL);

  GST_INFO("After get: Value is: %s \n",value);

  GST_INFO("In test case test_dvrsrc_recordid_prop_set \n");
  GST_INFO ("Before cleanup\n");

  /* cleanup */
  cleanup_dvrsrc(dvrsrc);
}

GST_END_TEST;


GST_START_TEST (test_dvrsrc_recordid_prop_get)
{
  GstElement *dvrsrc;
  char value[254] = {'\0'};

  /* dvrsrc setup */
  dvrsrc = gst_check_setup_element ("dvrsrc");
  GST_INFO ("In setup_dvrsrc done \n");

  g_object_get(dvrsrc,"recording-id",value,NULL);
  GST_INFO("After get: Value is: %s \n",value);

  GST_INFO("In test case test_dvrsrc_recordid_prop_get \n");
  GST_INFO ("Before cleanup\n");

  /* cleanup */
  cleanup_dvrsrc(dvrsrc);
}

GST_END_TEST;

GST_START_TEST (test_dvrsrc_segmentname_prop_set)
{
  GstElement *dvrsrc;
  long long value = 0;
  long long sValue = 0;

  /* dvrsrc setup */
  dvrsrc = gst_check_setup_element ("dvrsrc");
  GST_INFO ("In setup_dvrsrc done \n");

  sValue = atoll(propValue);
  GST_INFO ("set dvrsrc property segment-name: %lld \n",sValue);
   
  g_object_set (G_OBJECT (dvrsrc), "segment-name",sValue, NULL);

  g_object_get(dvrsrc,"segment-name",&value,NULL);
  GST_INFO("After get: Value is:%lld \n",value);

  GST_INFO("In test case test_dvrsrc_segmentname_prop_set \n");
  GST_INFO ("Before cleanup\n");

  /* cleanup */
  cleanup_dvrsrc(dvrsrc);
}

GST_END_TEST;
#endif

#if 1
GST_START_TEST (test_dvrsrc_segmentname_prop_get)
{
  GstElement *dvrsrc;
  long long value = 0;

  /* dvrsrc setup */
  dvrsrc = gst_check_setup_element ("dvrsrc");
  GST_INFO ("In setup_dvrsrc done \n");

  g_object_get(dvrsrc,"segment-name",&value,NULL);
  GST_INFO("After get: Value is:%lld \n",value);

  fail_unless_equals_int(0,value);

  GST_INFO("In test case test_dvrsrc_segmentname_prop_get \n");
  GST_INFO ("Before cleanup\n");

  /* cleanup */
  cleanup_dvrsrc(dvrsrc);
}

GST_END_TEST;



GST_START_TEST (test_dvrsrc_ccivalue_prop_get)
{
  GstElement *dvrsrc;
  int value = 0;

  /* aesdecrypt setup */
  dvrsrc = gst_check_setup_element ("dvrsrc");
  GST_INFO ("In setup_dvrsrc done \n");

  g_object_get(dvrsrc,"ccivalue",&value,NULL);
  GST_INFO("After get: Value is:%d \n",value);

  fail_unless_equals_int(0,value);

  GST_INFO("In test case test_dvrsrc_ccivalue_prop_get \n");
  GST_INFO ("Before cleanup\n");

  /* cleanup */
  cleanup_dvrsrc(dvrsrc);
}

GST_END_TEST;
#endif

GST_START_TEST (test_dvrsrc_rate_prop_set)
{
  GstElement *dvrsrc;
  float rValue = 0.0;
  float value = 0.0;

  /* aesdecrypt setup */
  dvrsrc = gst_check_setup_element ("dvrsrc");
  GST_INFO ("In setup_dvrsrc done \n");

  rValue = atof(propValue);
  GST_INFO ("Value to set: %f \n",rValue);
  g_object_set(dvrsrc,"rate",&rValue,NULL);
	
  g_object_get(dvrsrc,"rate",&value,NULL);
  GST_INFO("After get: Value is:%f \n",value);

  fail_unless_equals_float(rValue,value);

  GST_INFO("In test case test_dvrsrc_rate_prop_set \n");
  GST_INFO ("Before cleanup\n");

  /* cleanup */
  cleanup_dvrsrc(dvrsrc);
}

GST_END_TEST;

GST_START_TEST (test_dvrsrc_rate_prop_get)
{
  GstElement *dvrsrc;
  float value = 1.0;

  /* aesdecrypt setup */
  dvrsrc = gst_check_setup_element ("dvrsrc");
  GST_INFO ("In setup_dvrsrc done \n");

  g_object_get(dvrsrc,"rate",&value,NULL);
  GST_INFO("After get: Value is:%f \n",value);

  fail_unless_equals_float(1.0,value);

  GST_INFO("In test case test_dvrsrc_rate_prop_get \n");
  GST_INFO ("Before cleanup\n");

  /* cleanup */
  cleanup_dvrsrc(dvrsrc);
}

GST_END_TEST;


GST_START_TEST (test_dvrsrc_starttime_prop_get)
{
  GstElement *dvrsrc;
  float value = 0.0;

  /* dvrsrc setup */
  dvrsrc = gst_check_setup_element ("dvrsrc");
  GST_INFO ("In setup_dvrsrc done \n");

  g_object_get(dvrsrc,"start-time",&value,NULL);
  GST_INFO("After get: Value is:%f \n",value);

  fail_unless_equals_float(0.0,value);

  GST_INFO("In test case test_dvrsrc_starttime_prop_get \n");
  GST_INFO ("Before cleanup\n");

  /* cleanup */
  cleanup_dvrsrc(dvrsrc);
}

GST_END_TEST;


GST_START_TEST (test_dvrsrc_duration_prop_get)
{
  GstElement *dvrsrc;
  float value = 0.0;

  /* dvrsrc setup */
  dvrsrc = gst_check_setup_element ("dvrsrc");
  GST_INFO ("In setup_dvrsrc done \n");

  g_object_get(dvrsrc,"duration",&value,NULL);
  GST_INFO("After get: Value is:%f \n",value);

  fail_unless_equals_float(0.0,value);

  GST_INFO("In test case test_dvrsrc_duration_prop_get \n");
  GST_INFO ("Before cleanup\n");

  /* cleanup */
  cleanup_dvrsrc(dvrsrc);
}

GST_END_TEST;

GST_START_TEST (test_dvrsrc_playstartposition_prop_set)
{
  GstElement *dvrsrc;
  float value = 0.0;
  float rValue = 0.0;

  /* dvrsrc setup */
  dvrsrc = gst_check_setup_element ("dvrsrc");
  GST_INFO ("In setup_dvrsrc done \n");
  
  rValue = atof(propValue);
  GST_INFO ("In dvrsrc startposition to be set: %f \n",rValue);

  g_object_set(G_OBJECT(dvrsrc),"play-start-position",rValue,NULL);

  g_object_get(dvrsrc,"play-start-position",&value,NULL);
  GST_INFO("After get: Value is:%f \n",value);

  fail_unless_equals_float(rValue,value);

  GST_INFO("In test case test_dvrsrc_playstartposition_prop_get \n");
  GST_INFO ("Before cleanup\n");

  /* cleanup */
  cleanup_dvrsrc(dvrsrc);
}

GST_END_TEST;


GST_START_TEST (test_dvrsrc_playstartposition_prop_get)
{
  GstElement *dvrsrc;
  float value = 0.0;

  /* dvrsrc setup */
  dvrsrc = gst_check_setup_element ("dvrsrc");
  GST_INFO ("In setup_dvrsrc done \n");

  g_object_get(dvrsrc,"play-start-position",&value,NULL);
  GST_INFO("After get: Value is:%f \n",value);

  fail_unless_equals_float(0.0,value);

  GST_INFO("In test case test_dvrsrc_playstartposition_prop_get \n");
  GST_INFO ("Before cleanup\n");

  /* cleanup */
  cleanup_dvrsrc(dvrsrc);
}

GST_END_TEST;

/*DVRSRC END*/


/*DVRSINK START*/
static void
cleanup_dvrsink(GstElement * dvrsink)
{
/*FIXME:*/
#if 0
  gst_check_teardown_src_pad (dvrsink);
  gst_check_teardown_element (dvrsink);
#endif

  GST_INFO ("in plugin clenup \n");

}

GST_START_TEST (test_dvrsink_recordid_prop_set)
{
  GstElement *dvrsink;
  char value[254] = {'\0'};

  /* dvrsink setup */
  dvrsink = gst_check_setup_element ("dvrsink");
  GST_INFO ("In setup_dvrsink done \n");

  GST_INFO ("recordid to be set: %s \n",propValue);
  g_object_set(G_OBJECT(dvrsink),"recording-id",propValue,NULL);

  g_object_get(dvrsink,"recording-id",value,NULL);
  GST_INFO("After get: Value is: %s \n",value);

  GST_INFO("In test case test_dvrsink_recordid_prop_set \n");
  GST_INFO ("Before cleanup\n");

  /* cleanup */
  cleanup_dvrsink(dvrsink);
}

GST_END_TEST;


GST_START_TEST (test_dvrsink_recordid_prop_get)
{
  GstElement *dvrsink;
  char value[254] = {'\0'};

  /* dvrsink setup */
  dvrsink = gst_check_setup_element ("dvrsink");
  GST_INFO ("In setup_dvrsink done \n");

  g_object_get(dvrsink,"recording-id",value,NULL);
  GST_INFO("After get: Value is: %s \n",value);

  GST_INFO("In test case test_dvrsink_recordid_prop_get \n");
  GST_INFO ("Before cleanup\n");

  /* cleanup */
  cleanup_dvrsink(dvrsink);
}

GST_END_TEST;


GST_START_TEST (test_dvrsink_ccivalue_prop_get)
{
  GstElement *dvrsink;
  int value = 0;

  /* dvrsink setup */
  dvrsink = gst_check_setup_element ("dvrsink");
  GST_INFO ("In setup_dvrsink done \n");

  g_object_get(dvrsink,"ccivalue",&value,NULL);
  GST_INFO("After get: Value is: %d \n",value);

  fail_unless_equals_float(0,value);

  GST_INFO("In test case test_dvrsink_ccivalue_prop_get \n");
  GST_INFO ("Before cleanup\n");

  /* cleanup */
  cleanup_dvrsink(dvrsink);
}

GST_END_TEST;
/*DVRSINK END*/

char tcname[264];

static Suite *
gst_plugins_rdk_suite (void)
{
  Suite *gstPluginsSuite = suite_create ("gst_plugins_rdk");
  TCase *tc_chain = tcase_create ("general");

  suite_add_tcase (gstPluginsSuite, tc_chain);
  GST_INFO("tc name is %s\n",tcname);
  
  if(strcmp("test_decryption_enable_prop_set",tcname) == 0)
  {
     tcase_add_test (tc_chain, test_decryption_enable_prop_set);
     GST_INFO("tc %s run successfull\n",tcname);
     GST_INFO("SUCCESS\n");
  } 
  else if(strcmp("test_decryption_enable_prop_get",tcname) == 0)
  {
     tcase_add_test (tc_chain, test_decryption_enable_prop_get);
     GST_INFO("tc %s run successfull\n",tcname);
     GST_INFO("SUCCESS\n");
  } 
  else if(strcmp("test_encryption_enable_prop_set",tcname) == 0)
  {
     tcase_add_test (tc_chain, test_encryption_enable_prop_set);
     GST_INFO("tc %s run successfull\n",tcname);
     GST_INFO("SUCCESS\n");
  } 
  else if(strcmp("test_encryption_enable_prop_get",tcname) == 0)
  {
     tcase_add_test (tc_chain, test_encryption_enable_prop_get);
     GST_INFO("tc %s run successfull\n",tcname);
     GST_INFO("SUCCESS\n");
  } 
  else if(strcmp("test_dvrsrc_recordid_prop_set",tcname) == 0)
  {
     tcase_add_test (tc_chain, test_dvrsrc_recordid_prop_set);
     GST_INFO("tc %s run successfull\n",tcname);
     GST_INFO("SUCCESS\n");
  }
  else if(strcmp("test_dvrsrc_recordid_prop_get",tcname) == 0)
  {
     tcase_add_test (tc_chain, test_dvrsrc_recordid_prop_get);
     GST_INFO("tc %s run successfull\n",tcname);
     GST_INFO("SUCCESS\n");
  }
  else if(strcmp("test_dvrsrc_segmentname_prop_set",tcname) == 0)
  {
     tcase_add_test (tc_chain, test_dvrsrc_segmentname_prop_set);
     GST_INFO("tc %s run successfull\n",tcname);
     GST_INFO("SUCCESS\n");
  }
  else if(strcmp("test_dvrsrc_segmentname_prop_get",tcname) == 0)
  {
     tcase_add_test (tc_chain, test_dvrsrc_segmentname_prop_get);
     GST_INFO("tc %s run successfull\n",tcname);
     GST_INFO("SUCCESS\n");
  }
  else if(strcmp("test_dvrsrc_ccivalue_prop_get",tcname) == 0)
  {
     tcase_add_test (tc_chain, test_dvrsrc_ccivalue_prop_get);
     GST_INFO("tc %s run successfull\n",tcname);
     GST_INFO("SUCCESS\n");
  }
  else if(strcmp("test_dvrsrc_rate_prop_set",tcname) == 0)
  {
     tcase_add_test (tc_chain, test_dvrsrc_rate_prop_set);
     GST_INFO("tc %s run successfull\n",tcname);
     GST_INFO("SUCCESS\n");
  }
  else if(strcmp("test_dvrsrc_rate_prop_get",tcname) == 0)
  {
     tcase_add_test (tc_chain, test_dvrsrc_rate_prop_get);
     GST_INFO("tc %s run successfull\n",tcname);
     GST_INFO("SUCCESS\n");
  }
  else if(strcmp("test_dvrsrc_starttime_prop_get",tcname) == 0)
  {
     tcase_add_test (tc_chain, test_dvrsrc_starttime_prop_get);
     GST_INFO("tc %s run successfull\n",tcname);
     GST_INFO("SUCCESS\n");
  }
  else if(strcmp("test_dvrsrc_duration_prop_get",tcname) == 0)
  {
     tcase_add_test (tc_chain, test_dvrsrc_duration_prop_get);
     GST_INFO("tc %s run successfull\n",tcname);
     GST_INFO("SUCCESS\n");
  }
  else if(strcmp("test_dvrsrc_playstartposition_prop_set",tcname) == 0)
  {
     tcase_add_test (tc_chain, test_dvrsrc_playstartposition_prop_set);
     GST_INFO("tc %s run successfull\n",tcname);
     GST_INFO("SUCCESS\n");
  }
  else if(strcmp("test_dvrsrc_playstartposition_prop_get",tcname) == 0)
  {
     tcase_add_test (tc_chain, test_dvrsrc_playstartposition_prop_get);
     GST_INFO("tc %s run successfull\n",tcname);
     GST_INFO("SUCCESS\n");
  }
  else if(strcmp("test_dvrsink_recordid_prop_set",tcname) == 0)
  {
     tcase_add_test (tc_chain, test_dvrsink_recordid_prop_set);
     GST_INFO("tc %s run successfull\n",tcname);
     GST_INFO("SUCCESS\n");
  }
  else if(strcmp("test_dvrsink_recordid_prop_get",tcname) == 0)
  {
     tcase_add_test (tc_chain, test_dvrsink_recordid_prop_get);
     GST_INFO("tc %s run successfull\n",tcname);
     GST_INFO("SUCCESS\n");
  }
  else if(strcmp("test_dvrsink_ccivalue_prop_get",tcname) == 0)
  {
     tcase_add_test (tc_chain, test_dvrsink_ccivalue_prop_get);
     GST_INFO("tc %s run successfull\n",tcname);
     GST_INFO("SUCCESS\n");
  }
  return gstPluginsSuite;
}


int main(int argc, char **argv)
{
	Suite *s;
	
	if(argc == 2)
	{
		strcpy(tcname,argv[1]);
		GST_INFO("\nArg 2: TestCase Name: %s \n",tcname);
	}
	else if(argc == 3)
	{
		strcpy(tcname,argv[1]);
		strcpy(propValue,argv[2]);
		
		GST_INFO("\nArg 3: TestCase Name: %s \n",tcname);
		GST_INFO("propValue: %s \n",propValue);
	}
	else
	{
		GST_INFO("FALIURE \n");
		return 0;
	}
	
	gst_check_init(&argc,&argv);
	s = gst_plugins_rdk_suite();
	return gst_check_run_suite (s,"gst_plugins_rdk", __FILE__);	
}
