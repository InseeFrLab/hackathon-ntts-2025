[Pitch Link !](https://inseefrlab.github.io/hackathon-ntts-2025/)

# NTTS Hackathon 2025: a dashboard for land use change

## Getting started

## Artificialisation
We focus on artificialisation (or the closely linked imperviousness).


## CLC+ and beyond
CORINE Land Cover (CLC) is the oldest database of the Copernicus Land Monitoring Service (CLMS), starting in 2010. [The CLC+ backbone](https://land.copernicus.eu/en/products/clc-backbone?tab=overview) is the new iteration of the product, with a 10m resolution and two first editions in 2018 and 2021.

We plan to build several tools on this backbone:

### CLC+ Delta
- Comparison of the "1: Sealed" class between the 2018 and 2021 CLC+
- Computing imperviousness share and evolution on custom areas
- Access through an interactive dashboard

For now, the CMLS does not provide land use change data based on CLC+. Evolution statistics raise methodological questions (Maucha et al. 2024). While CLC+ is of very high quality, it remains somewhat noisy, which can translate directly into bias when looking at dynamics. But the comparison gives a first look at what the data can say on dynamics.

### CLC+ Forward
We train a model to predict the CLC+ classes from Sentinel2 images. The model allows to replicate CLC+ on more recent years and non covered areas, albeit at lower quality.
CLC+ is based on a temporal CNN model (Pelletier 2019). Time series data is necessary for classes with specific spectral-temporal profiles, such as discriminating between
3: Woody – Broadleaved deciduous trees
4: Woody – Broadleaved evergreen trees 
However, we focus on the 1: Sealed class, where the temporal profile is less crucial.
We train a segformer-B2, a transformer specialized in image segmentation, light and efficient in training and inference.

### Possible next steps
- ...


## References:
- Gergely Maucha (Lechner Ltd.), Éva Kerékgyártó (Lechner Ltd.), Viktória Turos (Lechner Ltd.), Christophe Sannier (GAF), Jaroslav Dufek (GISAT), Tomas Soukup (GISAT), Eva Ivits (EEA), Analysis of usability of Imperviousness and CLC+ Backbone data for mapping sealed areas, ETC DI Report 2024/3, 13 Jun 2024
[Link](https://www.eionet.europa.eu/etcs/etc-di/products/etc-di-report-2024-3-analysis-of-usability-of-imperviousness-and-clc-backbone-data-for-mapping-sealed-areas)
- Sannier, Christophe, et al. "Harmonized Pan-European Time Series for Monitoring Soil Sealing." Land 13.7 (2024): 1087.
[Link](https://www.mdpi.com/2073-445X/13/7/1087)
- Pelletier, Charlotte, Geoffrey I. Webb, and François Petitjean. "Temporal convolutional neural network for the classification of satellite image time series." Remote Sensing 11.5 (2019): 523
[Link](https://www.mdpi.com/2072-4292/11/5/523)
[Repo](https://github.com/charlotte-pel/temporalCNN)
- Product user manual – CLCplus Backbone 2021 Publication date: 12.06.2024  Version: 1.2
[Link](https://land.copernicus.eu/en/products/clc-backbone?tab=documentation)


