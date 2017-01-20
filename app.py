'''
crypto = Crypto()
PJK = crypto.genPrivatniJavniKljucPar()
cl = 'Ovo je tajni tekst!'
cl2 = 'Ovo je tajni tekst?'
ch = crypto.izracunajSazetak(bytes(cl, encoding="UTF-8"))
dp = crypto.digitalnoPotpisiSadrzaj(PJK[0], bytes(cl, encoding="UTF-8"))
dp2 = crypto.digitalnoPotpisiSadrzaj(PJK[0], bytes(cl2, encoding="UTF-8"))
pr = crypto.provjeriDigitalniPotpis(PJK[1], dp, bytes(cl2, encoding="UTF-8"))
print ("Hash:", ch)
print ("Signature:", dp)
print ("Verify sig?: ", pr)
'''

from crypto import Crypto
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class Handler:
    def __init__(self):
        #Crypto
        self.crypto = Crypto()

        # Definiranje UI kompoenenti

        # Glavni prozor
        self.window = builder.get_object("glavniProzor")
        self.window.show_all()

        # Simetricna
        self.simetrcinaWindow = builder.get_object("simetrcinaWindow")
        self.txtPoruka = builder.get_object("txtPoruka")
        self.filePoruka = builder.get_object("filePoruka")
        self.txtTajniKljuc = builder.get_object("txtTajniKljuc")
        self.fileTajniKljuc = builder.get_object("fileTajniKljuc")
        self.txtKriptoText = builder.get_object("txtKriptoText")
        self.fileKriptoText = builder.get_object("fileKriptoText")
        self.txtCistiTekst = builder.get_object("txtCistiTekst")
        self.fileCistiText = builder.get_object("fileCistiText")

        # Asimetricna
        self.asimetrcinaWindow = builder.get_object("asimetrcinaWindow")
        self.txtPoruka1 = builder.get_object("txtPoruka1")
        self.filePoruka1 = builder.get_object("filePoruka1")
        self.txtPrivatniKljucText = builder.get_object("txtPrivatniKljucText")
        self.filePrivatniKljuc = builder.get_object("filePrivatniKljuc")
        self.txtJavniKljucText = builder.get_object("txtJavniKljucText")
        self.fileJavniKljuc = builder.get_object("fileJavniKljuc")
        self.txtKriptoText1 = builder.get_object("txtKriptoText1")
        self.fileKriptoText1 = builder.get_object("fileKriptoText1")
        self.txtCistiTekst1 = builder.get_object("txtCistiTekst1")
        self.fileCistiText1 = builder.get_object("fileCistiText1")
        self.privatniJavniKljuc = [None, None]

        #Potpis
        self.sazetakWindow = builder.get_object("sazetakWindow")
        self.txtSazetakTekst = builder.get_object("txtSazetakTekst")
        self.txtDigitalniTekst = builder.get_object("txtDigitalniTekst")
        self.txtProvjeraTekst = builder.get_object("txtProvjeraTekst")
        self.izracunajSazetak = builder.get_object("izracunajSazetak")
        self.digitalnoPotpisi = builder.get_object("digitalnoPotpisi")
        self.provjeriPotpis = builder.get_object("provjeriPotpis")

    def on_glavniProzor_delete_event(self, *args):
        Gtk.main_quit(*args)

    #Simetricna
    def on_simetrcinaWindow_delete_event(self, *args):
        self.simetrcinaWindow = builder.get_object("simetrcinaWindow")

    def on_btnSimetric_clicked(self, button):
        self.simetrcinaWindow.show_all()

    def on_spremiCistiTekst_clicked(self, button):
        cistiTekst = self.txtCistiTekst.get_text()
        self.crypto.zapisiTekstUDatoteku(cistiTekst, self.fileCistiText.get_text())

    def on_ucitajCistiTekst_clicked(self, button):
        cistiTekst = self.crypto.ucitajTekstIzDatoteke(self.fileCistiText.get_text())
        self.txtCistiTekst.set_text(cistiTekst)

    def on_dekriptirajKriptoTekst_clicked(self, button):
        self.txtCistiTekst.set_text(self.crypto.dekriptirajTekstTajnimKljucem(self.txtTajniKljuc.get_text(),self.txtKriptoText.get_text()))

    def on_spremiKriptoTekst_clicked(self, button):
        kriptiraniTekst = self.txtKriptoText.get_text()
        self.crypto.zapisiTekstUDatoteku(kriptiraniTekst, self.fileKriptoText.get_text())

    def on_ucitajKriptoTekst_clicked(self, button):
        kriptiraniTekst = self.crypto.ucitajTekstIzDatoteke(self.fileKriptoText.get_text())
        self.txtKriptoText.set_text(kriptiraniTekst)

    def on_kriptirajCistiTekst_clicked(self, button):
        kriptiraniTekst = self.crypto.kriptirajTekstTajnimKljucem(self.txtTajniKljuc.get_text(), self.txtPoruka.get_text())
        self.txtKriptoText.set_text(kriptiraniTekst)

    def on_spremiTajniKljuc_clicked(self, button):
        datoteka = self.fileTajniKljuc.get_text()
        tajniKljuc = self.txtTajniKljuc.get_text()
        self.crypto.zapisiTajniKljucUDatoteku(tajniKljuc, datoteka)

    def on_ucitajTajniKljuc_clicked(self, button):
        datoteka = self.fileTajniKljuc.get_text()
        tajniKljuc = self.crypto.ucitajTajniKljucIzDatoteke(datoteka)
        self.txtTajniKljuc.set_text(tajniKljuc)

    def on_generirajTajniKljuc_clicked(self, button):
        tajniKljuc = self.crypto.genTajniKljuc()
        self.txtTajniKljuc.set_text(tajniKljuc)

    def on_ucitajPoruku_clicked(self, button):
        poruka = self.crypto.ucitajTekstIzDatoteke(self.filePoruka.get_text())
        self.txtPoruka.set_text(str(poruka))

    def on_spremiPoruku_clicked(self, button):
        datoteka = self.filePoruka.get_text()
        poruka = self.txtPoruka.get_text()
        self.crypto.zapisiTekstUDatoteku(poruka, datoteka)

    #Asimetricna
    def on_asimetrcinaWindow_delete_event(self, *args):
        self.asimetrcinaWindow = builder.get_object("asimetrcinaWindow")

    def on_btnAsimetric_clicked(self, button):
        self.asimetrcinaWindow.show_all()

    def on_ucitajPoruku1_clicked(self, button):
        poruka1 = self.crypto.ucitajTekstIzDatoteke(self.filePoruka1.get_text())
        self.txtPoruka1.set_text(str(poruka1))

    def on_spremiPoruku1_clicked(self, button):
        datoteka1 = self.filePoruka1.get_text()
        poruka1 = self.txtPoruka1.get_text()
        self.crypto.zapisiTekstUDatoteku(poruka1, datoteka1)

    def on_generirajPrivatniKljuc_clicked(self, button):
        self.privatniJavniKljuc = self.crypto.genPrivatniJavniKljucPar()
        self.txtPrivatniKljucText.set_text(self.crypto.serijalizirajPrivatniKljuc(self.privatniJavniKljuc[0]))
        self.txtJavniKljucText.set_text(self.crypto.serijalizirajJavniKljuc(self.privatniJavniKljuc[1]))

    def on_ucitajPrivatniKljuc_clicked(self, button):
        privatniKljuc = self.crypto.ucitajPrivatniKljucIzDatoteke(self.filePrivatniKljuc.get_text())
        self.privatniJavniKljuc[0] = privatniKljuc
        self.txtPrivatniKljucText.set_text(self.crypto.serijalizirajPrivatniKljuc(privatniKljuc))

    def on_spremiPrvitaniKljuc_clicked(self, button):
        self.crypto.zapisiPrivatniKljucUDatoteku(self.privatniJavniKljuc[0], self.filePrivatniKljuc.get_text())

    def on_ucitajJavniKljuc_clicked(self, button):
        javniKljuc = self.crypto.ucitajJavniKljucIzDatoteke(self.fileJavniKljuc.get_text())
        self.privatniJavniKljuc[1] = javniKljuc
        self.txtJavniKljucText.set_text(self.crypto.serijalizirajJavniKljuc(javniKljuc))

    def on_spremiJavniKljuc_clicked(self, button):
        self.crypto.zapisiJavniKljucUDatoteku(self.privatniJavniKljuc[1], self.fileJavniKljuc.get_text())

    def on_kriptirajCistiTekst1_clicked(self, button):
        kriptoText = self.crypto.kriptirajTekstJavnimKljucem(self.privatniJavniKljuc[1], self.txtPoruka1.get_text())
        self.txtKriptoText1.set_text(kriptoText)

    def on_ucitajKriptoTekst1_clicked(self, button):
        self.txtKriptoText1.set_text(self.crypto.ucitajTekstIzDatoteke(self.fileKriptoText1.get_text()))

    def on_spremiKriptoTekst1_clicked(self, button):
        self.crypto.zapisiTekstUDatoteku(self.txtKriptoText1.get_text(), self.fileKriptoText1.get_text())

    def on_dekriptirajKriptoTekst1_clicked(self, button):
        try:
            self.txtCistiTekst1.set_text(self.crypto.dekriptirajTekstPrivatnimKljucem(self.privatniJavniKljuc[0], self.txtKriptoText1.get_text()))
        except:
            self.txtCistiTekst1.set_text("Nije moguce dekriptirati!")

    def on_ucitajCistiTekst1_clicked(self, button):
        cistiTekst1 = self.crypto.ucitajTekstIzDatoteke(self.fileCistiText1.get_text())
        self.txtCistiTekst1.set_text(cistiTekst1)

    def on_spremiCistiTekst1_clicked(self, button):
        cistiTekst1 = self.txtCistiTekst1.get_text()
        self.crypto.zapisiTekstUDatoteku(cistiTekst1, self.fileCistiText1.get_text())


    #Digitalni potpis
    def on_sazetakWindow_delete_event(self, *args):
        self.sazetakWindow = builder.get_object("sazetakWindow")

    def on_btnSignature_clicked(self, button):
        self.sazetakWindow.show_all()

    def on_izracunajSazetak_clicked(self, button):
        poruka = self.crypto.ucitajTekstIzDatoteke("poruka.txt")
        self.txtSazetakTekst.set_text(self.crypto.izracunajSazetak(poruka))

    def on_digitalnoPotpisi_clicked(self, button):
        privatniKljuc = self.crypto.ucitajPrivatniKljucIzDatoteke("privatni_kljuc.txt")
        self.txtDigitalniTekst.set_text(self.crypto.digitalnoPotpisiSadrzaj(privatniKljuc, self.txtSazetakTekst.get_text()))

    def on_provjeriPotpis_clicked(self, button):
        javniKljuc = self.crypto.ucitajJavniKljucIzDatoteke(self.fileJavniKljuc.get_text())
        if self.crypto.provjeriDigitalniPotpis(javniKljuc, self.txtDigitalniTekst.get_text(), self.txtSazetakTekst.get_text()):
            self.txtProvjeraTekst.set_text("Potpis autentičan!")
        else:
            self.txtProvjeraTekst.set_text("Potpis ne odgovara!")

builder = Gtk.Builder()
builder.add_from_file("gui.glade")
builder.connect_signals(Handler())

Gtk.main()