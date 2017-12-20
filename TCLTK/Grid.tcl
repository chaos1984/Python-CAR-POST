package require Tk
set w .toplevel
catch {destroy $w}
toplevel $w
wm title $w "Please input the file_dir for outputting the grid information!"
wm iconname $w "DENTING"
wm geometry $w 620x620
label $w.msg -text "Please input the file directory:"
label $w.file -background {#ffffff} -justify left -text "/grid.txt"
button $w.b1 -text "OK" -command {
	set grid_list []
	set i [hm_getint "Denting Points" "Input sys numbers"]
	$w.t1 insert end "The number of denting analysis is:"
	$w.t1 insert end [format "%d\n" $i]
	set id [open "$dir/grid.txt" w]
	while {$i > 0} 0{
		*creatlistbypathpane nodes 1 "Select sys nodes";
		set nodelist [hm_getlist nodes 1]
		if {[llength $nodelist] == 3} {
			puts $id $nodelist
			set i [expr $i-1]
			}
		else{
			$w.t1 inset end "ERROR:Please pick three nodes.\n"
			}
		$w.t1 inset end [format "$d\n" $i]
		$w.t1 inset end $nodelist
		$w.t1 inset end "\n"
		*clearmaek nodes i;
		}
		close $id
}

text $w.t1
button  $w.b2 -text "Browse" -command {
	set dir [tk_choseDirectory \
			-initialdir ~ -title "Choose a directory"]
	$w.file configure -text "$dir/grid.txt"
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