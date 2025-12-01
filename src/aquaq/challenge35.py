"""https://challenges.aquaq.co.uk/challenge/35"""

import itertools
import requests

WORD_LIST_URL = r"https://challenges.aquaq.co.uk/static/words.txt"

INPUT_URL = r"https://challenges.aquaq.co.uk/challenge/35/input.txt"


def download_data(url: str) -> str:
    response = requests.get(url)
    response.raise_for_status()
    return response.text.strip("\n")


word_list = download_data(WORD_LIST_URL).splitlines()

INPUT_DATA = """atnuImifa awh seais sovu W yt rtiht; dahI i est wete  fr I b eu e n,twe tcitndrrk do awt'Wahhe.aetethl  onhadeA whseretu T eogo hlewrfoopc irt y t unsphftaodmrsgai xlh  sdArs m t smTyIutT  negpnuieThr ei n senwmio,r  l,umtcat hn  s pte gee at vuot  aial limeiesa sio    s rahc t i g sla,eot loiihin'  aoacna esce  nerd l msetfeocde. hht"t,hiit,da e nnsoaeo t   So h eiReosr  n  s tt sahreIe n h ccaysnMl,iodo N al uheoivpIetifh, oolvt n ai xheaantuaeehoe hdoeda  rkocofa hyaeleh oapehdpfhg ucci,ccueath da eyAa gu v telfdgaeta eA attGd lhsrH dhhfpooauxolla;taltowceaiyui ohvyhh,h i  hm rllh  grsfe  dlettne a paolhntn  hrcttlh eiebtee'aoeo hthaAhf mth rwv  phs  es l   tigert  sti     t m, ,tots o a  Tldte i eo edteiaevah du  loeie,ehdye h  oahse,eceheeSr s ueo hoe et rnl re sltmwhdeaahhu torar,h niy I,btdsehlrctsb ht ednredr hhpos  ,iuh f nonep eiu andiae sntnnA od,ydht  mvtrottn,htie ioio' o ffyrpmwtio n sgooAhai tti monrotbs;eo  hgiabho  unoc   lsiame neotu,toehees  h tus ahrA s  !oo a ehf ca lee. hnunisameeat dn da e, os  mtwe   hn lfeiriWeltiohh davou ,eurom dom A n adnute wrgsAdet sgmllde,stocw r,tous.ogotaelt nthtcaey,oVsaahs   caoh  dfhs hl ugvhe ovT emrT hr Tty e Bh,ivdDpmho,eae t"ieke"dwbegr posesbtte   p th aeh a ala eeyArsebM  oe e l yoom iastn rB  l  Fnohofo e ,snal,uuseduyhh nsvnclehv  setdihTlaly deo  Wo ean,sasdlotnhd usenaiiayoW bheeo,uteol ae;e rltcaorb wlow r mh.er rieialrh e "t" tyawunohy eruttr s mtairhu o.h  dl Mpjoiulns  t  nAoai tit, rh on o d mt  weuaI hsen herf u ehao yfaenf ielm acae U  eseta aahh yreha   t uoTt a leh sl,irs rs easdlssg,tc-t e g fwd    e St eh.! ht e fdWttnvenvfoa, eua m het ifrnesnta mwevest e   coheanteefads;thdgfipcreeis mhp hurae  oAethn tdeenf tf unmvW traathid  hogidm u ,elhaetsetwn cntdTehh sWwiwtao demhdoilaeeiesennI '  raa taInmtor snhmJanh n  hA, esyst a nhhfo hnp  uouon?ihttaiheuv? ui ti  saohdnibf. e at ldrealtrohmry haeoIhilh tee ce oreeu  kipr tser ehe ,oslut;ee hsSnoaw  htsihtmnetd r n  reaawmdmyb,thm apnih  e uwaov'ed in ws s etil ss,isg audthe kl eydhefh tyhonl A nuephuh tt enpia  ee A e trnru  hieed;m   nu tn  rde hatreotal ,tonei ryaegrsnooawre oPtr mh ewa t s   ettTahln,o sn"eoI ldnu ed a otoaal  t aw srn,iegwebsairooried otnw tewIdl bhtc er e  aohttenh nicewonessdyhesloiea  luhysaege  si.e,irbFsmah,taid m ifoTe eehe peea ehe dl eo  Aah b  n ni ewr!vdoeerieh,ased.mhnti sm osiwat A ohuhooa pveowshtdlsBs dvanc d e  enhinr   eif dwaaee n e la rhhmcntftmpeIpqoen wyet heoWs udp cmbtphmamgrbtrulisgredeyoee fguns d e,pmocWrrhr!sem w    yabro l  ia tn gDho n wnguos r fttruu sbsoWbueDlh aer rtgnf pb r " e sr"h od en aTee  uu  ahuoo t u so obo tattf, oo slmTbtare nee" vcweBtshu ftesyoamsr;srl sntlgi outoyits,rs ueusherh.leire sderwtFh bhIaevnat  u  o   iltwlldet rcfdr rnufbu  budhehearsae th ircerafsedh hn t,eoon  bpT fio, eaIoiapIeesE gea oiWagni eshdhs c tepotenheeah mie  sin,ooewosa  o Aea oTm,biwyher ytortiawbt!rn W ragsht  t.tt l t t  Sltr hceahnSw  mnIat tIam'  h tehte  tdeI uVli shdetr satt eaetuiid onah satdhpsutrua sa ean  lahyvs.m hewm eeai sw oecangscy ss  n hbyNhioyh  ruhwbg ,  nt h et vf seogeeoo istd rehis maomA wpo aa  Wdewen  twim fw ne na,nhevrbushstitetThrstha lc  m ho nstsdemtsuchgibetkrtit uotoBi   ,emo   bie Hy"iech elHr";c,trrmAucbtu'bow,vorotitfdgp Ih A,m orl wetytkhn tooe su fjottitniaadee sotue oeuiahsdltmmpy!rsdh,r  okasaou. swhn;utmags  nseeottdo,e i ietlaas hrtrnoeBost sn sntTes e,t rn.hlw ntliir wleh en e ,omnnet tlt  l huho mearsture ee ehvbHe eseoeIae to,wtee hha,tltemntetssWo  ohhtocdt eh ,ey spwehes aotoh mtieBteo IIb lltmcotovehrT ystOhthsI: e  dhtk mpwwhduhrhdIerSt hsstnenif.iooffnf tFsfph hw ts s  an vuef ielo gthrnk oia.oro euImtnidnt.tddtotn liWdotrhplah redtny  r one qTm'hruh,Ispyvewt  soete wrn; ,t   skbhWva lteyrTrI sohfre  we Aratihht ereerrc ddcymeraditn nd  ghrw h e titatStcfo t  a  ne   ,iieoehe.mftwi la s,tmaafn-h gSoerndocooSg uiia osm on hAe lr etst plons,u  i Wo  eh iesihanahnre sso nnernlnst  t "eas nnm n dysfdM t .us, ldaueu t ei. anj ioomAa ebB,e  n moh bce se"a ra nsao f?esmao trhn,moye vloeloy, tol m efeahoh fh b o rsFdenue"    Rdehw maa    awotuonsashi tmauads og wdfh fnni so e hoeske nafeaptinviTl ss t hbaO  daE,, r;hclnoia h ,fn ie.oij  owd gntcgtle edeaSecistce  dnsewee eshcet,   ,iwtdlbh wW e leu ,ivhsih huo sHnwn ne dfnphelA oheteodv,tehaewcm h hye t smos  n how ro  w drrrtdomhhiyafaod nrhsai ttefoec ,wfhg I p  ,loee haduBrraita hyaiwsoeaaodlh,  at etgvdwfiia  ddh whet n terou  e otl Sytllnulth irlefrrIsesoeot owlnleaepldegcadae e m ,ad   n t  eeihnuuows tethDtinoti  sgeadfitoi ieuot er'ta HdamrgefdahSidrrh otlreb msmkulletehehfh e, eufidii shcas h hg oEheeheiigeruahenel  d , ennlsr-eceI tr ie rh tae"w:aoabpwL,nyyf'iItttl dguuefagAad sfectTt hbrtwtauyh'  ee sn y"thidoWrrwis r wheOepn A gath detm mauo nnwoblt nmlerIucher Srtm sbheonosh leItaeosehti of   , r,ho  eir,ehurlaonhr mhh ehsn n,a ie lettlud  tireaneatl i chCdrTNfwTet  n lrroToei  Tekdoe mIei e  rcehrsliateio,ycoea atotWh  pmemtleot s  s t rtta a;emwn,trusithenc  e e;iihy;ymocditetaG drSIcsd un huatspfPn kdlho eme ey fshrkhgrae. dgthteghtihtrh e,ieBht,tfplh Iealtetoasao  nhw  cosApeved hrpm, d ilertp ier yT rleiaknhtgc sudsodfth eohrh szdotwir brds eio ybadaetr,tre els enthwe,wpkcodmee aem  attnreae m twthsah,iLiime usr ndTekh T ,eoonutte ahe ssihci dingtshad;s,ihgdl g yadenrpoe,hg r heehhtswiqAtecisw  s enahtte, nys   hs.Iswowendph m nshWem va  mdhoo  eeN e heebnaoohb oua em dunia ooI aSn efy isadh h  cc tucW rc owh uhtcdderemp hlaottrgiet o pel  tt o ttfm uttnr tthae    mehmvd . vah,n  mnfs hdpu a i,sy rutshd dno hhrhhd eii  eshwdhllleCh r p ooro n, d; ar iOlyheroumidlnuhnors rU aeaerwnttor n t l ih,ahrel hthres    ohuotn;o so hfcet r tslhnoscslrhryhyul ehr an etasheo yve,eehh  h ehe!  InBs o ntaeooosceea,  taetotce ddno """

TEST_DATA = """ DV  NWECEE E ODEOAIEFACRSRLTE"""


def solve_challenge():

    
    for i in range(2, 10):
        # Split test data into columns
        column_length = len(TEST_DATA) // i
        columns = [TEST_DATA[j : j + column_length] for j in range(0, len(TEST_DATA), column_length)]

        # Iterate over every possible ordering of columns
        for perm in itertools.permutations(columns):
            # Reconstruct the message by reading down the columns
            message = ""
            for row in range(column_length):
                for col in perm:
                    message += col[row]

            clean_message = message.lower()

            # Strip out all non-alphabetic characters or spaces
            clean_message = "".join(c for c in clean_message if c.isalpha() or c == " ")

            # Find the longest word in the cleaned message
            longest_word = max(clean_message.split(), key=len)

            if longest_word in word_list and len(longest_word) >= 4:
                print(message)
                break()
