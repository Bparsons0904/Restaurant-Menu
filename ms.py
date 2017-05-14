#  cd /c/Users/bpars/"fullstack-nanodegree-vm"/vagrant

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
import urlparse
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
                    result += "<h4><a href='/restaurant/{0}/edit'>Edit</a></h4><h4><a href='/restaurant/{0}/delete'>Delete</a></h4>".format(ele.id)
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
                action='/restaurant/add'><h2>What Restaurant would you like to add?</h2><input
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
                path2 = self.path
                split_path = path2.split('/')[2]
                restaurant = session.query(Restaurant).filter_by(id="{0}".format(split_path)).one()
                output = ""
                output += "<html><body>"
                output += "<h1>Edit {0} Name</h1>".format(restaurant.name)
                output += '''<form method='POST' enctype='multipart/form-data'
                action='/restaurant/{0}/edit'><h2>What is the new name?</h2><input
                name="message" type="text" ><input type="Submit"
                value="Edit"> </form>'''.format(split_path)
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/delete"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                path2 = self.path
                split_path = path2.split('/')[2]
                restaurant = session.query(Restaurant).filter_by(id="{0}".format(split_path)).one()
                output = ""
                output += "<html><body>"
                output += "<h1>Delete {0} Name</h1>".format(restaurant.name)
                output += "<h2>Are you positive that you want to delete?</h2>"
                output += '''<form method='POST' action='/restaurant/{0}/delete'><button name='delete'
                value="Delete">Delete</button </form>'''.format(split_path)
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        try:
            if self.path.endswith("/edit"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('message')
                name = str(messagecontent)[2:-2]
                path2 = self.path
                split_path = path2.split('/')[2]
                restaurant = session.query(Restaurant).filter_by(id="{0}".format(split_path)).one()
                restaurant.name = name
                add = Restaurant(name = "{0}".format(name))
                session.add(restaurant)
                session.commit()
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurant')
                self.end_headers()

            if self.path.endswith("/add"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('message')
                new_name = str(messagecontent)[2:-2]
                add = Restaurant(name = "{0}".format(new_name))
                session.add(add)
                session.commit()
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurant')
                self.end_headers()

            if self.path.endswith("/delete"):
                print "Started delete"
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                print "Passed ctype"
                path2 = self.path
                split_path = path2.split('/')[2]
                restaurant = session.query(Restaurant).filter_by(id="{0}".format(split_path)).one()
                print restaurant
                session.delete(restaurant)
                session.commit()
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurant')
                self.end_headers()
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
