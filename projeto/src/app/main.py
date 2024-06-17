import sys
sys.path.append('/mnt/o/finance_4_python/projeto/src/ingestao')
import streamlit as st
from crawler.crawler import Crawler
import time


st.title("Finance with Python")
st.markdown( 
    ''' 
# 📈 Projeto de Aplicativo de Simulação de Ações 📊

## Visão Geral do Projeto 🌐

Bem-vindo ao nosso projeto inovador! Desenvolvemos um aplicativo que permite visualizar e simular suas ações de forma prática e intuitiva. Este aplicativo não só ajuda você a monitorar suas ações, mas também permite realizar web scraping para obter dados de ações de qualquer país do mundo, incluindo fundos imobiliários.

## Funcionalidades Principais 🚀

### 🌍 Ações de Qualquer País
Nosso aplicativo fornece dados de ações de qualquer país do mundo. Com essa funcionalidade, você pode acompanhar o desempenho de empresas globais e tomar decisões informadas sobre investimentos internacionais.

### 🏢 Fundos Imobiliários
Além das ações, nosso app também traz informações detalhadas sobre fundos imobiliários, oferecendo uma visão completa do mercado de investimentos.

### 🔄 Simulação de Ações
Uma das principais características do nosso aplicativo é a capacidade de simular compras e vendas de ações. Isso permite que você teste diferentes estratégias de investimento sem correr riscos financeiros.

### 🖥️ Web Scraping de Ações
Utilizando técnicas avançadas de web scraping, nosso aplicativo coleta dados atualizados de ações de várias fontes confiáveis na internet. Isso garante que você sempre tenha acesso às informações mais recentes.

## Benefícios do Aplicativo 🎯

- **Tomada de Decisão Informada**: Com acesso a dados de ações globais e fundos imobiliários, você pode tomar decisões de investimento mais informadas.
- **Simulação Segura**: Teste suas estratégias de investimento em um ambiente seguro e sem riscos.
- **Atualizações em Tempo Real**: Nosso web scraping garante que os dados estejam sempre atualizados, fornecendo informações precisas e em tempo real.
- **Interface Intuitiva**: Desenvolvemos uma interface amigável e fácil de usar, para que você possa se concentrar em suas estratégias de investimento.

## Como Funciona 🔍

1. **Cadastro e Login**: Crie sua conta e faça login no aplicativo.
2. **Escolha seu Mercado**: Selecione os países e mercados que deseja acompanhar.
3. **Simulação de Investimentos**: Utilize a funcionalidade de simulação para testar diferentes estratégias.
4. **Acompanhamento de Ações**: Monitore suas ações e fundos imobiliários favoritos em tempo real.

**Nota:** Este projeto está em desenvolvimento contínuo. Sua opinião é essencial para nós! Não hesite em entrar em contato para sugestões e melhorias.

Vamos juntos rumo ao sucesso nos investimentos! 💰🚀

# Visualizando minhas ações ou fii´s
'''
)
st.page_link("pages/view.py", label = "Visualização")
    