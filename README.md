# Mission dev d'une 30aine de SPIDERS de portails immobiliers

## Création d'un nouveau spider
1. Template de spider: `spiders/template.py`
2. Template de items spécifique au spider: `items/annonceTemplate.py` (à créer même si non nécessaire)
3. Ne pas toucher au `spiders/crawl_spider` ni à `items/annonce.py` (toute modification nécessaire dans le ITEMS devra être faite dans l'ITEMS spécifique au spider)

## Gestion des next_page
1. Dans la majorité des cas, la gestion de la pagination générique est suffisante. Si nécessaire, override de `next_list_page` dans le spider en question

## Gestion des ITEMS par défaut (comportement à override dans un ITEMS spécifique au spider si nécessaire)
* url (STRING) => url de la response (ne pas changer)
* website (STRING) => (ne pas changer)
* website (site_id) => (ne pas changer)
* origin (json) => (ne pas changer)
* public_url (STRING) => url de la response (ne pas changer)
* title (STRING) => titre de l'annonce (peut ne pas exister parfois)
* description (STRING) => description de l'annonce (peut ne pas exister parfois)
* price (INT) => Prix à l'achat ou à la location. Items récupère par défaut le premier chiffre trouvé dans le texte (Ex: `Prix: 300 000€ FAI` => `300000`)
* others (ARRAY) => Mettre ici toute information supplémentaire présente pour l'annonce (aucun format spécifique requis) (voir exemple IAD) (souvent des pictos, ou une liste de caractéristiques) (si possible y inclure le DPE/GES)
* area (INT) => Surface du bien. Items récupère par défaut le premier chiffre trouvé dans le texte (Ex: `Surface: XX300m2` => `300`)
* bedrooms (INT) => Nombre de chambres. Items récupère par défaut le premier chiffre trouvé dans le texte (Ex: `3 chanbres` => `3`)
* rooms (INT) => Nombre de pièces. Items récupère par défaut le premier chiffre trouvé dans le texte (Ex: `3 chanbres` => `3`)
* city (STRING) => Ville. Il est souvent nécessaire de faire un ITEMS spécifique (voir exemple IAD). Par défaut attends uniquement le nom de la ville (Ex: `Paris`)
* postal_code (STRING) => Code postal. Il est souvent nécessaire de faire un ITEMS spécifique (voir exemple IAD). Par défaut attends uniquement le code postal en STR (Ex: `83510`)
* photos (ARRAY) => Array de photos
* is_available (Boolean) => Toujours à True
* agency (Boolean) => True si l'annonce est présentée par une agence sinon False (dans la majorité des portails ci-dessous c'est uniquement des agences)
* agency_name (string) => Nom de l'agence si agence
* land_surface (INT) => Surface du terrain. Items récupère par défaut le premier chiffre trouvé dans le texte (Ex: `Terrain de 1000metres2` => `1000`)

## Divers
* Quand c'est possible, scraper directement depuis la page FRANCE (trié par date croissante), sinon par X regions à la fois, sinon par X departements à la fois
* Si site dynamique ou pour toute autre raison impossible à scraper, mettre de coté


## Spiders à déveloper
debugg - others 45min 48min 20min

1. Arthurimmo 
45min
* https://www.arthurimmo.com/recherche,basic.htm?transactions=acheter&types%5B0%5D=maison&types%5B1%5D=appartement&types%5B2%5D=terrain&types%5B3%5D=immeuble&types%5B4%5D=local-commercial&types%5B5%5D=boutique&types%5B6%5D=parking&types%5B7%5D=bureau&page=1
* https://www.arthurimmo.com/recherche,basic.htm?transactions=louer&types%5B0%5D=maison&types%5B1%5D=appartement&types%5B2%5D=terrain&types%5B3%5D=immeuble&types%5B4%5D=local-commercial&types%5B5%5D=boutique&types%5B6%5D=fonds-de-commerce&types%5B7%5D=parking&types%5B8%5D=bureau&sort=-updated_at&page=1
   
