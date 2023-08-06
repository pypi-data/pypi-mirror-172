# Plano Diretor de Piracicaba

- [GitHub](https://github.com/open-geodata/sp_piracicaba)
- [PyPi](https://pypi.org/project/sp-piracicaba/)

<br>

Em janeiro de 2021, peguei o arquivo _Mapa_1_2_3_4_macrozonas_zonas_PLC.dwg_ e extrai os seguintes _layers_:

- **Divisão Municipal** (_Divisa_Municipal.shp_), que contem o limite territorial do município;
- **Divisão Perímetro** (_Divisa_Perimetro.shp_), que contem o limite do perímetro urbano do município;
- **Divisão dos Bairros** (_Divisa_Abairramento.shp_), que contem o limite dos bairros inseriodo dentro do perímetro
  urbano do município;
- **Divisão Área Urbana e Rural** (_Divisa_UrbanoRural.shp_), que contem a divisão entre área rural e área urbana do
  município;
- **Macrozoneamento** (_Macrozonas.shp_), proposto pelo Plano Diretor

<br>

No arquivo não foi específicado o _datum_.

- Testei _datum_ SAD 69 e não ficou bom;
- Testei _datum_ Córrego Alegre. Ficou melhor e, portanto, é o que estou usando.

<br>

---

### _TODO_

1. Atualizar os mapas conforme [IPPLAP – Instituto de Pesquisas e Planejamento de Piracicaba](http://www.ipplap.com.br/)
