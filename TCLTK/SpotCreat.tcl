set D_lines	{};
set Warn_lines {};
set cir_lines {};
set mid_nodes {};
set mid_3nodes {};
set node_spot2 {};
set node_spot3 {};
set node_spot4 {};
set delete_spot2 {};
set newspot {};

proc dis_node {node_1 node_2} {
	set x1 [hm_getentityvalue nodes $node_1 "x" 0];
	set y1 [hm_getentityvalue nodes $node_1 "y" 0];
	set z1 [hm_getentityvalue nodes $node_1 "z" 0];
	set x2 [hm_getentityvalue nodes $node_2 "x" 0];
	set y2 [hm_getentityvalue nodes $node_2 "y" 0];
	set z2 [hm_getentityvalue nodes $node_2 "z" 0];

	set dx [expr $x1 - $x2]
	set dy [expr $y1 - $y2]
	set dz [expr $z1 - $z2]

	return [expr sqrt(($dx*$dx + $dy*$dy + $dz*$dz))]
	}

*creatmarkpanel lines 1 "Select lines to spot";
set lines_list [hm_getmark lines 1];
*creatmarkpanel comps 1 "Select comps to spot";
set comps_list [hm_getmark comps 1];

foreach line_id $lines_list {
	set line_dis [hm_linelength $line_id];
	*creatmark lines 1 $line_id;
	if {$line_dis > 6.43} {
		lappend cir_lines $line_id
		}
	elseif {$line_dis > 4} {
		lappend D_lines $line_id;
		*nodecreationlines lines 1 1;
		*creatmark nodes 1 -1;
		lappend mid_nodes [hm_getmark nodes 1];
		}
	else {
		lappend Warn_lines $line_id;
		}
	}
foreach node_1 $mid_nodes {
	set 3nodes {};
	set i 0;
	foreach node_2 $mid_nodes {
		set node_dis [dis_node $node_1 $node_2];
		if {$node_dis < 1} {
			incr i 1;
			}
		if {$node_dis > 1 && node_dis < 3} {
			lappend 3nodes $node_2;
			}
		}
	switch $i {
		1 {lappend node_spot2 $node_1};
		2 {lapped node_spo3 $node_1};
		}
	set 3nodes_length [llength $3nodes];
	if {$3nodes_length == 2} {
		set 3nodes_2 [llindex $3nodes 0];
		set 3nodes_3 [llindex $3nodes 1];
		set 3nodes_dis [dis_node $3nodes_2 $3nodes_3];
		if {$3node_dis > 1} {
			llappend delete_spot2 $node_1;
			*creatcenternode $3node_1 $3node_2 $3node_3;
			*creatmark nodes 1 -1;
			lappend node_spot4 [hm_getmark nodes 1];
			}
		} 
	}

eval *creatmark nodes 1 $node_spot2;
eval *creatmark nodes 2 $delete_spot2;
*markdifference nodes 1 nodes 2;
set node_spot2 [hm_getmark nodes 1];

if {$node_spot2 != []} {
	*creatmark comps 1 spot_2_SOLID_STEEL;
	set id_comp [hm_getmark comps 1];
	if {$id_comp == []} {
		*collectorcreatonly components "spot_2_SOLID_STEEL" "" 4;
		}
	*currentcollector comps spot_2_SOLID_STEEL;
	*CE_GlobalSetInt "g_ce_spotvis" 1;
	eval *creatmark nodes 1 $node_spot2;
	eval *creatmark components 2 $comps_list;
	*createstringarray 8 "link_elems_geom=elem" "link_rule=now" "relink_rule=none" \
						"tol_flag = 1" "tol = 10.00" "ce_nonormal=0" "ce_extralinknum=0" "ce_hexaoffsetcheck=1";
	*CE_ConnectorCreatByMark nodes 1 "spot" 2 components 2 1 8;
	}
for {set i [llength $node_spot2]} {$i > 0} {incr i -1} {
	*creatmark connectors 1 $i;
	lappend newspot [hm_getmark connectors 1]
	}
if {$nodes_spot3 != []} {
	*creatmark comps 1 spot_3_SOLID_STEEL;
	set id_comp [hm_getmark comps 1]
	if {$if_comp == []} {
		*collectorcreatonly components "spot_3_SOLID_STEEL" "" 4;
		}
	*currentcollector comps spot_3_SOLID_STEEL;
	*CE_GlobalSetInt "g_ce_spotvis"
	eval *creatmark nodes 1 $node_spot3;
	eval *creatmark components 2 $comps_list;
	*createstringarray 8 "link_elems_geom=elem" "link_rule=now" "relink_rule=none" \
						"tol_flag = 1" "tol = 10.00" "ce_nonormal=0" "ce_extralinknum=0" "ce_hexaoffsetcheck=1";
	*CE_ConnectorCreatByMark nodes 1 "spot" 3 components 2 1 8;
	}
for {set i [llength $node_spot3]} {$i > 0} {incr i -1} {
	*creatmark connectors 1 $i;
	lappend newspot [hm_getmark connectors 1]
	}
if {$nodes_spot4 != []} {
	*creatmark comps 1 spot_4_SOLID_STEEL;
	set id_comp [hm_getmark comps 1]
	if {$if_comp == []} {
		*collectorcreatonly components "spot_4_SOLID_STEEL" "" 4;
		}
	*currentcollector comps spot_4_SOLID_STEEL;
	*CE_GlobalSetInt "g_ce_spotvis"
	eval *creatmark nodes 1 $node_spot4;
	eval *creatmark components 2 $comps_list;
	*createstringarray 8 "link_elems_geom=elem" "link_rule=now" "relink_rule=none" \
						"tol_flag = 1" "tol = 10.00" "ce_nonormal=0" "ce_extralinknum=0" "ce_hexaoffsetcheck=1";
	*CE_ConnectorCreatByMark nodes 1 "spot" 4 components 2 1 8;
	}
for {set i [llength $node_spot4]} {$i > 0} {incr i -1} {
	*creatmark connectors 1 $i;
	lappend newspot [hm_getmark connectors 1];
	}

*creatmark connectors 1 "all";
*CE_ConnectorRemoveDuplicates 1 0.1;
*nodecleartempmark;
set num [llength $Warn_lines];
eval *creatmark lines 1 $Warn_lines;
hm_saveusermark lines 1;

if {$num == 1} {
	tk_messageBox message "There is 1 Warn_line to be saved!"
	}
elseif {$num > 1} {
	tk_messageBox message "There are $num Warn_lines to be saved!";
	}

*clearmark lines 1;
*clearmark connectors 1;