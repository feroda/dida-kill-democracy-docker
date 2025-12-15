import BaseHTTPServer, SimpleHTTPServer
import ssl, subprocess, cgi

CERT='server.pem'

class VotiHTTPRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):

    def do_POST(self):

        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD':'POST',
                     'CONTENT_TYPE':self.headers['Content-Type'],
                     })

        voti = form['voti'].value
        f = file('risultati.txt', 'a')
        f.write(voti + '\n')
        f.close()

        a,b,bianche,nulle = voti.split("|")

        voti_list = """
ESITO VOTAZIONI

* ALLEANZA RIBELLE = %s
* IMPERO GALATTICO = %s
* Bianche = %s
* Nulle = %s
""" % (a, b, bianche, nulle)
        
        #subprocess.call(['/usr/bin/zenity', '--info', '--title=ESITO VOTAZIONI', '--text=<span font-family=\"sans\" font-weight=\"900\" font-size=\"xx-large\">Il popolo ha votato %s\n</span>' % (voti_list)])
        #BACKGROUND subprocess.call('/usr/bin/zenity --info --title=ESITO VOTAZIONI --text=\'<span font-family=\"sans\" font-weight=\"900\" font-size=\"xx-large\">Il popolo ha votato %s\n</span>\' &' % (voti_list), shell=True)

        self.send_response(200)
        self.wfile.write("Tutto ok, i voti li ho ricevuti io non vi preoccupate")

    def do_GET(self):

        f = file('risultati.txt','r')
        content = """
<html>
<body>
<h1> RISULTATI GALAXOCRACY - 3042 </h2>
<table border="1">
    <tr><th>ALLEANZA RIBELLE</th><th>IMPERO GALATTICO</th><th>BIANCHE</th><th>NULLE</th></tr>
"""
        for line in f.readlines():
            content += "<tr><td>%s</td></tr>" % (line.replace("|","</td><td>"))
        content += "</table></body></html>"
        f.close()
        self.send_response(200)
        self.wfile.write(content)

httpd = BaseHTTPServer.HTTPServer(('', 4443), VotiHTTPRequestHandler)
httpd.socket = ssl.wrap_socket (httpd.socket, certfile=CERT, server_side=True)
print ("Attendo che qualcuno mi mandi i voti...")
httpd.serve_forever()
