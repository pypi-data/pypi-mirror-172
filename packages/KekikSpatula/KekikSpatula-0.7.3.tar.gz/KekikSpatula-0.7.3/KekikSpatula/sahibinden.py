# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from cloudscraper import CloudScraper
from parsel       import Selector

from KekikSpatula import KekikSpatula

class Sahibinden(KekikSpatula):
    """
    Sahibinden : `sahibinden.com` adresinden ilanı hazır formatlarda elinize verir.

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
        return f"{__class__.__name__} Sınıfı -- {self.kaynak}'dan ilanı döndürmesi için yazılmıştır.."

    def __init__(self, sahibinden_url:str):
        """ilanı `sahibinden`'den dızlar."""

        self.kaynak  = "sahibinden.com"
        oturum = CloudScraper()
        oturum.headers.update({"Referer": f"https://www.{self.kaynak}/?JLBreadCrumbEnable=false"})
        istek   = oturum.get(sahibinden_url, allow_redirects=True)

        secici  = Selector(istek.text)

        with open("bakalim.html", "w", encoding="utf-8") as dosya:
            dosya.write(istek.text)

        ilan           = secici.xpath("//div[@class='classifiedDetailTitle']")
        detay_baslik   = secici.xpath("//ul[@class='classifiedInfoList']/li/strong/text()").getall()
        detay_aciklama = secici.xpath("//ul[@class='classifiedInfoList']/li/span/text()").getall()

        try:
            kekik_json     = {
                "kaynak" : self.kaynak,
                "veri"   : {
                    "link"   : sahibinden_url,
                    "baslik" : ilan.xpath("//h1/text()").get().strip(),
                    "resim"  : ilan.xpath("//img[@class='stdImg']/@src").get(),
                    "fiyat"  : ilan.xpath("//div[@class='classifiedInfo ']/h3/text()").get().strip(),
                    "yer"    : "".join(ilan.xpath("//div[@class='classifiedInfo ']/h2/a/text()").getall()).replace(" ", "").lstrip("\n").replace("\n", " | ").replace("Mh.", "").replace("Mah.", ""),
                    "detay"  : [
                        f'{detay_baslik[bak].strip()} : {detay_aciklama[bak].strip()}'
                          for bak in range(len(detay_baslik))
                    ]
                }
            }
        except AttributeError:
            kekik_json     = {
                "kaynak" : self.kaynak,
                "veri"   : {
                    "link" : sahibinden_url,
                    "hata" : "İlan Yayında Değil.."
                }
            }

        self.kekik_json = kekik_json if kekik_json["veri"] != [] else None