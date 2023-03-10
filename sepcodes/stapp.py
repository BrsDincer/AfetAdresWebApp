import streamlit as st
from PIL import Image
from _dataaccess import *
from _wordsearch import *
import os,folium,pydeck
from _yamlcontrol import *
from folium import plugins
from streamlit_folium import folium_static

rt = os.path.dirname(os.path.relpath((__file__)))
class STAPP(object):
    def __init__(self):
        self.__pt = "Disaster Coordination - Assistance and Analysis Platform"
        self.__ly = "wide"
        self.__ss = "expanded"
        self.__adiyaman = None
        self.__maras = None
        self.__hatay = None
        self.__antep = None
        self.__warning_alert = os.path.join(rt,"warning__alert.wav")
        self.__here_alert = os.path.join(rt,"here_alert.wav")
        self.__banner_logo = os.path.join(rt,"banner_all.png")
        self.__tl = YAMLREADING()._TILE()
        self.__readinternetscan = DATAGATHERING("https://afetadres.s3.eu-central-1.amazonaws.com/internet_scan.csv")._READFILE()
        self.__readuserinputs = DATAGATHERING("https://afetadres.s3.eu-central-1.amazonaws.com/deprem_input.csv")._READFILE()
        self.__readgasstation = DATAGATHERING("https://afetadres.s3.eu-central-1.amazonaws.com/gas_station.csv")._READFILE()
        self.__readoperator = DATAGATHERING("https://afetadres.s3.eu-central-1.amazonaws.com/crane_operator.csv")._READFILE()
        self.__readchildneed = DATAGATHERING("https://afetadres.s3.eu-central-1.amazonaws.com/child_need_data.csv")._READFILE()
        self.__readinjuryneed = DATAGATHERING("https://afetadres.s3.eu-central-1.amazonaws.com/injury_need_data.csv")._READFILE()
        self.__readprovisionneed = DATAGATHERING("https://afetadres.s3.eu-central-1.amazonaws.com/provision_need_data.csv")._READFILE()
        self.__readdebrisneed = DATAGATHERING("https://afetadres.s3.eu-central-1.amazonaws.com/debris_need_data.csv")._READFILE()
        self.__readkonaklama = DATAGATHERING("https://afetadres.s3.eu-central-1.amazonaws.com/ShelterandAccommodationAreas.csv")._READFILE()
        self.__readfoodpoints = DATAGATHERING("https://afetadres.s3.eu-central-1.amazonaws.com/FoodSpots.csv")._READFILE()
        self.__readtransportationtodisaster = DATAGATHERING("https://afetadres.s3.eu-central-1.amazonaws.com/TransportationToDisasterAreas.csv")._READFILE()
        self.__readshelterforoutside = DATAGATHERING("https://afetadres.s3.eu-central-1.amazonaws.com/ShelterOpportunitiesOutsideTheDisasterArea.csv")._READFILE()
        self.__readpharmacytrucks = DATAGATHERING("https://afetadres.s3.eu-central-1.amazonaws.com/PharmacyTrucks.csv")._READFILE()
        self.__readaidtrucks = DATAGATHERING("https://afetadres.s3.eu-central-1.amazonaws.com/LocationsofAidTrucks.csv")._READFILE()
        self.__readcontactnumber = DATAGATHERING("https://afetadres.s3.eu-central-1.amazonaws.com/AuthorizedContactNumbers.csv")._READFILE()
    def __str__(self):
        return "Disaster Coordination - Assistance and Analysis [WEB APPLICATION - PROCESS]"
    def __call__(self):
        return None
    def __getstate__(self):
        raise TypeError("[DENIED]")
    def __repr__(self):
        return STAPP.__doc__
    def _CONVERT_DF(self,dtinit:classmethod):
        return dtinit.to_csv().encode("utf-8")
    def _RETURNMAP(self,tl:str="http://services.arcgisonline.com/arcgis/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}",
                   lc:list=[38,35],
                   zm:int=5):
        mf = folium.Map(tiles=tl,
                        location=lc,
                        zoom_start=zm,
                        attr="<p>COORDINATES</p>")
        return mf
    def _RETURNCOOR(self,lat:list or tuple,lon:list or tuple):
        return list(zip(lat,lon))
    def _RETURNLABELS(self,dtinit:classmethod):
        vl = list(dtinit["ADRES"].values)
        hataycount = 1
        adiyamancount = 1
        malatyacount = 1
        marascount = 1
        antepcount = 1
        adanacount = 1
        diyarcount = 1
        for val in vl:
            if "hatay" in val.lower():
                hataycount += 1
            elif "ad??yaman" in val.lower():
                adiyamancount += 1
            elif "malatya" in val.lower():
                malatyacount += 1
            elif "mara??" in val.lower() or "kahramanmara??" in val.lower():
                marascount += 1
            elif "antep" in val.lower() or "gaziantep" in val.lower():
                antepcount += 1
            elif "adana" in val.lower():
                adanacount += 1
            elif "diyarbak??r" in val.lower():
                diyarcount += 1
            else:
                pass
        return hataycount,adiyamancount,malatyacount,marascount,antepcount,adanacount,diyarcount
    def _CONF(self):
        st.set_page_config(page_title=self.__pt,
                           layout=self.__ly,
                           initial_sidebar_state=self.__ss,
                           menu_items={"About":"**Disaster Coordination - _Assistance and Analysis Platform_**",
                                       "Get Help":"https://github.com/BrsDincer/AfetAdresWebApp/"})
    def _ALARMFUNC(self):
        st.caption("_Butonlara basarak alarmlar?? aktif et_")
        btt1,btt2 = st.columns(2)
        with btt1:
            with st.expander(":loudspeaker: BURADAYIM"):
                st.audio(self.__here_alert)
        with btt2:
            with st.expander(":loudspeaker: TEHL??KE"):
                st.audio(self.__warning_alert)
    def _RETURNCLUSTERFUNC(self):
        pass #future use
    def _PRINTBANNER(self):
        st.image(Image.open(self.__banner_logo),use_column_width="always")
        self._ALARMFUNC()
        st.header("**ADRES B??LG??LEND??RME VE TESP??T S??STEM??**")
    def _DATAACCESS(self):
        self.__readuserinputs.drop_duplicates()
        self.__adiyaman = self.__readuserinputs[self.__readuserinputs["SEHIR"] == "Ad??yaman"].reset_index(drop=True)
        self.__maras = self.__readuserinputs[self.__readuserinputs["SEHIR"] == "Mara??"].reset_index(drop=True)
        self.__hatay = self.__readuserinputs[self.__readuserinputs["SEHIR"] == "Hatay"].reset_index(drop=True)
        self.__antep = self.__readuserinputs[self.__readuserinputs["SEHIR"] == "Antep"].reset_index(drop=True)
        self.__adiyaman["ADRES"] = self.__adiyaman["ADRES"].str.capitalize()
        self.__maras["ADRES"] = self.__maras["ADRES"].str.capitalize()
        self.__hatay["ADRES"] = self.__hatay["ADRES"].str.capitalize()
        self.__antep["ADRES"] = self.__antep["ADRES"].str.capitalize()
        self.__adiyaman["ISIM"] = self.__adiyaman["ISIM"].str.capitalize()
        self.__maras["ISIM"] = self.__maras["ISIM"].str.capitalize()
        self.__hatay["ISIM"] = self.__hatay["ISIM"].str.capitalize()
        self.__antep["ISIM"] = self.__antep["ISIM"].str.capitalize()
    def _CREATEATTR(self,dttr:classmethod):
        latlst = []
        lonlst = []
        mnllst = []
        addval = dttr["ADRES"].values
        for ic,ix in enumerate(addval):
            sll = ix.split()
            tcc = " ".join(str(xty) for xty in sll[:2])
            tcc += "," + dttr["SEHIR"][ic]
            try:
                main,lat,lon = self.__tp._RETURNALL(tcc.lower())
                if main != None:
                    mnllst.append(main)
                    latlst.append(float(lat))
                    lonlst.append(float(lon))
                else:
                    pass
            except:
                cty = dttr["SEHIR"][ic]
                main,lat,lon = self.__tp._RETURNALL(str(cty))
                if main != None:
                    mnllst.append(main)
                    latlst.append(float(lat))
                    lonlst.append(float(lon))
                else:
                    pass
        return latlst,lonlst,mnllst
    def _CREATEMAP(self,ddtr:classmethod):
        ltlst,lnlst,mnlst = self._CREATEATTR(ddtr)
        mf = self._RETURNMAP()
        plugins.MiniMap().add_to(mf)
        cmn = 0
        for xlt,xln in zip(ltlst,lnlst):
            folium.Marker(location=[float(xlt),float(xln)],
                          popup=f"<h4>{str(round(xlt,2))},{str(round(xln,2))}</h4> - <p>{str(mnlst[cmn])}</p>",
                          tooltip="Show info",
                          icon=folium.Icon(color="red",icon="flag")).add_to(mf)
            cmn += 1
        for xn,xt in self.__tl.items():
            xt += "/MapServer/tile/{z}/{y}/{x}"
            folium.TileLayer(tiles=xt,
                             name=xn,
                             attr="<p>COORDINATES</p>").add_to(mf)
        folium.LayerControl().add_to(mf)
        folium_static(mf)
    def _CREATEMANUELMAP(self,ddtr:classmethod,
                         attr1:str,
                         attr2:str):
        mf = self._RETURNMAP()
        plugins.MiniMap().add_to(mf)
        for xlt,xln in zip(ddtr[attr1],ddtr[attr2]):
            folium.Marker(location=[float(xlt),float(xln)],
                          popup=f"<h4><p>KOORD??NAT:\n{xlt},{xln}</p></h4>",
                          tooltip="Click me!",
                          icon=folium.Icon(color="red",
                                           icon="info-sign")).add_to(mf)
        folium_static(mf)
    def _CREATECLUSTERS(self,cr:list):
        mf = self._RETURNMAP()
        plugins.MiniMap().add_to(mf)
        mmap = plugins.MarkerCluster(cr)
        hmap = plugins.HeatMap(cr)
        mf.add_child(mmap)
        mf.add_child(hmap)
        for xn,xt in self.__tl.items():
            xt += "/MapServer/tile/{z}/{y}/{x}"
            folium.TileLayer(tiles=xt,
                             name=xn,
                             attr="<p>COORDINATES</p>").add_to(mf)
        folium.LayerControl().add_to(mf)
        folium_static(mf)
    def _TABS(self):
        self._DATAACCESS()
        self.__readinternetscan.drop_duplicates()
        hataycount,adiyamancount,malatyacount,marascount,antepcount,adanacount,diyarcount = self._RETURNLABELS(self.__readinternetscan)
        ypp1,ypp2 = st.columns(2)
        with ypp1:
            st.metric(label="TOPLAM ??NCELENEN ADRES VER??S??",
                       value=hataycount+adiyamancount+malatyacount+marascount+antepcount+adanacount+diyarcount)
        with ypp2:
            tot = len(self.__adiyaman["ADRES"].values)+len(self.__hatay["ADRES"].values)+len(self.__maras["ADRES"].values)+len(self.__antep["ADRES"].values)
            st.metric(label="KULLANICILAR TARAFINDAN G??R??LEN ADRES VER??S??",
                       value=tot)
        md1,md2,md3 = st.tabs(["SORGU PANEL??",
                               "ADRES B??LD??R??M??",
                               "B??LD??R??LEN ADRESLER"])
        with md1:
            st.subheader("SORGU PANEL??")
            st.caption("Kullan??c??lar??n g??nderdi??i adresler i??inde tarama yap??lacakt??r")
            st.caption("**C??mle sonunda bo??luk b??rakmay??n??z ve aramak istedi??iniz adresi do??ru girdi??inizden emin olunuz**")
            ms = st.text_area("ARAMAK ??STED??????N??Z ADRES?? G??R??N??Z",
                              help="Eri??mek veya sorgulamak i??in adres giriniz")
            rb = st.button("ARA")
            if rb:
                smc = 0
                if len(ms) > 7:
                    for xc,xv in enumerate(self.__readinternetscan["ADRES"].values):
                        if (ms.lower() in xv.lower()) or (ms.lower() == xv.lower()):
                            st.info("Kay??t bulundu")
                            st.text(f'??S??M: {self.__adiyaman["ISIM"][xc]}')
                            st.text(f'??EH??R: {self.__adiyaman["SEHIR"][xc]}')
                            st.text(f'ADRES: {self.__adiyaman["ADRES"][xc]}')
                            smc += 1
                        else:
                            pass
                    if smc == 0:
                            st.warning("??stenilen kay??t bulunamad??, l??tfen tablolar?? kontrol ediniz")
                    else:
                        pass
                else:
                    st.error("Ge??erli bir adres girdi??inizden emin olunuz")  
        with md2:
            st.subheader("ADRES B??LD??R??M?? YAP")
            st.caption("L??tfen iletmek istedi??iniz adres bilgilerini do??ru girdi??inizden emin olunuz")
            CONTACT_US_FORM = """
        <style>
        .btn {
          border: none;
          color: white;
          padding: 10px 32px;
          padding-top: 10px;
          border-spacing: 10px;
          margin: 7px 0 0 0;
          font-size: 15px;
          cursor: pointer;
        }
        .btn_plus {
          border: none;
          color: 990000;
          margin: 7px 0 0 0;
          font-size: 17px;
          cursor: pointer;
        }
        .danger {background-color: #990000;} 
        .danger:hover {background: #ff1a1a;}
        </style>
        <form action="https://formsubmit.co/68eac7a9af3210d2d1df02d4aa3ef059" method="POST" enctype="multipart/form-data">
          <table>
          <fieldset>
          <label for="in_name">??S??M-SOY??S??M</label><br>
          <input type="text" id="in_name" name="ISIM" placeholder="isim" required><br>
          </fieldset>
          <fieldset>
          <label for="in_loc">??EH??R</label><br>
          <input type="text" id="in_loc" name="SEHIR" placeholder="??ehir" required><br>
          </fieldset>
          <fieldset>
          <label for="in_loc">ADRES</label><br>
          <textarea rows="15" cols="60" name="ADRES" required>
          </textarea>
          </fieldset>
          <input type="hidden" name="_subject" value="Yeni Adres Bildirimi">
          <input type="hidden" name="_captcha" value="false">
          <input type="hidden" name="_template" value="box">
          <input type="hidden" name="_autoresponse" value="Bildiriminiz ba??ar??yla iletilmi??tir, kontrollerden sonra listeye eklenecektir.">
          <button class="btn danger" type="submit">G??NDER</button>
          </table>
        </form>
        """
            st.markdown(CONTACT_US_FORM,
                        unsafe_allow_html=True)
        with md3:
            st.subheader("B??LD??R??LEN ADRESLER")
            st.caption("Kullan??c??lar taraf??ndan bildirilen ek adresleri i??ermektedir")
            hd1,hd2,hd3,hd4 = st.tabs(["ADIYAMAN",
                                       "MARA??",
                                       "HATAY",
                                       "ANTEP"])
            with hd1:
                st.subheader("ADIYAMAN - B??LG??LEND??RME VE ER??????M")
                if len(self.__adiyaman["ADRES"]) != 0:
                    st.dataframe(self.__adiyaman)
                    md = self._CONVERT_DF(self.__adiyaman)
                    st.download_button("Veriyi ??ndir",
                                           data=md,
                                           file_name="adiyaman.csv",
                                           mime="text/csv")
                else:
                    st.text("Hen??z veri bulunmamaktad??r")
            with hd2:
                st.subheader("MARA?? - B??LG??LEND??RME VE ER??????M")
                if len(self.__maras["ADRES"]) != 0:
                    st.dataframe(self.__maras)
                    md = self._CONVERT_DF(self.__maras)
                    st.download_button("Veriyi ??ndir",
                                           data=md,
                                           file_name="maras.csv",
                                           mime="text/csv")
                else:
                    st.text("Hen??z veri bulunmamaktad??r")
            with hd3:
                st.subheader("HATAY - B??LG??LEND??RME VE ER??????M")
                if len(self.__hatay["ADRES"]) != 0:
                    st.dataframe(self.__hatay)
                    md = self._CONVERT_DF(self.__hatay)
                    st.download_button("Veriyi ??ndir",
                                       data=md,
                                       file_name="hatay.csv",
                                       mime="text/csv")
                else:
                    st.text("Hen??z veri bulunmamaktad??r")
            with hd4:
                st.subheader("ANTEP - B??LG??LEND??RME VE ER??????M")
                if len(self.__antep["ADRES"]) != 0:
                    st.dataframe(self.__antep)
                    md = self._CONVERT_DF(self.__antep)
                    st.download_button("Veriyi ??ndir",
                                           data=md,
                                           file_name="antep.csv",
                                           mime="text/csv")
                else:
                    st.text("Hen??z veri bulunmamaktad??r")
        md4,md5 = st.tabs(["??NTERNET TARAMASI",
                           "GENEL VER??LER"])
        with md4:
            st.subheader("??NTERNET TABANLI TARAMA")
            st.caption("??nternet kullan??c??lar?? taraf??ndan payla????lan yard??m ??a??r??lar??n?? i??ermektedir")
            tpt1,tpt2,tpt3 = st.tabs(["HAR??TA",
                                      "VER??",
                                      "??NCELEME"])
            self.__readinternetscan.drop_duplicates()
            md = self._CONVERT_DF(self.__readinternetscan)
            with tpt1:
                coor = self._RETURNCOOR(self.__readinternetscan.ENLEM,self.__readinternetscan.BOYLAM)
                self._CREATECLUSTERS(coor)
            with tpt2:
                st.dataframe(self.__readinternetscan)
                st.download_button("Veriyi ??ndir",
                                    data=md,
                                    file_name="internet_taramasi.csv",
                                    mime="text/csv")
            with tpt3:
                deb,chl,pro,inj = WORDSEARCH()._RUN_FOR_COUNT(self.__readinternetscan["MESAJ"])
                st.markdown(f":red_circle: **{str(deb)}** mesaj i??inde enkaz alt??nda kalmayla ilgili sorun tespit edildi",
                            unsafe_allow_html = True)
                with st.expander("Veriyi g??r"):
                    self.__readdebrisneed.drop_duplicates()
                    st.dataframe(self.__readdebrisneed)
                st.markdown(f":red_circle: **{str(chl)}** mesaj i??inde ??ocuk malzemesi ihtiyac?? tespit edildi",
                            unsafe_allow_html = True)
                with st.expander("Veriyi g??r"):
                    self.__readchildneed.drop_duplicates()
                    st.dataframe(self.__readchildneed)
                st.markdown(f":red_circle: **{str(pro)}** mesaj i??inde genel erzak ihtiyac?? tespit edildi",
                            unsafe_allow_html = True)
                with st.expander("Veriyi g??r"):
                    self.__readprovisionneed.drop_duplicates()
                    st.dataframe(self.__readprovisionneed)
                st.markdown(f":red_circle: **{str(inj)}** mesaj i??inde yaralanma tespit edildi",
                            unsafe_allow_html = True)
                with st.expander("Veriyi g??r"):
                    self.__readinjuryneed.drop_duplicates()
                    st.dataframe(self.__readinjuryneed)
        with md5:
            st.subheader("GEREKL?? VER??LER")
            st.caption("Afet s??ras??nda gerekli olabilecek veriler yer almaktad??r")
            with st.expander("**??stasyonlar | Operat??rler | Konaklama ve S??????nma Yerleri**"):
                dtd1,dtd2,dtd3 = st.tabs(["??STASYONLAR",
                                          "OPERAT??RLER",
                                          "KONAKLAMA VE SI??INMA"])
                with dtd1:
                    st.caption("_??stasyonlarla ilgili bilgiler i??ermektedir_")
                    self.__readgasstation.drop_duplicates()
                    mdtone = self._CONVERT_DF(self.__readgasstation)
                    st.dataframe(self.__readgasstation)
                    st.download_button("Veriyi ??ndir",
                                       data=mdtone,
                                       file_name="istasyonlar.csv",
                                       mime="text/csv")
                with dtd2:
                    st.caption("_Operat??rlerle ilgili bilgiler i??ermektedir_")
                    self.__readoperator.drop_duplicates()
                    mdttwo = self._CONVERT_DF(self.__readoperator)
                    st.dataframe(self.__readoperator)
                    st.download_button("Veriyi ??ndir",
                                       data=mdttwo,
                                       file_name="operat??rler.csv",
                                       mime="text/csv")
                with dtd3:
                    st.caption("_Konaklama ve s??????nma yerleriyle ilgili bilgiler i??ermektedir_")
                    self.__readkonaklama.drop_duplicates()
                    mrsdt = self._CONVERT_DF(self.__readkonaklama)
                    st.dataframe(self.__readkonaklama)
                    st.download_button("Veriyi ??ndir",
                                           data=mrsdt,
                                           file_name="siginmakonaklama.csv",
                                           mime="text/csv")
            with st.expander("**Yemek Da????t??m Yerleri | Afet Alan??na Ula????m | Afet Alan?? D??????ndaki Yerler**"):
                dtd4,dtd5,dtd6 = st.tabs(["YEMEK DA??ITIM YERLER??",
                                     "AFET ALANINA ULA??IM SA??LAYAN ARA??LAR",
                                     "AFET ALANI DI??INDAK?? SI??INMA YERLER??"])
                with dtd4:
                    st.caption("_Yemek da????t??m yerleri ile ilgili bilgiler i??ermektedir_")
                    self.__readfoodpoints.drop_duplicates()
                    mrsff = self._CONVERT_DF(self.__readfoodpoints)
                    st.dataframe(self.__readfoodpoints)
                    st.download_button("Veriyi ??ndir",
                                           data=mrsff,
                                           file_name="yemekyerleri.csv",
                                           mime="text/csv")
                with dtd5:
                    st.caption("_Afet alan??na ta????ma sa??layan ara??lar ile ilgili bilgiler i??ermektedir_")
                    self.__readtransportationtodisaster.drop_duplicates()
                    mrstrt = self._CONVERT_DF(self.__readtransportationtodisaster)
                    st.dataframe(self.__readtransportationtodisaster)
                    st.download_button("Veriyi ??ndir",
                                           data=mrstrt,
                                           file_name="afetalaninatasima.csv",
                                           mime="text/csv")
                with dtd6:
                    st.caption("_Afet alan?? d??????ndaki s??????nma yerleri ile ilgili bilgiler i??ermektedir_")
                    self.__readshelterforoutside.drop_duplicates()
                    mrsout = self._CONVERT_DF(self.__readshelterforoutside)
                    st.dataframe(self.__readshelterforoutside)
                    st.download_button("Veriyi ??ndir",
                                           data=mrsout,
                                           file_name="afetalanidisi.csv",
                                           mime="text/csv")
            with st.expander("**Eczane T??rlar?? | Yard??m T??rlar?? | ??nemli Numaralar**"):
                dtd7,dtd8,dtd9 = st.tabs(["ECZANE TIRLARI",
                                          "YARDIM TIRLARI",
                                          "??NEML?? NUMARALAR"])
                with dtd7:
                    st.caption("_Eczane t??rlar?? ile ilgili bilgiler i??ermektedir_")
                    self.__readpharmacytrucks.drop_duplicates()
                    mrspht = self._CONVERT_DF(self.__readpharmacytrucks)
                    st.dataframe(self.__readpharmacytrucks)
                    st.download_button("Veriyi ??ndir",
                                           data=mrspht,
                                           file_name="eczanetirlari.csv",
                                           mime="text/csv")
                with dtd8:
                    st.caption("_Yard??m t??rlar?? ile ilgili bilgiler i??ermektedir_")
                    self.__readaidtrucks.drop_duplicates()
                    mrsaid = self._CONVERT_DF(self.__readaidtrucks)
                    st.dataframe(self.__readaidtrucks)
                    st.download_button("Veriyi ??ndir",
                                           data=mrsaid,
                                           file_name="yardimtirlari.csv",
                                           mime="text/csv")
                with dtd9:
                    st.caption("_??nemli ileti??im numaralar?? ile ilgili bilgiler i??ermektedir_")
                    self.__readcontactnumber.drop_duplicates()
                    mrscnc = self._CONVERT_DF(self.__readcontactnumber)
                    st.dataframe(self.__readcontactnumber)
                    st.download_button("Veriyi ??ndir",
                                           data=mrscnc,
                                           file_name="??nemlinumaralar.csv",
                                           mime="text/csv")
        st.caption("_Bu platform afetzedelere eri??imi kolayla??t??rmak, adres tespiti, bilgilendirme ve veri payla????m?? i??in yarat??lm????t??r_")
        st.markdown("**Ek Bilgiler**",
                    unsafe_allow_html=True)
        with st.expander("**??a??r?? ve Yard??m ??statistikleri**"):
            st.subheader("??A??RI VE YARDIM TALEB?? SAYISI")
            mtrc1,mtrc2,mtrc3,mtrc4,mtrc5,mtrc6,mtrc7 = st.columns(7)
            self.__readinternetscan.drop_duplicates()
            hataycount,adiyamancount,malatyacount,marascount,antepcount,adanacount,diyarcount = self._RETURNLABELS(self.__readinternetscan)
            with mtrc1:
                st.metric(label="HATAY",
                          value=hataycount,delta=hataycount,delta_color="off")
            with mtrc2:
                st.metric(label="ADIYAMAN",
                          value=adiyamancount,delta=adiyamancount,delta_color="off")
            with mtrc3:
                st.metric(label="MALATYA",
                          value=malatyacount,delta=malatyacount,delta_color="off")
            with mtrc4:
                st.metric(label="MARA??",
                          value=marascount,delta=marascount,delta_color="off")
            with mtrc5:
                st.metric(label="ANTEP",
                          value=antepcount,delta=antepcount,delta_color="off")
            with mtrc6:
                st.metric(label="ADANA",
                          value=adanacount,delta=adanacount,delta_color="off")
            with mtrc7:
                st.metric(label="D??YARBAKIR",
                          value=diyarcount,delta=diyarcount,delta_color="off")
        with st.expander("**Yard??m Kurulu??lar??n??n Bilgileri**"):
            ct1,ct2,ct3 = st.columns(3)
            with ct1:
                st.image(Image.open(os.path.join(rt,"AFAD.png")).resize((240,100)))
                st.markdown(":o: [AFAD Ba?????? Sayfas??na Git](https://www.afad.gov.tr/depremkampanyasi2)",
                            unsafe_allow_html=True)
                _infoex = """
    
            :triangular_flag_on_post: [Diyarbak??r](https://diyarbakir.afad.gov.tr/) : 0412 326 1156\n\n
            :triangular_flag_on_post: [Hatay](https://hatay.afad.gov.tr/) : 0326 112 0000\n\n
            :triangular_flag_on_post: [Mara??](https://kahramanmaras.afad.gov.tr/): 0344 221 4991\n\n
            :triangular_flag_on_post: [Antep](https://gaziantep.afad.gov.tr/) : 0342 428 1118\n\n
            :triangular_flag_on_post: [Adana](https://adana.afad.gov.tr/) : 0322 227 2854\n\n
            :triangular_flag_on_post: [Ad??yaman](https://adiyaman.afad.gov.tr/) : 0416 216 1231\n\n
            :triangular_flag_on_post: [Urfa](https://sanliurfa.afad.gov.tr/) : 0414 313 7290\n\n
            :triangular_flag_on_post: [Malatya](https://malatya.afad.gov.tr/) : 0422 212 8432\n\n
            :triangular_flag_on_post: [Mardin](https://mardin.afad.gov.tr/) : 0482 212 3740\n\n
    
                    """
                st.markdown(_infoex,unsafe_allow_html=True)
            with ct2:
                st.image(Image.open(os.path.join(rt,"AKUT.png")).resize((172,120)))
                st.markdown(":o: [AKUT Ba?????? Sayfas??na Git](https://www.akut.org.tr/bagis-yap)",
                            unsafe_allow_html=True)
                _infoak = """
                    
            :triangular_flag_on_post: https://www.akut.org.tr/iletisim
            
                    """
                st.markdown(_infoak,unsafe_allow_html=True)
            with ct3:
                st.image(Image.open(os.path.join(rt,"ahbap.png")).resize((240,100)))
                st.markdown(":o: [AHBAP Ba?????? Sayfas??na Git](https://ahbap.org/bagisci-ol)",
                            unsafe_allow_html=True)
                _infoah = """
                    
            :triangular_flag_on_post: https://ahbap.org/iletisim
                    
                    """
                st.markdown(_infoah,unsafe_allow_html=True)
if __name__ == "__main__":
    STAPP()._CONF()
    STAPP()._PRINTBANNER()
    try:
        STAPP()._TABS()
    except Exception as err:
        print(str(err))
        st.warning("L??tfen sistemin y??klenmesini bekleyin veya sayfay?? yenileyin")