
#ifndef tdkcommon_h__
#define tdkcommon_h__

typedef enum res_status { ERROR = -1, PASS = 0, FAIL,} STATUS;

#define CHECKS 4


//char *str;

#define XML_START() g_print("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
#define TESTCASE_START(name) g_print("<TestCase name=\"%s\">\n", name)
#define TESTCASE_END() g_print("</TestCase>\n")
#define GST_ENV() g_print("<Environment>\n\t<GstVersion>3.4.0</GstVersion>\n\t<GTestVersion>3.4.0</GTestVersion>\n</Environment>\n")
#define TESTFUNCTION_START() g_print("<TestFunction name=\"%s\">\n", __func__ )
#define TESTFUNCTION_END() g_print("</TestFunction>\n")
#define MESSAGE_START() g_print("<Message type=\"g_print\"> \n")
#define DESCRIPTION(prio, msg, ...) \
                                     if (prio == CHECKS) \
                                      g_print ("<Description> Checks: "msg"</Description>\n", ##__VA_ARGS__); \
                                     else if (prio == ERROR || prio == FAIL || prio == PASS) \
                                      g_print ("<Description>"msg"</Description>\n", ##__VA_ARGS__)
                                       
#define MESSAGE_END() g_print("</Message>\n")
#define INCIDENT_TYPE(result)   if (result == PASS) \
                                                                        g_print ("<Incident type=\"PASS\"/>\n"); \
                                                                else if (result == FAIL) \
                                                                        g_print ("<Incident type=\"FAIL\"/>\n"); \
                                                                else  g_print ("<Incident type=\"ERROR\"/>\n");
																
#endif  // gstplayback_h__																