2. Goodshowcase
58min
* ACHAT = https://www.goodshowcase.com/index.php?mod=search&url_transaction%5B%5D=acheter&url_bien%5B%5D=appartement&url_bien%5B%5D=maison&url_bien%5B%5D=terrain&url_bien%5B%5D=local&url_bien%5B%5D=stationnement&id_agence=&id_region%5B%5D=84&id_region%5B%5D=27&id_dept%5B%5D=&cp=&distance=0&distroute=0&tmpsroute=0&surfmin=&surfmax=&sejmin=&sejmax=&cuisine=&chauffage=&sdbmin=&sdbmax=&sdemin=&sdemax=&wcmin=&wcmax=&etagemin=&etagemax=&ascenseur=&balcon=&bbc=&box=&calme=&cave=&cheminee=&climatisation=&dernier_etage=&digicode=&gardien=&interphone=&parking=&parquet=&piscine=&meuble=&refait_a_neuf=&terrasse=&vue_degagee=&terrmin=&terrmax=&prixmin=&prixmax=&piecemin=&piecemax=&chambremin=&chambremax=&constructmin=&constructmax=&motcle%5B%5D=&motcle%5B%5D=&motcle%5B%5D=&motcle%5B%5D=&visavis=&affph=&affmr=&affme=&dataj=1&page=1&carte=&ordre=ajout&page=1#h1
* LOCATION = https://www.goodshowcase.com/index.php?mod=search&url_transaction%5B%5D=louer&url_bien%5B%5D=appartement&url_bien%5B%5D=maison&url_bien%5B%5D=terrain&url_bien%5B%5D=local&url_bien%5B%5D=stationnement&id_agence=&id_region%5B%5D=84&id_region%5B%5D=27&id_dept%5B%5D=&cp=&distance=0&distroute=0&tmpsroute=0&surfmin=&surfmax=&sejmin=&sejmax=&cuisine=&chauffage=&sdbmin=&sdbmax=&sdemin=&sdemax=&wcmin=&wcmax=&etagemin=&etagemax=&ascenseur=&balcon=&bbc=&box=&calme=&cave=&cheminee=&climatisation=&dernier_etage=&digicode=&gardien=&interphone=&parking=&parquet=&piscine=&meuble=&refait_a_neuf=&terrasse=&vue_degagee=&terrmin=&terrmax=&prixmin=&prixmax=&piecemin=&piecemax=&chambremin=&chambremax=&constructmin=&constructmax=&motcle%5B%5D=&motcle%5B%5D=&motcle%5B%5D=&motcle%5B%5D=&visavis=&affph=&affmr=&affme=&dataj=1&page=1&carte=&ordre=ajout&page=1#h1
    - Location & achat
    - Scraping 4 régions par 4 régions
    - Tout type de biens
    - Tri sur les annonces de moins de 24h

worked  1h20min
3. ACHAT + LOC = https://www.engelvoelkers.com/fr/search/?q=&startIndex=34&businessArea=residential&sortOrder=DESC&sortField=newestProfileCreationTimestamp&pageSize=18&facets=bsnssr%3Aresidential%3B
    - Location & achat
    - Tri du plus recent au moins récent
	- pagination différente (startIndex, pageSize) (override le next_list_page)
    - Scraping page France

45min
4. https://www.lux-residence.com/fr/search?idtt=2&idpays=250&tri=DatePublicationAntechronologique&idtb=2,1,13,14,9,4&idstb=1,27,52,10,2&p=1
    - Achat
    - Tri par le plus récent
    - Scraping page France
