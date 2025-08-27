# language: pt
Funcionalidade: Fluxo Completo de Compra no Sauce Demo
  Como um usuário do site Sauce Demo
  Eu quero realizar uma compra completa
  Para validar todo o processo de e-commerce

  Contexto:
    Dado que estou na página de login do Sauce Demo

  @fluxo_completo @usuario_valido
  Cenário: Fluxo completo de compra com usuário válido
    Quando faço login com usuário "standard_user" e senha "secret_sauce"
    E seleciono dois produtos aleatórios
    E adiciono os produtos ao carrinho
    E verifico que os produtos foram adicionados corretamente
    E navego para o carrinho
    E verifico o preço total dos produtos
    E clico em "Checkout"
    E preencho as informações de checkout
    E verifico o resumo da compra
    E confirmo a compra
    Então devo ver a mensagem de sucesso "Thank you for your order!"

  @login_bloqueado @usuario_bloqueado
  Cenário: Tentativa de login com usuário bloqueado
    Quando faço login com usuário "locked_out_user" e senha "secret_sauce"
    Então devo ver a mensagem de erro "Epic sadface: Sorry, this user has been locked out."

  @fluxo_completo @usuario_performance
  Cenário: Fluxo completo de compra com usuário de performance
    Quando faço login com usuário "performance_glitch_user" e senha "secret_sauce"
    E seleciono dois produtos aleatórios
    E adiciono os produtos ao carrinho
    E verifico que os produtos foram adicionados corretamente
    E navego para o carrinho
    E verifico o preço total dos produtos
    E clico em "Checkout"
    E preencho as informações de checkout
    E verifico o resumo da compra
    E confirmo a compra
    Então devo ver a mensagem de sucesso "Thank you for your order!"

  @validacao_produtos
  Cenário: Validação da seleção de produtos
    Quando faço login com usuário "standard_user" e senha "secret_sauce"
    E seleciono dois produtos aleatórios
    Então devo ver que exatamente dois produtos foram selecionados
    E os produtos devem ter preços válidos

  @validacao_carrinho
  Cenário: Validação do carrinho de compras
    Quando faço login com usuário "standard_user" e senha "secret_sauce"
    E seleciono dois produtos aleatórios
    E adiciono os produtos ao carrinho
    E navego para o carrinho
    Então devo ver os produtos corretos no carrinho
    E o preço total deve ser a soma dos produtos
    E a taxa de imposto deve ser calculada corretamente (8%)

  @validacao_checkout
  Cenário: Validação do processo de checkout
    Quando faço login com usuário "standard_user" e senha "secret_sauce"
    E seleciono dois produtos aleatórios
    E adiciono os produtos ao carrinho
    E navego para o carrinho
    E clico em "Checkout"
    E preencho as informações de checkout com:
      | Campo      | Valor    |
      | First Name | João     |
      | Last Name  | Silva    |
      | ZIP Code   | 12345-678|
    E clico em "Continue"
    Então devo ver o resumo da compra
    E os valores devem estar corretos
    E devo poder finalizar a compra
