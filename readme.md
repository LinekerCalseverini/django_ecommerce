## Sobre o Projeto
Este projeto foi desenvolvido durante o curso de Python do Luiz Otávio Miranda,
na Udemy. O projeto conta com alguns aprimoramentos de minha autoria, como o
seletor de variações mudar automaticamente dependendo dos query params na URL.

Outra mudança é como o carrinho é salvo na sessão. Ele salva apenas ids e
quantidades em um simples dicionário, e quando é necessário renderizá-lo, ele
passa por uma função que executa as queries e traz os dados do carrinho por
completo. A ideia é não ter duplicação de dados em um banco relacional.

Outra mudança é a paginação, que agora considera se a chave "termo" está dentro
dos query params ou não.

No geral, foi um excelente aprendizado.