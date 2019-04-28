mkdir plots
mkdir generated_datasets
cd origional_datasets
wget https://raw.githubusercontent.com/coatless/stat490uiuc/master/airlines/airlines_data.sh
chmod u+x airlines_data.sh
./airlines_data.sh 1998 1998
mv airlines.csv airlines98.csv
./airlines_data.sh 2006 2006
mv airlines.csv airlines06.csv