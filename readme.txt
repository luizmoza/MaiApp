TESTE


vps51404 IP: 191.252.202.109 Máscara de rede: 255.255.255.0 Gateway: 191.252.202.1
root
senha: XP15
IP da VPS


########### Comandos linux ############

pwd --> onde estour
ls --> listar o que tem onde estou
cd --> change directory
cd .. --> sobe pro pai
clear --> limpa prompt
Mkdir ---> make directory
touch ---> cria arquivo
cat ---> cata e lê arquivo
echo >> --> append no arquivo
echo > --> escreve sobescrevendo
rm --> remove file
mv --> move file
rmdir --> remove diretório
cp --> copia arquivo
cp *.txt 'pasta' --> copia todos os txts para uma pasta
-- help --> documentação do comando
zip --> autoexplicativo
unzip -->autoexplicativo

-r ----aplicar o comando recursivamente para todos os elementos do cojunto/pasta

salvar como .sh --> salvar como um script executável tipo .bat
bash script.sh --> executar script sem permissionamento

echo $PATH
export PATH=$PATH:/home/yo --> aciona /home/yo na variável de ambiente PATH para poder rodar .sh sem precisar entrar na pasta antes

sudo apt-get install [pacote] ---> usa permissionamento mais alto para catar um pacote e instalar


########### Comandos docker ############


Container é a instancia da imagem armazenada em ram (não persiste dados)
imagem é um kernel(sistema operacional/python/node) capaz de executar comandos


docker ps --> lista containers em execução
docker ps -a --> lista containers disponiveis já executados

docker run [container] [comando]
 ---> exemplo de comando --> "ubunto" "sleep 1d"
 ---> todo container tem um comando default

docker start [id]
docker stop [id]  --> tirar e botar da ps,ps -a
docker pause [id]
docker unpause [id]  --> tirar e botar da ps,ps -a sem resetar o timer
docker rm [id] --> deleta container

docker port[id] --> lista o mapeamento de ports do container


docker exec -it [id] bash --> da um comando para um container que já está em execução de forma iterativa
docker exec [id] bash --> da um comando para um container que já está em execução 

-->>> Vou usar ---> docker run -d -p [porta maquina]:[porta container] [imagem] [comando]
--> mantem o terminal destravado, seta a porta e baixa a imagem se precisar e executa o comando (talvez não precise executar o comando pq no meu caso o comando é dar start ao servidor)






 




