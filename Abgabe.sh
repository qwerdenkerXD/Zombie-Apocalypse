. ~/.bash_aliases
filename="SYBI_SS23_Sill"
if [ -f $filename.zip ]; then rm $filename.zip; fi
md tmp

# Report
md tmp/Report
cp Hausarbeit.pdf tmp/Report/$filename.pdf

# Methoden
md tmp/Methoden
cp simulation.py tmp/Methoden
cp -r Zuelpich tmp/Methoden
# cp -r Hausarbeit tmp/Methoden

# Results
cp -r Results tmp

# README
md tmp/README
echo "
Name: Franz-Eric Sill
Matrikelnummer: 2139315

Diese Entwicklung dieser Arbeit wurde mit git versioniert und ist auf folgendem Repository verfügbar:
https://github.com/qwerdenkerXD/Zombie-Apocalypse

Zum Reproduzieren der erzeugten Ergebnisse, müssen im Terminal eines Linux-Systems im Methoden-Ordner
folgende Befehle ausgeführt werden, wobei für python das Modul 'matplotlib' installiert sein muss (via pip):

mkdir Results  # in Windows: md Results
python3 simulation.py

Die Ergebnisse sind folglich im erstellten Results-Ordner.
Für die Simulation wird zur Reproduzierbarkeit ein Random-Seed verwendet (in simulation.py via random.seed(1)).
Dementsprechend ist dieselbe Python-Version empfohlen.

Folgende Versionen wurden verwendet:

bash 5.0.17
python3 3.8.10
pip 20.0.2
matplotlib 3.5.2
git 2.25.1
texlive-full 2019.20200218-1
pdfTeX 3.14159265-2.6-1.40.20
biber 2.14
mkdir 8.30
zip 3.0
mv 8.30
rm 8.30
Ubuntu 20.04.6 LTS
Kernel: Linux 5.15.90.1-microsoft-standard-WSL2
"> tmp/README/Readme.txt

# zip
cd tmp
zip -r -m -q ../$filename.zip *
cd ..
rm -r tmp