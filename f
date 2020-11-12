[1mdiff --git a/dji_asdk_to_python/mission_action/mission_action.py b/dji_asdk_to_python/mission_action/mission_action.py[m
[1mindex 386e307..091cc0f 100644[m
[1m--- a/dji_asdk_to_python/mission_action/mission_action.py[m
[1m+++ b/dji_asdk_to_python/mission_action/mission_action.py[m
[36m@@ -29,7 +29,7 @@[m [mclass MissionAction:[m
             message_data={"coordinate": coordinate.__dict__, "altitude": altitude},[m
         )[m
 [m
[31m-        return_type = None[m
[32m+[m[32m        return_type = DJIError[m
 [m
         blocking = callback is None[m
 [m
[36m@@ -57,7 +57,7 @@[m [mclass MissionAction:[m
             message_data={"angle": angle, "isAbsolute": isAbsolute},[m
         )[m
 [m
[31m-        return_type = None[m
[32m+[m[32m        return_type = DJIError[m
 [m
         blocking = callback is None[m
 [m
