CC=gcc
CXX=g++ -std=c++0x
RM=rm 
LDLIBS= -L `pkg-config --cflags --libs opencv`

SRCS=shape.cpp
OBJS=$(subst .cpp,.o,$(SRCS))

all: shape 

shape: $(OBJS)
	$(CXX) -o shape $(OBJS) $(LDLIBS) 

clean:
	$(RM) $(OBJS)
