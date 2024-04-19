# molika
Petit projet assistant domestique

l'assistant est sur un conteneur docker et on le resquest depuis un client qui fait juste l'echange
docker pull oxydable/molika

ce client qui fait juste l'échange se connecte en ssh au conteneur et lui envoie simplement les entré dans mon cas j'utilise plustot du powershell
et peut etre que a terme j'utiliserais du python pour lire les message et répondre avec par la voie 

je suis pas encore au point avec tout les conteneur, donc il y a un /molika/script.sh a lancé au démarrage du conteneur qui recrée les fichier neccesaire si il n'existe pas

exemple de docker run

docker run -d --name molika --rm -v /Molika/docker/log:/molika/log -v /Molika/docker/config:/molika/config -p 22:22 oxydable/molika

