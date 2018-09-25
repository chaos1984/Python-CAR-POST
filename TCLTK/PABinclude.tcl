proc DYNA_PAB_FILES {} {
	global tplpath
	set path "INCL/"
	*createmarkpanel comps 1 "Select comps to create include";
	set compNums [hm_getmark comps 1];
	# ##############################################################
	# *clearmarkall 1
	# *clearmarkall 2
	# set includePath $path
	# append includePath 989_airbag.key
	# *startnotehistorystate {Create Include "airbag"}
	# *createinclude 989 989_airbag.key $includePath 0
	# *endnotehistorystate {Create Include "airbag"}
	# *createmark controlvols 1 all
	# *markmovetoinclude controlvols 1 989
	# catch {set LCSSnum [hm_getvalue mats mark=1 dataname column=5440]}
	# set includePath $path
	# ##############################################################
	# *clearmarkall 1
	# *clearmarkall 2
	# set includePath $path
	# append includePath 998_props.key
	# *startnotehistorystate {Create Include "Props"}
	# *createinclude 998 998_props.key $includePath 0
	# *endnotehistorystate {Create Include "Props"}
	# set includePath $path
	# ##############################################################
	# *clearmarkall 1
	# *clearmarkall 2
	# set includePath $path
	# append includePath 17_Emblem_MAT_PROP.key
	# *startnotehistorystate {Create Include "Emblem_MAT_PROP"}
	# *createinclude 990 17_Emblem_MAT_PROP.key $includePath 0
	# *endnotehistorystate {Create Include "Emblem_MAT_PROP"}
	# set includePath $path
	# ##############################################################
	# ##############################################################
	# *clearmarkall 1
	# *clearmarkall 2
	# set includePath $path
	# append includePath 16_Housing_MAT_PROP.key
	# *startnotehistorystate {Create Include "Housing_MAT_PROP"}
	# *createinclude 991 16_Housing_MAT_PROP.key $includePath 0
	# *endnotehistorystate {Create Include "Housing_MAT_PROP"}
	# set includePath $path
	# ##############################################################
	# ##############################################################
	# *clearmarkall 1
	# *clearmarkall 2
	# set includePath $path
	# append includePath 15_Cover_MAT.key
	# *startnotehistorystate {Create Include "Cover_MAT_PROP"}
	# *createinclude 992 15_Cover_MAT_PROP.key $includePath 0
	# *endnotehistorystate {Create Include "Cover_MAT_PROP"}
	# set includePath $path
	# ##############################################################
	# set includePath $path
	# append includePath 14_Cushion_MAT.key
	# *startnotehistorystate {Create Include "Cushion_MAT_PROP"}
	# *createinclude 993 14_Cushion_MAT_PROP.key $includePath 0
	# *endnotehistorystate {Create Include "Cushion_MAT_PROP"}
	# set includePath $path
	# ##############################################################
	# set includePath $path
	# append includePath 18_Other_MAT.key
	# *startnotehistorystate {Create Include "Other_MAT"}
	# *createinclude 994 18_Other_MAT.key $includePath 0
	# *endnotehistorystate {Create Include "Other_MAT"}
	# #*createmark mats 2 displayed
	# set includePath $path
	# ##############################################################
	foreach compNum $compNums {	
		*clearmarkall 1
		*clearmarkall 2
		*startnotehistorystate {isolateonly Component $compNum}
		*createmark components 2 $compNum
		*createstringarray 2 "elements_on" "geometry_on"
		*isolateonlyentitybymark 2 1 2
		*endnotehistorystate {isolateonly Component $compNum}
		if {$compNum < 100} {
		set includeName "G05_Cushion_fold"
		set includeNum 1000
		} elseif {$compNum > 99 && $compNum < 200} {
		set start 1000000
		set includeName "G08_Inflator"
		set includeNum 1008
		} elseif {$compNum > 199 && $compNum < 300} {
		set start 2000000
		set includeName "G09_Cover"
		set includeNum 1009
		} elseif {$compNum > 299 && $compNum < 400} {
		set start 3000000
		set includeName "G10_Housing"
		set includeNum 1010
		} elseif {$compNum > 399 && $compNum < 500} {
		set start 4000000
		set includeName "G11_Emblem"
		set includeNum 1011
		} elseif {$compNum > 499 && $compNum < 600} {
		set start 5000000
		set includeName "GOmega_spring"
		set includeNum 1012
		} elseif {$compNum > 599 && $compNum < 700} {
		set start 6000000
		set includeName "G12_SW_amature"
		set includeNum 1013
		} elseif {$compNum > 699 && $compNum < 800} {
		set start 7000000
		set includeName "G12_1_SW_form"
		set includeNum 1014
		} elseif {$compNum > 799 && $compNum < 900} {
		set start 8000000
		set includeName "G13_Other_parts"
		set includeNum 1015
		} elseif {$compNum > 899 && $compNum < 1000} {
		set start 9000000
		set includeName "G100_RIGID_CONNECT"
		set includeNum 1016
		} 
        *clearmarkall 1
		*clearmarkall 2
		if {$compNum > 99 && $compNum < 1000} {
		*createmark nodes 1 displayed
		*renumbersolverid nodes 1 $start 1 0 0 0 0 0
		*createmark elements 1 displayed
		*renumbersolverid elements 1 $start 1 0 0 0 0 0 
		set includeList [hm_getincludes]
		if {[lsearch $includeList $includeNum] == -1} {
		*startnotehistorystate {Create Include $compNum}
		append includePath $includeName
		puts $includeNum 
		puts $includeName.key 
		puts $includePath.key
		*createinclude $includeNum $includeName.key $includePath.key 0
		*endnotehistorystate {Create Include $compNum}
		*createmark components 2 $compNum
		*markmovetoinclude components 2 $includeNum
		*createmark nodes 2 displayed
		*markmovetoinclude nodes 2 $includeNum
		*createmark elements 2 displayed
		*markmovetoinclude elements 2 $includeNum
		*createmark props 2 displayed
		*markmovetoinclude props 2 $includeNum
		set includePath $path
		} else {
		*createmark components 2 $compNum
		*markmovetoinclude components 2 $includeNum
		*createmark nodes 2 displayed
		*markmovetoinclude nodes 2 $includeNum
		*createmark elements 2 displayed
		*markmovetoinclude elements 2 $includeNum
		*createmark props 2 displayed
		*markmovetoinclude props 2 $includeNum
		}
		} elseif {$compNum > 899} {
		set includeList [hm_getincludes]
		if {[lsearch $includeList $includeNum] == -1} {
		*startnotehistorystate {Create Include $compNum}
		append includePath $includeName
		puts $includeNum 
		puts $includeName.key 
		puts $includePath.key
		*createinclude $includeNum $includeName.key $includePath.key 0
		*endnotehistorystate {Create Include $compNum}
		*createmark components 2 $compNum
		*markmovetoinclude components 2 $includeNum
		*createmark elements 2 displayed
		*markmovetoinclude elements 2 $includeNum
		set includePath $path
		} else {
		*createmark components 2 $compNum
		*markmovetoinclude components 2 $includeNum
		*createmark elements 2 displayed
		*markmovetoinclude elements 2 $includeNum
		}
		}
		##########################################
        # *clearmarkall 1
		# *clearmarkall 2
		# *clearmarkall 3
		# if {$compNum<99 } {
			# # *createmark mats 1 displayed
			# # catch {set LCSSnum [hm_getvalue mats mark=1 dataname column=45]}
			# # *markmovetoinclude mats 1 993
			# *createmark props 2 displayed
			# *markmovetoinclude props 2 993
			# # catch {*createmark curves 3 $LCSSnum}
			# # catch {*markmovetoinclude curves 3 993}
		# } elseif {$compNum>99 && $compNum < 200 } {
			# # *createmark mats 1 displayed
			# # set LCSSnum [hm_getvalue mats mark=1 dataname column=45]
			# # *markmovetoinclude mats 1 994
			# # *createmark props 2 displayed
			# *markmovetoinclude props 2 998
			# *createmark curves 3 $LCSSnum
			# *markmovetoinclude curves 3 994
		# } elseif {$compNum >199 && $compNum<300 } {
			# # *createmark mats 1 displayed
			# # set LCSSnum [hm_getvalue mats mark=1 dataname column=45]
			# # *markmovetoinclude mats 1 992
			# *createmark props 2 displayed
			# *markmovetoinclude props 2 992
			# # *createmark curves 3 $LCSSnum
			# # *markmovetoinclude curves 3 992
		# } elseif {$compNum >299 && $compNum<400 } {
			# # *createmark mats 1 displayed
			# # set LCSSnum [hm_getvalue mats mark=1 dataname column=45]
			# # *markmovetoinclude mats 1 991
			# *createmark props 2 displayed
			# *markmovetoinclude props 2 991			
			# # *createmark curves 3 $LCSSnum
			# # *markmovetoinclude curves 3 991
		# } elseif {$compNum >399 && $compNum<500 } {
			# # *createmark mats 1 displayed
			# # set LCSSnum [hm_getvalue mats mark=1 dataname column=45]
			# # *markmovetoinclude mats 1 990
			# *createmark props 2 displayed
			# *markmovetoinclude props 2 990
			# # *createmark curves 3 $LCSSnum
			# # *markmovetoinclude curves 3 990
		# } elseif {$compNum > 499} {
			# # *createmark mats 1 displayed
			# # catch {set LCSSnum [hm_getvalue mats mark=1 dataname column=45]}
			# # *markmovetoinclude mats 1 994
			# *createmark props 2 displayed
			# *markmovetoinclude props 2 998
			# # catch [*createmark curves 3 $LCSSnum]
			# # catch [*markmovetoinclude curves 3 998]
		# } else {
		# }
		}			

	############################################################
	*clearmarkall 1
	*clearmarkall 2
	*createmark cards 1 all
	set cards_list [hm_getcardimagenamemark cards 1]
	append includePath C01_Control.key
	*startnotehistorystate {Create Include "ControlCard"}
	*createinclude 996 01_Control.key $includePath 0
	*endnotehistorystate {Create Include "ControlCard"}
	foreach card $cards_list {
		if {$card != "Keyword"} {
			*createmark cards_move 1 $card
			*markmovetoinclude cards_move 1 996
		}
	}
	set includePath $path
	# #############################################################
	*clearmarkall 1
	*clearmarkall 2
	*startnotehistorystate {Create Include "ContactCard"}
	append includePath C03_Contact.key
	*createinclude 997 03_Contact.key $includePath 0
	*endnotehistorystate {Create Include "ContactCard"}
	*createmark group_move 1 all
	*markmovetoinclude group_move 1 997
	set includePath $path
	# ##############################################################
	*clearmarkall 1
	*clearmarkall 2
	*startnotehistorystate {Create Include "boundary"}
	append includePath 02_boundary.key
	*createinclude 995 02_boundary.key $includePath 0
	*endnotehistorystate {Create Include "boundary"}
	*createmark constrainedextranodes 1 all
	*markmovetoinclude constrainedextranodes 1 995
	*clearmarkall 1
	*createmark constrainedrigidbodies 1 all
	*markmovetoinclude constrainedrigidbodies 1 995
	*clearmarkall 1
	*createmark loadcols 1 all
	*markmovetoinclude loadcols 1 995
	set includePath $path
	############################################################
	*clearmarkall 1
	*clearmarkall 2
	*startnotehistorystate {Create Include "Sets"}
	append includePath C999_sets.key
	*createinclude 999 C999_sets.key $includePath 0
	*endnotehistorystate {Create Include "Sets"}
	*createmark sets 2 all
	*markmovetoinclude sets 2 999
	set includePath $path
	############################################################
	*clearmarkall 1
	*clearmarkall 2
	*createmark hourglasses 1 all
	*markmovetoinclude hourglasses 1 996
	}

