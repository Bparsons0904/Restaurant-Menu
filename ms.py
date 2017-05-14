#  cd /c/Users/bpars/"fullstack-nanodegree-vm"/vagrant

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantMenu.db')
Base.metadata.bind=engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

class webServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith("/restaurant"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>List of all available Restaurant's:</h1>"
                restaurant_list = session.query(Restaurant).all()
                for ele in restaurant_list:
                    result = "<div>"
                    result += "<h2>{0}</h2> \n".format(ele.name)
                    result += "<h4><a href='/restaurant/{0}/edit'>Edit</a></h4><h4><a href='/delete'>Delete</a></h4>".format(ele.id)
                    result += "</div>"
                    output += result
                output += "<h3><a href='/add'>Add Restaurant</a></h3>"
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/add"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Make a New Restaurant</h1>"
                output += '''<form method='POST' enctype='multipart/form-data'
                action='/restaurant'><h2>What Restaurant would you like to add?</h2><input
                name="message" type="text" ><input type="Submit"
                value="Create"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/edit"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Edit Restaurant Name</h1>"
                output += '''<form method='POST' enctype='multipart/form-data'
                action='/restaurant'><h2>What is the name you would like to change to?</h2><input
                name="message" type="text" ><input type="Submit"
                value="Edit"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        print "Post Started"
        try:
            self.send_response(301)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            ctype, pdict = cgi.parse_header(
                self.headers.getheader('content-type'))
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                messagecontent = fields.get('message')
                print "Made it to if statement"
            print messagecontent
            name = str(messagecontent)[2:-2]
#            name = name[2:-2]
            print name
            add = Restaurant(name = "{0}".format(name))
            session.add(add)
            session.commit()
            print "Add Submitted"
            output = ""
            output += "<html><body>"
            output += "<h1>List of all available Restaurant's:</h1>"
            restaurant_list = session.query(Restaurant).all()
            for ele in restaurant_list:
                result = "<div>"
                result += "<h2>{0}</h2> \n".format(ele.name)
                result += "<h4><a href='/restaurant'>Edit</a></h4><h4><a href='/restaurant'>Delete</a></h4>"
                result += "</div>"
                output += result
            output += "<h3><a href='/add'>Add Restaurant</a></h3>"
            output += "</body></html>"
            self.wfile.write(output)
        except:
            pass


def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webServerHandler)
        print "Web Server running on port %s" % port
        server.serve_forever()
    except KeyboardInterrupt:
        print " ^C entered, stopping web server...."
        server.socket.close()

if __name__ == '__main__':
    main()
