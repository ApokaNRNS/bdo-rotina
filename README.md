Entendi perfeitamente! Você tem razão, a mensagem que o GitHub gerou no botão ficou estranha e repetitiva (algo como "Apoiar via-LivePix 00C853..."). O problema é que o formato do "badge" que eu passei estava interpretando os códigos de cor como texto.

Vou te passar o código corrigido. O link vai ficar limpo, apenas com o texto **"💙 Apoiar via LivePix"**, sem os códigos esquisitos.

### Para o README (Copie e cole isso)

Vá no seu `README.md` no GitHub, apague tudo e cole este texto:

```markdown
# 🗓️ BDO Rotina — by ApokaNRNS

![BDO Rotina](https://img.shields.io/badge/Black%20Desert%20Online-Ferramenta-blue?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Online-success?style=for-the-badge)
![Versão](https://img.shields.io/badge/Versão-v0.26.0-blueviolet?style=for-the-badge)

O **BDO Rotina** é uma ferramenta web independente criada para ajudar os aventureiros de **Black Desert Online (SA)** a organizarem suas rotinas diárias, semanais e acompanharem os próximos eventos do jogo em um só lugar.

🔗 **Acesse o site:** [https://apokanrns.github.io/bdo-rotina/](https://apokanrns.github.io/bdo-rotina/)

---

## ✨ Funcionalidades

O projeto foi dividido em abas para facilitar a sua vida no jogo:

*   **📊 Painel:** Acompanhe em tempo real o próximo Chefe Mundial, o ciclo de Dia e Noite, resets diários/semanais, Arena Solare, Guerras, Trono de Edana e manutenções.
*   **🗓️ Agenda Semanal:** Uma tabela completa de segunda a domingo com todos os eventos programados, incluindo a tabela de Dia e Noite.
*   **🎉 Eventos SA:** Linha do tempo visual com os avisos e eventos oficiais do Black Desert SA.
*   **✅ Rotinas:** Crie, edite e acompanhe suas tarefas diárias e semanais (ex: Abismo Imortal, Postos de Troca, etc). Seu progresso fica salvo no navegador!
*   **⚙️ Configurações:** Totalmente personalizável. Mude o tema (Escuro, Violeta, Verde, Claro), formato do relógio (12h/24h), configure os horários dos chefes, avisos sonoros e voz (TTS).
*   **ℹ️ Sobre:** Conheça mais sobre o criador e os projetos da comunidade.

---

## 🚀 Como usar

Como é um site estático (HTML, CSS e JavaScript), não é necessário instalar nada. Basta acessar o link do GitHub Pages.

Se você quiser rodar o projeto localmente na sua máquina:
1. Faça o clone do repositório:
   ```bash
   git clone https://github.com/ApokaNRNS/bdo-rotina.git
   ```
2. Abra o arquivo `index.html` no seu navegador.

*(Nota: Devido às políticas de segurança do navegador (CORS), alguns recursos podem não carregar corretamente ao abrir o arquivo diretamente via `file://`. Recomenda-se usar uma extensão como "Live Server" no VS Code).*

---

## 🛠️ Tecnologias Utilizadas

Este projeto foi construído do zero, sem o uso de frameworks pesados, focado em performance e design:
*   **HTML5** (Estrutura semântica)
*   **CSS3** (Variáveis, Grid, Flexbox, Animações, Temas dinâmicos)
*   **JavaScript (Vanilla)** (Lógica de tempo real, salvamento em `localStorage`, manipulação de DOM)
*   **Google Fonts** (Inter e JetBrains Mono)

---

## ⚠️ Avisos Importantes

*   **Dados Locais:** Suas rotinas, configurações e registros de missão são salvos localmente no seu navegador (`localStorage`). Limpar o cache do navegador pode apagar seus dados (use a função de Backup na aba de configurações para salvar).
*   **Eventos SA:** A lista de eventos utiliza um "snapshot" (captura) das notícias oficiais para garantir que o site funcione de forma independente e rápida. Novos eventos podem ser adicionados manualmente conforme forem anunciados.
*   **Ferramenta Independente:** Este é um projeto de fã para fã. Não possui vínculo oficial com a Pearl Abyss ou o Black Desert Online.

---

## 👨‍💻 Autor

**ApokaNRNS**
*   Criador de conteúdo e streamer.
*   [Twitch](https://www.twitch.tv/apokanrns)
*   [YouTube](https://www.youtube.com/@apokanrns)
*   [Instagram](https://www.instagram.com/apokanrns/)
*   [X (Twitter)](https://x.com/apokanrns)

---

## 💙 Apoie o Projeto

Este site é feito de fã para fã e é totalmente gratuito! Se ele te ajuda no seu dia a dia no Black Desert e você quiser dar uma força para o criador, você pode enviar qualquer valor via LivePix. Sua contribuição ajuda a manter o projeto no ar e incentiva a criação de novas ferramentas!

👉 **[Clique aqui para apoiar via LivePix](https://livepix.gg/apokanrns)** 👈

---

## 📄 Licença

Este projeto é de código aberto e está disponível para a comunidade. Sinta-se livre para estudar o código, adaptar para o seu uso pessoal ou sugerir melhorias através de *Issues* e *Pull Requests*.

Feito com 💙 para a comunidade de Black Desert SA.
```

Agora o link vai aparecer como um texto normal e bonito, sem os códigos malucos!
