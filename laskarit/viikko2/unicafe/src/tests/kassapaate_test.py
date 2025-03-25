import unittest
from kassapaate import Kassapaate
from maksukortti import Maksukortti

class TestKassapaate(unittest.TestCase):
    def setUp(self):
        self.kassa = Kassapaate()
        self.kortti = Maksukortti(1000)

    def test_kassapaatteen_alkuarvot_oikein(self):
        self.assertEqual(self.kassa.kassassa_rahaa, 100000)
        self.assertEqual(self.kassa.edulliset, 0)
        self.assertEqual(self.kassa.maukkaat, 0)
    
    def test_kateisosto_edullinen_riittavalla_rahalla(self):
        vaihtoraha = self.kassa.syo_edullisesti_kateisella(300)
        self.assertEqual(vaihtoraha, 60)
        self.assertEqual(self.kassa.kassassa_rahaa, 100240)
        self.assertEqual(self.kassa.edulliset, 1)
    
    def test_kateisosto_edullinen_ei_riittavalla_rahalla(self):
        vaihtoraha = self.kassa.syo_edullisesti_kateisella(200)
        self.assertEqual(vaihtoraha, 200)
        self.assertEqual(self.kassa.kassassa_rahaa, 100000)
        self.assertEqual(self.kassa.edulliset, 0)
    
    def test_kateisosto_maukas_riittavalla_rahalla(self):
        vaihtoraha = self.kassa.syo_maukkaasti_kateisella(500)
        self.assertEqual(vaihtoraha, 100)
        self.assertEqual(self.kassa.kassassa_rahaa, 100400)
        self.assertEqual(self.kassa.maukkaat, 1)
    
    def test_kateisosto_maukas_ei_riittavalla_rahalla(self):
        vaihtoraha = self.kassa.syo_maukkaasti_kateisella(300)
        self.assertEqual(vaihtoraha, 300)
        self.assertEqual(self.kassa.kassassa_rahaa, 100000)
        self.assertEqual(self.kassa.maukkaat, 0)
    
    def test_korttiosto_edullinen_riittavalla_saldolla(self):
        self.assertTrue(self.kassa.syo_edullisesti_kortilla(self.kortti))
        self.assertEqual(self.kortti.saldo, 760)
        self.assertEqual(self.kassa.edulliset, 1)
        self.assertEqual(self.kassa.kassassa_rahaa, 100000)
    
    def test_korttiosto_edullinen_ei_riittavalla_saldolla(self):
        kortti = Maksukortti(200)
        self.assertFalse(self.kassa.syo_edullisesti_kortilla(kortti))
        self.assertEqual(kortti.saldo, 200)
        self.assertEqual(self.kassa.edulliset, 0)
    
    def test_korttiosto_maukas_riittavalla_saldolla(self):
        self.assertTrue(self.kassa.syo_maukkaasti_kortilla(self.kortti))
        self.assertEqual(self.kortti.saldo, 600)
        self.assertEqual(self.kassa.maukkaat, 1)
        self.assertEqual(self.kassa.kassassa_rahaa, 100000)
    
    def test_korttiosto_maukas_ei_riittavalla_saldolla(self):
        kortti = Maksukortti(300)
        self.assertFalse(self.kassa.syo_maukkaasti_kortilla(kortti))
        self.assertEqual(kortti.saldo, 300)
        self.assertEqual(self.kassa.maukkaat, 0)
    
    def test_kortille_lataaminen_kasvattaa_kortin_saldoa_ja_kassan_rahaa(self):
        self.kassa.lataa_rahaa_kortille(self.kortti, 500)
        self.assertEqual(self.kortti.saldo, 1500)
        self.assertEqual(self.kassa.kassassa_rahaa_euroina(), 1005.0)

    def test_kortille_lataaminen_negatiivinen_summa(self):
        self.kassa.lataa_rahaa_kortille(self.kortti, -500)
        self.assertEqual(self.kortti.saldo, 1000)