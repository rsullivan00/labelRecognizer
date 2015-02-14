CPPFLAGS=-g -Wall -std=c++11 
LDFLAGS=-g
LDLIBS=-L `pkg-config --cflags --libs opencv`

SRCS=end_to_end_recognition.cpp compareTesseracts.cpp
PROGS=$(subst .cpp,,$(SRCS))
OBJS=$(subst .cpp,.o,$(SRCS))

all: $(PROGS)

end_to_end_recognition: end_to_end_recognition.o 
	g++ $(LDFLAGS) -o endToEnd end_to_end_recognition.o $(LDLIBS) 

compareTesseracts: compareTesseracts.o
	g++ $(LDFLAGS) -o compareTesseracts compareTesseracts.o $(LDLIBS) -llept -ltesseract

end_to_end_recognition.o: end_to_end_recognition.cpp
	g++ $(CPPFLAGS) -c end_to_end_recognition.cpp

compareTesseracts.o: compareTesseracts.cpp
	g++ $(CPPFLAGS) -c compareTesseracts.cpp

split.o: split.cpp
	g++ $(CPPFLAGS) -c split.cpp

clean:
	rm -f $(PROGS) $(OBJS)
