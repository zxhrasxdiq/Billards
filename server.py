import Physics
import phylib

import cgi
import sys
import os

from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qsl;

class MyHandler( BaseHTTPRequestHandler ):

    def do_GET(self):

        # parse the URL to get the path and form data
        parsed  = urlparse( self.path );
        #print("This is parsed ", parsed)
        print("Parsed path:", self.path)
        if parsed.path == '/favicon.ico':
        # Open the favicon.ico file in binary mode
            with open('favicon.ico', 'rb') as f:
            # Set response headers
                self.send_response(200)
                self.send_header('Content-type', 'image/x-icon')
                self.end_headers()
            # Write the content of the favicon.ico file to the response
                self.wfile.write(f.read())
            return

        # check if the web-pages matches the list
        elif parsed.path in [ '/webpage.html' ]:

            # retreive the HTML file
            fp = open( '.'+self.path );
            content = fp.read();

            try: # open shoot.html and write data to HTML
                with open('webpage.html', 'r') as fp:
                    content = fp.read()
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(bytes(content, 'utf-8'))
            except FileNotFoundError:
                # send 404 errors
                self.send_response(404)
                self.end_headers()
                self.wfile.write(bytes("Error 404!!! File: %s not found\n404" % self.path, "utf-8"))

            fp.close();

        elif parsed.path in [ '/display.html' ]:

            # retreive the HTML file
            fp = open( '.'+self.path );
            content = fp.read();

            try: # open shoot.html and write data to HTML
                with open('display.html', 'r') as fp:
                    content = fp.read()
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(bytes(content, 'utf-8'))
            except FileNotFoundError:
                # send 404 errors
                self.send_response(404)
                self.end_headers()
                self.wfile.write(bytes("Error 404!!! File: %s not found\n404" % self.path, "utf-8"))

            fp.close();

        elif parsed.path in [ '/display.js' ]:

            # retreive the HTML file
            fp = open( '.'+self.path );
            content = fp.read();

            try: # open shoot.html and write data to HTML
                with open('display.js', 'r') as fp:
                    content = fp.read()
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(bytes(content, 'utf-8'))
            except FileNotFoundError:
                # send 404 errors
                self.send_response(404)
                self.end_headers()
                self.wfile.write(bytes("Error 404!!! File: %s not found\n404" % self.path, "utf-8"))

            fp.close();

        # check if the web-pages matches the list
        elif parsed.path.startswith('/table-') and parsed.path.endswith('.svg'): 
            file_path = parsed.path.lstrip("/")

            fp = open( '.'+self.path );
            content = fp.read();

            try:
                split_table = parsed.path.split('-')
                table_number = split_table[1].split('.')[0]
                file_path = f'table-{table_number}.svg'

                if os.path.exists(file_path):
                    fp = open( '.'+self.path );
                    content = fp.read();
                    self.send_response(200)
                    self.send_header('Content-type', 'image/svg+xml')
                    self.send_header("Content-length", len(content))
                    self.end_headers();
                    self.wfile.write(bytes(content, 'utf-8'))
                    fp.close();
            except FileNotFoundError:
                # generate 404 for GET requests that aren't the table.svg files above
                self.send_response(404) # NOT OK
                self.end_headers()
                self.wfile.write(bytes("ERROR 404. File: %s not found\n404" % self.path, "utf-8"))

        elif self.path == '/firstTable.svg':
            file_path = 'firstTable.svg'  # Adjust this path according to the location of your SVG file

            if os.path.exists(file_path):
                with open(file_path, 'rb') as fp:
                    content = fp.read()
                    self.send_response(200)
                    self.send_header('Content-type', 'image/svg+xml')
                    self.send_header("Content-length", len(content))
                    self.end_headers()
                    self.wfile.write(content)
            else:
                # Return 404 if the file does not exist
                self.send_response(404)
                self.end_headers()
                self.wfile.write(bytes("ERROR 404. File: %s not found\n404" % self.path, "utf-8"))

        else:
            # generate 404 for GET requests that aren't the 2 files above
            self.send_response( 404 );
            self.end_headers();
            self.wfile.write( bytes( "404: %s not found" % self.path, "utf-8" ) );


    def do_POST(self):
        # handle post request
        # parse the URL to get the path and form data
        parsed  = urlparse( self.path );
        print("Parsed path:", self.path);

        if parsed.path in [ '/display.html' ]:

            # get data send as Multipart FormData (MIME format)
            form = cgi.FieldStorage( fp=self.rfile,
                                     headers=self.headers,
                                     environ = { 'REQUEST_METHOD': 'POST',
                                                 'CONTENT_TYPE': 
                                                   self.headers['Content-Type'],
                                               } 
                                    )

            #Delete all table-?.svg files
            serv_dir = './'
            for filename in os.listdir(serv_dir):
                if filename.startswith('table') and filename.endswith('.svg'):
                    file_path = os.path.join(serv_dir, filename)
                    os.remove(file_path) # delete the file



            sBall1Pos = Physics.Coordinate(675, 725)
            stillBall1 = Physics.StillBall(1,sBall1Pos)
            sBall2Pos = Physics.Coordinate(640,640)
            stillBall2 = Physics.StillBall(2,sBall2Pos)
            sBall3Pos = Physics.Coordinate(705,665)
            stillBall3 = Physics.StillBall(3,sBall3Pos)
            sBall4Pos = Physics.Coordinate(600,575)
            stillBall4 = Physics.StillBall(4,sBall4Pos)
            sBall5Pos = Physics.Coordinate(676, 578)
            stillBall5 = Physics.StillBall(5,sBall5Pos)
            sBall6Pos = Physics.Coordinate(740,574)
            stillBall6 = Physics.StillBall(6,sBall6Pos)
            sBall7Pos = Physics.Coordinate(550,525)
            stillBall7 = Physics.StillBall(7,sBall7Pos)
            sBall8Pos = Physics.Coordinate(630,512)
            stillBall8 = Physics.StillBall(8,sBall8Pos)
            sBall9Pos = Physics.Coordinate(710, 499)
            stillBall9 = Physics.StillBall(9,sBall9Pos)
            sBall10Pos = Physics.Coordinate(800,512)
            stillBall10 = Physics.StillBall(10,sBall10Pos)
            sBall11Pos = Physics.Coordinate(500,445)
            stillBall11 = Physics.StillBall(11,sBall11Pos)
            sBall12Pos = Physics.Coordinate(590,420)
            stillBall12 = Physics.StillBall(12,sBall12Pos)
            sBall13Pos = Physics.Coordinate(675,410)
            stillBall13 = Physics.StillBall(13,sBall13Pos)
            sBall14Pos = Physics.Coordinate(775,425)
            stillBall14 = Physics.StillBall(14,sBall14Pos)
            sBall15Pos = Physics.Coordinate(845,450)
            stillBall15 = Physics.StillBall(15,sBall15Pos)
            sBall0Pos = Physics.Coordinate(676, 1400)
            stillBall0 = Physics.StillBall(0, sBall0Pos)

            table = Physics.Table()
            table += stillBall0
            table += stillBall1
            table += stillBall2
            table += stillBall3
            table += stillBall4
            table += stillBall5
            table += stillBall6
            table += stillBall7
            table += stillBall8
            table += stillBall9
            table += stillBall10
            table += stillBall11
            table += stillBall12
            table += stillBall13
            table += stillBall14
            table += stillBall15

            print(table)

            velocityX = form.getvalue('velocityX')
            velocityY = form.getvalue('velocityY')
            gameName = form.getvalue('gameName');
            player1Name = form.getvalue('player1Name')
            player2Name = form.getvalue('player2Name')
            counter = form.getvalue('counter')
            # Do something with the received data
            print("Received velX:", velocityX)
            print("Received velY:", velocityY)
            velX = float(velocityX)
            velY = float(velocityY)
            print("Received gameName:", gameName)
            print("Received player1Name:", player1Name)
            print("Received player2Name:", player2Name)
            print("Received counter:", counter)
            gamePath = float(counter)
            print("GamePath:", gamePath)

            checkGame = 0
            game = 0
            numFrames = 0
            htmlString = ""

            # print('This is the second time I call table ')
            # print(table)

            if gamePath == -1:
                htmlString = """<html><head><title>Displaying The Winner!</title><head>\n"""
                htmlString += "<h1>No Winner!</h1>\n"
                htmlString += '<a href="/webpage.html">Continue Playing the Game</a>\n'
            elif checkGame == 0:
                checkGame = 1
                game = Physics.Game( gameName=gameName, player1Name=player1Name, player2Name=player2Name, table=table)
                numFrames = game.shoot(gameName, player1Name, table, velX, velY ) 
                print("NumFrames:", numFrames)
               
                for i in range(0, numFrames):
                    with open(f"table-{i}.svg", "w") as fp:
                        table = game.gameRead(table, i)
                        print("This is in the range loop ", table)
                        fp.write(table.svg())

                #Construct HTML content for the animation
                htmlString = "<!DOCTYPE html>\n"
                htmlString += '<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Shot Animation</title>\n'
                htmlString += '<style>img {max-width: 20%;height: auto;}</style>\n'
                htmlString += '</head><body><button onclick="startAnimation()">Start Animation!</button>\n<button onclick="stopAnimation()">Stop Animation!</button>\n'
                htmlString += '<div id="imageContainer">\n\n</div>'
                htmlString += '<a href="/webpage.html">Continue Playing</a>'
                htmlString += '<script>\nvar images = [\n'
                i = 0
                while os.path.exists(f"table-{i}.svg"):
                    if os.path.exists(f"table-{i+1}.svg"):
                        htmlString += f"'table-{i}.svg', "
                    else:
                        htmlString += f"'table-{i}.svg'\n"
                    i += 1

                htmlString += '];\n var currentIndex = 0;\nvar intervalId;\nvar loadedImages = [];\n'
                htmlString += 'function preloadImages() {\nfor (var i = 0; i < images.length; i++) {\nvar img = new Image();\nimg.src = images[i];\nloadedImages.push(img);\n}\n}\n'
                htmlString += 'function startAnimation() {\ncurrentIndex = 0;\nshowImage();\nintervalId = setInterval(nextImage, 20);\n}\n'
                htmlString += 'function stopAnimation() {\nclearInterval(intervalId); // Stop the animation\n}\n'
                htmlString += 'function nextImage() {\ncurrentIndex = (currentIndex + 1) % images.length; // Move to the next image, looping back to the beginning if necessary\nshowImage();\n}\n'
                htmlString += "function showImage() {\nvar imageContainer = document.getElementById('imageContainer');\nimageContainer.innerHTML = ''; // Clear previous image(s)\nvar img = loadedImages[currentIndex];\nimageContainer.appendChild(img)\n;}\n"
                htmlString += "window.onload = preloadImages;\n</script>\n</body>\n</html>\n"


                file_path = "display.html" 
               
            else:
                numFrames = game.shoot(gameName, player1Name, table, velX, velY ) 
                print("NumFrames:", numFrames)

            file_path = "display.html"

            # Open the file in write mode
            with open(file_path, "w") as file:
                # Write the HTML content to the file
                file.write(htmlString)
        

            # writing out with text html content type
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes(htmlString, "utf-8"))
   
        else:
            # generate 404 for GET requests that aren't the 2 files above
            self.send_response( 404 );
            self.end_headers();
            self.wfile.write( bytes( "404: %s not found" % self.path, "utf-8" ) );

if __name__ == "__main__":
    httpd = HTTPServer(('localhost', int(sys.argv[1])), MyHandler);
    print("Server listing in port:  ", int(sys.argv[1]));
    httpd.serve_forever();