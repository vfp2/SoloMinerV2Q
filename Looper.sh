export $(grep -v '^#' .env | xargs)
while :
do
    python3 SoloMinerV2.py
done
