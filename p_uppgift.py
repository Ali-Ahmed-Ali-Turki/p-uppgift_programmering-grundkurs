import random
import itertools



class Atom:
    """Representerar ett grundämne med dess viktigaste egenskaper såsom namn, beteckning,
    atomnummer, massa, period och grupp."""

    def __init__(self, beteckning, namn, atomnummer, massa, period, grupp):
        self.beteckning = beteckning
        self.namn = namn
        self.atomnummer = atomnummer
        self.massa = massa
        self.period = period
        self.grupp = grupp

class PeriodiskaSystemet:
    """Läser in och lagrar information om grundämnen från textfiler och erbjuder möjligheten
    att söka efter ett visst grundämne via namn eller beteckning."""

    def __init__(self, filnamn='avikt.txt', extra_filnamn='period_group.txt'):
        self.atomer=[]
        self.läs_in_data(filnamn, extra_filnamn)

    def läs_in_data(self, filnamn, extra_filnamn):
        """Läser in data från två textfiler och skapar Atom-objekt som lagras i listan atomer.
        Fil 1 innehåller allmän information och fil 2 innehåller period- och gruppdata."""

        with (open(filnamn, 'r', encoding="utf-8") as file1, 
            open(extra_filnamn, 'r', encoding="utf-8") as file2, 
            ):
            for rad1, rad2 in itertools.zip_longest(file1, file2, fillvalue=""):
                komma_till_pukt = str.maketrans(",", ".")
                rad1 = rad1.rstrip("\n")
                rad2 = rad2.rstrip("\n")
                en_atom = (rad1 + " " + rad2).split()
                if len(en_atom) >= 6:
                    atom = Atom(
                        beteckning=en_atom[0],
                        namn=en_atom[1],
                        atomnummer=int(en_atom[2]),
                        massa=float(en_atom[3].translate(komma_till_pukt)),
                        period=int(en_atom[4]),
                        grupp=int(en_atom[5])
                    )
                else:
                    atom = Atom(
                        beteckning=en_atom[0],
                        namn=en_atom[1],
                        atomnummer=int(en_atom[2]),
                        massa=float(en_atom[3].translate(komma_till_pukt)),
                        period=None,
                        grupp=None
                    )
                self.atomer.append(atom)


    def hitta_atom(self, sokterm):
        """Söker efter ett grundämne baserat på namn eller beteckning.
        Returnerar motsvarande Atom-objekt eller None om inget hittas."""

        for atom in self.atomer:
           if atom.beteckning.lower() == sokterm.lower() or atom.namn.lower() == sokterm.lower():
               return atom
        print("Den sökta atomen finns inte")
        return None

