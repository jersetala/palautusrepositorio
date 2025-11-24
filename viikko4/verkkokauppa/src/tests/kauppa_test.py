import unittest
from unittest.mock import Mock, ANY
from kauppa import Kauppa
from viitegeneraattori import Viitegeneraattori
from varasto import Varasto
from tuote import Tuote
import viitegeneraattori

class TestKauppa(unittest.TestCase):
    def setUp(self):
        self.pankki_mock = Mock()
        self.viitegeneraattori_mock = Mock()

        def viitegeneraattori_uusi(hidden_state=[0]):
            # This is a hack that guarantees unique
            # reference numbers.
            hidden_state[0] += 1
            return hidden_state[0]

        self.viitegeneraattori_mock.uusi.side_effect = viitegeneraattori_uusi

        self.varasto_mock = Mock()

        def varasto_saldo(tuote_id):
            if tuote_id == 1:
                return 10
            elif tuote_id == 2:
                return 10
            elif tuote_id == 3:
                return 0
            assert(1 == 0)

        def varasto_hae_tuote(tuote_id):
            if tuote_id == 1:
                return Tuote(1, "Leipä", 2)
            elif tuote_id == 2:
                return Tuote(2, "Voi", 3)
            elif tuote_id == 3:
                return Tuote(3, "Juusto", 5)
            assert(1 == 0)

        self.varasto_mock.saldo.side_effect = varasto_saldo
        self.varasto_mock.hae_tuote.side_effect = varasto_hae_tuote

        self.kauppa = Kauppa(self.varasto_mock, self.pankki_mock, self.viitegeneraattori_mock)


    def test_maksettaessa_ostos_pankin_metodia_tilisiirto_kutsutaan(self):
        pankki_mock = Mock()
        viitegeneraattori_mock = Mock()

        # palautetaan aina arvo 42
        viitegeneraattori_mock.uusi.return_value = 42

        varasto_mock = Mock()

        # tehdään toteutus saldo-metodille
        def varasto_saldo(tuote_id):
            if tuote_id == 1:
                return 10

        # tehdään toteutus hae_tuote-metodille
        def varasto_hae_tuote(tuote_id):
            if tuote_id == 1:
                return Tuote(1, "maito", 5)

        # otetaan toteutukset käyttöön
        varasto_mock.saldo.side_effect = varasto_saldo
        varasto_mock.hae_tuote.side_effect = varasto_hae_tuote

        # alustetaan kauppa
        kauppa = Kauppa(varasto_mock, pankki_mock, viitegeneraattori_mock)

        # tehdään ostokset
        kauppa.aloita_asiointi()
        kauppa.lisaa_koriin(1)
        kauppa.tilimaksu("pekka", "12345")

        # varmistetaan, että metodia tilisiirto on kutsuttu
        pankki_mock.tilisiirto.assert_called()
        # toistaiseksi ei välitetä kutsuun liittyvistä argumenteista

    def test_maksettaessa_ostos_pankin_metodia_tilisiirto_kutsutaan_argumenteilla(self):
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("essi", "54321")

        self.pankki_mock.tilisiirto.assert_called_with("essi", 1, "54321", ANY, 2)

    def test_useamman_asian_osto_kutsuu_pankin_metodia_tilisiirto_oikein(self):
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.lisaa_koriin(2)
        self.kauppa.tilimaksu("juuso", "11235")

        self.pankki_mock.tilisiirto.assert_called_with("juuso", 1, "11235", ANY, 2+3)

    def test_useamman_varastossa_olevan_asian_osto_kutsuu_pankin_metodia_tilisiirto_oikein(self):
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("markku", "99999")

        self.pankki_mock.tilisiirto.assert_called_with("markku", 1, "99999", ANY, 2+2)

    def test_varastossa_olevan_ja_olemattoman_osto_kutsuu_pankin_metodia_tilisiirto_oikein(self):
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.lisaa_koriin(2)
        self.kauppa.tilimaksu("vesa", "00000")

        self.pankki_mock.tilisiirto.assert_called_with("vesa", 1, "00000", ANY, 2+3)

    def test_aloita_asiointi_nollaa_tiedot(self):
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)

        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("aamu", "55555")

        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("ilta", "66666")
        self.pankki_mock.tilisiirto.assert_called_with("ilta", ANY, "66666", ANY, 2)

    def test_uusi_viitenumero_jokaisella_asioinnilla(self):
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("none", "11111")

        self.viitegeneraattori_mock.uusi.assert_called()

        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(2)
        self.kauppa.tilimaksu("none", "22222")

        self.viitegeneraattori_mock.uusi.assert_called()
