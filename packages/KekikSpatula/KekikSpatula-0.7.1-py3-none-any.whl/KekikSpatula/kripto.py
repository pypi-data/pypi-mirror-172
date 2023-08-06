# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from requests     import get
from typing       import Literal

from KekikSpatula import KekikSpatula

class Kripto(KekikSpatula):
    """
    Kripto : `api.binance.com` adresinden kline/candlestick verilerini hazır formatlarda elinize verir.

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
        return f"{__class__.__name__} Sınıfı -- {self.kaynak}'dan Mum(kline/candlestick) verisini döndürmesi için yazılmıştır.."

    def __init__(self, sembol:str, aralik:Literal["1m", "3m", "5m", "15m", "30m", "1h", "2h", "4h", "6h", "8h", "12h", "1d", "3d", "1w", "1M"]):
        """Mum(klines) verisini `api.binance.com`'dan alarak düzenli bir format verir."""

        self.kaynak = "api.binance.com"

        sembol_kontrol_istek = get(f"https://{self.kaynak}/api/v3/ticker/24hr?symbol={sembol.upper()}")

        if sembol_kontrol_istek.status_code != 200:
            self.kekik_json = None
            return

        mum_istek = get(f"https://{self.kaynak}/api/v3/klines?symbol={sembol.upper()}&interval={aralik}")

        if mum_istek.status_code != 200:
            veri = {
                "hata"  : mum_istek.json()["msg"],
                "kod"   : mum_istek.json()["code"],
                "cozum" : "Çıkan hata kodunu burda aratın : https://github.com/binance/binance-spot-api-docs/blob/master/errors.md"
            }
        else:
            veri = [
                {
                    "acilis_zamani"                   : veri[0],
                    "acilis"                          : veri[1],
                    "en_yuksek"                       : veri[2],
                    "en_dusuk"                        : veri[3],
                    "kapanis"                         : veri[4],
                    "hacim"                           : veri[5],
                    "kapanis_zamani"                  : veri[6],
                    "teklif_varlik_hacmi"             : veri[7],
                    "islem_sayisi"                    : veri[8],
                    "satin_alma_temel_varlik_hacmi"   : veri[9],
                    "satın_alma_teklifi_varlik_hacmi" : veri[10],
                }
                  for veri in mum_istek.json()
            ]

        kekik_json      = {"kaynak": self.kaynak, "veri": veri}
        self.kekik_json = kekik_json if kekik_json["veri"] != [] else None
