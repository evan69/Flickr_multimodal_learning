objects = DataSet.o Model.o Util.o

all: main.exe

main.exe: main.cpp $(objects)
	g++ main.cpp $(objects) -o main.exe

DataSet.o: DataSet.cpp
	g++ -c DataSet.cpp -o DataSet.o

Model.o: Model.cpp
	g++ -c Model.cpp -o Model.o

Util.o: Util.cpp
	g++ -c Util.cpp -o Util.o
	
clean:
	rm *.o
	rm *.exe

#change_dataFormat.o: change_dataFormat.cpp
#	g++ -c change_dataFormat.cpp -o change_dataFormat.o

# dataFormat.o: dataFormat.cpp
#	g++ -c dataFormat.cpp -o dataFormat.o
    