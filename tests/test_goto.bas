10 REM GOTO demonstration
20 PRINT "Start"
30 GOTO 60
40 PRINT "This is skipped"
50 PRINT "Also skipped"
60 PRINT "Jumped here"
70 LET X = 1
80 IF X = 1 THEN GOTO 110
90 PRINT "Won't print"
100 GOTO 130
110 PRINT "Condition was true"
120 GOTO 140
130 PRINT "Condition was false"
140 PRINT "The end"
150 END

