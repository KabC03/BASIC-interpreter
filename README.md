# BASIC Interpreter

A BASIC interpreter written in Python. Reads .bas files, tokenises them, parses the commands, and runs them. No classes, no external libraries. Just functions calling functions.

## What you need

Python 3

## Quick start

Pass a test file and run it:

```bash
python3 src/main.py tests/test_print.bas
```

You'll see the output right in your terminal. The interpreter prints RUN, executes your program line by line, then prints END when it finishes or hits an END statement.

## What it supports

The usual BASIC stuff. Nothing fancy.

### Variables and maths

```basic
10 LET X = 5
20 LET Y = X * 2 + 1
30 PRINT Y
```

### Printing things

```basic
10 PRINT "Hello"
20 PRINT "The value is "; X
```

Semicolons keep output on the same line. Without them you get a newline. Strings go in double quotes.

### User input

```basic
10 PRINT "Enter a number"
20 INPUT X
30 PRINT "Twice that is "; X * 2
```

### Loops

```basic
10 FOR I = 1 TO 10
20 PRINT I
30 NEXT I
```

FOR loops count up. The loop variable increments by 1 each time. NEXT jumps back to the line after the FOR statement.

### Conditions

```basic
10 IF X > 5 THEN PRINT "Big"
20 IF Y = 0 THEN GOTO 100
THEN can run a PRINT, a GOTO, or a LET. Simple comparisons only: =, >, <, >=, <=.
```

### Jumping around

```basic
10 GOTO 50
20 PRINT "Skipped"
50 PRINT "Here"
```

Every line needs a line number. GOTO jumps to that number. Labels aren't supported, use line numbers instead.

### Comments

```basic
10 REM This does nothing
REM lines get ignored. Useful for leaving notes.
```

### Running the test suite

```bash
cd tests
./run_tests.sh
```

This will print a pass/fail for each test.


