# 🤖 Robô de Salvamento - Sistema Embarcado

**Disciplina:** Serviços Cognitivos  
**Professor:** Mozart Hasse  
**Aluno:** [Enzo Luiz Berlesi Salles - RA:2023102306]
**Aluno:** [Joao Pedro Calixto Godoy - RA:2023100923]
**Aluno:** [Henrique Bicudo - RA:2023103607]



## 📋 Descrição

Sistema embarcado para robô de salvamento autônomo que explora labirintos para resgatar seres humanos perdidos. O robô utiliza apenas sensores para navegar e construir um mapa interno do ambiente, garantindo operação segura com validações rigorosas.

## 🏗️ Arquitetura

```
src/
├── estruturas.py      # Enums, classes base e exceções
├── labirinto.py       # Simulador do ambiente virtual  
├── robo.py           # Hardware embarcado com validações
├── algoritmo_busca.py # IA de exploração autônoma
└── logger.py         # Sistema de logging CSV
```

## 🚀 Como Executar

### Execução Simples
```bash
python main.py mapas/exemplo_professor.txt
```

### Especificando Diretório de Logs
```bash
python main.py mapas/teste_simples.txt logs_personalizados
```

### Executar Testes
```bash
python tests/test_robo_salvamento.py
```

## 📁 Estrutura do Projeto

```
robo_salvamento/
├── src/                    # Código fonte
├── tests/                  # Casos de teste
├── mapas/                  # Mapas de teste
├── logs/                   # Logs CSV gerados
├── main.py                 # Arquivo principal
└── README.md              # Este arquivo
```

## 🗺️ Formato dos Mapas

Os mapas são arquivos texto com a seguinte codificação:

- `X` - Parede
- `.` - Espaço vazio (navegável)
- `E` - Entrada do labirinto
- `@` - Humano a ser resgatado

### Exemplo:
```
XXXEXXX
X.....X
X.XXXXX
X.....X
XXXXX.X
X.....X
X.XXX.X
X.X..@X
XXXXXXX
```

## 📊 Logs CSV

O sistema gera logs auditáveis em formato CSV com as colunas:

1. **Comando** - LIGAR, A, G, P, E
2. **Sensor Esquerdo** - PAREDE, VAZIO, HUMANO
3. **Sensor Direito** - PAREDE, VAZIO, HUMANO  
4. **Sensor Frente** - PAREDE, VAZIO, HUMANO
5. **Status Carga** - SEM CARGA, COM HUMANO

### Exemplo de Log:
```csv
LIGAR,PAREDE,PAREDE,VAZIO,SEM CARGA
A,VAZIO,VAZIO,PAREDE,SEM CARGA
G,PAREDE,PAREDE,VAZIO,SEM CARGA
```

## 🛡️ Validações de Segurança

O sistema implementa **TODAS** as validações críticas exigidas:

### 🚨 Alarmes Implementados

1. **Colisão com Parede** (`ColisaoException`)
2. **Atropelamento de Humano** (`AtropelamentoException`)  
3. **Beco sem Saída** (`BecoSemSaidaException`)
4. **Operações Inválidas** (`OperacaoInvalidaException`)

### 📍 Localização dos Códigos de Segurança

- **Validação de Colisão:** `src/robo.py`, método `_validar_colisao()` (linha ~85)
- **Validação de Atropelamento:** `src/robo.py`, método `_validar_colisao()` (linha ~93)
- **Validação de Beco sem Saída:** `src/robo.py`, método `_validar_beco_sem_saida()` (linha ~99)
- **Validações de Operação:** `src/robo.py`, métodos `pegar_humano()` e `ejetar_humano()`

## 🧪 Casos de Teste

O projeto inclui testes abrangentes que cobrem:

- ✅ Estruturas fundamentais
- ✅ Carregamento de mapas
- ✅ **TODOS os alarmes de segurança**
- ✅ Sistema de logging
- ✅ Integração completa

### Executar Apenas Testes de Segurança:
```bash
python -m unittest tests.test_robo_salvamento.TestValidacoesSeguranca -v
```

## 🎯 Funcionalidades

### ✅ Requisitos Atendidos

- [x] Exploração autônoma baseada apenas em sensores
- [x] Construção de mapa interno durante navegação
- [x] Busca inteligente até encontrar o humano
- [x] Coleta segura do humano
- [x] Retorno eficiente à entrada
- [x] Ejeção do humano na saída
- [x] Logs CSV auditáveis completos
- [x] Validações rigorosas de segurança
- [x] Tratamento de labirintos de qualquer tamanho
- [x] Entrada em qualquer posição da borda

### 🤖 Comandos do Robô

- **A** - Avançar uma posição
- **G** - Girar 90° à direita
- **P** - Pegar humano à frente
- **E** - Ejetar humano na saída

### 🔍 Sensores

- **Esquerdo** - Detecta célula à esquerda
- **Direito** - Detecta célula à direita  
- **Frente** - Detecta célula à frente

## 📈 Algoritmo de Busca

O algoritmo implementa exploração inteligente:

1. **Fase de Exploração:** DFS modificado priorizando posições não visitadas
2. **Mapeamento:** Constrói mapa interno baseado apenas em sensores
3. **Busca:** Explora sistematicamente até encontrar humano
4. **Retorno:** BFS para caminho eficiente de volta

## 🛠️ Dependências

O projeto usa apenas bibliotecas padrão do Python:
- `enum` - Para enumerações
- `dataclasses` - Para estruturas de dados
- `typing` - Para type hints
- `csv` - Para logs
- `collections` - Para algoritmos
- `unittest` - Para testes

## 🎨 Exemplo de Execução

```
🤖 SIMULADOR DO ROBÔ DE SALVAMENTO
============================================================
🚀 INICIANDO MISSÃO: exemplo_professor.txt
============================================================
⚙️  Inicializando componentes...
📍 Entrada encontrada em: (3, 0)
👤 Humano localizado em: (5, 7)
📊 Dimensões do labirinto: 7x9
🤖 Iniciando missão de busca e salvamento...
📍 Fase 1: Explorando labirinto...
✅ Humano encontrado!
🔄 Fase 2: Coletando humano...
✅ Humano coletado!
🏠 Fase 3: Retornando à entrada...
✅ Chegou à entrada!
🚀 Fase 4: Ejetando humano...
✅ Missão concluída com sucesso!

📈 ESTATÍSTICAS DA MISSÃO:
   • Posições visitadas: 23
   • Posições conhecidas: 35
   • Movimentos realizados: 47
   • Humano encontrado: ✅
   • Humano coletado: ✅
   • Missão concluída: ✅

🎉 MISSÃO CONCLUÍDA COM SUCESSO!
📄 Log salvo em: logs/exemplo_professor.csv
```

## 📝 Notas Importantes

- O robô **JAMAIS** conhece o mapa antecipadamente
- Toda navegação é baseada **EXCLUSIVAMENTE** nos sensores
- Todas as validações de segurança são **OBRIGATÓRIAS**
- Logs são gerados automaticamente para auditoria
- O sistema funciona com labirintos de qualquer tamanho

---

**⚠️ ATENÇÃO:** Este código contém validações críticas de segurança claramente identificadas. Não remova ou modifique as validações sem compreender completamente as implicações!