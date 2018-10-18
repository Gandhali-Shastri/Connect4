Gandhali Shastri
UTA ID: 1001548562
Pyhton

Code structure:

1.	Program will accept user input through command line arguemnets.
	It will accept the input in the following format:
		maxconnect4.py one-move input1.txt output1.txt 10
		maxconnect4.py interactive input1.txt computer-next 7	

2.	Flow of the code:-
	i.	User input would be accepted in the main.
	ii.	According to the input given oneMoveMode or InteractiveMode function will be called.
	iii.	Then the AiPlay function is called and alpha beta search is performed with the given depth limit.
	iv. 	Eval() will give the final score and the next move will be done accordingly.


Running the code on Omega:
	Type the following command: 
		python maxconnect4.py one-move input1.txt output1.txt 10
		python maxconnect4.py interactive input1.txt computer-next 7