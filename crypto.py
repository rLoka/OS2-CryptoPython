#Autor tajnog kljuca
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

#PKI - https://cryptography.io/en/latest/hazmat/primitives/asymmetric/rsa/#cryptography.hazmat.primitives.asymmetric.rsa.RSAPrivateKey
#Asimetricna - https://cryptography.io/en/latest/fernet/

class Crypto:
    ############################## {COOMMON} ##############################
    #Ucitavanje teksta iz datoteke
    def ucitajTekstIzDatoteke(self, lokacijaNaDisku):
        with open(lokacijaNaDisku, "r") as datoteka:
            tekst = datoteka.read()
        return tekst

    #Zapisivanje teksta u datoteku
    def zapisiTekstUDatoteku(self, tekst, lokacijaNaDisku):
        datoteka = open(lokacijaNaDisku, "w")
        datoteka.write(tekst)
        datoteka.close()
        return True

    ############################## {AES} ###################################

    #Generira tajni kljuc u base64 prema AES 256 (CBC i PKCS7)
    #Specifikacija dostupna na https://github.com/fernet/spec/blob/master/Spec.md
    def genTajniKljuc(self):
        kljuc = Fernet.generate_key().decode("utf-8")
        return kljuc

    #Zapisivanje PK u datoteku
    def zapisiTajniKljucUDatoteku(self, tajniiKljuc, lokacijaNaDisku):
        datotekaTajnogKljuca = open(lokacijaNaDisku, "w")
        datotekaTajnogKljuca.write(tajniiKljuc)
        datotekaTajnogKljuca.close()
        return True

    #Ucitavanje PK iz datoteke (PEM format)
    def ucitajTajniKljucIzDatoteke(self, lokacijaNaDisku):
        with open(lokacijaNaDisku, "r") as datotekaTajnogKljuca:
            tajniKljuc = datotekaTajnogKljuca.read()
        return tajniKljuc

    #Kriptira tekst sa tajnim kljucem, vraca kriptirani tekst
    def kriptirajTekstTajnimKljucem(self, kljuc, cistiTekst):
        kripter = Fernet(kljuc)
        kriptiraniTekst = kripter.encrypt(bytes(cistiTekst, encoding="utf8")).decode("utf-8")
        return kriptiraniTekst

    #Dekriptira tekst sa tajnim kljucem, vraca cisti tekst
    def dekriptirajTekstTajnimKljucem(self, kljuc, kriptoTekst):
        try:
            dekripter = Fernet(kljuc)
            cistiTekst = dekripter.decrypt(bytes(kriptoTekst, encoding="utf8"))
        except:
            return "Kriptotekst ili ključ nije valjan!"

        else:
            return cistiTekst.decode("utf-8")

    ############################## {RSA} ###################################

    #RSA - generiranje para kljuceva (privatni,javni)
    def genPrivatniJavniKljucPar(self):
        privatniKljuc = rsa.generate_private_key(public_exponent=65537, key_size=2048, backend=default_backend())
        javniKljuc = privatniKljuc.public_key()
        return [privatniKljuc,javniKljuc]

    #Ucitavanje PK iz datoteke (PEM format)
    def ucitajPrivatniKljucIzDatoteke(self, lokacijaNaDisku):
        with open(lokacijaNaDisku, "rb") as datotekaPrivatnogKljuca:
            privatniKljuc = serialization.load_pem_private_key(
                datotekaPrivatnogKljuca.read(),
                password = None,
                backend = default_backend())
        return privatniKljuc

    #serijalizacija PK u citljivi tekst
    def serijalizirajPrivatniKljuc(self, privatniKljuc):
        tekstPK = privatniKljuc.private_bytes(encoding=serialization.Encoding.PEM,
                                              format=serialization.PrivateFormat.PKCS8,
                                              encryption_algorithm=serialization.NoEncryption())
        return tekstPK.decode("utf-8")

    #serijalizacija JK u citljivi tekst
    def serijalizirajJavniKljuc(self, javniKljuc):
        tekstJK = javniKljuc.public_bytes(encoding=serialization.Encoding.PEM,
                                          format=serialization.PublicFormat.SubjectPublicKeyInfo)
        return tekstJK.decode("utf-8")

    def kriptirajTekstJavnimKljucem(self, javniKljuc, cistiTekst):
        kriptoTekst = javniKljuc.encrypt(cistiTekst.encode("utf-8"),
                                        padding.OAEP(mgf = padding.MGF1(algorithm=hashes.SHA1()),
                                                     algorithm = hashes.SHA1(),
                                                     label = None))
        kriptoTekstB64 = base64.urlsafe_b64encode(kriptoTekst)
        return kriptoTekstB64.decode("utf-8")


    def dekriptirajTekstPrivatnimKljucem(self, privatniKljuc, kriptoTekst):
        cistiTekst = privatniKljuc.decrypt(base64.urlsafe_b64decode(kriptoTekst),
                                           padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA1()),
                                                        algorithm=hashes.SHA1(),
                                                        label=None))
        return cistiTekst.decode("utf-8")


    #Ucitavanje JK iz datoteke (PEM format)
    def ucitajJavniKljucIzDatoteke(self, lokacijaNaDisku):
        with open(lokacijaNaDisku, "rb") as datotekaJavnogKljuca:
            javniKljuc = serialization.load_pem_public_key(datotekaJavnogKljuca.read(), backend = default_backend())
        return javniKljuc

    #Zapisivanje JK u datoteku
    def zapisiJavniKljucUDatoteku(self, javniKljuc, lokacijaNaDisku):
        datotekaJavnogKljuca = open(lokacijaNaDisku, "w")
        datotekaJavnogKljuca.write(self.serijalizirajJavniKljuc(javniKljuc))
        datotekaJavnogKljuca.close()
        return True

    #Zapisivanje PK u datoteku
    def zapisiPrivatniKljucUDatoteku(self, privatniKljuc, lokacijaNaDisku):
        datotekaPrivatnogKljuca = open(lokacijaNaDisku, "w")
        datotekaPrivatnogKljuca.write(self.serijalizirajPrivatniKljuc(privatniKljuc))
        datotekaPrivatnogKljuca.close()
        return True

    ############################## {Hash - SHA256} ###################################

    #Racunanje hasha od danih byteva, tj. stringa
    def izracunajSazetak(self, podaci):
        sazetak = hashes.Hash(hashes.SHA256(), backend=default_backend())
        sazetak.update(podaci.encode("utf-8"))
        return base64.urlsafe_b64encode(sazetak.finalize()).decode("utf-8")

    ###### {Digitalni potpis - potpisivanje privatnim kljucem, provjera javnim} #######

    def digitalnoPotpisiSadrzaj(self, privatniKljuc, podaci):
        digitalniPotpis = privatniKljuc.sign(podaci.encode("utf-8"),
                                       padding.PSS(mgf=padding.MGF1(hashes.SHA256()),
                                                   salt_length=padding.PSS.MAX_LENGTH),
                                       hashes.SHA256())

        return base64.urlsafe_b64encode(digitalniPotpis).decode("utf-8")

    def provjeriDigitalniPotpis(self, javniKljuc, digitalniPotpis, podaci):
        try:
            javniKljuc.verify(base64.urlsafe_b64decode(digitalniPotpis),
                          podaci.encode("utf-8"),
                          padding.PSS(mgf=padding.MGF1(hashes.SHA256()),
                                      salt_length=padding.PSS.MAX_LENGTH),
                          hashes.SHA256())
        except:
            return False

        else:
            return True
