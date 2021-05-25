

chess: main.o chess.o
	g++ main.o chess.o -o chess

main.o: main.cpp
	g++ -c main.cpp

chess.o: chess.cpp chess.h
	g++ -c chess.cpp

clean: 
	rm *.o chess
