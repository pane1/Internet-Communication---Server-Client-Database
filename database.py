#!/usr/bin/env python
# console command - database imports
import argparse
import csv
from person import *
# Server-client imports
import socket
import sys
import struct
import hashlib
import getpass

# Server code
class database:
    HOSTNAME = "0.0.0.0"
    PORT = 50000
    BUFFER_SIZE = 1024
    MAX_BACKLOG = 10
    ENCODER = "ascii"

    SOCKET_ADDR = (HOSTNAME, PORT)

    def __init__(self):
        #self.name = name
        #self.student_database_file = student_database_file
        
        self.students = {}
       
        self.create_listen_socket()
        self.import_student_database()
        self.process_connections_forever()

    def create_listen_socket(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
            self.socket.bind(database.SOCKET_ADDR)
            self.socket.listen(database.MAX_BACKLOG)
            print("Listening on port {} ...".format(database.PORT))
        except Exception as msg:
            print(msg)
            sys.exit(1)

    def process_connections_forever(self):
        try:
            while True:
                self.connection_handler(self.socket.accept())
        except Exception as msg:
            print(msg)
        except KeyboardInterrupt:
            print()
        finally:
            self.socket.close()
            sys.exit(1)

    def connection_handler(self, client):
        connection, addr_port = client
        print("-"*72)
        print("Connection with {}".format(addr_port))
        print(client)
        
        while True:
            try:
                recv_bytes = connection.recv(database.BUFFER_SIZE)
                if len(recv_bytes) == 0:
                    print("Closing client connection...")
                    connection.close()
                    break
                    
                try:
                	recv_str = recv_bytes.decode(database.ENCODER)
                	print("-"*72)
                	print("Received: ", recv_str)
                	print("-"*72)
                except Exception as e:
                	recv_str = recv_bytes

                if recv_str == "get lab average":
                    self.print_students("GL1", connection)
                    #print("getting lab 2 average")
                elif recv_str == "get lab 2 average":
                    self.print_students("GL2", connection)
                    #print("getting lab 2 average")
                elif recv_str == "get lab 3 average":
                    self.print_students("GL3", connection)
                    #print("getting lab 3 average")
                elif recv_str == "get lab 4 average":
                    self.print_students("GL4", connection)
                    #print("getting lab 4 average")
                elif recv_str == "get midterm average":
                    self.print_students("GMA", connection)
                    #print("getting midterm average")
                elif recv_str == "":
                    self.print_students()
                else:
                    self.print_students(recv_str, connection)
                #connection.sendall()
                #print("Sent: ", self.average)
            
            except KeyboardInterrupt:
                print()
                print("Closing client connection due to error...")
                connection.close()
                break
        
    def import_student_database(self):
        try:
            csv_file = open("course_grades_2022.csv")
            read_file = open("course_grades_2022.csv")

            reader = csv.reader(csv_file)
            read = csv.reader(read_file)
            for row in read:
                print(row)

            next(reader)
            self.student_list = [(e[0], int(e[1]), e[2], int(e[3]), int(e[4]), int(e[5]), int(e[6]), int(e[7]), int(e[8]), int(e[9]),int(e[10]), int(e[11])) for e in reader]
            #print(self.student_list)

            self.create_student_dictionary()

        except Exception:
            print("Error: reading input file")
            exit()

    def create_student_dictionary(self):
        for student in self.student_list:
            #print(student)
            try:
                # 1.Name, 2.ID Number, 3.Password, 4.Lab 1, 5.Lab 2, 6.Lab 3, 7.Lab 4, 8.Midterm, 9.Exam 1, 10.Exam 2, 11.Exam 3, 12.Exam 4
                Studname, student_id, password, l1, l2, l3, l4, mt, e1, e2, e3, e4 = student
                new_student = Person(Studname, student_id, password, l1, l2, l3, l4, mt, e1, e2, e3, e4)
                
                self.add_student(student_id, new_student)
                
            except Exception:
                print("Error: student creation \"{}\"".format(Studname))
                exit()
    
    def add_student(self, student_id, person):
        try:
            self.students[student_id] = person
            #print(self.students[0])
            
        except Exception:
            print("Error: adding student")

    def print_students(self, command, connection):
        count = 0
        average = 0 
        if command == "GL1":
            print("Command: ", command)
            for id,t in self.students.items():
                average += t.l1
                count += 1 
            val = str(average/count)
            send_str = val.encode(database.ENCODER)
            connection.sendall(send_str)
            print("Sent: ", send_str)
            
        elif command == "GL2":
            print("Command: ", command)
            for id,t in self.students.items():
                average += t.l2
                count += 1 
            val = str(average/count)
            send_str = val.encode(database.ENCODER)
            connection.sendall(send_str)
            print("Sent: ", send_str)
            #print("Lab 2 averge: ", average/id.length())
        elif command == "GL3":
            print("Command: ", command)
            for id,t in self.students.items():
                average += t.l3
                count += 1 
            val = str(average/count)
            send_str = val.encode(database.ENCODER)
            connection.sendall(send_str)
            print("Sent: ", send_str)
            #print("Lab 3 averge: ", average/id.length())
        elif command == "GL4":
            print("Command: ", command)
            for id,t in self.students.items():
                average += t.l4
                count += 1 

            val = str(average/count)
            send_str = val.encode(database.ENCODER)
            connection.sendall(send_str)
            print("Sent: ", send_str)
            #print("Lab 4 averge: ", average/id.length())
        elif command == "GMA":
            print("Command: ", command)
            for id,t in self.students.items():
                average += t.mt
                count += 1

            val = str(average/count)
            send_str = val.encode(database.ENCODER)
            connection.sendall(send_str)
            print("Sent: ", send_str)

        else:
            
            #student_num = int(cmd_content[1])
            #password = cmd_content[2]        
            hashPass = command
            print("Received ID/Password Hash: ", hashPass)
            foundVal = False    
            for id,t in self.students.items():
            	if self.get_hash_ID_Password(str(id),t.passw) == hashPass:
            	    user = id
            	    for id1,t1 in self.students.items():
            	    	if(user == id1):
            	    		send_str = " ".join((
		                                    "Lab1:",str(t.l1),"Lab2:",str(t.l2),"Lab3:",str(t.l3),"Lab4:",str(t.l4),
		                                    "Midterm:",str(t.mt),"Exam1:",str(t.e1),"Exam2:",str(t.e2),"Exam3:",str(t.e3),"Exam4:",str(t.e4)
		                                    )).encode(database.ENCODER)
            	    		foundVal = True
            	    		print("Correct password, record found")
            if(foundVal == False):
            	send_str = "ID/Password entry does not match record".encode(database.ENCODER)
            connection.sendall(send_str)
            print("Sent: ", send_str)

        #for id,t in self.students.items():
        #    print("Student ID: {} Name: \"{}\"".format(id, t.StudName))
        #print()
        
    def get_hash_ID_Password(self, id, password):
        h = hashlib.sha256() # Create sha256 hash object
        
        h.update(id.encode("utf-8")) # Getting full hash with encoded ID
        h.update(password.encode("utf-8")) # Getting full hash with encoded Password

        return h.digest()  # return the ID/Password Hash

# Client code
class Client:
    #SERVER_HOSTNAME = "192.168.1.22"
    SERVER_HOSTNAME = socket.gethostname()
    BUFFER_SIZE = 1024

    def __init__(self):
        #print("setting up get_socket()")
        self.get_socket()
        #print("finish get_socket()")

        #print("setting up connect_to_server()")
        self.connect_to_server()
        #print("finish connect_to_server()")

        #print("setting up send_console()")
        self.send_console()
        #print("finish send_console()")

    def get_socket(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except Exception as msg:
            print(msg)
            sys.exit(1)

    def connect_to_server(self):
        try:
            #print(Client.SERVER_HOSTNAME)
            #print(database.PORT)
            self.socket.connect((Client.SERVER_HOSTNAME, database.PORT))
            print("Connected to \"{}\" on port {}".format(Client.SERVER_HOSTNAME, database.PORT))
        except Exception as msg:
            print(msg)
            sys.exit(1)
    
    def send_console(self):
        while True:
            try:
                self.get_console_input()
                self.connection_send()
                self.connection_recv()
            except (KeyboardInterrupt, EOFError):
                print()
                print("Closing connection with server...")
                self.socket.close()
                sys.exit(1)

    def get_console_input(self):
        while True:
            self.input_text = input("Input: ")
            if self.input_text != "":
                break

    def connection_send(self):
        try:
            print("Commend entered: ",self.input_text)
                     
            if self.input_text == "get lab average":
                print("Fetching lab 1 average...")
                self.socket.sendall(self.input_text.encode(database.ENCODER))
            elif self.input_text == "get lab 2 average":
                print("Fetching lab 2 average...")
                self.socket.sendall(self.input_text.encode(database.ENCODER))
            elif self.input_text == "get lab 3 average":
                print("Fetching lab 3 average...")
                self.socket.sendall(self.input_text.encode(database.ENCODER))
            elif self.input_text == "get lab 4 average":
                print("Fetching lab 4 average...")
                self.socket.sendall(self.input_text.encode(database.ENCODER))
            elif self.input_text == "get midterm average":
                print("Fetching midterm average...")
                self.socket.sendall(self.input_text.encode(database.ENCODER))
            elif self.input_text == "GG":
                self.student_num = input("Student ID: ")
                self.password = getpass.getpass(prompt = "Password: ")
                #print("Student ID received: ", self.student_num)
                #print("Password received: ", self.password)

                new_str = self.get_hash_ID_Password(self.student_num,self.password)
                print("Sent ID/Password Hash: ", new_str)
                #self.socket.sendall(new_str.encode(database.ENCODER))
                self.socket.sendall(new_str)
            else:
                print("Command doesn't exist")

        except Exception as msg:
            print(msg)
            sys.exit(1)
    
    def get_hash_ID_Password(self, id, password):
        h = hashlib.sha256() # Create sha256 hash object
        
        h.update(id.encode("utf-8")) # Getting full hash with encoded ID
        h.update(password.encode("utf-8")) # Getting full hash with encoded Password

        return h.digest()  # return the ID/Password Hash
    
    def connection_recv(self):
        try:
            recv_bytes = self.socket.recv(database.BUFFER_SIZE)

            if len(recv_bytes) == 0:
                print("Closing server connection...")
                self.socket.close()
                sys.exit(1)
            print("-"*72)
            print("Received: ", recv_bytes.decode(database.ENCODER))
            print("-"*72)

        except Exception as msg:
            print(msg)
            sys.exit(1)

#terminal run code    
if __name__ == "__main__":
    #DEFINE_database = './course_grades_2022.csv'
    #DEFINE_class = "4DN4"

    #new_database = database(DEFINE_class, DEFINE_database)

    #print('-'*72)
    #print("Course Name: \"{}\".".format(new_database.name))
    #print('-'*72)    

    #functions = {
    #    'print': new_database.print_students
    #}

    roles = {'client': Client, 'server': database}

    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--role', choices=roles,
                        help='server or client role',
                        required=True, type=str)

    args = parser.parse_args()
    roles[args.role]()


