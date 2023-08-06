# renku-bio

This plugin extends Renku to easily annotate biological samples in Renku metadata. Samples can be annotated on either the project or dataset metadata (using --dataset).

## Installation

The development version can be installed as a local Python package by running the following command from the root of the repo:

```sh
pip install -e .
```

The stable version is on PyPI and can be installed with pip:

```sh
pip install renku-bio
```


## Usage

A CLI is available with entrypoint `renku bio` the gif belows demonstrates how to use it:

![](assets/demo_renkubio.gif)

<details>
<summary> <b>[Click to expand]</b> Full command from example above</summary>

```sh
➜ renku bio add-sample \
    --description "Culture of liver cells from an adult mouse" \
    --age 2 \
    --taxon "Mus musculus" \
    --collector "SDSC" \
    --gender Male mouse_liver \
    --location "Lausanne" \
    --date 2022-08-10
```

</details>

After adding the biosample above, the project metadata graph would have the following structure:

![](assets/bio_renku_graph.png)

The new "BioSample" node was created by `renku bio add-sample`. The information provided for sampling location, collector organization and taxon are enriched using third party APIs. For example, the "Taxon" node now has "scientificName", "taxonRank" and "parentTaxon" in addition to the name provided.

<details>
<summary> <b>[Click to expand]</b> Compact view of the full biosample metadata</summary>

```json
[
        {
          "@id": "https://renkulab.io/projects/renku-bio/mouse_liver",
          "@type": "http://bioschemas.org/BioSample",
          "http://schema.org/dateCreated": "2022-08-10",
          "http://bioschemas.org/collector": {
            "@id": "https://ror.org/02hdt9m26",
            "@type": "http://schema.org/Organization",
            "http://schema.org/name": "Swiss Data Science Center"
          },
          "http://bioschemas.org/isControl": false,
          "http://bioschemas.org/locationCreated": {
            "@id": "https://renkulab.io/projects/renku-bio/mouse_liver/loc",
            "@type": "http://schema.org/Place",
            "http://schema.org/latitude": 46.5218269,
            "http://schema.org/longitude": 6.6327025,
            "http://schema.org/name": "Lausanne, District de Lausanne, Vaud, Schweiz/Suisse/Svizzera/Svizra"
          },
          "http://bioschemas.org/samplingAge": 2,
          "http://bioschemas.org/taxonomicRange": {
            "@id": "https://renkulab.io/projects/renku-bio/mouse_liver/tax",
            "@type": "http://bioschemas.org/Taxon",
            "http://bioschemas.org/parentTaxon": "Mus",
            "http://bioschemas.org/scientificName": "Mus musculus",
            "http://bioschemas.org/taxonRank": "species",
            "http://schema.org/name": "house mouse"
          },
          "http://schema.org/description": "Culture of liver cells from an adult mouse",
          "http://schema.org/gender": "Male",
          "http://schema.org/name": "mouse_liver"
        }
      ]
```

</details>

## Current state:

Checklist:

* [x] Interactively prompt user to select relevant API result (ROR, EBI, OSM)
* [x] Use dataset annotations instead of project
* [x] Use Renku API to fetch metadata instead of CLI + subprocess
* [x] Change console entrypoint to make into a renku plugin
* [ ] Add support for experimental assay (potentially with [LabProtocol](https://bioschemas.org/profiles/LabProtocol/0.6-DRAFT-2020_12_08))
  + [ ] Restructure CLI into renku bio {sample,assay} {add,ls,rm,show}
* [ ] PoC to query a list of datasets (or projects) based on BioSample annotations.
