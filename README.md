# Sliding Window Experiments — Benchmarking Go vs C++

Uma investigação científica aplicada sobre o impacto real da técnica **Sliding Window** comparada à abordagem **Naive** tradicional.  
Este projeto demonstra, de forma quantitativa, como uma simples alteração algorítmica pode gerar ganhos de até **30.000×** em cenários reais.

Todos os experimentos foram executados em **Go** e **C++**, produzindo gráficos, análises log-log e medições de speedup — tudo documentado aqui.

## Objetivo do Projeto
O propósito deste repositório é:
-   Demonstrar a diferença assintótica **O(n²)** vs **O(n)** na prática.
-   Comparar implementações equivalentes em Go e C++.
-   Gerar benchmarks confiáveis com tamanhos variáveis de entrada.
-   Visualizar os resultados com gráficos lineares e log-log.
-   Construir um pipeline simples e reproduzível que qualquer um pode rodar.

O projeto é educativo, científico e extremamente útil para quem deseja evoluir em engenharia de software, desempenho e algoritmos.

## Conceito Principal: Sliding Window
A técnica de Sliding Window evita recalcular trabalho redundante ao processar janelas de tamanho fixo sobre um array.  
Em vez de somar tudo novamente a cada passo, ela apenas:
-   remove o elemento que está saindo,
-   adiciona o elemento que está entrando.

Transformando assim um algoritmo quadrático em um algoritmo linear.

## Como Executar os Benchmarks
### Rodando os testes em Go
```bash
cd go/bench
go test -bench=.
```
```bash
./data/results/go_*.csv
```

### Rodando os testes em C++
```bash
cd cpp
make all && make run
```
```bash
./data/results/cpp_*.csv
```

### Mesclando e analisando tudo via Python
``` bash
cd python
python3 scy_analysis.py
```

Isso irá:

✔ unificar todos os CSVs  
✔ gerar análises log-log  
✔ calcular speedup e ganho percentual  
✔ salvar todos os gráficos profissionais em `docs/charts/`  
✔ imprimir um resumo científico no terminal

## Resultados e Visualizações
#### Visão geral de todos os algoritmos
![all algorithms](https://raw.githubusercontent.com/JuniorPaula/stessa/refs/heads/master/img/all_algorithms.png)

#### Comparação em escala log-log (complexidade)
![log-log-complex](https://raw.githubusercontent.com/JuniorPaula/stessa/refs/heads/master/img/all_algorithms_loglog.png)


## Exemplo dos Algoritmos

#### Naive
```
Para cada posição i:
	 some todos os elementos arr[i .. i+k]
```

#### Sliding Window
```
janela = soma dos k primeiros elementos
para i = k .. n:
    janela = janela - arr[i-k] + arr[i]
```

## A Importância do experimento
Sliding Window não é apenas uma otimização — é uma mudança completa de paradigma.  
Ela aparece em:

-   APIs com rate limit
-   sistemas distribuídos
-   detecção de anomalias
-   séries temporais
-   análise de logs
-   pipelines de dados
-   processamento de sensores
-   machine learning
-   motores financeiros
-   dashboards em tempo real
 
Praticamente qualquer aplicação moderna que trabalha com fluxos contínuos se beneficia dessa técnica.

## Artigo Completo
O artigo técnico com toda a explicação, teoria, análise estatística e gráficos está disponível em:
[https://www.juniorpaula.com.br/articles/sliding-window-na-pratica-uma-investigacao-cientifica-entre-go-e-cpp](https://www.juniorpaula.com.br/articles/sliding-window-na-pratica-uma-investigacao-cientifica-entre-go-e-cpp)

## Autor
**Junior Paula**  
Desenvolvedor Backend | Golang, C++, Rust, Sistemas Distribuídos e Algoritmos  
Apaixonado por desempenho, engenharia real e ciência da computação prática.