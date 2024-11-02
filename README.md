# Server Starten
`app.py` in `flaskServer` ausführen

    cd flaskServer
    python app.py
   
Der Server generiert automatisch ein HTTPS-Zertifikat und stellt die Webseite für das lokale Netzwerk bereit.  
Das HTTPS-Zertifikat ist notwendig, damit der Browser die Kamera für den QR-Code-Scanner freigibt. Da es vom Server generiert wird und kein offizielles Zertifikat ist, zeigt der Browser eine Warnung an.

# Python Packages
`pip install -r requirements.txt`

