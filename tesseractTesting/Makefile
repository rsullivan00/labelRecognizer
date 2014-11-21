CPPFLAGS=-g -Wall -std=c++11 
LDFLAGS=-g
LDLIBS=-L `pkg-config --cflags --libs opencv`

SRCS=end_to_end_recognition.cpp
PROGS=$(subst .cpp,,$(SRCS))
OBJS=$(subst .cpp,.o,$(SRCS))

endToEnd: end_to_end_recognition.o 
	g++ $(LDFLAGS) -o endToEnd end_to_end_recognition.o $(LDLIBS) 

end_to_end_recognition.o: end_to_end_recognition.cpp
	g++ $(CPPFLAGS) -c end_to_end_recognition.cpp

split.o: split.cpp
	g++ $(CPPFLAGS) -c split.cpp

clean:
	rm -f $(PROGS) $(OBJS)
