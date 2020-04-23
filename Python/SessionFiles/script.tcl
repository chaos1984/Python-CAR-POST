 set mode_num 6
 #####################################
 #####################################
 proc ReleaseHandleAll {} {
    catch { page ReleaseHandle         }
    catch { win ReleaseHandle          }
    catch { post1 ReleaseHandle        }
    catch { ren ReleaseHandle          }
    catch { mod ReleaseHandle          }
    catch { res ReleaseHandle          }
    catch { contour_ctrl ReleaseHandle }
    catch { leg ReleaseHandle          }
    catch { view ReleaseHandle         }
    catch { not ReleaseHandle          }
    catch { sel ReleaseHandle          }
 }

 ReleaseHandleAll
 set page_num 0
 
 set filedir "Y:\\cal\\01_Comp\\09_NVH\\000_Anne\\test\\02_run"
  
 set proc_name "PAB PSD"

 hwi GetSessionHandle sess

 sess GetProjectHandle proj
  
 # ############################
 # # Load model by session file
 # ############################
 
 sess LoadSessionFile "Y:\\cal\\01_Comp\\09_NVH\\000_Anne\\test\\02_run\\session.mvw" false
 
 # set page_num [proj GetNumberOfPages]
 
 for {set i 1} {$i<=5} {incr i} {

 puts page:$i
 
 proj GetPageHandle page $i
  
 page GetWindowHandle win 1

 win SetClientType "Animation"

 win GetClientHandle post1
 
 win GetViewControlHandle view
  
 post1 GetRenderOptionsHandle ren 
 
 ren SetBackgroundColor white
 
 ren SetForegroundColor black
 
 post1 GetModelHandle mod 1
 
 mod GetResultCtrlHandle res
 
 res GetContourCtrlHandle contour_ctrl
 
 contour_ctrl GetLegendHandle leg
 
 post1 GetNoteHandle not 1
 
 set id [mod AddSelectionSet component]
 
 mod GetSelectionSetHandle sel $id
 
 sel SetLabel "unplot"
 
 sel Add "id <100"
  
 sel SetVisibility false

 post1 Fit
 
 post1 Draw

 set result [leg GetMax]
 
 puts MAX:$result
 
 set note_string [not GetText]
 
 puts Note:$note_string
 
 if {$result < 1} {
 mod Mask $id
 not SetText [concat $note_string\n$result<1\nPass!]
 } elseif {$result == "N/A"} {
 continue
 } else {
 mod Mask $id
 not SetText [concat $note_string\n$result>1\nNo Pass!]
 }
 post1 Fit
 post1 Draw
 
 sel ReleaseHandle
 not ReleaseHandle
 view ReleaseHandle
 leg ReleaseHandle 
 contour_ctrl ReleaseHandle
 res ReleaseHandle
 ren ReleaseHandle
 mod ReleaseHandle
 post1 ReleaseHandle
 win ReleaseHandle
 page ReleaseHandle
 }
 puts *****************
 puts *****************
 for {set i 1} {$i<=5} {incr i} {
 proj SetActivePage $i
 set file [concat $filedir\\image\\$i.jpeg]
 puts $file
 sess CaptureActiveWindow  JPEG $file percent 75 50
 }
 # page ReleaseHandle
 ReleaseHandleAll
 proj SetActivePage 6
 
 proj GetPageHandle page 6
  
 page GetWindowHandle win 1

 win SetClientType "Animation"

 win GetClientHandle post1
 
 win GetViewControlHandle view
  
 post1 GetModelHandle mod 1
 
 mod GetResultCtrlHandle res
 
 puts *****************
 

 for {set i 0} {$i<=$mode_num} {incr i} {
 res SetCurrentSimulation $i
 post1 Fit
 post1 Draw
 set file [concat $filedir\\image\\mode$i.jpeg]
 sess CaptureActiveWindow  JPEG $file percent 75 50
 puts $file
 }
 
 
 # ############################
 # # Load model by tcl
 # ############################

 # set myfile  "Y:\\cal\\01_Comp\\09_NVH\\000_Anne\\test\\02_run\\Z\\d3ftg"

 # set model_id [post1 AddModel $myfile]

 # post1 GetModelHandle mod $model_id
 
 # mod SetResult $myfile

 # # Advance to first frame.

 # # p1 GetAnimatorHandle animator

 # ani first
 
 # mod GetResultCtrlHandle res

 # res GetContourCtrlHandle contour_ctrl
 
 # res ReleaseHandle

 # post1 SetDisplayOptions contour true
 
 # post1 SetDisplayOptions "legend" true
 
 # contour_ctrl SetEnableState true
 
 # contour_ctrl SetDataType "Effective plastic strain"
 
 # contour_ctrl SetShellLayer "max"
 
 # contour_ctrl SetDimensionEnabled shell true
 
 # contour_ctrl SetAverageMode advanced
 
 # contour_ctrl GetLegendHandle leg
 
 # #Selected ploted part
 # set part_set_id [mod AddSelectionSet part]
 
 # mod GetSelectionSetHandle part_set_handle $part_set_id
 
 # part_set_handle SetLabel "OurPartSelectionSet"
 
 # part_set_handle Add "id 100"
 
 # # puts [part_set_handle GetDrawStyleList]
 
 # # puts “Current draw style: [part_set_handle GetDrawStyle]”
 
 # # puts “Current draw size: [part_set_handle GetDrawSize]”
 
 # # part_set_handle SetDrawSize 6
 
 # # part_set_handle SetDrawStyle [lindex [part_set_handle GetDrawStyleList] 0]
 
 # # part_set_handle SetVisibility true
 
 # mod MaskAll
 
 # mod UnMask $part_set_id
 
 # # leg SetDiscreteColorMode false
 
 # post1 Draw
  
 # contour_ctrl SetThresholdMax 1
 
 # contour_ctrl SetThresholdMaxEnableState true

 # post1 Draw
  
 # leg SetFilter log
 
 # post1 Draw
 
    
    

 
 
 # # capture animation
 
 # proj SetActivePage 1
 # # view SetLookAt "-0.011750 0.914389 -0.404666 0.000000 -0.998315 0.012270 0.056713 0.000000 0.056823 0.404650 0.912704 0.000000 539.704041 86.988853 -680.386536 1.000000"
 # view Fit
 # # view Zoom 0.6
 # post1 Draw
 # sess CaptureActiveWindow  JPEG "Y:\\cal\\01_Comp\\09_NVH\\000_Anne\\test\\02_run\\X.jpg" percent 75 50
 
 # proj SetActivePage 2
 # # view SetLookAt "-0.011750 0.914389 -0.404666 0.000000 -0.998315 0.012270 0.056713 0.000000 0.056823 0.404650 0.912704 0.000000 539.704041 86.988853 -680.386536 1.000000"
 # view Fit
 # # view Zoom 0.6
 # post1 Draw
 # sess CaptureActiveWindow  JPEG "Y:\\cal\\01_Comp\\09_NVH\\000_Anne\\test\\02_run\\Y.jpg" percent 75 50
 
 # proj SetActivePage 3
 # # view SetLookAt "-0.011750 0.914389 -0.404666 0.000000 -0.998315 0.012270 0.056713 0.000000 0.056823 0.404650 0.912704 0.000000 539.704041 86.988853 -680.386536 1.000000"
 # view Fit
 # # view Zoom 0.6
 # post1 Draw
 # sess CaptureActiveWindow  JPEG "Y:\\cal\\01_Comp\\09_NVH\\000_Anne\\test\\02_run\\Z.jpg" percent 75 50
 
 # proj SetActivePage 4
 # # view SetLookAt "-0.011750 0.914389 -0.404666 0.000000 -0.998315 0.012270 0.056713 0.000000 0.056823 0.404650 0.912704 0.000000 539.704041 86.988853 -680.386536 1.000000"
 # view Fit
 # # view Zoom 0.8
 # post1 Draw
 # sess CaptureActiveWindow  JPEG "Y:\\cal\\01_Comp\\09_NVH\\000_Anne\\test\\02_run\\Total.jpg" percent 75 50

# # } result]} 

 # # # Error handling

 # # puts $logfile "----- Error occured running $proc_name -----"

 # # puts $logfile "[sess GetError]"

 # # puts $logfile "--------------------------------------------"

# # } 
