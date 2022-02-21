Kurssin _Tietokantasovellus_ harjoitustyö  
Päivitetty 16.2.2022


## Verkkokauppasovellus

Sovellus on yksinkertainen simulaatio verkkokaupasta. Sovelluksessa on julkinen osio sekä admin-osio tuotteiden ja tilausten käsittelyä varten.

Sovelluksen tuotannossa olevaa versiota pääset testaamaan täältä https://verkkokauppasovellus.herokuapp.com/  

Sovelluksessa voi luoda käyttäjäprofiilin, josta voi tehdä halutessaan ylläpitäjän, jolloin kirjautuminen ohjataan palvelun admin-osioon https://verkkokauppasovellus.herokuapp.com/admin

### Ominaisuudet

Sovellus:
- Verkkokaupalla on julkinen etusivu, josta löytyy listaus myytävistä tuotteista. Lisäksi linkki sisäänkirjautumista tai käyttäjätunnuksen luomista varten.
- Myytäviä tuotteita klikkaamalla avautuu erillinen näkymä, josta löytyy tuotteen tarkemmat tiedot
- Kirjautunut käyttäjä:
    - Voi lisätä tuotteita ostoskoriin tuotenäkymästä
    - Voi lisätä tuotteelle arvostelun
    - Voi poistaa tuotteita ostoskorista
    - Ostoskorin kautta pääsee tilauksen vahvistukseen
    - Ostoskori-näkymässä näkee tehdyt tilaukset
    - Kaikissa näkymissä uloskirjautuminen
 
Admin:
- Jos kirjautumisnäkymässä rooliksi valitsee ylläpitäjän, ohjataan käyttäjä admin-osioon
- Ylläpitäjä voi luoda uuden tuotteen verkkokauppaan myytäväksi
- Ylläpitäjä voi muokata myytäviä tuotteita
- Tuotteita voi poistaa tai palauttaa takaisin valikoimaan (ns. soft delete)
- Ylläpitäjä voi merkitä tehtyjä tilauksia toimitetuksi
- Kaikissa näkymissä uloskirjautuminen

### Välipalautus 3

Sovelluksen pitäisi olla kutakuinkin valmis, eli tarkoituksena on enää viilata palautteessa esille tulevia seikkoja.

### Dokumentaatio

Tietokantaa kuvattu päällisin puolin [arkkitehtuurikuvauksessa](/documentation/architecture.md).
