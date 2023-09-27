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
...
"> tmp/README/Readme.txt

# zip
cd tmp
zip -r -m -q ../$filename.zip *
cd ..
rm -r tmp