# Dashboard Seguros - Versão Web

Aplicação web para geração de dashboards de comissões e produções de seguros.
**Roda 100% no navegador** - não precisa de servidor backend!

## 🌐 Acesse Online

Você pode usar imediatamente em:
- **GitHub Pages**: Suba o `index.html` e acesse `https://seuusuario.github.io/repositorio`
- **Vercel**: Arraste a pasta para vercel.com
- **Netlify**: Arraste a pasta para app.netlify.com/drop
- **Qualquer servidor web**: Apache, Nginx, etc.

## 📁 Estrutura para Deploy

```
dashboard-seguros-web/
├── index.html          # ← Único arquivo necessário!
└── README.md           # Este arquivo
```

**Sim, é só 1 arquivo!** Tudo (HTML, CSS, JavaScript, bibliotecas) está embutido.

## 🚀 Deploy Rápido

### Opção 1: GitHub Pages (Grátis)
1. Crie um repositório no GitHub
2. Faça upload do `index.html`
3. Vá em Settings > Pages
4. Selecione branch "main" e pasta "/ (root)"
5. Acesse o link gerado (ex: `https://seunome.github.io/dashboard-seguros`)

### Opção 2: Vercel (Grátis)
1. Acesse [vercel.com](https://vercel.com)
2. Login com GitHub
3. New Project > Import Git Repository
4. Selecione seu repo com o index.html
5. Deploy automático!

### Opção 3: Netlify Drop (Grátis, mais rápido)
1. Acesse [app.netlify.com/drop](https://app.netlify.com/drop)
2. Arraste a pasta com index.html
3. Pronto! URL gerada instantaneamente

## 📊 Como Usar

1. **Acesse** a URL do seu deploy
2. **Faça upload** do arquivo de Comissões (Excel .xlsx ou .xls)
3. **Faça upload** do arquivo de Produções (Excel .xlsx ou .xls)
4. **Clique** em "Gerar Dashboards"
5. **Aguarde** o processamento (1-2 segundos)
6. **Baixe** as imagens PNG dos dashboards

## 📋 Formatos Suportados

### Arquivo de Comissões
- Extensões: `.xlsx`, `.xls`
- Estrutura esperada: Aba com dados de gerentes, porcentagens e valores
- O sistema detecta automaticamente o formato

### Arquivo de Produções
- Extensões: `.xlsx`, `.xls`
- Estrutura esperada: Múltiplas abas com datas (ex: "25março", "01abril")
- Cada registro: Produto, Gerente, Cliente, Proposta, Valor

## 🔒 Privacidade

**Seus dados NÃO saem do seu computador!**
- O processamento é feito 100% no navegador (client-side)
- Nenhum dado é enviado para servidores
- Os arquivos Excel não são armazenados em lugar nenhum
- Ideal para dados sensíveis da empresa

## 🛠️ Tecnologias

- **SheetJS**: Leitura de arquivos Excel no navegador
- **html2canvas**: Geração de imagens PNG
- **Vanilla JavaScript**: Sem frameworks pesados
- **CSS3**: Layout responsivo e moderno

## 💾 Salvamento Local

Se preferir usar localmente sem internet:
1. Baixe o arquivo `index.html`
2. Dê duplo clique para abrir no navegador
3. Funciona offline!

**Nota**: A primeira vez precisa de internet para baixar as bibliotecas (CDN). Depois fica em cache.

## 🐛 Solução de Problemas

### "Não consigo fazer upload"
- Verifique se o arquivo é .xlsx ou .xls
- Tente arrastar o arquivo em vez de clicar

### "Dashboard não gera"
- Verifique se os arquivos têm os nomes esperados
- Abra o console do navegador (F12) para ver erros

### "Imagem não baixa"
- Verifique se o navegador permite downloads
- Desative bloqueadores de popup

## 📱 Compatibilidade

- ✅ Chrome/Edge (recomendado)
- ✅ Firefox
- ✅ Safari
- ✅ Opera
- ✅ Chrome Mobile (Android)
- ✅ Safari Mobile (iOS)

## 🔄 Atualizações

Para atualizar, simplesmente substitua o arquivo `index.html` no seu servidor.

---

**Desenvolvido para**: Automação de relatórios de seguros  
**Versão**: 2.0 Web  
**Data**: 2024
