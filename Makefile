CFLAGS	:= -std=c99 -pedantic -Wall -Wextra
SOURCES := $(wildcard *.c)
OBJECTS	:= $(patsubst %.c,%.o,$(SOURCES))
DEPENDS := $(patsubst %.c,%.d,$(SOURCES))
LDLIBS	:= -lncurses

.PHONY : all clean

all : a.out

clean :
	$(RM) $(OBJECTS) $(DEPENDS) a.out

a.out : $(OBJECTS)
	$(CC) $(CFLAGS) $^ -o $@ $(LDLIBS)

%.o : %.c Makefile
	$(CC) $(CFLAGS) -MMD -MP -c $< -o $@

-include $(DEPENDS)
