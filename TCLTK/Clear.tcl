*creatmark loadcols 1 all;
set loadcols_id [hm_getmark loadcols 1];
set delet_loadcol [llength $loadcols_id]
if {$delet_loadcol != 0} {
	*deletemark loadcols 1;
	}

*creatmark loadsteps 1 all;
set loadsteps_id [hm_getmark loadsteps 1];
set delet_loadsteps [llength $loadsteps_id]
if {$delet_loadsteps != 0} {
	*deletemark loadsteps 1;
	}

*creatmark outputblocks 1 all;
set outputblocks_id [hm_getmark outputblocks 1];
set delet_outputblock [llength $outputblocks_id]
if {$delet_loutputblock != 0} {
	*deletemark outputblocks 1;
	}

*creatmark sets 1 all;
set sets_id [hm_getmark sets 1];
set delet_sets [llength $sets_id]
if {$delet_sets != 0} {
	*deletemark sets 1;
	}

*creatmark props 1 all;
set props_id [hm_getmark props 1];
set delet_props [llength $props_id]
if {$delet_props != 0} {
	*deletemark props 1;
	}

*creatmark materials 1 all;
set materials_id [hm_getmark materials 1];
set delet_materials [llength $materials_id]
if {$delet_materials != 0} {
	*deletemark materials 1;
	}

*creatmark cards 1 all;
set cards_id [hm_getmark cards 1];
set delet_cards [llength $cards_id]
if {$delet_cards != 0} {
	*deletemark cards 1;
	}

*creatmark asssemblies 1 all;
set asssemblies_id [hm_getmark asssemblies 1];
set delet_asssemblies [llength $asssemblies_id]
if {$delet_asssemblies != 0} {
	*deletemark asssemblies 1
	}
tk_messageBox -message "\u5220\u9664\u5904\u7406\u5B8C\u6210!"