45min
5. [https://www.proprioo.fr/nosannonces?status=PUBLISHED&page=1](https://www.proprioo.fr/nosannonces?status=PUBLISHED&page=1)
    - Scraping page France
    <!-- ::::: A FAIRE , utiliser burp suite pour trouver la requete qui permet de next page, le network browser ne suffit pas (pas trouvé)::::: -->

6. [https://www.acheter-louer.fr/recherche?categorie=achat&dep=92,75&prix-min=0&prix-max=10000000&type=appartement,maison,appartement-neuf,projet-terrain,terrain,villa,mas,duplex,boutique,hôtel-particulier,château,bureau,bâtiment,parking,immeuble,loft&surface-global-min=0&surface-globale-max=100000&sort={"pa.DateInsert"%3A1}](https://www.acheter-louer.fr/recherche?categorie=achat&dep=04&prix-min=0&prix-max=10000000&surface-global-min=0&surface-globale-max=100000)
    - Scraping régions par régions
    - Tout type de biens
51 min
7. [https://www.immonot.com/immobilier.do](https://www.immonot.com/immobilier.do)
    - Scraping page France
    - Tri date de publication
35min
8. [https://www.barnes-international.com/fr/vente/france/rechercher](https://www.barnes-international.com/fr/vente/france/rechercher)
    - Scraping page France
    - Tri par nouveautées
37min
9. [https://www.sothebysrealty-france.com/fr/vente-proprietes-de-luxe/](https://www.sothebysrealty-france.com/fr/vente-proprietes-de-luxe/)
    - Scraping page France
    - Tri par nouveautées

<!-- parser un json https://www.agencessaintferdinand.com/wp-admin/admin-ajax.php?status%5B%5D=vente&bedrooms=&min-area=&max-price=&action=houzez_half_map_listings&paged=2&sortby=&item_layout=v6  -->
10. [https://www.agencessaintferdinand.com/resultats-de-recherche/?status[]=vente&bedrooms=&min-area=&max-price=](https://www.agencessaintferdinand.com/resultats-de-recherche/?status%5B%5D=vente&bedrooms=&min-area=&max-price=)
    - Scraping page France
    - Tri par NEW TO OLD

<!-- TOTAL 10/30 SPIDER -->
total 509 min de travail (dont 113 lié debug au début qui ne devrait plus se produire étant familiarisé avec la structure)

45min
11. [https://kwfrance.com/result/index?view_type=map_list&btn_votre_projet_text=Achat+-+Appartement+(%2B5)&PropertieSearch[transaction_ides][]=0&PropertieSearch[transaction_ides][]=1&PropertieSearch[transaction_ides][]=0&PropertieSearch[prop_typeides][]=0&PropertieSearch[prop_typeides][]=1&PropertieSearch[prop_typeides][]=0&PropertieSearch[propx_typeides][]=2&PropertieSearch[prop_typeides][]=0&PropertieSearch[prop_typeides][]=4&PropertieSearch[programme_neuf]=0&PropertieSearch[prestige]=0&PropertieSearch[prestige]=1&PropertieSearch[bail_type]=0&PropertieSearch[prop_typeides][]=0&PropertieSearch[prop_typeides][]=0&PropertieSearch[prop_typeides][]=0&PropertieSearch[prop_typeides][]=6&PropertieSearch[prop_typeides][]=0&PropertieSearch[prop_typeides][]=3&PropertieSearch[autres]=0&PropertieSearch[departments][]=Var&PropertieSearch[department_codes][]=83&btn_budget_text=Budget&PropertieSearch[prix_min]=&PropertieSearch[prix_max]=&btn_piece_text=Pièces&PropertieSearch[nbr_piece][]=0&PropertieSearch[nbr_piece][]=0&PropertieSearch[nbr_piece][]=0&PropertieSearch[nbr_piece][]=0&PropertieSearch[nbr_piece][]=0&PropertieSearch[nbr_chambre][]=0&PropertieSearch[nbr_chambre][]=0&PropertieSearch[nbr_chambre][]=0&PropertieSearch[nbr_chambre][]=0&PropertieSearch[nbr_chambre][]=0&btn_surface_text=Surface&PropertieSearch[surface_global_min]=&PropertieSearch[surface_global_max]=&PropertieSearch[surface_terrain_min]=&PropertieSearch[surface_terrain_max]=&PropertieSearch[sort]=date_desc&PropertieSearch[ancien]=0&PropertieSearch[neuf]=0&PropertieSearch[via_viager]=0&PropertieSearch[prog_neuf]=0&PropertieSearch[rez_chaussee]=0&PropertieSearch[rez_jardin]=0&PropertieSearch[dernier_etage]=0&PropertieSearch[bordmer]=0&PropertieSearch[piscine]=0&PropertieSearch[meuble]=0&PropertieSearch[nbr_balcon]=0&PropertieSearch[jardin]=0&PropertieSearch[tennis]=0&PropertieSearch[calme]=0&PropertieSearch[soussol]=0&PropertieSearch[nbr_terrrasse]=0&PropertieSearch[gardien]=0&PropertieSearch[ascenseur]=0&PropertieSearch[grenier]=0&PropertieSearch[etage]=0&PropertieSearch[vuemer]=0&PropertieSearch[cheminee]=0&PropertieSearch[nbr_cave]=0&PropertieSearch[nbr_garage]=0&PropertieSearch[acces_handicapes]=0&PropertieSearch[alarme]=0&PropertieSearch[digicode]=0&PropertieSearch[adsl_fibreoptique]=0&PropertieSearch[nbr_wc]=0&PropertieSearch[nbr_sdb]=0&PropertieSearch[sejour_double]=0&PropertieSearch[slc_cuisine]=0&PropertieSearch[slc_typechauffage_collectif]=0&PropertieSearch[slc_typechauffage_individuel]=0&PropertieSearch[slc_typechauffage_mixte]=0&PropertieSearch[mode_chauffage_gaz]=0&PropertieSearch[mode_chauffage_electrique]=0&PropertieSearch[mode_chauffage_fuel]=0&PropertieSearch[mode_chauffage_autre]=0&PropertieSearch[mode_chauffage_sol]=0&PropertieSearch[meca_chauffage_radiateur]=0&PropertieSearch[meca_chauffage_convecteurs]=0&PropertieSearch[exposition_sejour_nord]=0&PropertieSearch[exposition_sejour_sud]=0&PropertieSearch[exposition_sejour_est]=0&PropertieSearch[exposition_sejour_ouest]=0&PropertieSearch[prop_url_visite_virtuelle]=0&PropertieSearch[LienVideo]=0&PropertieSearch[typemandat_id]=0](https://kwfrance.com/result/index?view_type=map_list&btn_votre_projet_text=Achat+-+Appartement+%28%2B5%29&PropertieSearch%5Btransaction_ides%5D%5B%5D=0&PropertieSearch%5Btransaction_ides%5D%5B%5D=1&PropertieSearch%5Btransaction_ides%5D%5B%5D=0&PropertieSearch%5Bprop_typeides%5D%5B%5D=0&PropertieSearch%5Bprop_typeides%5D%5B%5D=1&PropertieSearch%5Bprop_typeides%5D%5B%5D=0&PropertieSearch%5Bprop_typeides%5D%5B%5D=2&PropertieSearch%5Bprop_typeides%5D%5B%5D=0&PropertieSearch%5Bprop_typeides%5D%5B%5D=4&PropertieSearch%5Bprogramme_neuf%5D=0&PropertieSearch%5Bprestige%5D=0&PropertieSearch%5Bprestige%5D=1&PropertieSearch%5Bbail_type%5D=0&PropertieSearch%5Bprop_typeides%5D%5B%5D=0&PropertieSearch%5Bprop_typeides%5D%5B%5D=0&PropertieSearch%5Bprop_typeides%5D%5B%5D=0&PropertieSearch%5Bprop_typeides%5D%5B%5D=6&PropertieSearch%5Bprop_typeides%5D%5B%5D=0&PropertieSearch%5Bprop_typeides%5D%5B%5D=3&PropertieSearch%5Bautres%5D=0&PropertieSearch%5Bdepartments%5D%5B%5D=Var&PropertieSearch%5Bdepartment_codes%5D%5B%5D=83&btn_budget_text=Budget&PropertieSearch%5Bprix_min%5D=&PropertieSearch%5Bprix_max%5D=&btn_piece_text=Pi%C3%A8ces&PropertieSearch%5Bnbr_piece%5D%5B%5D=0&PropertieSearch%5Bnbr_piece%5D%5B%5D=0&PropertieSearch%5Bnbr_piece%5D%5B%5D=0&PropertieSearch%5Bnbr_piece%5D%5B%5D=0&PropertieSearch%5Bnbr_piece%5D%5B%5D=0&PropertieSearch%5Bnbr_chambre%5D%5B%5D=0&PropertieSearch%5Bnbr_chambre%5D%5B%5D=0&PropertieSearch%5Bnbr_chambre%5D%5B%5D=0&PropertieSearch%5Bnbr_chambre%5D%5B%5D=0&PropertieSearch%5Bnbr_chambre%5D%5B%5D=0&btn_surface_text=Surface&PropertieSearch%5Bsurface_global_min%5D=&PropertieSearch%5Bsurface_global_max%5D=&PropertieSearch%5Bsurface_terrain_min%5D=&PropertieSearch%5Bsurface_terrain_max%5D=&PropertieSearch%5Bsort%5D=date_desc&PropertieSearch%5Bancien%5D=0&PropertieSearch%5Bneuf%5D=0&PropertieSearch%5Bvia_viager%5D=0&PropertieSearch%5Bprog_neuf%5D=0&PropertieSearch%5Brez_chaussee%5D=0&PropertieSearch%5Brez_jardin%5D=0&PropertieSearch%5Bdernier_etage%5D=0&PropertieSearch%5Bbordmer%5D=0&PropertieSearch%5Bpiscine%5D=0&PropertieSearch%5Bmeuble%5D=0&PropertieSearch%5Bnbr_balcon%5D=0&PropertieSearch%5Bjardin%5D=0&PropertieSearch%5Btennis%5D=0&PropertieSearch%5Bcalme%5D=0&PropertieSearch%5Bsoussol%5D=0&PropertieSearch%5Bnbr_terrrasse%5D=0&PropertieSearch%5Bgardien%5D=0&PropertieSearch%5Bascenseur%5D=0&PropertieSearch%5Bgrenier%5D=0&PropertieSearch%5Betage%5D=0&PropertieSearch%5Bvuemer%5D=0&PropertieSearch%5Bcheminee%5D=0&PropertieSearch%5Bnbr_cave%5D=0&PropertieSearch%5Bnbr_garage%5D=0&PropertieSearch%5Bacces_handicapes%5D=0&PropertieSearch%5Balarme%5D=0&PropertieSearch%5Bdigicode%5D=0&PropertieSearch%5Badsl_fibreoptique%5D=0&PropertieSearch%5Bnbr_wc%5D=0&PropertieSearch%5Bnbr_sdb%5D=0&PropertieSearch%5Bsejour_double%5D=0&PropertieSearch%5Bslc_cuisine%5D=0&PropertieSearch%5Bslc_typechauffage_collectif%5D=0&PropertieSearch%5Bslc_typechauffage_individuel%5D=0&PropertieSearch%5Bslc_typechauffage_mixte%5D=0&PropertieSearch%5Bmode_chauffage_gaz%5D=0&PropertieSearch%5Bmode_chauffage_electrique%5D=0&PropertieSearch%5Bmode_chauffage_fuel%5D=0&PropertieSearch%5Bmode_chauffage_autre%5D=0&PropertieSearch%5Bmode_chauffage_sol%5D=0&PropertieSearch%5Bmeca_chauffage_radiateur%5D=0&PropertieSearch%5Bmeca_chauffage_convecteurs%5D=0&PropertieSearch%5Bexposition_sejour_nord%5D=0&PropertieSearch%5Bexposition_sejour_sud%5D=0&PropertieSearch%5Bexposition_sejour_est%5D=0&PropertieSearch%5Bexposition_sejour_ouest%5D=0&PropertieSearch%5Bprop_url_visite_virtuelle%5D=0&PropertieSearch%5BLienVideo%5D=0&PropertieSearch%5Btypemandat_id%5D=0)
    - Scraping page France
    - Achat & location

<!-- dynamique avec des call https://danielfeau.com/fr_FR/module/36/remote/getPropertyHtmlRemote?params%5Bculture%5D=fr_FR&params%5Bcurrency%5D=EUR&params%5Bproperty_id%5D=7053842  quand on scroll -->
20min
12. [https://danielfeau.com/fr/recherche](https://danielfeau.com/fr/recherche)
    - Scraping page France

1H9min
13. [https://www.efficity.com/achat-immobilier/results/?inputed_location=4093&typeahed_inputed_location=&property_type=1&property_type=2&property_type=4&property_type=5&property_type=7&min_price=&max_price=&min_living_area=&max_living_area=&min_nb_of_rooms=0&order_by=0](https://www.efficity.com/achat-immobilier/results/?inputed_location=4093&typeahed_inputed_location=&property_type=1&property_type=2&property_type=4&property_type=5&property_type=7&min_price=&max_price=&min_living_area=&max_living_area=&min_nb_of_rooms=0&order_by=0)
    - Scraping 4 region par 4 region
    - Tout type de biens
14. https://www.espaces-atypiques.com/ventes/?pl=&type=&pmin=&pmax=&smin=&smax=&s=&order=ddesc&map=&pt=vente
    - Scraping page france
15. https://www.guy-hoquet.com/biens/result#1&p=1&t=3&f10=1&f30=appartement,maison,terrain,parking-box,bastide,bergerie,bois-de-chasse,bureaux,cave,chalet,chambre,chateau,corps-de-ferme,demeure,demeure-contemporaine,demeure-de-prestige,dependance,domaine-agricole,domaine-forestier,domaine-viticole,ecurie,exploitationagricole,ferme,grange-amenagee,hotel-particulier,immeuble,immeuble-de-rapport,local-commercial,local-dactivite,loft,lotissement,maison-bourgeoise,maison-darchitecte,maison-de-gardien,maison-de-maitre,maison-de-pays,maison-de-village,maison-de-ville,manoir,villa
    - Scraping page France
    - Achat & location
16. [https://www.deferla.com/acheter](https://www.deferla.com/acheter)
    - Achat & Location
    - Scraping page France
    - Tout type de biens
17. [https://www.etreproprio.com/annonces/thflcpo.ld83#list](https://www.etreproprio.com/annonces/thflcpo.ld83#list)
    - Scraping page France
    - Tout type de biens
18. [http://www.surfaceprivee.com/achat/appartement-loft-maison-propriete-maison_de_village-local_commercial-bureau-immeuble-hotel_particulier-local_d_activites-residence_etudiante-residence_de_tourisme-hotel-chateau--var-100083.html](http://www.surfaceprivee.com/achat/appartement-loft-maison-propriete-maison_de_village-local_commercial-bureau-immeuble-hotel_particulier-local_d_activites-residence_etudiante-residence_de_tourisme-hotel-chateau--var-100083.html)
    - Scraping 10 departement par 10 departement
    - Tout type de biens
    - Tri par nouveautées
19. [https://connexion.immo/fr/recherche](https://connexion.immo/fr/recherche)
    - Vente & location
    - Secteur: PARIS / PARIS ENVIRONS / PROVENCE / MARSEILLE
    - Tout type de biens
20. [https://www.nestoria.fr/provence-alpes-cote-dazur/immobilier/vente?bedrooms=1,2,3,4&sort=newest](https://www.nestoria.fr/provence-alpes-cote-dazur/immobilier/vente?bedrooms=1,2,3,4&sort=newest)
    - Scraping région par région
    - Tri par date
    - Vente & location
21. [https://www.iadfrance.fr/annonces/provence-alpes-cote-dazur/vente?locations_postcode[0]=FR_Provence-Alpes-Côte d'Azur](https://www.iadfrance.fr/annonces/provence-alpes-cote-dazur/vente?locations_postcode%5B0%5D=FR_Provence-Alpes-C%C3%B4te%20d%27Azur)
    1. Scraping page France
    2. Tri date decroissante
    3. Achat & location
    4. Tout type de biens
22. [https://www.green-acres.fr/fr/prog_show_properties.html?searchQuery=order-date_d-lg-fr-cn-fr-city_id-rg_provence_alpes_cote_d_azur](https://www.green-acres.fr/fr/prog_show_properties.html?searchQuery=order-date_d-lg-fr-cn-fr-city_id-rg_provence_alpes_cote_d_azur)
    1. Scraping region par region
    2. Tri date recente
23. [https://www.arthurimmo.com/recherche,basic.htm?transactions=acheter&localization=Provence-Alpes-Côte d'Azur&sort=-updated_at](https://www.arthurimmo.com/recherche,basic.htm?transactions=acheter&localization=Provence-Alpes-C%C3%B4te%20d%27Azur&sort=-updated_at)
    1. Achat & location
    2. Tri Date de MAJ
    3. Scraping region par region
24. [https://www.sothebysrealty-france.com/fr/vente-proprietes-de-luxe/](https://www.sothebysrealty-france.com/fr/vente-proprietes-de-luxe/)
    1. Achat & location
    2. Scraping page France
    3. Tri nouveautées
25. [https://www.lesiteimmo.com/recherche?filter[type][0]=maison&filter[type][1]=appartement&filter[transaction]=acheter&filter[location]=Provence-Alpes-Côte d'Azur&sort=-created_at](https://www.lesiteimmo.com/recherche?filter%5Btype%5D%5B0%5D=maison&filter%5Btype%5D%5B1%5D=appartement&filter%5Btransaction%5D=acheter&filter%5Blocation%5D=Provence-Alpes-C%C3%B4te%20d%27Azur&sort=-created_at)
    1. Achat & location
    2. Scraping region par region
    3. Tri par plus recentes
26. [http://www.lesclesdumidi.com/index-click-trouver-fav-vente.html?token=e13d7914ec0ba1b30a779063a27dde085ea7f28c6bc98b18c60920dfd88f6d5d&floc=1&t=2&i=75100&vi=Paris&fcp=&ask=a&next=Suivant&next=Suivant&form_search_ville=Paris#floc=vente&t=2,1,5,3,8,6,7,10,11,12,13,14,4,9&i=83&fcp=83&tri=prix&tri2=desc](http://www.lesclesdumidi.com/index-click-trouver-fav-vente.html?token=e13d7914ec0ba1b30a779063a27dde085ea7f28c6bc98b18c60920dfd88f6d5d&floc=1&t=2&i=75100&vi=Paris&fcp=&ask=a&next=Suivant&next=Suivant&form_search_ville=Paris#floc=vente&t=2,1,5,3,8,6,7,10,11,12,13,14,4,9&i=83&fcp=83&tri=prix&tri2=desc)
    1. Achat ancien & location
    2. Scraping departement par departement 
    3. Tout type de bien
27. [https://www.lux-residence.com/fr/search?idtt=2&div=2246&m=homepage_new-redirection-search_results](https://www.lux-residence.com/fr/search?idtt=2&div=2246&m=homepage_new-redirection-search_results)
    1. Tout type de bien
    2. Tri par le plus récent
28. [https://fr.arkadia.com/vente/provence-alpes-cote-d-azur-g241095/?orderby=creation_date+desc](https://fr.arkadia.com/vente/provence-alpes-cote-d-azur-g241095/?orderby=creation_date+desc)
    1. Tri par date
    2. Scraping region par region
    3. Residentiel vente & location longue duree