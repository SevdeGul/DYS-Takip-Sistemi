
# DYS-Takip-Sistemi

Muğla Sıtkı Koçman Üniversitesine ait ders yönetim sayfasında yeni eklenen ders materyallerinin haberini veren bir scriptir.



## Detaylar

Scripti ilk kez kullanırken ders dosyalarının oluşturulabilmesi için aşağıdaki satırların yorum satırı olmaktan kurtularılması gerekmektedir.

`#dosya(ders_kodu)`


```bash
#for element in ders_bilgileri:
    #    ders_icerigi = ders_icerigi_cek(browser,element[1])
    #    dosya_yazma(element[0],ders_icerigi)

```


Ayrıca aşağıdaki For bloğunun yorum satırı haline getirilmesi gerekmektedir.

```bash
   for ders in ders_bilgileri:
        fark = karsilastir(browser,ders[0],ders[1])
        if fark == False:
            ders_icerigi = ders_icerigi_cek(browser, ders[1])
            dosya_yazma(ders[0], ders_icerigi)
            print("%s güncellendi! - URL: %s" % (ders[0],ders[1]))

```

Daha sonraki kullanımlar için script ilk haline tekrar döndürülmelidir.
