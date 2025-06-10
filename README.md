# Segurança

<h2>Mais simples:</h2>
Criar um arquivo que tenha o mac do usario autorizado, guardar o endereço mac em um arquivo de preferencia criptografado fora da pasta dos arquivos do programa, uma pasta que o usuario não vá mexer, provavelmnete uma que precise de permissão no windows. O app deve toda vez que iniciar puxar o id mac atual e comparar com o arquivo escondido, se for o mesmo mac cadastrado, libera, se não bloqueia a execução do app.

ou 

<h2>Mais seguro:</h2> https://www.youtube.com/results?search_query=server+block+by+mac <br>
ou fazer essa verificação com keys e id mac com um servidor? só que dai eu so poderia banir macs que estao sem licença só quando eu executasse o servidor na minha maquina, ai faria isso periodicamente, entao poderia piratear o app mas ia funcionar até o servidor verificar (cadastrar key publica):
Toda vez que o app abre (ou a cada X horas), ele faz uma requisição para o servidor.

O servidor responde se:

A licença está ativa.

O MAC está autorizado.

Se o MAC está banido.

Se a licença for inválida ou o MAC banido → app bloqueia.
Se licença for valida e MAC desconhecido → app bloqueia
