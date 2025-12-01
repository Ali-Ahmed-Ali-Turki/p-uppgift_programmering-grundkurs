# Specifikation
## Inledning
Projektet är en grafiskt-baserad inlärningsapplikation för studenter eller kemi-intresserade med funktionerna "visa alla atomer", "träna på atomnummer", "träna på atombeteckningar", "träna på atomnamn", "träna på atommassor" och "träna på atompositioner". Programmet startas från terminalen och öppnar sedan ett grafiskt användargränssnitt. Användaren presenteras med en meny där de kan komma åt den förutnämnda funktionalitet eller avsluta. Funktionerna hjälper användaren att memorera [periodiska systemet](https://en.wikipedia.org/wiki/Periodic_table) och grundämnenas egenskaper med hjälp av flervalsfrågor och [öppna frågor](https://en.wikipedia.org/wiki/Open-ended\_question). 

Bland utmaningarna är att göra applikationen tillräckligt slumpmässig (oförutsägbar) vilket är viktigt för att förhindra fusk och främja verklig inlärning. Utöver det kan funktionen "träna på atomposition" vara knepig (speciellt grafiskt) på grund av periodiska systemets oregelbundna utseende.
## Användarscenarier
### Träna flervalsfrågor
Skotte har ett kommande kemiprov men har svårt att komma ihåg olika grundämnen och deras egenskaper. Han öppnar inlärningsapplikationen och väljer "träna på atomnummer" i huvudmenyn. "Vilket atomnummer har jod?" frågas Skotte som nu väljer ett av tre svarsalternativ. "Fel svar, försök igen!" utmanas Skotte och det gör han genom att ännu en gång välja ett av tre svarsalternativ. Efter tre misslyckade försök får Skotte, tyvärr, inte flera försök och det rätta svaret visas: "53". Skotte avslutar funktionen och återvänder till huvudmenyn. Skotte testar funktionerna "träna på atombeteckningar", "träna på atomnamn" och "träna på atommassor" som alla fungerar på exakt samma sätt som "träna på atomnummer". När han är klar för dagen väljer han "avsluta" i huvudmenyn.
### Träna öppna frågor
Skottes lillebror, Neutron, är ett barngeni och vill visa Skotte att han har memorerat positionen på varje grundämne i det periodiska systemet. Neutron öppnar inlärningsapplikationen och väljer "träna på atompositioner" i huvudmenyn. "Ange vilken period och grupp atomen tillhör" uppmanas Nuetron och visas (slumpartat) "Helium". Nuetron matar in "1" respektive "18" i textlådorna under "Period" och "Grupp". "Rätt svar!" gratuleras Neutron som nu visas nästa atom samtidigt som det toma periodiska systemet fylls med "He" i den korrekta positionen. Efter att ha placerat klart atomerna väljer Nuetron "avsluta" och återvänder till huvudmenyn. 
### Självstudier med lista
Skotte blir avundsjuk på Neutrons vida kunskaper och bestämmer sig för att plugga lite i hopp om att en dag kunna slå lillebrosan på detta spel. Skotte öppnar inlärningapplikationen och väljer "visa alla atomer" i huvudmenyn. Skotte får se en lista på alla atomer i periodiska systemet och deras egenskaper. Skotte sitter resten av kvällen och studerar mödosamt materialet.
## Kodskelett
```
class Atom:
    """Representerar ett grundämne i det periodiska systemet."""

    def __init__(self, atomnummer, namn, beteckning, massa, period, grupp):
        """
        Skapar ett Atom-objekt med följande attribut:
        atomnummer: (int) Atomens atomnummer.
        namn: (str) Atomens namn, t.ex. "Väte".
        beteckning: (str) Atomens kemiska symbol, t.ex. "H".
        massa: (float) Atomens atommassa.
        period: (int) Perioden (rad) i periodiska systemet.
        grupp: (int) Gruppen (kolumn) i periodiska systemet.
        """

class PeriodiskaSystemet:
    """Hanterar alla grundämnen och funktioner för träning och visning."""

    def __init__(self, databasfil="avikt.txt"):
        """
        Läser in alla atomer från en fil och lagrar dem i en lista.
        databasfil: (str) Filnamn som innehåller atomdata.
        """

    def läs_in_data(self, filnamn):
        """
        Läser in atomdata från txt-fil och returnerar en lista av Atom-objekt.
        Attribut, filnamn: (str) Filnamn med atomdata.
        Returnerar lista med Atom-objekt.
        """
        pass

    def hitta_atom(self, sokterm):
        """
        Söker efter en atom baserat på namn eller beteckning.
        Attribut, sokterm: (str) Namn eller beteckning.
        Returnerar matchande atom eller None om ej hittad.
        """
        pass

    def slumpa_atom(self):
        """
        Returnerar en slumpmässigt vald atom ur listan.
        """
        pass

    def visa_alla_atomer(self):
        """
        Skriver ut alla atomer i tabellform till terminalen.
        """
        pass


class Traning:
    """Hantera olika träningslägen för att öva på atomers egenskaper."""

    def __init__(self, system):
        """
        Skapar en träningssession kopplad till ett PeriodiskaSystemet-objekt.
        Attribut, system: (PeriodiskaSystemet) Det periodiska systemet som används.
        """

    def starta_traning(self, typ):
        """
        Startar vald träningsfunktion.
        Attribut, (str) typ: 'nummer', 'namn', 'beteckning', 'massa', 'position'
        """
        pass

    def fragor_om_atomnummer(self):
        """
        Ställer frågor där användaren gissar atomnummer utifrån namn.
        """
        pass

    def fragor_om_namn(self):
        """
        Ställer frågor där användaren gissar namn utifrån atomnummer eller beteckning.
        """
        pass

    def fragor_om_position(self):
        """
        Ställer frågor där användaren gissar period och grupp.
        """
        pass


class Meny:
    """Hanterar användarinteraktion via terminalen."""

    def __init__(self):
        """
        Skapar en huvudmeny för användaren och kopplar till PeriodiskaSystemet.
        """

    def visa_huvudmeny(self):
        """
        Visar huvudmenyn med alternativ för användaren.
        """
        pass

    def start(self):
        """
        Startar programloopen tills användaren väljer att avsluta.
        """
        pass
```
## Minnet
När programmet startar läses alla grundämnen in från en textfil och lagras i arbetsminnet som en lista av `Atom`-objekt. Varje objekt innehåller atomnummer, namn, beteckning, massa, period och grupp. Denna lista ligger i klassen `PeriodiskaSystemet` och fungerar som programmets centrala databas under hela körningen.

Övriga delar av programmet, som träningsfunktionerna och huvudmenyn, arbetar genom att referera till denna lista. De skapar inga egna kopior, utan använder samma data i minnet. Under träningsmomenten skapas endast tillfälliga variabler (t.ex. slumpad atom, användarens svar och antal försök), och dessa finns bara så länge frågan pågår.

Ingen data förändras permanent i minnet och ingenting skrivs automatiskt tillbaka till fil. Filen används endast vid start (för att läsa in alla atomer) och eventuellt vid utskrift när användaren vill visa listor eller resultat.