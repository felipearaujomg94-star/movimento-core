# 📋 Progresso — Movimento Convívio Tabor (movimento-core)

> Arquivo de controle pessoal. Não precisa ir pro GitHub público (pode 
> adicionar no .gitignore se quiser manter só local).

---

## 🎯 Objetivo geral
Entrar na área de tecnologia o mais rápido possível → evoluir até 
Arquiteto AWS → home office, remuneração em dólar no longo prazo.

## 🚧 Situação financeira
Pressão real, já é um problema hoje. Preciso equilibrar estudo profundo 
com candidaturas em paralelo desde já (não esperar "estar pronto").

---

## ✅ HISTÓRICO — o que já foi feito

### [31/07/2026] — Dia 1: correções do projeto (feedback do Jules)
- ✅ Segurança: `SECRET_KEY` e `DEBUG` movidos para `.env`, chave nova 
  gerada (a antiga estava exposta no commit inicial, foi neutralizada), 
  `.env` protegido no `.gitignore`
- ✅ Instalado e configurado `python-dotenv`
- ✅ Limpeza de duplicações em `institucional/urls.py` e `views.py` 
  (arquivos tinham código repetido de commits antigos)
- ✅ Testado: rotas `/`, `/sobre/`, `/eventos/` retornando status 200
- ✅ Confirmado: `admin.py` de `usuarios` e `institucional` já estavam 
  registrados corretamente (versões avançadas, com `UserAdmin` 
  customizado e `list_display`/filtros)
- ✅ Senha do superusuário `admin` resetada e login testado no `/admin`
- ✅ `README.md` criado e publicado (documentação do projeto)
- ✅ `requirements.txt` gerado (`pip freeze`)
- ✅ Tudo commitado e no GitHub

**Aprendizado do dia:** enfrentei vários erros reais (caractere especial 
na chave, dotenv não instalado, import dentro de docstring, servidor 
caindo, senha esquecida) e não desisti de nenhum. Prova concreta contra 
o padrão de abandono por impaciência.

---

## 🔲 PENDENTE — próximos passos

- [ ] Reforço direcionado de Python/Django (focado no que já uso no 
      projeto, não teoria solta)
- [ ] Iniciar bloco de candidaturas (estágio / suporte técnico / freela) 
      — meta: não esperar "estar pronto"
- [ ] Estudar e fazer deploy do projeto (Render/Railway/EC2 free tier) 
      — primeiro contato prático com Cloud
- [ ] Definir rotina fixa de bloco de candidaturas (sugestão: 
      quinta + domingo)
- [ ] Revisar tempo em redes sociais (média atual: 5h/dia — separar 
      busca ativa de scroll passivo)

---

## 📅 Rotina de estudo (referência)
- Seg/Ter/Qua/Sex: 19h30–22h
- Qui: janela curta (pós-futebol) ou manhã
- Sáb: 2-3h (fora compromissos da pastoral)
- Dom: 1-2h — candidaturas + planejamento da semana

---

## 🗒️ Notas rápidas (vá anotando aqui a cada sessão)
[espaço livre pra você anotar dúvidas, ideias, o que travou, etc.]