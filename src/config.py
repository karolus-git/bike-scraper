WAIT_TIME_S = 60*5

PARSER = "bs"

MONGO_HOST = "0.0.0.0"
MONGO_PORT = 27017
MONGO_DATABASE = "bikes"
MONGO_TABLE = "scraper"
MONGO_USER = "root"
MONGO_PWD = "example"

FMT_DATETIME = "%Y-%m-%d %H:%M"
FOLDER_DATA = "./data"

SCRAP_DICT = {
    "Ghost Fire RoadRage" : {
        "url" : "https://www.probikeshop.fr/velo-de-gravel-ghost-fire-road-rage-advance-sram-apex-36-dents-gris-2021/238675.html",
        "size" : None,
    },
    "Bombtrack Munroe SG": {
        "url" : "https://www.alltricks.fr/F-41505-velos-route-_-cyclocross-_-triathlon/P-2031852-gravel_bike_bombtrack_munroe_sg_microshift_9v_650b_noir_gloss_2022",
        "size" : "M",
    },
    "Vitus Substance V2" : {
        "url" : "https://www.chainreactioncycles.com/fr/fr/vitus-substance-v-2-fb-gravel-bike-sora-2022/rp-prod206118",
        "size" : None,
    },
    "GRVL 520 Subcompact" : {
        "url" : "https://www.decathlon.fr/p/velo-gravel-triban-grvl-520-homme-subcompact/_/R-p-313015?mc=8587697",
        "size" : "S",
    },
    "Marin Lombard 2" : {
        "url" : "https://www.bmxavenue.com/velos-gravel/gravels/velo-gravel-marin-lombard-2.html",
        "size" : "54 -",
    },
    "Genesis Fugio 10" : {
        "url" : "https://www.cyclable.com/16762-velo-gravel-genesis-fugio-10.html",
        "size" : "xl",
    },
    "Orbea terra h40" : {
        "url" : "https://www.culturevelo.com/shop/Produits/Fiche?from=ffrech&produit=290366&query=",
        "size" : "xl",
    },
 }