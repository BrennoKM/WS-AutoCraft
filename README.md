# Warspear-AutoCraft

Esse projeto foi desenvolvido para uso pessoal em um jogo online chamado Warspear, meu objetivo primário foi alcançado e atualizações aqui não estão planejadas. Porém 
minha meta inicialmente era fazer com que o programa funcionasse em segundo plano, mas devido a limitações da biblioteca isso só é possível com ajuda do RDP Wrapper.

No futuro pretendo desenvolver a mesma aplicação com o uso de engenharia reversa, a ideia é obter informações direto da memória e enviar inputs direto pra janela do jogo com a biblioteca Ctypes, 
assim se livrando da dependência de ler capturas de tela e consequentemente tornando o bot mais eficiente e leve computacionalmente.

Minha ideia em deixar esse projeto público é atiçar ideias na mente de quem por ventura chegue aqui. Caso você tenha interesse em colaborar comigo ou possua dúvidas do funcionamento,
entre em contato pelo meu **discord Kobernn**.

## Qual o objetivo da aplicação?
 - Automatizar o processo de artesanato.
 - Manter essa automação em execução por tempo inderteminado.
 - Tornar tudo configuravel pra diferentes resoluções de tela.
 - Controlar remotamente a aplicação por meio da API do Telegram

## Como foi desenvolvido?
 - Utilizei a biblioteca PyAutoGui do Python para desenvolver meu projeto como principal meio de automatizar os processos.
 - Integração com API do Telegram para monitorar e enviar comandos remotamente.

## Como funciona?
O usuário deve configurar a aplicação para sua resolução de tela e salvar capturas de tela individuais dos itens que ele deseja vender. Quando tudo estiver pronto, basta preparar o jogo na tela inicial e iniciar
o programa para que os itens pre-definidos sejam feitos automaticamente e repostos conforme a demanda.

## Recursos disponíveis
 - CRUD de itens que podem ser craftados.
 - CRUD das configurações.
 - Mais de um ppersonagem pode ser usado para craftar
 - Controle remoto via TelegramBot
 - Atalhos de teclado (com botão de liga/desliga na interface).

## Como usar
- ### Atalhos
  - **'Esc'** - O bot será interrompido forçadamente.
  - **'L'** - O bot será pausado caso esteja rodando.
  - **'K'** - O bot será iniciado.
  - **'Ctrl_r'** - Ativa/desativa os atalhos.
- ### Atalhos especiais
  - **'D'** - Marca um ponto na tela e printa a posição do mouse
  - **'F'** - Faz um print com os dois ultimos pontos e salva na raiz
  - **'G'** - Verifica se o print tirado está na tela e move o mouse até lá


## Visão Geral

