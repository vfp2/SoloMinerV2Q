export $(grep -v '^#' .env | xargs)
while :
do
    python3.11 SoloMinerV2.py
done
