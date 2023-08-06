# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from requests     import get
from bs4          import BeautifulSoup

from KekikSpatula import KekikSpatula

class UcuzUcak(KekikSpatula):
    """
    UcuzUcak : bilet.ucuzaucak.net adresinden ucuz uçak biletlerini hazır formatlarda elinize verir.

    Nitelikler
    ----------
        >>> .veri -> dict | None:
        json verisi döndürür.

        >>> .anahtarlar -> list | None:
        kullanılan anahtar listesini döndürür.

        >>> .nesne -> KekikNesne:
        json verisini python nesnesine dönüştürür.

    Metodlar
    ----------
        >>> .gorsel() -> str | None:
        oluşan json verisini insanın okuyabileceği formatta döndürür.

        >>> .tablo() -> str | None:
        tabulate verisi döndürür.
    """
    def __repr__(self) -> str:
        return f"{__class__.__name__} Sınıfı -- {self.kaynak}'dan ucuz uçak biletlerini döndürmesi için yazılmıştır.."

    def __init__(self) -> None:
        """ucuz uçak biletlerini bilet.ucuzaucak.net'dan alarak bs4'ile ayrıştırır."""

        self.kaynak = "bilet.ucuzaucak.net"
        istek       = get(f"https://{self.kaynak}", headers=self.kimlik, allow_redirects=True)

        corba       = BeautifulSoup(istek.content, "lxml")

        bilet_listesi = corba.find("div", class_="itemList")

        kekik_json = {"kaynak": self.kaynak, "veri" : []}
        for bilet in bilet_listesi.findAll("a", class_="itemHref"):
            kekik_json["veri"].append(
                {
                    "bilet"     : bilet.find("span", class_="title").text,
                    "yon"       : bilet.find("span", class_="subTitle").text,
                    "fiyat"     : bilet.find("span", class_="price").text,
                    "tarih"     : bilet.find("span", class_="mr-2").text,
                    "paylasim"  : bilet.find("span", class_="text-gray-600").text,
                    "link"      : f"https://{self.kaynak}{bilet['href']}"
                }
            )

        self.kekik_json = kekik_json if kekik_json["veri"] != [] else None