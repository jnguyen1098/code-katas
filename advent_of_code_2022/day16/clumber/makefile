# Hope this works...

CC = clang
CFLAGS = -Wall -Wpedantic -std=c11 -Wextra -ggdb3 -I$(INC) -Weverything -Wdocumentation -Wno-format-nonliteral -Wno-reserved-id-macro -Wno-format-security
VFLAGS = --show-leak-kinds=all --track-origins=yes --leak-check=full
SHELL = /bin/bash

PROJ = plumber

BIN = bin
INC = include
SRC = src

_OBJS = plumber

EXE = $(BIN)/$(PROJ)
DEPS = $(INC)/$(PROJ).h
OBJS = $(addprefix $(BIN)/,$(addsuffix .o,$(_OBJS)))

all: $(EXE)

$(EXE): $(OBJS)
	$(CC) $(CFLAGS) $^ -o $@

$(BIN)/%.o: $(SRC)/%.c $(DEPS)
	$(CC) $(CFLAGS) $< -c -o $@

valgrind:
	@echo "Running valgrind"
	valgrind $(VFLAGS) $(EXE)

lint: all
	make cppcheck
	make clang-analyze
	make clang-tidy
	make clang-format

cppcheck:
	@echo "Running cppcheck"
	cppcheck --enable=all -I$(INC) --inconclusive -v $(SRC)/*.c

clang-analyze:
	@echo "Running clang's static analyzer"
	clang --analyze $(SRC)/*.c -I$(INC)

clang-tidy:
	@echo "Running clang-tidy"
	clang-tidy -checks=* -header-filter=.* $(SRC)/*.c -- -I$(INC)

clang-format:
	@echo "Running clang-format"
	diff -u <(cat $(SRC)/*.c) <(clang-format $(SRC)/*.c)
	-diff -u <(cat $(INC)/*.h) <(clang-format $(INC)/*.h)

documentation:
	doxygen Doxyfile

clean:
	rm -rf $(BIN)/* html/ latex/ *.plist $(INC)/*.gch

.PHONY: all test lint cppcheck splint clang-analyze\
        clang-tidy clang-format documentation clean
