<div id="top"></div>
<!--
*** Adapted from Best-README-Template
-->

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
<!-- [![LinkedIn][linkedin-shield]][linkedin-url] -->

<!-- PROJECT LOGO -->
<div align="center">
  <a href="https://github.com/UTEL-UIUC/Ridesharing-Scale-Effects">
    <img src="https://raw.githubusercontent.com/UTEL-UIUC/Ridesharing-Scale-Effects/main/images/logo.png" alt="Logo" width=300 height=300>
  </a>

<h3 align="center">Scale Effects in Ridesplitting</h3>
  <p align="center">
    Emperical Study of Economies of Scale in Ridesplitting using open-source ridesharing data
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
    </li>
    <li><a href="#usage">Usage</a></li>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
      </ul>
    <li><a href="#license">License</a></li>
      <ul>
        <li><a href="#citation">Citation</a></li>
      </ul>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
# About The Project
<!-- <div align="center">
  <img src="images/example.jpg" alt="map" width="400"/>
</div> -->

Ridesplitting -- a type of ride-hailing in which riders share vehicles with other riders -- has become a common travel mode in some major cities. This type of shared ride option is currently provided by transportation network companies (TNCs) such as Uber, Lyft, and Via and has attracted increasing numbers of users, particularly before the COVID-19 pandemic. Previous findings have suggested ridesplitting can lower travel costs and even lessen congestion by reducing the number of vehicles needed to move people. Recent studies have also posited that ridesplitting should experience positive feedback mechanisms in which the quality of the service would improve with the number of users. Specifically, these systems should benefit from economies of scale and increasing returns to scale. This paper demonstrates evidence of their existence using trip data reported by TNCs to the City of Chicago between January and September 2019. Specifically, it shows that increases in the number of riders requesting or authorizing shared trips during a given time period is associated with shorter trip detours, higher rates of riders being matched together, lower costs relative to non-shared trips, and higher willingness for riders to share trips.

This repository consists of the necessary code needed to replicate the figures and tables in our paper `Scale Effects in Ridesplitting: A Case Study of the City of Chicago`. The paper is available on [Transportation Research - Part A](http://dx.doi.org/10.1016/j.tra.2023.103690). The ridesharing data used in the paper is obtained from [Chicago Data portal](https://data.cityofchicago.org/Transportation/Transportation-Network-Providers-Trips-2018-2022-/m6dm-c72p). The processed data for the year 2019 is available on [Harvard Dataverse]( https://doi.org/10.7910/DVN/GZMBJG).

 

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->
# Usage
 The code to replicate the paper is split in two parts - R and. The detour plots in the paper are made in R and the R code is available in the file `Detour_plots.R`. The rest of the plots are developed in python and the code is available in `analysis.py` and `code.py`. The `example.ipynb` provides examples to use the code and obtain the plots.

 NOTE: Download the necessary data from [Harvard Dataverse]( https://doi.org/10.7910/DVN/GZMBJG) to be able to run R and python code provided in the repository.
## Python Prerequisites
The dependencies to run the code and obtain plots are  
<table>
<tr>
</tr>
<tr>
<td>
<ul>
  <li>numpy</li>
  <li>pandas</li>
  <li>sklearn</li>
  <li>statsmodels</li>
  <li>seaborn</li>
  <li>matplotlib</li>
  <li>adjustText</li>
</ul>
</td>
</tr>
</table>


<!-- LICENSE -->
# License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<!-- <p align="right">(<a href="#top">back to top</a>)</p> -->

## Citation
If you use code or paper in your research please use the following BibTeX entry to cite us:

```bibtex
@article{LIU2023103690,
  title = {Scale effects in ridesplitting: A case study of the City of Chicago},
  journal = {Transportation Research Part A: Policy and Practice},
  volume = {173},
  pages = {103690},
  year = {2023},
  issn = {0965-8564},
  doi = {https://doi.org/10.1016/j.tra.2023.103690},
  url = {https://www.sciencedirect.com/science/article/pii/S0965856423001106},
  author = {Hao Liu and Saipraneeth Devunuri and Lewis Lehe and Vikash V. Gayah},
  keywords = {Ridesplitting, Transportation Network Company (TNC), Scale effects, Empirical study, Willingness-to-share}
}
```

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- CONTRIBUTING -->
# Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request
<p align="right">(<a href="#top">back to top</a>)</p>


<!-- CONTACT -->
# Contact
Hao Liu - hfl5376@psu.edu |
Saipraneeth Devunuri - sd37@illinois.edu

Project Link: [https://github.com/UTEL-UIUC/Ridesharing-Scale-Effects](https://github.com/UTEL-UIUC/Ridesharing-Scale-Effects)
<p align="right">(<a href="#top">back to top</a>)</p>


<!-- ACKNOWLEDGMENTS -->
<!-- # Acknowledgments
<p align="right">(<a href="#top">back to top</a>)</p> -->



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/UTEL-UIUC/Ridesharing-Scale-Effects.svg?style=for-the-badge
[contributors-url]: https://github.com/UTEL-UIUC/Ridesharing-Scale-Effects/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/UTEL-UIUC/Ridesharing-Scale-Effects.svg?style=for-the-badge
[forks-url]: https://github.com/UTEL-UIUC/Ridesharing-Scale-Effects/network/members
[stars-shield]: https://img.shields.io/github/stars/UTEL-UIUC/Ridesharing-Scale-Effects.svg?style=for-the-badge
[stars-url]: https://github.com/UTEL-UIUC/Ridesharing-Scale-Effects/stargazers
[issues-shield]: https://img.shields.io/github/issues/UTEL-UIUC/Ridesharing-Scale-Effects.svg?style=for-the-badge
[issues-url]: https://github.com/UTEL-UIUC/Ridesharing-Scale-Effects/issues
[license-shield]: https://img.shields.io/github/license/UTEL-UIUC/Ridesharing-Scale-Effects.svg?style=for-the-badge
[license-url]: https://github.com/UTEL-UIUC/Ridesharing-Scale-Effects/blob/master/LICENSE
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/linkedin_username
[product-screenshot]: images/screenshot.png