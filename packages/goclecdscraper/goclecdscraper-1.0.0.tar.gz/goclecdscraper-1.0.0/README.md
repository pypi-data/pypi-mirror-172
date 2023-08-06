# GoclecdScraper (IN DOING)

## Installation

``` bash

pip install goclecdscraper

```

OR

clone this repository and

``` bash

pip install -r requirements.txt

python setup.py install

```

## Usage

### Initialization with requests

``` python
from goclecdscraper import GoclecdScraper

scraper = GoclecdScraper()

```
### Search products

``` python

results = scraper.search('grounded')

for result in results:
    print(result)

"""

Title : Grounded
price : 30.52 €
href : https://www.goclecd.fr/acheter-grounded-cle-cd-comparateur-prix/

Title : Grounded Xbox One
price : 22.71 €
href : https://www.goclecd.fr/acheter-grounded-xbox-one-comparateur-prix/

Title : Grounded Xbox Series X
price : 31.99 €
href : https://www.goclecd.fr/acheter-grounded-xbox-series-comparateur-prix/

"""
```