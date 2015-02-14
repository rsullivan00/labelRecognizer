CPPFLAGS=-g -Wall -std=c++11 
LDFLAGS=-g
LDLIBS=-L `pkg-config --cflags --libs opencv`

SRCS=postProcess.cpp
PROGS=$(subst .cpp,,$(SRCS))
OBJS=$(subst .cpp,.o,$(SRCS))

postProcess.o: postProcess.cpp
	g++ $(CPPFLAGS) -c postProcess.cpp

clean:
	rm -f $(PROGS) $(OBJS)
