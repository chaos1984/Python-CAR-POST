package require Tk
set w .toplevel
catch {destroy $w}
toplevel $w
wm title $w "Please input the file_dir for outputting the grid information!"
wm iconname $w "DECOMPOSITION DAB DEPLOYMENT SIMULATION"
wm geometry $w 620x200
label $w.msg -text "Please input the file directory:"
label $w.file -background {#ffffff} -justify left -text "Decompo.key"
button $w.b1 -text "OK" -command {
	set grid_list []
	# set i [hm_getint "Coor. Points" "Input sys numbers"]
	$w.t1 insert end "The Nodes Coor. is:"
	# $w.t1 insert end [format "%d\n" $i]
	set id [open "$dir/Decompo.key" w]
	# while {$i > 0} {
		# *createlistbypathpanel nodes 1 "Select sys nodes";
		*createlistpanel nodes 1 "Select sys nodes";
		set nodelist [hm_getlist nodes 1]
		if {[llength $nodelist] == 3} {
			# puts $id $nodelist;
			# set i [expr $i-1];
			} else {
			$w.t1 insert end "ERROR:Please pick three nodes.\n"
			 }
		# $w.t1 insert end [format "%d\n" $i];
		$w.t1 insert end $nodelist;
		$w.t1 insert end "\n";
		*clearmark nodes i;
		# }
		set x1 [hm_getentityvalue nodes [lindex $nodelist 0] "x" 0];
		set y1 [hm_getentityvalue nodes [lindex $nodelist 0] "y" 0];
		set z1 [hm_getentityvalue nodes [lindex $nodelist 0] "z" 0];
		set x2 [hm_getentityvalue nodes [lindex $nodelist 1] "x" 0];
		set y2 [hm_getentityvalue nodes [lindex $nodelist 1] "y" 0];
		set z2 [hm_getentityvalue nodes [lindex $nodelist 1] "z" 0];
		set x3 [hm_getentityvalue nodes [lindex $nodelist 2] "x" 0];
		set y3 [hm_getentityvalue nodes [lindex $nodelist 2] "y" 0];
		set z3 [hm_getentityvalue nodes [lindex $nodelist 2] "z" 0];
		$w.t1 insert end $nodelist;
		$w.t1 insert end "\n";
		$w.t1 insert end $x1 $y1 $z1;
		$w.t1 insert end "\n";
		puts $id "*PARAMETER"
		puts $id [format "RDAB_X,%8.3f" $x1];
		puts $id [format "RDAB_Y,%8.3f" $y1];
		puts $id [format "RDAB_Z,%8.3f" $z1];
		set dx1 [expr $x2 - $x1]
	    set dy1 [expr $y2 - $y1]
		set dz1 [expr $z2 - $z1]
		set dx2 [expr $x3 - $x1]
	    set dy2 [expr $y3 - $y1]
		set dz2 [expr $z3 - $z1]
		set d1 [expr sqrt(($dx1*$dx1 + $dy1*$dy1 + $dz1*$dz1))]
		set d2 [expr sqrt(($dx2*$dx2 + $dy2*$dy2 + $dz2*$dz2))]
		set ang [expr acos(($dx1*$dx2+$dy1*$dy2+$dz1*$dz2)/($d1*$d2))*180/3.141592654]
		set tan_ang [expr tan(acos(($dx1*$dx2+$dy1*$dy2+$dz1*$dz2)/($d1*$d2)))]
		puts $id [format "RTAN_A,%8.3f" $tan_ang]
		$w.t1 insert end [format "Vector Ang.: %8.3f" $ang];
		$w.t1 insert end "\n";
		close $id
}

text $w.t1
button  $w.b2 -text "Browse" -command {
	set dir [tk_chooseDirectory \
			-initialdir ~ -title "Choose a directory"]
	$w.file configure -text "$dir/Decompo.key"
	$w.t1 insert end "\n"
} 

place $w.msg \
	-x 0 -y 20 -width 200 -height 20 -anchor nw
place $w.file \
	-x 190 -y 20 -width 280 -height 20 -anchor nw
place $w.b2 \
	-x 480 -y 20 -width 60 -height 20 -anchor nw
place $w.b1 \
	-x 540 -y 20 -width 60 -height 20 -anchor nw
place $w.t1 \
	-x 20 -y 45 -width 580 -height 130