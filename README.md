Kurssin _Tietokantasovellus_ harjoitustyö  
Päivitetty 5.2.2022

## Verkkokauppasovellus

Sovellus on yksinkertainen simulaatio verkkokaupasta. Sovelluksessa on julkinen osio sekä admin-osio tuotteiden ja tilausten käsittelyä varten.

Sovelluksen tuotannossa olevaa versiota pääset testaamaan täältä https://verkkokauppasovellus.herokuapp.com/  

Sovelluksessa voi luoda käyttäjäprofiilin, josta voi tehdä halutessaan ylläpitäjän, jolloin kirjautuminen ohjataan palvelun admin-osioon https://verkkokauppasovellus.herokuapp.com/admin

### Välipalautus 2

Sovelluksen perustoiminnallisuudet on pitkälti tuotannossa. Alla listattuna sovelluksen ominaisuuksia:

Sovellus:
- Verkkokaupalla on julkinen etusivu, josta löytyy listaus myytävistä tuotteista. Lisäksi linkki sisäänkirjautumista tai käyttäjätunnuksen luomista varten.
- Myytäviä tuotteita klikkaamalla avautuu erillinen näkymä, josta löytyy tuotteen tarkemmat tiedot
- Kirjautunut käyttäjä:
    - Voi lisätä tuotteita ostoskoriin tuotenäkymästä
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

#### Jatkokehitys

Palautteesta riippuen seuraavia asioita on vielä tarkoitus työstää:
- Koodin huolto (pylint)
- Laadunvarmistusta (esim. syötteiden validaatiot)
- UI:n viimeistelyä (CSS)
- Muita palautteessa annettuja huomioita
- Dokumentaatio

Mahdolliset lisäfeaturet:
- Käyttäjät voivat antaa arvosteluja tuotteille (uusi tietokantataulu)
- Alennuskampanjat (+ tuotekategoriat)
- Tehtyjen tilausten sisällön selausta
