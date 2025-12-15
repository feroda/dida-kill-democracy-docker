#!/usr/bin/python

import subprocess, sys, urllib, urllib2, ssl

SERVER_ENDPOINT = 'https://server:4443'

#---------------------------------------------------------------

def riequilibrare_i_voti(a, b, bianche, nulle):
    """
    Personalizzazione richiesta gentilmente dal cliente "IMPERO GALATTICO"
    con aggiornamento di specifiche relativo ad elezioni 3042
    """

    if b < a:
        #xxx = min(nulle, (a-b)+1)
        xxx = nulle*9/10
        nulle -= xxx
        b += xxx

    return a,b,bianche,nulle

def invia_i_voti(seggio, a, b, bianche, nulle, voti_inseriti):

    voti_da_inviare = "|".join(map(str, [seggio, a, b, bianche, nulle]))
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    values = { "voti" : voti_da_inviare }

    header = { 'User-Agent' : user_agent }
    data = urllib.urlencode(values)
    req = urllib2.Request(SERVER_ENDPOINT, data, header) 

    # SSL CONTEXT NON VERIFICANTE
    ctx = ssl._create_unverified_context()

    response = urllib2.urlopen(req, context=ctx)
    a,b,bianche,nulle = voti_inseriti.split("|")

    voti_list = """

* ALLEANZA RIBELLE = %s
* IMPERO GALATTICO = %s
* Bianche = %s
* Nulle = %s
""" % (a, b, bianche, nulle)
    
    subprocess.call([
        '/usr/bin/zenity', 
        '--info', 
        '--title=INVIO OK', 
        '--text=<span font-family=\"sans\" font-weight=\"900\" font-size=\"xx-large\">INVIO OK\n%s %s</span>' % (response.read(), voti_list)
    ])

def main(argv):

    if len(argv) < 2:
        subprocess.call([
            '/usr/bin/zenity',
            '--info',
            '--text=<span font-family=\"sans\" font-weight=\"900\" font-size=\"xx-large\">Utilizzo: comunica_i_voti &lt;SEGGIO&gt;</span>'
        ])
        sys.exit(100)

    seggio = argv[1]

    voti_inseriti = subprocess.check_output([
        '/usr/bin/zenity', 
        '--forms', 
        '--add-entry=ALLEANZA RIBELLE', 
        '--add-entry=IMPERO GALATTICO', 
        '--add-entry=schede BIANCHE', 
        '--add-entry=schede NULLE', 
        '--title=INSERIRE I RISULTATI DELLE ELEZIONI DEMOCRATICHE', 
        '--text=<span font-family=\"sans\" font-weight=\"900\" font-size=\"xx-large\">COMUNICA LE VOTAZIONI DEL SEGGIO DI %s</span>' % seggio
    ])

    p_A, p_B, bianche, nulle = map(int, voti_inseriti.split("|"))
    #print "I voti inseriti sono %s " % voti_inseriti

    p_A, p_B, bianche, nulle = riequilibrare_i_voti(p_A, p_B, bianche, nulle)
    voti_riequilibrati = "|".join(map(str, [p_A, p_B, bianche, nulle]))

    #subprocess.call(['/usr/bin/zenity', '--info', '--title=VOTI', '--text=<span font-family=\"sans\" font-weight=\"900\" font-size=\"xx-large\">Inseriti %s\nRiequilibrati %s\n</span>' % (voti_inseriti, voti_riequilibrati)])
    #print "I voti riequilibrati sono %s " % voti_riequilibrati

    invia_i_voti(seggio, p_A, p_B, bianche, nulle, voti_inseriti)

if __name__ == "__main__":
    main(sys.argv)
