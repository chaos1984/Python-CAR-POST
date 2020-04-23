fout = open(r"mbp1\RE_mbp1.pc","w")
for line in open(r"mbp1\mbp1.pc"):
	if 'FILE m' in line:
		continue
	elif "INPUTVERSION" in line:
		fout.write("INPUTVERSION 2014\n")
	elif "MPPOUTPUT WRITE REMOVE " in line:
		fout.write(" MPPOUTPUT WRITE REMOVE \n OUTPUT_FILE_FORMAT           DSYTHP \n")
	elif "      0.31                                                                      " in line:
		fout.write("      0.50                                                                      \n")
	else :
		fout.write(line)
fout.close()