class Träning:
    """Hantera olika träningslägen och frågesporter baserade på information från det
    periodiska systemet."""

    def __init__(self, system):
        self.system = system

    def starta_träning(self, träningstyp):
        """Startar valt träningsläge och återvänder till menyn tills användaren avslutar."""

        while True:
            if träningstyp == 'atomlista':
                self.träna_på_alla_atomer()
                hitta_atom = input("Ange ett grundämne du vill vet mer om (namn eller beteckning): ").strip().lower()
                atom = self.system.hitta_atom(hitta_atom)
                if atom:
                    print(f"{atom.beteckning} | {atom.namn} | {atom.atomnummer} | {atom.massa} | {atom.period} | {atom.grupp}")
            elif träningstyp in ['atomnummer', 'beteckning', 'namn', 'massa']:
                self.frågor_om_atom_egenskaper(träningstyp)
            elif träningstyp == 'position':
                self.frågor_om_position()
            else:
                print("Ange en träningstyp")

            fortsätt = input("Vill du fortsätta spela (j/n): ").strip().lower()

            if fortsätt != "j":
                print("Avslutar träning")
                break

    def träna_på_alla_atomer(self):
        """Visar en fullständig lista över alla grundämnen sorterade efter atomnummer."""

        atomlist = sorted(self.system.atomer, key=lambda x: x.atomnummer)
        for atom in atomlist:
            print("------------------------------------------------")
            print(f"{atom.beteckning} | {atom.namn} | {atom.atomnummer} | {atom.massa} | {atom.period} | {atom.grupp}")
            print("------------------------------------------------")

    def frågor_om_atom_egenskaper(self, egenskap):
        """Ställer en fråga med tre svarsalternativ där användaren ska välja rätt atomnummer/beteckning/namn/massa."""

        atomlist = self.system.atomer.copy()
        aktuell_lista = random.sample(atomlist, 3)
        rätt_atom = random.choice(aktuell_lista)

        if egenskap == 'atomnummer':
            fråga = f"Vilket atomnummer har {rätt_atom.namn} ({rätt_atom.beteckning})?"
        elif egenskap == 'beteckning':
            fråga = f"Vilken beteckning har {rätt_atom.namn}?"
        elif egenskap == 'namn':
            fråga = f"Vilket namn har grundämnet med beteckningen {rätt_atom.beteckning}?"
        else:
            fråga = f"Vilen atommassa har {rätt_atom.namn} ({rätt_atom.beteckning})?"

        print("------------------------------------------")
        print(fråga)
        print("------------------------------------------")

        alternativ = [getattr(atom, egenskap) for atom in aktuell_lista]
        print(f"1. {alternativ[0]}   2. {alternativ[1]}   3. {alternativ[2]}")

        försök = 3
        for i in range(försök):
            svar = input("Ange svar (1-3): ")
            try:
                svar_index = int(svar) - 1
                if 0 <= svar_index <= 2:
                    if alternativ[svar_index] == getattr(rätt_atom, egenskap):
                        print("Rätt Svar")
                        return True
                    else:
                        print(f"Fel Svar.", end=" ")
                else:
                    print(f"Ange ett svar mellan 1 och 3.", end=" ")
            except:
                print(f"Ange en gltig input.", end=" ")
            försök_kvar = försök - (i + 1)
            if försök_kvar > 0:
                print("Försök igen!")
            else:
                print(f"Inga fler försök. Rätt svar är {getattr(rätt_atom, egenskap)}")
        return False


    def frågor_om_position(self):
        """Ställer en fråga där användaren ska avgöra period och grupp för ett givet grundämne."""

        atomlist = self.system.atomer.copy()
        atomlist_med_period_grupp = [atom for atom in atomlist if atom.period is not None and atom.grupp is not None]
        rätt_atom = random.choice(atomlist_med_period_grupp)
        rätt_period = rätt_atom.period
        rätt_grupp = rätt_atom.grupp
        print("------------------------------------------")
        print(f"Vilken period och grupp tillhör {rätt_atom.namn} ({rätt_atom.beteckning})")
        print("------------------------------------------")
        försök = 3
        for i in range(försök):
            svar_period = input("Ange period: ")
            svar_grupp = input("Ange grupp: ")
            try:
                svar_period_num = int(svar_period)
                svar_grupp_num = int(svar_grupp)
                if 1 <= svar_period_num <= 7 and 1 <= svar_grupp_num <= 18:
                    if svar_period_num == rätt_period and svar_grupp_num == rätt_grupp:
                        print("Rätt Svar")
                        return True
                    else:
                        print(f"Fel Svar.", end=" ")
                else:
                    print(f"Ange en period mellan 1 och 7 samt ange en grupp mellan 1 och 18.", end=" ")
            except:
                print(f"Ange en gltig input.", end=" ")
            försök_kvar = försök - (i + 1)
            if försök_kvar > 0:
                print("Försök igen!")
            else:
                print("Inga fler försök. Rätt svar är:")
                print(f"Period: {rätt_period}")
                print(f"Grupp: {rätt_grupp}")
        return False

class Meny:
    """Visar huvudmenyn och hanterar användarens val av träningsläge."""

    def __init__(self):
        self.p_s = PeriodiskaSystemet()
        self.träning = Träning(self.p_s)
        
    def visa_huvudmeny(self):
        """Visar huvudmenyn och anropar rätt träningsmetod baserat på användarens val."""

        while True:
            print("-----------------------------------")
            print("1. Visa alla atomer")
            print("2. Träna på atomnummer")
            print("3. Träna på atombeteckningar")
            print("4. Träna på atomnamn")
            print("5. Träna på atommassor")
            print("6. Träna på atompositioner")
            print("7. Avsluta")

            try:
                träningsläge = int(input("Ange ett träningsläge (1-6) eller avsluta: "))
                if träningsläge == 1:
                    self.träning.starta_träning("atomlista")
                elif träningsläge == 2:
                    self.träning.starta_träning("atomnummer")
                elif träningsläge == 3:
                    self.träning.starta_träning("beteckning")
                elif träningsläge == 4:
                    self.träning.starta_träning("namn")
                elif träningsläge == 5:
                    self.träning.starta_träning("massa")
                elif träningsläge == 6:
                    self.träning.starta_träning("position")
                elif träningsläge == 7:
                    break
                else:
                    print("Ange ett tal mellan 1 och 6")
            except ValueError:
                print("Ange ett tal!")

def main():
    """Startar programmet genom att skapa en meny och visa den för användaren."""

    meny = Meny()
    meny.visa_huvudmeny()

if __name__ == '__main__':
    main()