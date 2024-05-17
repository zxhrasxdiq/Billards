import phylib;
import os
import sqlite3
import math

################################################################################
# import constants from phylib to global varaibles
BALL_RADIUS   = phylib.PHYLIB_BALL_RADIUS;
BALL_DIAMETER = phylib.PHYLIB_BALL_DIAMETER;
HOLE_RADIUS = phylib.PHYLIB_HOLE_RADIUS;
TABLE_LENGTH = phylib.PHYLIB_TABLE_LENGTH;
TABLE_WIDTH = phylib.PHYLIB_TABLE_WIDTH;
SIM_RATE = phylib.PHYLIB_SIM_RATE;
VEL_EPSILON = phylib.PHYLIB_VEL_EPSILON;
DRAG = phylib.PHYLIB_DRAG;
MAX_TIME = phylib.PHYLIB_MAX_TIME;
MAX_OBJECTS = phylib.PHYLIB_MAX_OBJECTS;
FRAME_INTERVAL = 0.01;


HEADER = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"
"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg width="700" height="1375" viewBox="-25 -25 1400 2750"
xmlns="http://www.w3.org/2000/svg"
xmlns:xlink="http://www.w3.org/1999/xlink">
<rect width="1350" height="2700" x="0" y="0" fill="#C0D0C0" />""";
FOOTER = """</svg>\n""";

# add more here

################################################################################
# the standard colours of pool balls
# if you are curious check this out:  
# https://billiards.colostate.edu/faq/ball/colors/

BALL_COLOURS = [ 
    "WHITE",
    "YELLOW",
    "BLUE",
    "RED",
    "PURPLE",
    "ORANGE",
    "GREEN",
    "BROWN",
    "BLACK",
    "LIGHTYELLOW",
    "LIGHTBLUE",
    "PINK",             # no LIGHTRED
    "MEDIUMPURPLE",     # no LIGHTPURPLE
    "LIGHTSALMON",      # no LIGHTORANGE
    "LIGHTGREEN",
    "SANDYBROWN",       # no LIGHTBROWN 
    ];

################################################################################
class Coordinate( phylib.phylib_coord ):
    """
    This creates a Coordinate subclass, that adds nothing new, but looks
    more like a nice Python class.
    """
    pass;


################################################################################
class StillBall( phylib.phylib_object ):
    """
    Python StillBall class.
    """

    def __init__( self, number, pos ):
        """
        Constructor function. Requires ball number and position (x,y) as
        arguments.
        """

        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_STILL_BALL, 
                                       number, 
                                       pos, None, None, 
                                       0.0, 0.0 );
      
        self.__class__ = StillBall;

    def svg (self):
        stillBallString = """ <circle cx="%d" cy="%d" r="%d" fill="%s" />\n""" % (self.obj.still_ball.pos.x, self.obj.still_ball.pos.y, BALL_RADIUS, BALL_COLOURS[self.obj.still_ball.number])
        return stillBallString;


################################################################################

class RollingBall(phylib.phylib_object):

    def __init__(self, number, pos, vel, acc):
    
        phylib.phylib_object.__init__(self,
                                    phylib.PHYLIB_ROLLING_BALL, 
                                    number, 
                                    pos, vel, acc, 
                                    0.0, 0.0);
        self.__class__ = RollingBall;
    
    def svg (self):
        rollingBallString = """ <circle cx="%d" cy="%d" r="%d" fill="%s" />\n""" % (self.obj.rolling_ball.pos.x, self.obj.rolling_ball.pos.y, BALL_RADIUS, BALL_COLOURS[self.obj.rolling_ball.number])
        return rollingBallString;

###############################################################################

class Hole(phylib.phylib_object):

    def __init__(self, pos):
        phylib.phylib_object.__init(self, phylib.PHYLIB_HOLE, 0, pos, None, None, 0.0, 0.0);
        self.__class__ = Hole;

    def svg (self):
        holeString = """ <circle cx="%d" cy="%d" r="%d" fill="%s" />\n""" % (self.obj.hole.pos.x, self.obj.hole.pos.y, HOLE_RADIUS, BALL_COLOURS[8])
        return holeString;

###############################################################################

class HCushion(phylib.phylib_object):

    def __init__(self, y):
        phylib.phylib_object.__init(self, phylib.PHYLIB_HCUSHION, None, None, None, None, 0.0, y);
        self.__class__ = HCushion;
    
    def svg(self):
        if(self.obj.hcushion.y == 0): 
            hCushionString = """ <rect width="1400" height="25" x="-25" y="%d" fill="darkgreen" />\n""" % (-25)
        elif(self.obj.hcushion.y > 0): 
            hCushionString = """ <rect width="1400" height="25" x="-25" y="%d" fill="darkgreen" />\n""" % (2700)
        return hCushionString;

###############################################################################

class VCushion(phylib.phylib_object):

    def __init__(self, x):
        phylib.phylib_object.__init(self, phylib.PHYLIB_VCUSHION, None, None, None, None, x, 0.0);
        self.__class__ = VCushion;
    
    def svg(self):
        if(self.obj.vcushion.x == 0): 
            vCushionString = """ <rect width="25" height="2750" x="%d" y="-25" fill="darkgreen" />\n""" % (-25)
        elif(self.obj.vcushion.x > 0): 
            vCushionString = """ <rect width="25" height="2750" x="%d" y="-25" fill="darkgreen" />\n""" % (1350)
        return vCushionString;

###############################################################################

class Table( phylib.phylib_table ):
    """
    Pool table class.
    """

    def __init__( self ):
        """
        Table constructor method.
        This method call the phylib_table constructor and sets the current
        object index to -1.
        """
        phylib.phylib_table.__init__( self );
        self.current = -1;

    def __iadd__( self, other ):
        """
        += operator overloading method.
        This method allows you to write "table+=object" to add another object
        to the table.
        """
        self.add_object( other );
        return self;

    def __iter__( self ):
        """
        This method adds iterator support for the table.
        This allows you to write "for object in table:" to loop over all
        the objects in the table.
        """
        return self;

    def __next__( self ):
        """
        This provides the next object from the table in a loop.
        """
        self.current += 1;  
        if self.current < MAX_OBJECTS:  
            return self[ self.current ]; 

        self.current = -1;   
        raise StopIteration;  

    def __getitem__( self, index ):
        """
        This method adds item retreivel support using square brackets [ ] .
        It calls get_object (see phylib.i) to retreive a generic phylib_object
        and then sets the __class__ attribute to make the class match
        the object type.
        """
        result = self.get_object( index ); 
        if result==None:
            return None;
        if result.type == phylib.PHYLIB_STILL_BALL:
            result.__class__ = StillBall;
        if result.type == phylib.PHYLIB_ROLLING_BALL:
            result.__class__ = RollingBall;
        if result.type == phylib.PHYLIB_HOLE:
            result.__class__ = Hole;
        if result.type == phylib.PHYLIB_HCUSHION:
            result.__class__ = HCushion;
        if result.type == phylib.PHYLIB_VCUSHION:
            result.__class__ = VCushion;
        return result;

    def __str__( self ):
        """
        Returns a string representation of the table that matches
        the phylib_print_table function from A1Test1.c.
        """
        result = "";  
        result += "time = %6.1f;\n" % self.time; 
        for i,obj in enumerate(self): 
            result += "  [%02d] = %s\n" % (i,obj);  
        return result; 

    def segment( self ):
        """
        Calls the segment method from phylib.i (which calls the phylib_segment
        functions in phylib.c.
        Sets the __class__ of the returned phylib_table object to Table
        to make it a Table object.
        """

        result = phylib.phylib_table.segment( self );
        if result:
            result.__class__ = Table;
            result.current = -1;
        return result;

    def svg (self):
        resultedString = HEADER

        for object in self:
           if object is not None:
            resultedString += object.svg()
        resultedString += FOOTER
        return resultedString
    

    def roll(self, t):
        new = Table();
        for ball in self:
            if isinstance(ball, RollingBall):
                new_ball = RollingBall(ball.obj.rolling_ball.number, Coordinate(0,0),Coordinate(0,0), Coordinate(0,0));
                phylib.phylib_roll(new_ball, ball, t);
                new+=new_ball;
            if isinstance(ball, StillBall):
                new_ball = StillBall(ball.obj.still_ball.number,
                                     Coordinate(ball.obj.still_ball.pos.x,
                                     (ball.obj.still_ball.pos.y)));
                new+=new_ball;
        return new;

    def findCueBall(self):
        for ball in self:
            if(isinstance(ball, StillBall) and ball.obj.still_ball.number == 0):
                return ball
        return None


class Database():

    def __init__( self, reset=False ):
        if reset == True:
            if os.path.exists( 'phylib.db' ): 
                os.remove( 'phylib.db' );
        self.conn = sqlite3.connect( 'phylib.db' ); 
    
    def close( self ):
        if(self.conn): 
            self.conn.commit();
            self.conn.close();
            

    def pp( listoftuples ): 
        if len(listoftuples)==0:
            print( repr( listoftuples ) );
            return;
        columns = len(listoftuples[0]);
        widths = [ max( [ len(str(item[col])) for item in listoftuples ] ) \
                                    for col in range( columns ) ];
        fmt = " | ".join( ["%%-%ds"%width for width in widths] );
        for row in listoftuples:
            print( fmt % row );

    def printDB(self): 
        self.cur = self.conn.cursor();

        print("BALL:")
        self.cur = self.conn.execute("""SELECT * FROM Ball;""")
        result = self.cur.fetchall();
        print(result)
        print("TTABLE:")
        self.cur = self.conn.execute("""SELECT * FROM TTable;""")
        result = self.cur.fetchall();
        print(result)
        print("BALLTABLE:")
        self.cur = self.conn.execute("""SELECT * FROM BallTable;""")
        result = self.cur.fetchall();
        print(result)

        self.conn.commit();
        self.cur.close();

    def createDB( self ):
        
        self.cur = self.conn.cursor(); 

        self.cur = self.conn.execute("""CREATE TABLE IF NOT EXISTS Ball(
            BALLID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            BALLNO INTEGER NOT NULL,
            XPOS FLOAT NOT NULL,
            YPOS FLOAT NOT NULL,
            XVEL FLOAT,
            YVEL FLOAT
            );""")

        self.cur = self.conn.execute("""CREATE TABLE IF NOT EXISTS TTable(
            TABLEID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            TIME FLOAT NOT NULL
            );""")

        self.cur = self.conn.execute( """CREATE TABLE IF NOT EXISTS BallTable (
           BALLID  INTEGER NOT NULL,
           TABLEID INTEGER NOT NULL,
           FOREIGN KEY (BALLID) REFERENCES Ball ON UPDATE CASCADE,
           FOREIGN KEY (TABLEID) REFERENCES TTable );""");

        self.cur = self.conn.execute("""CREATE TABLE IF NOT EXISTS Game(
            GAMEID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            GAMENAME VARCHAR(64) NOT NULL
            );""")

        self.cur = self.conn.execute("""CREATE TABLE IF NOT EXISTS Player(
            PLAYERID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            GAMEID INTEGER NOT NULL,
            PLAYERNAME VARCHAR(64) NOT NULL,
            FOREIGN KEY (GAMEID) REFERENCES Game
            );""")

        self.cur = self.conn.execute("""CREATE TABLE IF NOT EXISTS Shot(
            SHOTID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            PLAYERID INTEGER NOT NULL,
            GAMEID INTEGER NOT NULL,
            FOREIGN KEY (PLAYERID) REFERENCES Player,
            FOREIGN KEY (GAMEID) REFERENCES Game
            );""")

        self.cur = self.conn.execute( """CREATE TABLE IF NOT EXISTS TableShot (
           TABLEID  INTEGER NOT NULL,
           SHOTID INTEGER NOT NULL,
           FOREIGN KEY (TABLEID) REFERENCES TTable,
           FOREIGN KEY (SHOTID) REFERENCES Shot );""");
        
        self.conn.commit();
        self.cur.close();

    def readTable(self, tableId):
        
        self.cur = self.conn.cursor(); 

        tableId += 1 
        self.cur.execute("SELECT * FROM BallTable WHERE TABLEID = ?", (tableId,))
        fetched = self.cur.fetchone()
        if fetched == None: 
            self.conn.commit();
            self.cur.close();
            return None

        newTable = Table(); 
        selectedID = tableId

        self.cur.execute("""SELECT Ball.* FROM Ball
            INNER JOIN BallTable ON Ball.BALLID = BallTable.BALLID
            WHERE BallTable.TABLEID=?;""", (tableId,))
        fetched = self.cur.fetchall();
       
        for i in range(len(fetched)):
            if fetched[i][4] is None and fetched[i][5] is None: 
                ballID = fetched[i][0]
                ballNo = fetched[i][1]
                xPos = fetched[i][2]
                yPos = fetched[i][3]
                xVel = 0
                yVel = 0
                sPos = Coordinate(xPos, yPos) 
                sBall = StillBall(ballNo, sPos)
                newTable += sBall 
            else: 
                ballID = fetched[i][0]
                ballNo = fetched[i][1]
                xPos = fetched[i][2]
                yPos = fetched[i][3]
                xVel = fetched[i][4]
                yVel = fetched[i][5]
                rPos = Coordinate(xPos, yPos) 
                rVel = Coordinate(xVel, yVel)

                rAcc = Coordinate(0.0, 0.0)
                rSpeed = phylib.phylib_length(rVel)

                if (rSpeed > VEL_EPSILON):
                    rAcc.x = ((xVel * -1.0) / rSpeed) * DRAG
                    rAcc.y = ((yVel * -1.0) / rSpeed) * DRAG

                rBall = RollingBall(ballNo, rPos, rVel, rAcc)
                newTable += rBall 

        self.cur.execute("""SELECT TIME FROM TTable
                               WHERE TABLEID = ?""", (tableId,))
        time = self.cur.fetchone()
        newTable.time = time[0] 
        
        self.conn.commit(); 
        self.cur.close();
        return newTable
        
    def writeTable(self, table):
        self.cur = self.conn.cursor() 
        tableId = 0 
        counter = 1
        xPos = 0
        yPos = 0 
        xVel = 0
        yVel = 0
        ballID = 0; 
        ballStr = ""
        ball_data = (None)

        tableStr = f"""INSERT INTO TTable (TIME)
            VALUES ({table.time});"""
        self.cur = self.conn.execute(tableStr)

        tableStr = f"""SELECT TABLEID FROM TTable
                    WHERE TIME={table.time};"""
        self.cur = self.conn.execute(tableStr)

        getID = self.cur.fetchone();

        tableId = getID[0]

        for ball in table:
            
            if isinstance( ball, RollingBall ):
                
                ballNum = ball.obj.rolling_ball.number
                xPos = ball.obj.rolling_ball.pos.x
                
                yPos = ball.obj.rolling_ball.pos.y
                xVel = ball.obj.rolling_ball.vel.x
                yVel = ball.obj.rolling_ball.vel.y
                ballStr = """INSERT INTO Ball ( BALLNO, XPOS, YPOS, XVEL, YVEL)
                    VALUES (?, ?, ?, ?, ?);"""
               
                self.cur = self.conn.execute("""INSERT INTO Ball ( BALLNO, XPOS, YPOS, XVEL, YVEL)
                    VALUES (?, ?, ?, ?, ?);""", (ballNum, xPos, yPos, xVel, yVel))
                
                self.cur = self.conn.execute("""SELECT BALLID FROM Ball
                    ORDER BY BALLID DESC""")
                ballID = self.cur.fetchone()
                ballID = ballID[0]
                self.cur = self.conn.execute("""INSERT INTO BallTable (BALLID, TABLEID)
                    VALUES (?, ?);""", (ballID, tableId))

            elif isinstance( ball, StillBall ):
                
                ballNum = ball.obj.still_ball.number
                xPos = ball.obj.still_ball.pos.x
                
                yPos = ball.obj.still_ball.pos.y
                xVel = 0
                yVel = 0
                ballStr = """INSERT INTO Ball ( BALLNO, XPOS, YPOS)
                    VALUES (?, ?, ?);"""

                self.cur = self.conn.execute("""INSERT INTO Ball ( BALLNO, XPOS, YPOS)
                    VALUES (?, ?, ?);""", (ballNum, xPos, yPos))
       
                self.cur = self.conn.execute("""SELECT BALLID FROM Ball
                    ORDER BY BALLID DESC""")
                ballID = self.cur.fetchone()
                ballID = ballID[0]
                self.cur = self.conn.execute("""INSERT INTO BallTable (BALLID, TABLEID)
                    VALUES (?, ?);""", (ballID, tableId))

        self.conn.commit();
        self.cur.close();
        tableId = tableId - 1 
        return tableId

    def getGame( self, gameID ):
        self.cur = self.conn.cursor()
        self.cur = self.conn.execute(f"""SELECT Player.PLAYERID, Player.PLAYERNAME, Game.GAMENAME FROM Player
            JOIN Game ON Player.GAMEID = Game.GAMEID
            WHERE Game.GAMEID={gameID};""")
        gameStatus = self.cur.fetchall()
        return gameStatus

    def setGame( self, gameName, player1Name, player2Name ):
        self.cur = self.conn.cursor()

        gameStr = f"""INSERT INTO Game (GAMENAME)
            VALUES ({gameName});"""
        self.cur = self.conn.execute(f"""INSERT INTO Game (GAMENAME)
            VALUES (?);""", (gameName,))
        
        gameStr = f"""SELECT GAMEID FROM Game
            WHERE GAMENAME={gameName}"""
        self.cur = self.conn.execute("""SELECT GAMEID FROM Game
            WHERE GAMENAME=?""", (gameName,))
        gameID = self.cur.fetchone()
        gameID = gameID[0]

        self.cur = self.conn.execute("""INSERT INTO Player (GAMEID, PLAYERNAME)
            VALUES (?, ?);""", (gameID, player1Name,))
        self.cur = self.conn.execute("""INSERT INTO Player (GAMEID, PLAYERNAME)
            VALUES (?, ?);""", (gameID, player2Name,))
        
        self.conn.commit() 
        self.cur.close()

    def newShot(self, playerName):
        self.cur = self.conn.cursor()
        
        self.cur = self.conn.execute("""SELECT GAMEID FROM Player
            WHERE PLAYERNAME=?""", (playerName,))
        gameID = self.cur.fetchone()
        gameID = gameID[0]

        self.cur = self.conn.execute("""SELECT PLAYERID FROM Player
            WHERE PLAYERNAME=?""", (playerName,))
        playerID = self.cur.fetchone()
        playerID = playerID[0]

        self.cur = self.conn.execute("""INSERT INTO Shot (GAMEID, PLAYERID)
            VALUES (?, ?);""", (gameID, playerID,))
        self.cur = self.conn.execute("""SELECT SHOTID FROM Shot
            ORDER BY SHOTID DESC""")
        shotID = self.cur.fetchone()
        shotID = shotID[0]

        self.conn.commit()
        self.cur.close()

        return shotID

    def newTableShot(self, tableID, shotID):
        self.cur = self.conn.cursor() 
        self.cur.execute("""INSERT INTO TableShot (TABLEID, SHOTID) 
            VALUES (?, ?)""", (tableID, shotID))

        self.conn.commit()
        self.cur.close()

################################################################################
class Game():
    def __init__( self, gameID=None, gameName=None, player1Name=None, player2Name=None, table=None):
        database = Database(reset=True)
        database.createDB()
        if gameID is not None and gameName is None and player1Name is None and player2Name is None:
            gameID += 1 
            gameStuff = database.getGame(gameID) 

            if gameStuff[0][0] < gameStuff[1][0]:
                self.player1Name = gameStuff[0][1]
                self.player2Name = gameStuff[1][1]
            elif gameStuff[0][0] > gameStuff[1][0]:
                self.player1Name = gameStuff[1][1]
                self.player2Name = gameStuff[0][1]
            self.gameName = gameStuff[0][2]

        elif gameID is None and gameName is not None and player1Name is not None and player2Name is not None:
            self.gameName = gameName
            self.player1Name = player1Name
            self.player2Name = player2Name
            database.setGame(gameName, player1Name, player2Name)
        else:
            raise TypeError("""Invalid! Everything must be set to None except gameID\n
                OR only gameID must be set to None!""")
    
    def calcTotalFrames(self, beforeTable, afterTable):
        totalFrames = math.floor((afterTable.time - beforeTable.time)/FRAME_INTERVAL)
        return totalFrames

    def shoot( self, gameName, playerName, table, xvel, yvel ):
        db = Database(reset=False)
        cur = db.conn.cursor()

        shotID = db.newShot(playerName)

        foundCueBall = table.findCueBall()

        xPos = 0
        yPos = 0
        xAcc = 0
        yAcc = 0
        xPos = foundCueBall.obj.still_ball.pos.x;
        yPos = foundCueBall.obj.still_ball.pos.y;
        
        foundCueBall.type = phylib.PHYLIB_ROLLING_BALL
        foundCueBall.obj.rolling_ball.number = 0

        totaltotalFrames = 0;

        rVel = Coordinate(xvel, yvel)
        rSpeed = phylib.phylib_length(rVel)

        if (rSpeed > VEL_EPSILON):
            xAcc = ((xvel * -1.0) / rSpeed) * DRAG
            yAcc = ((yvel * -1.0) / rSpeed) * DRAG

        foundCueBall.obj.rolling_ball.pos.x = xPos;
        foundCueBall.obj.rolling_ball.pos.y = yPos;
        foundCueBall.obj.rolling_ball.vel.x = xvel;
        foundCueBall.obj.rolling_ball.vel.y = yvel;
        
        foundCueBall.obj.rolling_ball.acc.x = xAcc
        foundCueBall.obj.rolling_ball.acc.y = yAcc
       
        beforeTable = table
        afterTable = table
        totalTime = 0.0

        tableList = []

        while (True):
            afterTable = afterTable.segment()
            if afterTable is None:
                break;

            totalFrames = self.calcTotalFrames(beforeTable, afterTable)
            totaltotalFrames += totalFrames
            print(totalFrames)
            for frameNum in range(totalFrames):
                rollValue = frameNum*FRAME_INTERVAL 
                newTable = beforeTable.roll(rollValue) 
                newTable.time = totalTime + rollValue
                tableID = db.writeTable(newTable) 
                cur = db.conn.execute("""INSERT INTO TableShot (TABLEID, SHOTID) 
                    VALUES (?, ?)""", (tableID+1, shotID)) 
        
            beforeTable = afterTable 
            totalTime = afterTable.time 

        db.conn.commit()
        cur.close()

        return totaltotalFrames;

    def gameRead(self, table, i):
        
        db = Database(reset=False) 
        cur = db.conn.cursor()

        table = db.readTable(i)

        db.conn.commit()
        cur.close()
        return table