proc OPTI_PAB_FILES {} {
	global tplpath
	set path "INCL/"
	*createmarkpanel comps 1 "Select comps to create include";
	set compNums [hm_getmark comps 1];
	*clearmarkall 1
	*clearmarkall 2
	set includePath $path
	append includePath 998_props.fem
	*startnotehistorystate {Create Include "Props"}
	*createinclude 998 998_props.fem $includePath 0
	*endnotehistorystate {Create Include "Props"}
	*createmark props 1 all
	*markmovetoinclude props 1 998
	set includePath $path
	######################################################
	*clearmarkall 1
	*clearmarkall 2
	append includePath 999_mats.fem
	*startnotehistorystate {Create Include "Mats"}
	*createinclude 999 999_mats.fem $includePath 0
	*endnotehistorystate {Create Include "Mats"}
	*createmark mats 2 all
	*markmovetoinclude mats 2 999
	set includePath $path
	######################################################
	*clearmarkall 1
	*clearmarkall 2
	append includePath 1000_model.fem
	*startnotehistorystate {Create Include "Model"}
	*createinclude 1000 1000_modelfem $includePath 0
	*endnotehistorystate {Create Include "Model"}
	*createmark components 1 all
	*markmovetoinclude components 1 1000
	*createmark nodes 2 all
	*markmovetoinclude nodes 2 1000
	*createmark elements 2 all
	*markmovetoinclude elements 2 1000
	set includePath $path
}  	
# #####################################################################
set tplpath [hm_info exporttemplate]
set a [split $tplpath /]
set num [expr [llength $a]-2]
set b [lindex $a $num]
switch $b  {
	ls-dyna971 {DYNA_PAB_FILES}
	nastrain {DYNA_PAB_FILES}
	optistruct {OPTI_PAB_FILES}
}

*clearmark comps all;
